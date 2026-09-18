# 📸 Telegram AI Image Enhancer Bot (Real-ESRGAN Powered)

A Telegram bot that turns blurry, noisy, or low-resolution images into crisp HD photos using **Real-ESRGAN Deep Learning AI** and local computer vision.

**100% Free, Runs Locally, Zero Watermarks, No External API Keys, and Supports 🇰🇭 ភាសាខ្មែរ (Khmer) & 🇬🇧 English!**

---

## 🌟 មុខងារពិសេសៗ / Features

1. **🤖 Real-ESRGAN 4x (ច្បាស់ខ្លាំង Ultra HD)**:
   - Deep learning neural network reconstruction.
   - Restores blurry faces, sharpens text, reconstructs fine textures, and quadruples (4x) the resolution.
2. **🤖 Real-ESRGAN 2x (ច្បាស់លឿន 2 ដង)**:
   - Fast neural deblurring and super-resolution at 2x resolution.
3. **✨ Auto Lighting (ពន្លឺស្វ័យប្រវត្តិ)**:
   - Adaptive histogram equalization (CLAHE) on luminance + bilateral noise cleaning.
4. **🎨 HDR Color Pop (បង្កើនពណ៌ HDR)**:
   - Shadow lifting and vibrance/saturation boost in LAB/HSV space.
5. **🔍 Edge Sharpen (ពង្រីកភាពមុត)**:
   - Fast edge-preserving filter to clean light blur and sensor noise.

---

## 🌐 ការគាំទ្រភាសា / Language Support

- **🇰🇭 ភាសាខ្មែរ (Khmer)**: កំណត់ជាភាសាដើម (Default)
- **🇬🇧 English**: Can be toggled anytime with `/lang` or `/language`.

---

## 🚀 របៀបដំណើរការ / How to Run

### In Git Bash:
```bash
./venv/Scripts/python bot.py
```

### In PowerShell:
```powershell
.\venv\Scripts\python bot.py
```

### In Command Prompt (CMD):
```cmd
venv\Scripts\python.exe bot.py
```

---

## 🧪 តេស្តក្នុងម៉ាស៊ីន / Local Testing

```bash
./venv/Scripts/python test_enhancer.py
```
