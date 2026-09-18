import io
import sys
import logging
import uuid
from typing import Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
)
from telegram.constants import ParseMode, ChatAction
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_BOT_TOKEN, MAX_IMAGE_SIZE_MB, validate_config
from enhancer import ImageEnhancer
from locales import get_text, get_mode_title

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("ImageEnhancerBot")

# User language preferences: {user_id: "km" | "en"}, default is "km" (Khmer)
USER_LANG: Dict[int, str] = {}

# In-memory storage for active sessions: {session_id: {"bytes": ..., "lang": ...}}
SESSIONS: Dict[str, Dict[str, Any]] = {}
MAX_SESSIONS = 100


def get_user_lang(user_id: int) -> str:
    """Retrieve user language preference, default to Khmer (km)."""
    return USER_LANG.get(user_id, "km")


def cleanup_old_sessions():
    """Limit stored sessions in memory."""
    if len(SESSIONS) > MAX_SESSIONS:
        oldest_keys = list(SESSIONS.keys())[:20]
        for k in oldest_keys:
            SESSIONS.pop(k, None)


def build_modes_keyboard(session_id: str, lang: str) -> InlineKeyboardMarkup:
    """Build the inline keyboard with localized enhancement mode choices."""
    keyboard = [
        [
            InlineKeyboardButton(get_text(lang, "btn_4x"), callback_data=f"enh:{session_id}:realesrgan_4x"),
        ],
        [
            InlineKeyboardButton(get_text(lang, "btn_2x"), callback_data=f"enh:{session_id}:realesrgan_2x"),
        ],
        [
            InlineKeyboardButton(get_text(lang, "btn_auto"), callback_data=f"enh:{session_id}:auto"),
            InlineKeyboardButton(get_text(lang, "btn_hdr"), callback_data=f"enh:{session_id}:vibrant"),
        ],
        [
            InlineKeyboardButton(get_text(lang, "btn_sharpen"), callback_data=f"enh:{session_id}:sharpen"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def build_language_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting language."""
    keyboard = [
        [
            InlineKeyboardButton("🇰🇭 ភាសាខ្មែរ (Khmer)", callback_data="setlang:km"),
            InlineKeyboardButton("🇬🇧 English", callback_data="setlang:en"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    welcome_text = get_text(lang, "welcome")
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    help_text = get_text(lang, "help")
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


async def lang_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /lang or /language command."""
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    msg = get_text(lang, "choose_lang")
    await update.message.reply_text(msg, reply_markup=build_language_keyboard(), parse_mode=ParseMode.MARKDOWN)


async def handle_lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language switch button click."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    parts = data.split(":")
    if len(parts) == 2 and parts[0] == "setlang":
        new_lang = parts[1]
        user_id = update.effective_user.id
        USER_LANG[user_id] = new_lang
        ack_text = get_text(new_lang, "lang_set")
        await query.edit_message_text(ack_text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle compressed Telegram photos."""
    message = update.message
    if not message.photo:
        return

    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    photo = message.photo[-1]
    
    if photo.file_size and photo.file_size > (MAX_IMAGE_SIZE_MB * 1024 * 1024):
        await message.reply_text(get_text(lang, "too_large", max_size=MAX_IMAGE_SIZE_MB))
        return

    status_msg = await message.reply_text(get_text(lang, "receiving_photo"), parse_mode=ParseMode.MARKDOWN)
    
    try:
        file = await photo.get_file(read_timeout=60, write_timeout=60)
        photo_bytes = await file.download_as_bytearray(read_timeout=60, write_timeout=60)
        
        session_id = uuid.uuid4().hex[:10]
        cleanup_old_sessions()
        SESSIONS[session_id] = {
            "bytes": bytes(photo_bytes),
            "size": (photo.width, photo.height),
            "orig_filesize_kb": round(len(photo_bytes) / 1024, 1),
            "lang": lang
        }

        caption = get_text(
            lang,
            "photo_received",
            width=photo.width,
            height=photo.height,
            size_kb=round(len(photo_bytes) / 1024, 1)
        )

        await status_msg.edit_text(
            caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=build_modes_keyboard(session_id, lang)
        )
    except Exception as e:
        logger.exception("Error receiving photo:")
        await status_msg.edit_text(get_text(lang, "error", err=str(e)), parse_mode=ParseMode.MARKDOWN)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle uncompressed image documents."""
    message = update.message
    doc = message.document
    if not doc:
        return

    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    mime = (doc.mime_type or "").lower()
    allowed_mimes = ["image/jpeg", "image/png", "image/webp", "image/bmp"]
    is_image = any(mime.startswith(m) for m in allowed_mimes) or doc.file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    
    if not is_image:
        await message.reply_text(get_text(lang, "invalid_file"))
        return

    if doc.file_size and doc.file_size > (MAX_IMAGE_SIZE_MB * 1024 * 1024):
        await message.reply_text(get_text(lang, "too_large", max_size=MAX_IMAGE_SIZE_MB))
        return

    status_msg = await message.reply_text(get_text(lang, "receiving_doc"), parse_mode=ParseMode.MARKDOWN)

    try:
        file = await doc.get_file(read_timeout=60, write_timeout=60)
        file_bytes = await file.download_as_bytearray(read_timeout=60, write_timeout=60)

        session_id = uuid.uuid4().hex[:10]
        cleanup_old_sessions()
        SESSIONS[session_id] = {
            "bytes": bytes(file_bytes),
            "filename": doc.file_name or "image.png",
            "orig_filesize_kb": round(len(file_bytes) / 1024, 1),
            "lang": lang
        }

        caption = get_text(
            lang,
            "doc_received",
            filename=doc.file_name,
            size_kb=round(len(file_bytes) / 1024, 1)
        )

        await status_msg.edit_text(
            caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=build_modes_keyboard(session_id, lang)
        )
    except Exception as e:
        logger.exception("Error receiving document:")
        await status_msg.edit_text(get_text(lang, "error", err=str(e)), parse_mode=ParseMode.MARKDOWN)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process enhancement mode button taps."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    parts = data.split(":")
    if len(parts) != 3 or parts[0] != "enh":
        return

    _, session_id, mode = parts
    session = SESSIONS.get(session_id)

    user_id = update.effective_user.id
    lang = session.get("lang") if session else get_user_lang(user_id)

    if not session:
        await query.edit_message_text(
            get_text(lang, "expired"),
            reply_markup=None
        )
        return

    localized_mode_title = get_mode_title(lang, mode)
    
    await query.edit_message_text(
        get_text(lang, "processing", mode=localized_mode_title),
        parse_mode=ParseMode.MARKDOWN
    )

    await context.bot.send_chat_action(chat_id=query.message.chat_id, action=ChatAction.UPLOAD_PHOTO)

    try:
        result = ImageEnhancer.process_image(session["bytes"], mode=mode)
        
        orig_w, orig_h = result["original_size"]
        new_w, new_h = result["new_size"]
        elapsed = result["elapsed_seconds"]
        out_buf = result["buffer"]

        caption = get_text(
            lang,
            "success",
            mode=localized_mode_title,
            orig_w=orig_w,
            orig_h=orig_h,
            new_w=new_w,
            new_h=new_h,
            elapsed=elapsed
        )

        # 1. Send photo preview
        out_buf.seek(0)
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=InputFile(out_buf, filename="preview.jpg"),
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            read_timeout=120,
            write_timeout=120,
        )

        # 2. Send uncompressed document file
        try:
            out_buf.seek(0)
            await context.bot.send_document(
                chat_id=query.message.chat_id,
                document=InputFile(out_buf, filename=result["filename"]),
                caption=get_text(lang, "uncompressed_caption"),
                parse_mode=ParseMode.MARKDOWN,
                read_timeout=120,
                write_timeout=120,
            )
        except Exception as doc_err:
            logger.warning(f"Could not deliver uncompressed document ({doc_err}), but photo was delivered successfully.")

        retry_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(get_text(lang, "btn_retry"), callback_data=f"reset:{session_id}")]
        ])
        await query.edit_message_text(
            get_text(lang, "done", mode=localized_mode_title),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=retry_markup
        )

    except Exception as e:
        logger.exception("Enhancement error:")
        await query.edit_message_text(
            get_text(lang, "error", err=str(e)),
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_reset_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow user to pick another mode for the same image."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    parts = data.split(":")
    if len(parts) != 2 or parts[0] != "reset":
        return

    session_id = parts[1]
    session = SESSIONS.get(session_id)
    user_id = update.effective_user.id
    lang = session.get("lang") if session else get_user_lang(user_id)

    if not session:
        await query.edit_message_text(get_text(lang, "expired"))
        return

    await query.edit_message_text(
        "👇 *សូមជ្រើសរើសជម្រើសកែរូបភាពខាងក្រោម:*" if lang == "km" else "👇 *Select another enhancement mode for your image:*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=build_modes_keyboard(session_id, lang)
    )


def main():
    """Start the bot."""
    is_valid, msg = validate_config()
    if not is_valid:
        print("\n" + "=" * 60)
        print("❌ CONFIGURATION ERROR:")
        print(f"   {msg}")
        print("   Please edit your '.env' file and set TELEGRAM_BOT_TOKEN.")
        print("   Get your free token from @BotFather on Telegram: https://t.me/botfather")
        print("=" * 60 + "\n")
        sys.exit(1)

    print("🚀 Initializing Telegram Image Enhancer Bot (with Real-ESRGAN AI & Khmer Language Support)...")
    try:
        print("🧠 Preloading Real-ESRGAN neural model into memory...")
        ImageEnhancer.get_ort_session()
        print("✅ Real-ESRGAN neural engine ready!")
    except Exception as e:
        print(f"⚠️ Note: Could not preload model ({e}), will load on first request.")

    # Generous HTTP timeouts to handle uploading large/upscaled files over mobile networks
    request_config = HTTPXRequest(
        connect_timeout=60.0,
        read_timeout=120.0,
        write_timeout=120.0,
        pool_timeout=60.0,
    )

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).request(request_config).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lang", lang_command))
    app.add_handler(CommandHandler("language", lang_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_document))
    app.add_handler(CallbackQueryHandler(handle_lang_callback, pattern="^setlang:"))
    app.add_handler(CallbackQueryHandler(handle_callback_query, pattern="^enh:"))
    app.add_handler(CallbackQueryHandler(handle_reset_query, pattern="^reset:"))

    print("🤖 Bot is now polling for messages! Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
