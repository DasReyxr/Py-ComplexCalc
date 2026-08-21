# Complex Calc 🧮

A powerful, user-friendly GUI application for solving linear systems with **complex numbers and phasors**. Built for electronics engineers, circuit analysts, and students working with AC circuits, impedance calculations, and complex mathematics.

**Solve Ax=b instantly** with dual-format output (polar & rectangular) and full system persistence.

---

## ✨ Features

- **🔢 Dual Input Format**
  - Rectangular: `3+4j`, `-j2`, `5`
  - Phasor: `10L30°`, `5L-90`, `3L0°`
  - Supports both `i` and `j` for imaginary unit

- **📊 Dual-Format Output**
  - Solutions shown in **polar** and **rectangular** simultaneously
  - Easy comparison and verification

- **🌓 Multiple Themes** (v2.7+)
  - Dark Mode (professional gray, ideal for long sessions)
  - Light Mode (clean white, perfect for presentations)
  - Toggle anytime with top-left switch

- **💾 Full System Persistence**
  - Auto-save to `saved_systems.txt`
  - Load/export systems anytime
  - Import from custom files
  - Session history with timestamps

- **🎯 Dynamic Matrix Sizing**
  - Solve 1×1 up to 10×10 systems
  - Window auto-resizes on size change

- **🚀 Windows Standalone Executable**
  - Single `.exe` file—no Python installation needed
  - Built with PyInstaller for easy distribution

---

## 📦 Versions

