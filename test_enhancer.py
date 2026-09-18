import io
import time
import sys
from PIL import Image, ImageDraw
from enhancer import ImageEnhancer

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def create_synthetic_test_image() -> bytes:
    """Create an in-memory test image with gradient, shapes and text."""
    img = Image.new("RGB", (200, 150), color=(50, 60, 80))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 90, 80], fill=(200, 100, 50), outline=(255, 255, 255), width=2)
    draw.ellipse([100, 30, 180, 100], fill=(40, 180, 120), outline=(220, 240, 255), width=2)
    draw.line([15, 120, 185, 120], fill=(255, 220, 80), width=3)
    draw.text((20, 85), "Real-ESRGAN AI Test", fill=(255, 255, 255))
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def run_tests():
    print("Testing ImageEnhancer with Real-ESRGAN Deep Learning AI...")
    raw_bytes = create_synthetic_test_image()
    print(f"Sample test image generated ({len(raw_bytes)} bytes, size 200x150)")

    for mode_key, mode_meta in ImageEnhancer.MODES.items():
        start = time.time()
        result = ImageEnhancer.process_image(raw_bytes, mode=mode_key)
        duration = round(time.time() - start, 3)
        print(f"[{mode_meta['title']}] Mode: '{mode_key}'")
        print(f"  Orig Size: {result['original_size']} -> New Size: {result['new_size']}")
        print(f"  Duration: {duration}s, Buffer size: {len(result['buffer'].getvalue())} bytes")
        assert len(result['buffer'].getvalue()) > 0, f"Mode {mode_key} produced empty buffer"

    print("\nALL ImageEnhancer & Real-ESRGAN AI modes passed successfully! ✅")


if __name__ == "__main__":
    run_tests()
