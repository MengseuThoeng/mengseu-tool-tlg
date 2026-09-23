# Localization strings for Khmer (km) and English (en)

TEXTS = {
    "km": {
        "welcome": (
            "👋 **សូមស្វាគមន៍មកកាន់ AI Image Enhancer Bot!**\n\n"
            "ដំណើរការដោយបច្ចេកវិទ្យា **Real-ESRGAN Deep Learning AI** ជួយកែរូបភាពបែក ព្រាល ឬរូបចាស់ៗ ឱ្យប្រែជាច្បាស់កម្រិត **Ultra HD** និងមុខងារ **លុបផ្ទៃខាងក្រោយ (Remove Background)** ដោយឥតគិតថ្លៃ!\n\n"
            "🌟 **មុខងារពិសេសៗ:**\n"
            "• **🤖 Real-ESRGAN 4x (Ultra HD)**: ប្រើប្រាស់ប្រព័ន្ធ AI បង្កើតលម្អិតថ្មីៗ បំបាត់ភាពព្រាល និងបង្កើនទំហំគុណភាព 4 ដង។\n"
            "• **🤖 Real-ESRGAN 2x (Balanced)**: កែភាពព្រាល និងបង្កើនភាពច្បាស់លឿនរហ័ស 2 ដង។\n"
            "• **✂️ Remove Background**: កាត់រូបមនុស្ស ឬវត្ថុ និងលុប background ចេញស្អាតកម្រិតថ្លា (Transparent PNG)។\n"
            "• **✨ Auto Lighting**: កែសម្រួលពន្លឺ ស្រមោល និងកម្រិតពណ៌ស្វ័យប្រវត្តិ (CLAHE)។\n"
            "• **🎨 HDR Color Pop**: បង្កើនពណ៌ធម្មជាតិឱ្យស្រស់ស្អាត និងលើកកម្ពស់ស្រមោល។\n"
            "• **🔍 Edge Sharpen**: បង្កើនភាពមុតស្រួចនៃគែម និងកាត់បន្ថយគ្រាប់ noise។\n\n"
            "📸 **របៀបប្រើប្រាស់:**\n"
            "គ្រាន់តែផ្ញើរូបភាព (Photo) ឬផ្ញើជាឯកសារ (Document/File) មកកាន់ខ្ញុំឥឡូវនេះ!\n\n"
            "🌐 *ប្តូរភាសា / Switch Language: វាយពាក្យ /lang*"
        ),
        "help": (
            "💡 **ការណែនាំអំពីការប្រើប្រាស់:**\n\n"
            "1. **សម្រាប់កាត់រូបលុបផ្ទៃខាងក្រោយ:**\n"
            "   - ជ្រើសរើស **✂️ លុបផ្ទៃខាងក្រោយ (Remove BG)** ដើម្បីកាត់យករូបមនុស្ស/វត្ថុ និងលុប Background ចេញជាឯកសារ PNG ថ្លា។\n\n"
            "2. **សម្រាប់រូបភាពព្រាល ឬបែកគុណភាព:**\n"
            "   - ជ្រើសរើស **Real-ESRGAN 4x** ឬ **2x**។ មុខងារ AI នេះបង្កើតឡើងពិសេសសម្រាប់បង្កើតផ្ទៃមុខ សរសៃសក់ និងរូបភាពឱ្យច្បាស់ឡើងវិញ។\n\n"
            "3. **សម្រាប់រូបភាពងងឹត ឬស្លេកពណ៌:**\n"
            "   - ជ្រើសរើស **Auto Lighting** ឬ **HDR Color Pop**។\n\n"
            "4. **គន្លឹះដើម្បីបានគុណភាពល្អបំផុត:**\n"
            "   - ផ្ញើរូបភាពជាប្រភេទ **ឯកសារ (Document/File)** នោះ Telegram នឹងមិនបង្រួមទំហំរូបភាពរបស់អ្នកឡើយ!\n\n"
            "🌐 ប្តូរភាសា: /lang"
        ),
        "receiving_photo": "📥 *កំពុងទទួលយករូបថត...*",
        "receiving_doc": "📥 *កំពុងទទួលយកឯកសាររូបភាពច្បាស់...*",
        "too_large": "⚠️ រូបភាពធំពេកហើយ! ទំហំអតិបរមាគឺ {max_size}MB។",
        "invalid_file": "⚠️ សូមផ្ញើឯកសារជារូបភាពត្រឹមត្រូវ (JPG, PNG, ឬ WEBP)។",
        "photo_received": (
            "🖼️ **បានទទួលរូបថតរួចរាល់!**\n"
            "• **ទំហំ Resolution:** `{width} × {height}` px\n"
            "• **ទំហំ File:** `{size_kb} KB`\n\n"
            "👇 *សូមជ្រើសរើសជម្រើសកែរូបភាពខាងក្រោម:*"
        ),
        "doc_received": (
            "📁 **បានទទួលឯកសាររូបភាពរួចរាល់!**\n"
            "• **ឈ្មោះ File:** `{filename}`\n"
            "• **ទំហំ:** `{size_kb} KB`\n\n"
            "👇 *សូមជ្រើសរើសជម្រើសកែរូបភាពខាងក្រោម:*"
        ),
        "btn_4x": "🤖 Real-ESRGAN 4x (ច្បាស់ខ្លាំង Ultra HD)",
        "btn_2x": "🤖 Real-ESRGAN 2x (ច្បាស់លឿន 2 ដង)",
        "btn_remove_bg": "✂️ លុបផ្ទៃខាងក្រោយ (Remove BG)",
        "btn_auto": "✨ ពន្លឺស្វ័យប្រវត្តិ (Auto Lighting)",
        "btn_hdr": "🎨 បង្កើនពណ៌ HDR (Color Pop)",
        "btn_sharpen": "🔍 ពង្រីកភាពមុត (Edge Sharpen)",
        "btn_retry": "🔄 សាកល្បងជម្រើសផ្សេងទៀតលើរូបនេះ",
        "processing": "⏳ **កំពុងដំណើរការ {mode}...**\nប្រព័ន្ធ AI កំពុងដំណើរការ សូមរង់ចាំបន្តិច...",
        "success": (
            "✅ **ដំណើរការបានជោគជ័យ!**\n\n"
            "⚙️ **ជម្រើស:** {mode}\n"
            "📐 **ទំហំ Resolution:** `{orig_w}×{orig_h}` ➔ `{new_w}×{new_h}` px\n"
            "⚡ **រយៈពេលកែច្នៃ:** `{elapsed}s`"
        ),
        "uncompressed_caption": "💾 *ឯកសារដើមគុណភាពច្បាស់កម្រិតខ្ពស់ (Uncompressed Master File)*",
        "done": "🎉 **រួចរាល់!** ដំណើរការជាមួយ {mode}។",
        "expired": "⚠️ សម័យកាលដំណើរការផុតកំណត់ហើយ។ សូមផ្ញើរូបភាពថ្មីម្តងទៀត។",
        "error": "❌ **មានបញ្ហាក្នុងការកែរូបភាព:** `{err}`\nសូមព្យាយាមម្តងទៀតជាមួយរូបភាព ឬជម្រើសផ្សេង។",
        "choose_lang": "🌐 **សូមជ្រើសរើសភាសា / Please choose your language:**",
        "lang_set": "🇰🇭 បានកំណត់ភាសាខ្មែររួចរាល់!",
    },
    "en": {
        "welcome": (
            "👋 **Welcome to AI Image Enhancer Bot!**\n\n"
            "Powered by **Real-ESRGAN Deep Learning AI** for photo deblurring, detail reconstruction, and **Background Removal (Remove BG)** completely free!\n\n"
            "🌟 **Features:**\n"
            "• **🤖 Real-ESRGAN 4x (Ultra HD)**: AI deep neural network removes blur and draws crisp textures (4x resolution).\n"
            "• **🤖 Real-ESRGAN 2x (Balanced)**: Fast AI deblurring at 2x resolution.\n"
            "• **✂️ Remove Background**: AI cuts out subject with clean transparent PNG output.\n"
            "• **✨ Auto Lighting**: Equalizes shadows & highlights (CLAHE).\n"
            "• **🎨 HDR Color Pop**: Boosts vibrance and shadow depth.\n"
            "• **🔍 Edge Sharpen**: Cleans minor blur and noise.\n\n"
            "📸 **How to use:**\n"
            "Send any photo or send an uncompressed document file to begin!\n\n"
            "🌐 *Switch Language: /lang*"
        ),
        "help": (
            "💡 **Image Enhancer Guide:**\n\n"
            "• **For Background Removal:**\n"
            "  Use **✂️ Remove Background** to cut out the subject into a transparent PNG file.\n\n"
            "• **For Blurry / Low-Quality Photos:**\n"
            "  Use **Real-ESRGAN (4x or 2x)**. This uses deep learning neural networks to hallucinate missing details rather than just sharpening noise.\n\n"
            "• **For Dark / Washed Out Photos:**\n"
            "  Use **Auto Lighting** or **HDR Color Pop**.\n\n"
            "• **Best Quality Tip:**\n"
            "  Send your image as an **Uncompressed Document** so Telegram doesn't shrink the file before we enhance it!\n\n"
            "🌐 Switch Language: /lang"
        ),
        "receiving_photo": "📥 *Receiving photo...*",
        "receiving_doc": "📥 *Receiving uncompressed document...*",
        "too_large": "⚠️ Image is too large! Maximum allowed size is {max_size}MB.",
        "invalid_file": "⚠️ Please send a valid image file (JPG, PNG, or WEBP).",
        "photo_received": (
            "🖼️ **Photo Received!**\n"
            "• **Resolution:** `{width} × {height}` px\n"
            "• **Size:** `{size_kb} KB`\n\n"
            "👇 *Choose an enhancement mode below:*"
        ),
        "doc_received": (
            "📁 **Uncompressed Document Received!**\n"
            "• **File:** `{filename}`\n"
            "• **Size:** `{size_kb} KB`\n\n"
            "👇 *Choose an enhancement mode below:*"
        ),
        "btn_4x": "🤖 Real-ESRGAN 4x (Ultra HD)",
        "btn_2x": "🤖 Real-ESRGAN 2x (Balanced)",
        "btn_remove_bg": "✂️ Remove Background",
        "btn_auto": "✨ Auto Lighting",
        "btn_hdr": "🎨 HDR Color Pop",
        "btn_sharpen": "🔍 Edge Sharpen",
        "btn_retry": "🔄 Try Another Mode On This Image",
        "processing": "⏳ **Running {mode}...**\nAI neural inference in progress, please wait a moment.",
        "success": (
            "✅ **Processed Successfully!**\n\n"
            "⚙️ **Mode:** {mode}\n"
            "📐 **Resolution:** `{orig_w}×{orig_h}` ➔ `{new_w}×{new_h}` px\n"
            "⚡ **Processing Time:** `{elapsed}s`"
        ),
        "uncompressed_caption": "💾 *Full-resolution master file without compression.*",
        "done": "🎉 **Done!** Processed with {mode}.",
        "expired": "⚠️ This session has expired. Please send your photo again.",
        "error": "❌ **Enhancement error:** `{err}`\nPlease try another image or mode.",
        "choose_lang": "🌐 **Please choose your language / សូមជ្រើសរើសភាសា:**",
        "lang_set": "🇬🇧 Language set to English successfully!",
    }
}