| Version | Theme | Status | Release |
|---------|-------|--------|---------|
| **v2.7** | Dark & Light Mode | Current | [Download](https://github.com/DasReyxr/Py-ComplexCalc/releases/tag/v2.7) |
| **v2.6** | Pink Theme | Stable | [Download](https://github.com/DasReyxr/Py-ComplexCalc/releases/tag/v2.6) |

---

## 🚀 Quick Start

### **Option 1: Windows Executable (Easiest)**

1. Download `UI_ComplexCalc.exe` from the latest [Release](https://github.com/DasReyxr/Py-ComplexCalc/releases).
2. Double-click to run. No dependencies needed.
3. Enter matrix **A** and vector **b** values.
4. Click **Solve** to see results.

### **Option 2: Run from Source**

**Requirements:** Python 3.8+ (tested on 3.10, 3.11)

```bash
# Clone the repo
git clone https://github.com/DasReyxr/Py-ComplexCalc.git
cd Py-ComplexCalc

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate          # Windows PowerShell
# or: source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install numpy pillow customtkinter

# Run the app
python UI_ComplexCalc.py
```

---

## 📝 Input Format Guide

### Rectangular Notation
```
3+4j      → 3 + 4i
-j2       → 0 - 2i
5         → 5 + 0i
2+1i      → 2 + 1i (alternative notation)
```

### Phasor Notation
```
10L30     → 10∠30°
5L-90     → 5∠-90°
3L0       → 3∠0°
```

### Mixed Example
```
Matrix A:
[2+1i    -1    0   ]
[-1    2+0.5i  -1  ]
[0      -1     2   ]

Vector b:
[1]
[0]
[1i]
```

---

## 🛠️ Building a Standalone Executable (Windows & Linux)

PyInstaller builds a native executable for whatever OS you run it on — it
does **not** cross-compile, so a Windows `.exe` must be built on Windows
and a Linux binary must be built on Linux.

```bash
# Install PyInstaller
pip install pyinstaller

# Build from the .spec file (recommended — same command on both OSes,
# already bundles HK.jpg, IE.png and themes.json)
cd code
pyinstaller UI_ComplexCalc.spec

# Output: code/dist/UI_ComplexCalc(.exe on Windows)
```

Building with raw CLI flags instead of the `.spec` also works, but the
`--add-data` separator differs by OS (`;` on Windows, `:` on Linux/macOS):

```powershell
# Windows
python -m PyInstaller --onefile --windowed UI_ComplexCalc.py --add-data "HK.jpg;." --add-data "IE.png;." --add-data "themes.json;."
```
```bash
# Linux / macOS
python -m PyInstaller --onefile --windowed UI_ComplexCalc.py --add-data "HK.jpg:." --add-data "IE.png:." --add-data "themes.json:."
```

---

## 📂 Project Structure

```
Py-ComplexCalc/
├── UI_ComplexCalc.py          # Main GUI application
├── ComplexCalc.py             # Core solver & parsing logic
├── HK.jpg                     # UI background asset
├── IE.png                     # Logo icon
├── saved_systems.txt          # Auto-generated saved systems
├── exported_systems.py        # Auto-generated Python export
├── README.md                  # This file
├── RELEASE_v2.6.md           # v2.6 release notes (pink theme)
├── RELEASE_v2.7.md           # v2.7 release notes (dark/light modes)
└── requirements.txt           # Python dependencies
```

---

## 📋 Dependencies

| Package | Purpose |
|---------|---------|
| `numpy` | Linear algebra solving (Gaussian elimination) |
| `customtkinter` | Modern, theme-aware GUI widgets |
| `pillow` (PIL) | Image loading for UI assets |

**Install all at once:**
```bash
pip install -r requirements.txt
```

---

## 🎨 Customization

### Change Theme Colors (v2.7+)

Edit `setup_colors()` in `UI_ComplexCalc.py`:

```python
self.colors_dark = {
    "bg": "#0f0f10",              # Main background
    "frame": "#1f1f20",           # Frame background
    "button": "#3a3a3a",          # Button color
    "button_hover": "#4a4a4a",    # Button hover
    # ... (see code for all options)
}
```

### Use Custom Images

Replace `HK.jpg` and `IE.png` with your own assets (same filenames, place in project root).

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **GUI won't start** | Install/upgrade customtkinter: `pip install --upgrade customtkinter` |
| **"Singular matrix" error** | Matrix A must be invertible. Check for duplicate/linearly dependent rows. |
| **Parsing error** | Verify input format: `10L30` (not `10L30°`), `3+4j` (not `3 + 4j`). |
| **Images not loading** | Ensure `HK.jpg` and `IE.png` exist in the same folder as `UI_ComplexCalc.py`. |
| **EXE blocked by antivirus** | False positive. Add to antivirus whitelist or build from source. |

---

## 📞 Support & Contributions

- **Bug Reports:** Open an [Issue](https://github.com/DasReyxr/Py-ComplexCalc/issues)
- **Feature Requests:** Describe in [Discussions](https://github.com/DasReyxr/Py-ComplexCalc/discussions) or [Issues](https://github.com/DasReyxr/Py-ComplexCalc/issues)
- **Pull Requests:** Welcome! Fork, branch, and submit a PR.

### Planned Features
- CSV import/export for batch processing
- Phasor diagram visualization
- Linux/macOS builds
- Additional theme presets

---

## ℹ️ About

| | |
|---|---|
| **Version** | 4.00 |
| **Last updated** | 2026-08-20 |
| **Repository** | [github.com/DasReyxr/Py-ComplexCalc](https://github.com/DasReyxr/Py-ComplexCalc) |
| **Institution** | Universidad Autónoma de Aguascalientes |
| **Department** | Ingeniería en Electrónica |

Also available inside the app itself: **Help → About Complex Calc...**

## 👥 Credits

**Developers:**
- Das Reyes — [das.reyxr@outlook.com](mailto:das.reyxr@outlook.com)
- Iker Garcia — [ikergarcia450@gmail.com](mailto:ikergarcia450@gmail.com)

**Built with:**
- [NumPy](https://numpy.org/) — Numerical computing
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern GUI toolkit
- [Pillow](https://python-pillow.org/) — Image processing
- [PyInstaller](https://pyinstaller.org/) — Executable packaging

---

## 📄 License

[Add your license here—e.g., MIT, GPL, etc.]

---

## 📖 Learn More

- [v2.7 Release Notes](./RELEASE_v2.7.md) — Latest features & dark/light modes
- [v2.6 Release Notes](./RELEASE_v2.6.md) — Original pink theme release
- [GitHub Releases](https://github.com/DasReyxr/Py-ComplexCalc/releases) — Download binaries

---

**For Electronics Engineers, By Electronics Engineers** ⚡

*"Solve complex systems instantly, focus on the circuit analysis that matters."*
