
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
    exponent = max(min(exponent, 12), -12)
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
    expr = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', '1*j', expr)
    expr = re.sub(r'(\d+)i', r'\1*j', expr)
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



# ---------------- Result formatting ----------------
def eng_format_result(raw_result):
    # Handles complex and real numbers
    if isinstance(raw_result, complex):
        real = raw_result.real
        imag = raw_result.imag
        if abs(imag) < 1e-12: imag = 0
        if abs(real) < 1e-12: real = 0
        if imag == 0:
            return f"{real}"
        elif real == 0:
            return f"{imag}i"
        else:
            sign = "+" if imag >= 0 else "-"
            return f"{real} {sign} {abs(imag)}i"
    else:
        return Eng_Num_OUT(float(raw_result))
