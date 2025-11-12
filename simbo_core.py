import numpy as np
import math
import json
import os
from datetime import datetime


def complejo_a_fasor(z):
    """Return polar form with 'c' as angle symbol, angle in degrees."""
    r = abs(z)
    ang = math.degrees(math.atan2(z.imag, z.real))
    return f"{r:.4g}c{ang:.4g}°"


def complejo_rect(z):
    """Return rectangular a + bj string with 4 significant digits."""
    return f"{z.real:.4g} + {z.imag:.4g}j"


class FasorCalculatorCore:
    """Core logic for parsing, solving and persistence — UI independent.

    Methods raise exceptions on fatal errors so the UI can show messages.
    """

    def __init__(self, saved_filename="saved_systems.txt", exported_py="exported_systems.py", max_size=10):
        self.saved_filename = saved_filename
        self.exported_py = exported_py
        self.max_size = max_size

    # ----------------------------
    # Parsing
    # ----------------------------
    def parse_value(self, text: str) -> complex:
        import re
        t = text.replace(" ", "")
        # Fasor form (e.g. 10c30 or 10∠30°)
        if "c" in t or "∠" in t:
            t = t.replace("∠", "c")
            r, ang = t.split("c")
            r = float(r)
            ang = ang.rstrip("°")
            ang = np.deg2rad(float(ang))
            return r * (np.cos(ang) + 1j * np.sin(ang))

        # Accept both 'j' (python) and 'i' (common math notation) for imaginary unit.
        # If user used 'i' (uppercase or lowercase) and didn't use 'j', convert.
        if ('i' in t or 'I' in t) and 'j' not in t:
            t = t.replace('I', 'i')
            t = t.replace('i', 'j')
            # normalize lonely j like 'j', '+j', '-j' to '1j', '+1j', '-1j'
            t = t.replace('+j', '+1j').replace('-j', '-1j')
            if t == 'j':
                t = '1j'
            elif t.startswith('j'):
                t = '1' + t

        # fallback to Python complex literal; raise if invalid
        return complex(t)

    # ----------------------------
    # Solver / formatter
    # ----------------------------
    def solve_from_strings(self, A_strings, b_strings):
        """Given A_strings as list of list of strings and b_strings list of strings,
        parse, solve and return a dict with numeric arrays and formatted results.
        """
        size = len(b_strings)
        if size == 0:
            raise ValueError("Empty system")
        if size > self.max_size:
            raise ValueError(f"Size {size} exceeds maximum {self.max_size}")

        A = np.zeros((size, size), dtype=complex)
        b = np.zeros(size, dtype=complex)
        for i in range(size):
            for j in range(size):
                A[i, j] = self.parse_value(A_strings[i][j])
            b[i] = self.parse_value(b_strings[i])

        x = np.linalg.solve(A, b)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # formatted
        A_f = [[complejo_a_fasor(A[i, j]) for j in range(size)] for i in range(size)]
        b_f = [complejo_a_fasor(b[i]) for i in range(size)]
        x_f = [complejo_a_fasor(x[i]) for i in range(size)]

        A_r = [[complejo_rect(A[i, j]) for j in range(size)] for i in range(size)]
        b_r = [complejo_rect(b[i]) for i in range(size)]
        x_r = [complejo_rect(x[i]) for i in range(size)]

        return {
            "timestamp": timestamp,
            "size": size,
            "A": A,
            "b": b,
            "x": x,
            "A_polar": A_f,
            "b_polar": b_f,
            "x_polar": x_f,
            "A_rect": A_r,
            "b_rect": b_r,
            "x_rect": x_r,
        }

    # ----------------------------
    # Persistence
    # ----------------------------
    def _rect_string_to_complex_literal(self, s):
        try:
            s_clean = s.replace(" ", "")
            return complex(s_clean)
        except Exception:
            return s

    def save_system(self, result_dict):
        """Append the result (dict returned by solve_from_strings) to
        saved_filename (JSON per entry separated by blank lines) and append a
        python-friendly export to exported_py.
        """
        data = {
            "timestamp": result_dict.get("timestamp"),
            "size": result_dict.get("size"),
            "A_polar": result_dict.get("A_polar"),
            "b_polar": result_dict.get("b_polar"),
            "x_polar": result_dict.get("x_polar"),
            "A_rect": result_dict.get("A_rect"),
            "b_rect": result_dict.get("b_rect"),
            "x_rect": result_dict.get("x_rect"),
        }

        # write JSON entry
        try:
            with open(self.saved_filename, "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write("\n\n")
        except Exception:
            raise

        # append python export
        try:
            header_needed = not os.path.exists(self.exported_py) or os.path.getsize(self.exported_py) == 0
            with open(self.exported_py, "a", encoding="utf-8") as f:
                if header_needed:
                    f.write("# Exported systems from FasorCalculator\n\n")
                varname = "system_" + datetime.now().strftime("%Y%m%d_%H%M%S")
                py_dict = {
                    "timestamp": result_dict.get("timestamp"),
                    "size": result_dict.get("size"),
                    "A": [[self._rect_string_to_complex_literal(s) for s in row] for row in result_dict.get("A_rect", [])],
                    "b": [self._rect_string_to_complex_literal(s) for s in result_dict.get("b_rect", [])],
                    "x": [self._rect_string_to_complex_literal(s) for s in result_dict.get("x_rect", [])],
                }
                # write using Python literal representation
                f.write(f"{varname} = {py_dict}\n\n")
        except Exception:
            raise

    def load_saved_items(self, file_path=None):
        """Return list of parsed saved entries from saved_filename or provided file_path."""
        path = file_path or self.saved_filename
        items = []
        if not os.path.exists(path):
            return items
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()
        if not raw:
            return items
        chunks = [c for c in raw.split("\n\n") if c.strip()]
        for idx, chunk in enumerate(chunks):
            try:
                obj = json.loads(chunk)
                items.append(obj)
            except Exception:
                # skip invalid entries
                continue
        return items

    def import_from_file(self, file_path):
        """Read a file and return the parsed entries (no UI)."""
        return self.load_saved_items(file_path)
