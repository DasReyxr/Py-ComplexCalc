import math
import numpy as np

def complejo_a_fasor(z):
    """Return polar form with 'c' as angle symbol, angle in degrees."""
    r = abs(z)
    ang = math.degrees(math.atan2(z.imag, z.real))
    return f"{r:.4g}c{ang:.4g}°"

def complejo_rect(z):
    """Return rectangular a + bj string with 4 significant digits."""
    return f"{z.real:.4g} + {z.imag:.4g}j"


class FasorCalculatorLogic:
    """Handles parsing and system solving (no GUI)."""

    def parse_value(self, text: str) -> complex:
        """Parse user-entered text (fasor or rectangular) into complex number."""
        text = text.replace(" ", "")
        if "c" in text or "∠" in text:
            text = text.replace("∠", "c")
            r, ang = text.split("c")
            r = float(r)
            ang = ang.rstrip("°")
            ang = np.deg2rad(float(ang))
            return r * (np.cos(ang) + 1j * np.sin(ang))
        return complex(text)

    def solve_system(self, A, b):
        """Solve linear system Ax = b (complex)."""
        return np.linalg.solve(A, b)
