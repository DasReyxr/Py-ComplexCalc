# Py-ComplexCalc 🧮⚡

**A complete ecosystem for solving n×n complex linear systems (Ax=b)** with both desktop GUI and embedded hardware solutions.

Built for electronics engineers, circuit analysts, and students working with **AC circuits, impedance calculations, and complex number mathematics**.

---

## 📦 Project Structure

```
Py-ComplexCalc/
├── Software Version/          # Desktop GUI application
│   ├── code/                  # Python source files
│   │   ├── UI_ComplexCalc.py  # Main GUI (customtkinter)
│   │   ├── ComplexCalc.py     # Core solver & parsing logic
│   │   ├── HK.jpg             # UI background
│   │   └── IE.png             # Logo icon
│   ├── dist/                  # Built .exe files
│   ├── doc/                   # Documentation
│   └── README.md              # Software-specific guide
│
├── HW Version/                # Embedded microcontroller solutions
│   ├── code/
│   │   ├── BlackPill STM32F411CE/    # Implementation for BlackPill
│   │   └── RayPill STM32F446ZE/      # Implementation for RayPill
│   ├── HW Files Schematic & Design/  # PCB schematics, layouts
│   └── (README coming soon)
│
├── OtherCalcs/                # Alternative implementations
├── LICENSE                    # MIT License
└── README_GENERAL.md          # This file
```

---

## 🚀 Quick Navigation

### **Want the Desktop Application?**
→ See [Software Version/README.md](./Software%20Version/README.md)

**Features:**
- ✅ Dual input format (rectangular & phasor notation)
- ✅ Dual-format output (polar & rectangular)
- ✅ Dark/Light themes
- ✅ Solve 1×1 to 10×10 systems
- ✅ Auto-save & system persistence
- ✅ Windows standalone `.exe`

**Get Started:**
```bash
# Option 1: Download .exe (no installation needed)
# See releases: https://github.com/DasReyxr/Py-ComplexCalc/releases

# Option 2: Run from source
git clone https://github.com/DasReyxr/Py-ComplexCalc.git
cd Py-ComplexCalc/Software\ Version/code
pip install numpy customtkinter pillow
python UI_ComplexCalc.py
```

---

### **Want Embedded Hardware?**
→ See [HW Version/](./HW%20Version/)

**Supported Platforms:**
- **BlackPill STM32F411CE** — Compact, cost-effective microcontroller
- **RayPill STM32F446ZE** — More powerful ARM-based alternative

**Features:**
- Real-time n×n solver on microcontroller
- Optimized floating-point arithmetic
- Embedded persistent storage

---

## ✨ Core Features (All Versions)

### 🔢 **Flexible Input Formats**
| Format | Examples | Notes |
|--------|----------|-------|
| **Rectangular** | `3+4j`, `-j2`, `5` | Supports `i` and `j` for imaginary unit |
| **Phasor** | `10L30`, `5L-90°`, `3L0` | Polar notation with degree angles |
| **Mixed** | Matrix rows can use both formats | Auto-converts internally |

### 📊 **Dual-Format Output**
Automatic conversion and display of results as:
- **Polar Form:** `10 L 30°` (magnitude ∠ angle)
- **Rectangular Form:** `8.66 + 5j` (real + imaginary)


### 💾 **Persistence & History**
- Auto-save all computed systems
- Load previous calculations
- Export results (`.py`, `.txt` formats)
- Session timestamps for tracking

---

## 🛠️ Technology Stack

### **Software Version**
| Component | Purpose | Version |
|-----------|---------|---------|
| **Python** | Runtime | 3.8+ (tested 3.10, 3.11) |
| **NumPy** | Linear algebra (Gaussian elimination) | Latest |
| **CustomTkinter** | Modern GUI widgets & theming | Latest |
| **Pillow** | Image loading for UI | Latest |
| **PyInstaller** | Windows executable packaging | Latest |

### **Hardware Version**
| Component | Purpose |
|-----------|---------|
| **STM32 HAL** | Microcontroller abstraction layer |
| **Arm CMSIS-DSP** | Optimized DSP library for ARM |
| **C/C++** | Core solver implementation |

---

## 📚 Documentation

- **[Software Version README](./Software%20Version/README.md)** — Complete GUI guide, features, troubleshooting
- **[HW Version](./HW%20Version/)** — Microcontroller implementations, schematics
- **[LICENSE](./LICENSE)** — MIT License

### Example: Solving a 3×3 Complex System

