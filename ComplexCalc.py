# fasor_core.py
import numpy as np
import math
import json
import os
from datetime import datetime

# ---------- UTILS ----------
def complejo_a_fasor(z):
    """Return polar form with 'c' as angle symbol, angle in degrees."""
    r = abs(z)
    ang = math.degrees(math.atan2(z.imag, z.real))
    return f"{r:.4g}c{ang:.4g}°"

def complejo_rect(z):
    """Return rectangular a + bj string with 4 significant digits."""
    return f"{z.real:.4g} + {z.imag:.4g}j"

def parse_value(text):
    """Parse text (like '3+4j' or '10c30°') into a complex number."""
    text = text.replace(" ", "")
    if "c" in text or "∠" in text:
        text = text.replace("∠", "c")
        r, ang = text.split("c")
        r = float(r)
        ang = np.deg2rad(float(ang.rstrip("°")))
        return r * (np.cos(ang) + 1j * np.sin(ang))
    return complex(text)

# ---------- CORE LOGIC ----------
class FasorSystem:
    def __init__(self, size=3):
        self.size = size
        self.saved_filename = "saved_systems.txt"
        self.exported_py = "exported_systems.py"

    def solve_system(self, A_text, b_text):
        """Solve given A and b from text matrix entries."""
        A = np.zeros((self.size, self.size), dtype=complex)
        b = np.zeros(self.size, dtype=complex)

        for i in range(self.size):
            for j in range(self.size):
                A[i, j] = parse_value(A_text[i][j])
            b[i] = parse_value(b_text[i])

        x = np.linalg.solve(A, b)
        return A, b, x

    def export_results(self, A, b, x):
        """Return dict with polar and rectangular representations."""
        A_f = [[complejo_a_fasor(A[i, j]) for j in range(self.size)] for i in range(self.size)]
        b_f = [complejo_a_fasor(b[i]) for i in range(self.size)]
        x_f = [complejo_a_fasor(x[i]) for i in range(self.size)]

        A_r = [[complejo_rect(A[i, j]) for j in range(self.size)] for i in range(self.size)]
        b_r = [complejo_rect(b[i]) for i in range(self.size)]
        x_r = [complejo_rect(x[i]) for i in range(self.size)]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return {
            "timestamp": timestamp,
            "size": self.size,
            "A_polar": A_f, "b_polar": b_f, "x_polar": x_f,
            "A_rect": A_r, "b_rect": b_r, "x_rect": x_r
        }

    def save_system(self, data):
        """Append system data to saved files."""
        timestamp = data["timestamp"]
        A_r, b_r, x_r = data["A_rect"], data["b_rect"], data["x_rect"]

        # Save JSON
        with open(self.saved_filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False))
            f.write("\n\n")

        # Export to Python file
        header_needed = not os.path.exists(self.exported_py) or os.path.getsize(self.exported_py) == 0
        with open(self.exported_py, "a", encoding="utf-8") as f:
            if header_needed:
                f.write("# Exported systems from FasorCalculator\n\n")
            varname = "system_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            py_dict = {
                "timestamp": timestamp,
                "size": self.size,
                "A": [[complex(s.replace(" ", "")) for s in row] for row in A_r],
                "b": [complex(s.replace(" ", "")) for s in b_r],
                "x": [complex(s.replace(" ", "")) for s in x_r],
            }
            f.write(f"{varname} = {py_dict}\n\n")

    def load_saved_systems(self):
        """Return list of saved systems as dicts."""
        if not os.path.exists(self.saved_filename):
            return []

        with open(self.saved_filename, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        if not raw:
            return []

        items = []
        for chunk in [c for c in raw.split("\n\n") if c.strip()]:
            try:
                items.append(json.loads(chunk))
            except Exception:
                pass
        return items