# Mode titles translated
MODE_TITLES = {
    "km": {
        "realesrgan_4x": "🤖 Real-ESRGAN 4x (ច្បាស់កម្រិតខ្ពស់)",
        "realesrgan_2x": "🤖 Real-ESRGAN 2x (ច្បាស់កម្រិតមធ្យម)",
        "remove_bg": "✂️ លុបផ្ទៃខាងក្រោយ (Remove BG)",
        "auto": "✨ ពន្លឺស្វ័យប្រវត្តិ (Auto Lighting)",
        "vibrant": "🎨 ពណ៌ HDR (Color Pop)",
        "sharpen": "🔍 ពង្រីកភាពមុត (Edge Sharpen)",
    },
    "en": {
        "realesrgan_4x": "🤖 Real-ESRGAN 4x (Ultra HD)",
        "realesrgan_2x": "🤖 Real-ESRGAN 2x (Balanced)",
        "remove_bg": "✂️ Remove Background",
        "auto": "✨ Auto Lighting",
        "vibrant": "🎨 HDR Color Pop",
        "sharpen": "🔍 Edge Sharpen",
    }
}

def get_text(lang: str, key: str, **kwargs) -> str:
    """Retrieve translated text by language code with fallback to Khmer/English."""
    lang_dict = TEXTS.get(lang, TEXTS["km"])
    raw_text = lang_dict.get(key, TEXTS["km"].get(key, ""))
    if kwargs:
        return raw_text.format(**kwargs)
    return raw_text

def get_mode_title(lang: str, mode: str) -> str:
    """Retrieve localized mode title."""
    titles = MODE_TITLES.get(lang, MODE_TITLES["km"])
    return titles.get(mode, mode)
