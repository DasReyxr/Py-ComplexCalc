
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
    # Match a number with optional scientific notation:  1, 1.23, 1e3, 2.5E-6
    sci = r'[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?'

    # Full pattern: number + optional engineering prefix
    pat = re.compile(
        rf'(?<![A-Za-z0-9_.])({sci})\s*([TGMkmunpf])(?![A-Za-z0-9_])'
    )

    def repl(m):
        number = float(m.group(1))      # already supports scientific notation
        prefix = m.group(2)
        return str(number * ENG_PREFIXES[prefix])

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

    # --- complex number i ---
    expr = re.sub(r'(?<![a-zA-Z0-9_])i(?![a-zA-Z0-9_])', '1*j', expr)
    expr = re.sub(r'(\d+)i', r'\1*j', expr)
    # ---- Preserve scientific notation ----
    # Convert scientific: ONLY match digits + 'e' + optional sign + digits
    # Example: 1e2, 3.5e-4, 10e+6
    sci_pattern = re.compile(r'(?i)(\d+(\.\d+)?)[eE][+-]?\d+')

    def mark(match):
        return f"__SCI__{match.group(0)}__"

    # Temporarily mark scientific notations
    expr = sci_pattern.sub(mark, expr)

    # Normal implicit multiplication and cleaning rules
    expr = re.sub(r'(\d|\))\s*\(', r'\1*(', expr)
    expr = re.sub(r'\)\s*(\d|[a-zA-Z])', r')*\1', expr)
    # Insert implicit multiplication only before letters EXCEPT e and j
    expr = re.sub(r'(\d)\s*([a-df-zA-DF-Z])', r'\1*\2', expr)


    # Restore scientific notation
    expr = re.sub(r'__SCI__(.*?)__', r'\1', expr)

    return expr

def insert_implicit_multiplication(expr: str) -> str:
    # number or ) before ( → multiply
    expr = re.sub(r'(\d|\))\s*\(', r'\1*(', expr)

    # ) before number or letter (except e, j) → multiply
    expr = re.sub(r'\)\s*(\d|[a-df-zA-DF-Z])', r')*\1', expr)

    # digit before letter, but exclude e (scientific) and j (complex)
    expr = re.sub(r'(\d)\s*([a-df-zA-DF-Z])', r'\1*\2', expr)

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