**Problem:** Solve Ax = b where:
```
A = [2+1i    -1      0   ]      b = [1  ]
    [-1    2+0.5i  -1  ]          [0  ]
    [0      -1      2   ]          [1i ]
```

**Using Software Version:**
1. Launch `UI_ComplexCalc.exe`
2. Select **3×3** from size dropdown
3. Enter matrix A values (supports both formats)
4. Enter vector b values
5. Click **Solve**
6. View results in polar & rectangular forms simultaneously

**Output:**
```
x₁ = 0.8 + 0.6j  (Rectangular)
   = 1.0 ∠ 36.87° (Polar)

x₂ = 0.4 + 0.2j
   = 0.447 ∠ 26.57°

x₃ = 0.2 - 0.4j
   = 0.447 ∠ -63.43°
```

---

## 🐛 Troubleshooting

### General Issues

| Problem | Solution |
|---------|----------|
| **Can't find the solver** | Check the folder you're in: `/Software Version/code/` for source or use `.exe` |
| **"Singular matrix" error** | Matrix must be invertible; check for linearly dependent rows |
| **Complex number parsing error** | Use `3+4j` (no spaces), `10L30` (not `10L30.5`) |

### Software-Specific

See [Software Version/README.md](./Software%20Version/README.md) for full troubleshooting guide.

### Hardware-Specific

See **HW Version/** for embedded debugging guides.

---


**How to contribute:**
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** changes: `git commit -m "Add your feature"`
4. **Push** to branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

**Areas we need help:**
- Linux/macOS builds
- Phasor diagram visualization
- CSV batch import/export
- Additional theme designs
- Hardware documentation
- Bug fixes & optimizations

---

## 📊 Roadmap

### ✅ Completed (v2.7)
- Dark & Light mode themes
- Dual-format input/output
- System persistence
- 1×10 matrix sizing
- Windows `.exe` distribution

### 🚀 Planned
- [ ] Linux/macOS standalone builds
- [ ] CSV import/export for batch solving
- [ ] Phasor diagram real-time visualization
- [ ] Web-based solver (WebAssembly)
- [ ] Mobile app (Qt/Flutter)
- [ ] Hardware documentation & guides
- [ ] Advanced matrix operations (eigenvalues, determinants)

---

## 👥 Credits

**Development Team:**
- **Das Reyes** — Lead developer, theming, Testing, documentation
- **Iker Garcia** — GUI design, user experience, documentation
- **Roberto Lopez** — PCB Design, core solver logic  
- **Kevin Lara** — Hardware integration, embedded systems

**Built With:**
- [NumPy](https://numpy.org/) — Numerical computing
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Modern UI toolkit
- [Pillow](https://python-pillow.org/) — Image processing
- [PyInstaller](https://pyinstaller.org/) — Executable packaging
- [STM32 HAL](https://www.st.com/) — Microcontroller support

---

## 📄 License

MIT License — See [LICENSE](./LICENSE) for details.

**TL;DR:** Use freely, attribute the authors, no warranty.

---

## 💡 Use Cases

**Who uses Py-ComplexCalc?**

- 🔌 **Circuit Engineers** — Analyze AC circuits, impedance networks, power factor calculations
- 📚 **Students** — Homework, exams, learning complex number algebra
- 🎓 **Universities** — Teaching linear algebra with complex numbers
- ⚡ **Hobbyists** — Electronics projects, signal processing experiments
- 🏭 **Industry** — Embedded solutions for real-time signal analysis

---

## 📞 Support

- **🐛 Bug Reports:** [GitHub Issues](https://github.com/DasReyxr/Py-ComplexCalc/issues)
- **💬 Feature Requests:** [GitHub Discussions](https://github.com/DasReyxr/Py-ComplexCalc/discussions)
- **📬 Contact:** Open an issue with the `[QUESTION]` tag
- **📖 Documentation:** Check [Software Version/README.md](./Software%20Version/README.md)

---

## 🎯 Quick Links

| Resource | Link |
|----------|------|
| **Latest Release** | [Download v2.7](https://github.com/DasReyxr/Py-ComplexCalc/releases) |
| **Software Guide** | [Software Version/README.md](./Software%20Version/README.md) |
| **Hardware Designs** | [HW Version/](./HW%20Version/) |
| **Source Code** | [Software Version/code/](./Software%20Version/code/) |
| **GitHub Repo** | [DasReyxr/Py-ComplexCalc](https://github.com/DasReyxr/Py-ComplexCalc) |

---

**For Electronics Engineers, By Electronics Engineers** ⚡

*"Solve complex systems instantly. Focus on the engineering that matters."*
