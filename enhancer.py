import io
import os
import sys
import time
import urllib.request
from typing import Tuple, Dict, Any, Optional
import numpy as np
import cv2
from PIL import Image

try:
    import onnxruntime as ort
except ImportError:
    ort = None

try:
    from rembg import remove as rembg_remove, new_session as rembg_new_session
except ImportError:
    rembg_remove = None
    rembg_new_session = None

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_FILENAME = "realesr-general-x4v3.onnx"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
MODEL_URL = "https://huggingface.co/Heliosoph/realesrgan-onnx/resolve/main/realesr-general-x4v3.onnx"


class ImageEnhancer:
    """
    State-of-the-art Image Enhancement engine featuring:
    1. Real-ESRGAN Deep Learning Super-Resolution (Deblur, Denoise & 4x Hallucinated Details).
    2. AI Background Removal (rembg / u2netp transparent PNG).
    3. Adaptive local computer vision filters (CLAHE, Bilateral, HDR).
    """

    _ort_session: Optional[Any] = None
    _rembg_session: Optional[Any] = None

    MODES = {
        "realesrgan_4x": {
            "title": "🤖 AI Real-ESRGAN 4x (Ultra HD)",
            "desc": "Neural AI reconstruction: removes blur, fixes faces/textures & 4x upscales."
        },
        "realesrgan_2x": {
            "title": "🤖 AI Real-ESRGAN 2x (Balanced)",
            "desc": "Neural AI deblurring and detail generation at 2x resolution."
        },
        "auto": {
            "title": "✨ Auto Lighting & Clarity",
            "desc": "Dynamic lighting balance (CLAHE) and micro-contrast enhancement."
        },
        "vibrant": {
            "title": "🎨 HDR & Color Pop",
            "desc": "Expands dynamic range, lifts shadows and enriches colors."
        },
        "sharpen": {
            "title": "🔍 Edge Sharpen & Denoise",
            "desc": "Fast edge-preserving bilateral filter and crisp texture sharpen."
        },
        "remove_bg": {
            "title": "✂️ Remove Background",
            "desc": "AI background cutout with transparent PNG output."
        }
    }

    @classmethod
    def ensure_model(cls) -> str:
        """Ensure Real-ESRGAN ONNX model file exists, download if missing."""
        if not os.path.exists(MODEL_PATH):
            os.makedirs(MODEL_DIR, exist_ok=True)
            print(f"📥 Downloading Real-ESRGAN AI model from Hugging Face (~5MB)...")
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
            print("✅ Real-ESRGAN model downloaded successfully.")
        return MODEL_PATH

    @classmethod
    def get_ort_session(cls):
        """Lazy loader for ONNX inference session."""
        if cls._ort_session is None:
            if ort is None:
                raise RuntimeError("onnxruntime is not installed. Please run: pip install onnxruntime")
            model_path = cls.ensure_model()
            # Use CPUExecutionProvider or DirectML if available
            providers = ['CPUExecutionProvider']
            if 'DmlExecutionProvider' in ort.get_available_providers():
                providers.insert(0, 'DmlExecutionProvider')
            cls._ort_session = ort.InferenceSession(model_path, providers=providers)
        return cls._ort_session

    @classmethod
    def get_rembg_session(cls):
        """Lazy loader for rembg session with lightweight u2netp model (~4.5MB)."""
        if cls._rembg_session is None and rembg_new_session is not None:
            try:
                cls._rembg_session = rembg_new_session("u2netp")
            except Exception as e:
                print(f"Warning: could not create u2netp rembg session ({e}), will use default.")
        return cls._rembg_session

    @classmethod
    def remove_background(cls, image_bytes: bytes) -> io.BytesIO:
        """Remove background using AI segmentation and return transparent PNG buffer."""
        pil_img = Image.open(io.BytesIO(image_bytes))
        sess = cls.get_rembg_session()
        if sess is not None and rembg_remove is not None:
            out_img = rembg_remove(pil_img, session=sess)
        elif rembg_remove is not None:
            out_img = rembg_remove(pil_img)
        else:
            raise RuntimeError("rembg library is not installed.")

        buf = io.BytesIO()
        out_img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    @staticmethod
    def _bytes_to_cv2(image_bytes: bytes) -> Tuple[np.ndarray, bool]:
        """Convert raw bytes to OpenCV BGR/BGRA numpy array."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Unable to decode image. Unsupported or corrupted format.")
        has_alpha = len(img.shape) == 3 and img.shape[2] == 4
        return img, has_alpha

    @staticmethod
    def _cv2_to_bytes(img: np.ndarray, output_format: str = "JPEG", quality: int = 95) -> io.BytesIO:
        """Encode OpenCV image back to in-memory bytes."""
        ext = ".png" if output_format.upper() == "PNG" else ".jpg"
        params = []
        if ext == ".jpg":
            params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        elif ext == ".png":
            params = [int(cv2.IMWRITE_PNG_COMPRESSION), 4]

        success, encoded_img = cv2.imencode(ext, img, params)
        if not success:
            raise ValueError("Failed to encode processed image.")
        buffer = io.BytesIO(encoded_img.tobytes())
        buffer.seek(0)
        return buffer

    @classmethod
    def enhance_realesrgan(cls, img: np.ndarray, scale: int = 4, tile_size: int = 400, tile_pad: int = 12) -> np.ndarray:
        """
        Run Real-ESRGAN deep learning AI restoration on image.
        Uses overlapping tiling to handle any image resolution cleanly without OOM.
        """
        session = cls.get_ort_session()
        has_alpha = len(img.shape) == 3 and img.shape[2] == 4
        alpha = None
        if has_alpha:
            alpha = img[:, :, 3]
            bgr = img[:, :, :3]
        else:
            bgr = img

        h, w = bgr.shape[:2]

        # Auto-rescale input if overly large to prevent CPU stall and Telegram upload timeouts
        # Max input: 1024px -> 4x upscale reaches 4096px (True 4K HD), which is optimal
        max_dim = 1024
        if max(h, w) > max_dim:
            scale_ratio = max_dim / max(h, w)
            target_w = int(w * scale_ratio)
            target_h = int(h * scale_ratio)
            bgr = cv2.resize(bgr, (target_w, target_h), interpolation=cv2.INTER_AREA)
            if has_alpha and alpha is not None:
                alpha = cv2.resize(alpha, (target_w, target_h), interpolation=cv2.INTER_AREA)
            h, w = target_h, target_w

        # Convert BGR -> RGB -> Float32 [0, 1]
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

        # If small enough, run in a single direct forward pass
        if h <= tile_size and w <= tile_size:
            inp = np.transpose(rgb, (2, 0, 1))[np.newaxis, :, :, :]
            out = session.run(None, {"input": inp})[0][0]
            out = np.clip(np.transpose(out, (1, 2, 0)) * 255.0, 0, 255).astype(np.uint8)
            res_bgr = cv2.cvtColor(out, cv2.COLOR_RGB2BGR)
        else:
            # Tiled inference with seamless blending
            step = tile_size - 2 * tile_pad
            out_h, out_w = h * 4, w * 4
            out_rgb = np.zeros((out_h, out_w, 3), dtype=np.float32)

            for y in range(0, h, step):
                for x in range(0, w, step):
                    # Bounding box with padding
                    y1 = max(0, y - tile_pad)
                    x1 = max(0, x - tile_pad)
                    y2 = min(h, y + step + tile_pad)
                    x2 = min(w, x + step + tile_pad)

                    tile = rgb[y1:y2, x1:x2, :]
                    inp = np.transpose(tile, (2, 0, 1))[np.newaxis, :, :, :]
                    tile_out = session.run(None, {"input": inp})[0][0]
                    tile_out = np.transpose(tile_out, (1, 2, 0))

                    # Crop padding in output coordinates (4x)
                    crop_y1 = (y - y1) * 4
                    crop_x1 = (x - x1) * 4
                    crop_y2 = crop_y1 + (min(h, y + step) - y) * 4
                    crop_x2 = crop_x1 + (min(w, x + step) - x) * 4

                    dest_y1 = y * 4
                    dest_x1 = x * 4
                    dest_y2 = dest_y1 + (crop_y2 - crop_y1)
                    dest_x2 = dest_x1 + (crop_x2 - crop_x1)

                    out_rgb[dest_y1:dest_y2, dest_x1:dest_x2] = tile_out[crop_y1:crop_y2, crop_x1:crop_x2]

            out_rgb = np.clip(out_rgb * 255.0, 0, 255).astype(np.uint8)
            res_bgr = cv2.cvtColor(out_rgb, cv2.COLOR_RGB2BGR)

        # If user requested 2x instead of 4x, downsample cleanly with area interpolation
        if scale == 2:
            res_bgr = cv2.resize(res_bgr, (w * 2, h * 2), interpolation=cv2.INTER_AREA)

        # Handle alpha channel if PNG
        if has_alpha and alpha is not None:
            new_h, new_w = res_bgr.shape[:2]
            alpha_up = cv2.resize(alpha, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            return cv2.merge((res_bgr[:, :, 0], res_bgr[:, :, 1], res_bgr[:, :, 2], alpha_up))

        return res_bgr

    @classmethod
    def enhance_auto(cls, img: np.ndarray) -> np.ndarray:
        """Dynamic lighting (CLAHE) + light denoise + unsharp mask."""
        has_alpha = len(img.shape) == 3 and img.shape[2] == 4
        alpha = img[:, :, 3] if has_alpha else None
        bgr = img[:, :, :3] if has_alpha else img

        denoised = cv2.bilateralFilter(bgr, d=7, sigmaColor=50, sigmaSpace=50)
        lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
        l_eq = clahe.apply(l)
        lab_eq = cv2.merge((l_eq, a, b))
        balanced = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

        blurred = cv2.GaussianBlur(balanced, (0, 0), sigmaX=2.0)
        sharpened = cv2.addWeighted(balanced, 1.4, blurred, -0.4, 0)

        if has_alpha and alpha is not None:
            return cv2.merge((sharpened[:, :, 0], sharpened[:, :, 1], sharpened[:, :, 2], alpha))
        return sharpened

    @classmethod
    def enhance_vibrant(cls, img: np.ndarray) -> np.ndarray:
        """Dynamic range boost (HDR look), shadow lifting and vibrant color saturation."""
        has_alpha = len(img.shape) == 3 and img.shape[2] == 4
        alpha = img[:, :, 3] if has_alpha else None
        bgr = img[:, :, :3] if has_alpha else img

        lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_boost = clahe.apply(l)
        lab_boost = cv2.merge((l_boost, a, b))
        bgr_boost = cv2.cvtColor(lab_boost, cv2.COLOR_LAB2BGR)

        hsv = cv2.cvtColor(bgr_boost, cv2.COLOR_BGR2HSV).astype(np.float32)
        h, s, v = cv2.split(hsv)
        s = np.clip(s * 1.25, 0, 255)
        v = np.clip(v * 1.05 + 5, 0, 255)
        hsv_enhanced = cv2.merge((h, s, v)).astype(np.uint8)
        result = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)

        if has_alpha and alpha is not None:
            return cv2.merge((result[:, :, 0], result[:, :, 1], result[:, :, 2], alpha))
        return result

    @classmethod
    def enhance_sharpen(cls, img: np.ndarray) -> np.ndarray:
        """Fast edge-preserving bilateral filter and crisp texture sharpen."""
        has_alpha = len(img.shape) == 3 and img.shape[2] == 4
        alpha = img[:, :, 3] if has_alpha else None
        bgr = img[:, :, :3] if has_alpha else img

        denoised = cv2.bilateralFilter(bgr, d=9, sigmaColor=75, sigmaSpace=75)
        blur_fine = cv2.GaussianBlur(denoised, (0, 0), sigmaX=1.2)
        fine_mask = cv2.addWeighted(denoised, 1.5, blur_fine, -0.5, 0)

        if has_alpha and alpha is not None:
            return cv2.merge((fine_mask[:, :, 0], fine_mask[:, :, 1], fine_mask[:, :, 2], alpha))
        return fine_mask

    @classmethod
    def process_image(cls, image_bytes: bytes, mode: str = "realesrgan_4x", quality: int = 95) -> Dict[str, Any]:
        """
        Process an image with the selected mode.
        """
        start_time = time.time()
        cv_img, has_alpha = cls._bytes_to_cv2(image_bytes)
        orig_h, orig_w = cv_img.shape[:2]

        if mode == "remove_bg":
            out_buffer = cls.remove_background(image_bytes)
            out_pil = Image.open(out_buffer)
            new_w, new_h = out_pil.size
            out_buffer.seek(0)
            elapsed = round(time.time() - start_time, 2)
            mode_info = cls.MODES.get(mode, {"title": "✂️ Remove Background"})
            return {
                "buffer": out_buffer,
                "format": "PNG",
                "filename": f"removed_bg_{int(time.time())}.png",
                "original_size": (orig_w, orig_h),
                "new_size": (new_w, new_h),
                "elapsed_seconds": elapsed,
                "mode_title": mode_info["title"]
            }
        elif mode == "realesrgan_4x":
            result_img = cls.enhance_realesrgan(cv_img, scale=4)
        elif mode == "realesrgan_2x":
            result_img = cls.enhance_realesrgan(cv_img, scale=2)
        elif mode == "auto":
            result_img = cls.enhance_auto(cv_img)
        elif mode == "vibrant":
            result_img = cls.enhance_vibrant(cv_img)
        elif mode == "sharpen":
            result_img = cls.enhance_sharpen(cv_img)
        else:
            raise ValueError(f"Unknown enhancement mode: '{mode}'")

        new_h, new_w = result_img.shape[:2]
        output_format = "PNG" if has_alpha else "JPEG"
        out_buffer = cls._cv2_to_bytes(result_img, output_format=output_format, quality=quality)
        elapsed = round(time.time() - start_time, 2)

        mode_info = cls.MODES.get(mode, {"title": mode.capitalize()})

        return {
            "buffer": out_buffer,
            "format": output_format,
            "filename": f"enhanced_{mode}_{int(time.time())}.{output_format.lower()}",
            "original_size": (orig_w, orig_h),
            "new_size": (new_w, new_h),
            "elapsed_seconds": elapsed,
            "mode_title": mode_info["title"]
        }
