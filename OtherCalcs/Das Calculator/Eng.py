
"""
------ Orlando Reyes ------
--------- Auf Das ---------
--------- Eng Calc ---------
-------- 15/11/2025 --------
"""
# ------- Main Library -------
import math
import cmath
import re

# -------- Variables --------
BASE_FUNCS = {
    "abs": abs,
    "sin": cmath.sin,
    "cos": cmath.cos,
    "tan": cmath.tan,
    "sqrt": cmath.sqrt,
    "log": cmath.log,
    "exp": cmath.exp,
    "pi": cmath.pi,
    "e": cmath.e,
    "j": 1j,
}

ENG_PREFIXES = {
    'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3,
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9,
    'p': 1e-12, 'f': 1e-15
}

# ---------------- Layout ----------------
ENG_LAYOUT = [
    ["DEG", "Modes", "funct", "(", ")"],
    ["7", "8", "9", "/", "^"],
    ["4", "5", "6", "*", "DEL"],
    ["1", "2", "3", "-", "CLR"],
    [".", "0", "i", "+", "="]
]
# --------- Function ---------

def deg_wrap(fn):
    return lambda x: fn(math.radians(x))

# ---------------- Input/Output ----------------
def Eng_Num_IN(expr: str) -> str:
    # First, handle number+prefix directly followed by optional spaces and 'i' (e.g., 1ki, 1k i)
    pat_i = re.compile(r'(?<![A-Za-z0-9_.])([0-9]*\.?[0-9]+)\s*([TGMkmunpf])\s*i(?![A-Za-z0-9_])')
    def repl_i(m):
        try:
            number = float(m.group(1))
            prefix = m.group(2)
            return f"{number * ENG_PREFIXES[prefix]}i"
        except Exception:
            return m.group(0)
    expr = pat_i.sub(repl_i, expr)

    # Then, handle standalone number+prefix tokens (e.g., 1k, 3.3u)
    pat = re.compile(r'(?<![A-Za-z0-9_.])([0-9]*\.?[0-9]+)\s*([TGMkmunpf])(?![A-Za-z0-9_\.])')
    def repl(m):
        try:
            number = float(m.group(1))
            prefix = m.group(2)
            return str(number * ENG_PREFIXES[prefix])
        except Exception:
            return m.group(0)
    return pat.sub(repl, expr)

def Eng_Num_OUT(value: float) -> str:
    if value == 0:
        return "0"
    exponent = int(math.floor(math.log10(abs(value)) / 3) * 3)
    exponent = max(min(exponent, 15), -15)
    scaled = value / (10 ** exponent)
    prefix_map = {
        12: "T", 9: "G", 6: "M", 3: "k",
        0: "",
        -3: "m", -6: "u", -9: "n", -12: "p"
    }
    prefix = prefix_map.get(exponent, f"e{exponent}")
    return f"{scaled:g}{prefix}"

def Input_Clean(expr: str) -> str:
    expr = expr.strip()
    expr = expr.replace("×", "*").replace("÷", "/")
    expr = expr.replace("^", "**")
    # Convert numeric followed by optional spaces then 'i' to numeric*j (handles decimals and exponents)
    num_pat = r'(?<![A-Za-z0-9_\.])((?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+\-]?\d+)?)'
    expr = re.sub(num_pat + r'\s*i(?![A-Za-z0-9_])', r'(\1)*j', expr)
    expr = re.sub(num_pat + r'i(?![A-Za-z0-9_])', r'(\1)*j', expr)
    # Standalone i -> 1*j
    expr = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', '1*j', expr)
    return expr

def insert_implicit_multiplication(expr: str):
    expr = re.sub(r'(\d|\))\s*\(', r'\1*(', expr)
    expr = re.sub(r'\)\s*(\d|[a-zA-Z])', r')*\1', expr)
    expr = re.sub(r'(\d)\s*([a-zA-Z])', r'\1*\2', expr)
    expr = expr.replace("pi", "*pi") if re.search(r'\dpi', expr) else expr
    expr = expr.replace("e", "*e") if re.search(r'\de', expr) else expr
    expr = expr.replace("*pi", "pi", 1) if expr.startswith("*pi") else expr
    expr = expr.replace("*e", "e", 1) if expr.startswith("*e") else expr
    return expr

# ---------------- Environment ----------------
def engineering_prepare_env(local_env):
    local_env.update(BASE_FUNCS.copy())


# ---------------- Polar/Rect helpers ----------------
def polar_literal_to_func(expr: str) -> str:
    """Convert occurrences like 'r L theta' (optionally with °) into 'pol(r,theta)'.
    Only supports simple numeric r and theta tokens (with optional sign/decimal/exponent).
    Multiple occurrences are supported.
    """
    # Allow spaces around L, allow degree symbol after angle.
    number = r"[+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?"
    pat = re.compile(rf"(?<![A-Za-z0-9_\.])\s*({number})\s*[L]\s*({number})(?:°)?(?![A-Za-z0-9_\.])")

    def repl(m):
        r = m.group(1)
        th = m.group(2)
        return f"pol({r},{th})"

    # Replace repeatedly to catch multiple literals
    prev = None
    out = expr
    while prev != out:
        prev = out
        out = pat.sub(repl, out)
    return out



# ---------------- Result formatting ----------------
def eng_format_result(raw_result, use_degrees: bool = True):
    """Format result always showing rectangular and polar when applicable.
    - For complex or real numbers: returns two lines: Rect and Pol.
    - For non-numeric types: falls back to str().
    """
    try:
        # Coerce ints to float/complex paths smoothly
        if isinstance(raw_result, (int, float, complex)):
            z = complex(raw_result)
            # Rectangular
            real = z.real
            imag = z.imag
            if abs(real) < 1e-12: real = 0.0
            if abs(imag) < 1e-12: imag = 0.0
            if imag == 0.0:
                rect = f"{Eng_Num_OUT(float(real))}"
            elif real == 0.0:
                rect = f"{Eng_Num_OUT(float(imag))}i"
            else:
                sign = "+" if imag >= 0 else "-"
                rect = f"{Eng_Num_OUT(float(real))} {sign} {Eng_Num_OUT(float(abs(imag)))}i"

            # Polar
            import math
            r = abs(z)
            theta = math.atan2(z.imag, z.real)
            if use_degrees:
                theta_val = math.degrees(theta)
                pol = f"{Eng_Num_OUT(r)} L {theta_val:g}°"
            else:
                pol = f"{Eng_Num_OUT(r)} L {theta:g}"

            return f"Rect: {rect}\nPol:  {pol}"
        else:
            return str(raw_result)
    except Exception:
        return str(raw_result)
