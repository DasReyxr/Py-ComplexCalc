"""
------ Orlando Reyes ------
--------- Auf Das ---------
--------- Dig Calc ---------
-------- 15/11/2025 --------
"""
# ------- Main Library -------
import re

# -------- Variables --------
DIG_LAYOUT = [
    ["HEX", "<", ">", "(", ")"],
    ["7", "8", "9", "A", ""],
    ["4", "5", "6", "B", "DEL"],
    ["1", "2", "3", "C", "CLR"],
    ["F", "0", "E", "D", "="]
]
# --------- Function ---------

def DIG_IN(base_mode, ch):
    if base_mode == "HEX":
        return ch.upper() in "0123456789ABCDEF"
    if base_mode == "DEC":
        return ch in "0123456789"
    if base_mode == "OCT":
        return ch in "01234567"
    if base_mode == "BIN":
        return ch in "01"
    return False

def programmer_prepare_env(local_env):
    allowed = {"int": int, "bin": bin, "hex": hex, "abs": abs, "pow": pow}
    local_env.update(allowed)

def prog_token_to_decimal(token: str, base_mode: str):
    tok = token.upper()
    if base_mode == "HEX":
        if re.fullmatch(r"[0-9A-F]+", tok):
            return str(int(tok, 16))
        raise ValueError(f"Invalid HEX token: {token}")
    if base_mode == "OCT":
        if re.fullmatch(r"[0-7]+", tok):
            return str(int(tok, 8))
        raise ValueError(f"Invalid OCT token: {token}")
    if base_mode == "BIN":
        if re.fullmatch(r"[01]+", tok):
            return str(int(tok, 2))
        raise ValueError(f"Invalid BIN token: {token}")
    if base_mode == "DEC":
        if re.fullmatch(r"[0-9]+", tok):
            return str(int(tok, 10))
        raise ValueError(f"Invalid DEC token: {token}")
    return token

def programmer_format_result(raw_result, base):
    try:
        if isinstance(raw_result, complex):
            real = raw_result.real; imag = raw_result.imag
            if abs(imag) < 1e-12: imag = 0
            if abs(real) < 1e-12: real = 0
            if imag == 0: return str(int(real)) if float(real).is_integer() else str(real)
            if real == 0: return f"{imag}i"
            sign = "+" if imag >= 0 else "-"
            return f"{real} {sign} {abs(imag)}i"
        if isinstance(raw_result, (int,)) or (isinstance(raw_result, float) and float(raw_result).is_integer()):
            val = int(raw_result)
            if base == "DEC": return str(val)
            elif base == "hex": return format_hex(val)
            elif base == "bin": return format_bin(val)
        else:
            from Eng import Eng_Num_OUT
            return Eng_Num_OUT(float(raw_result))
    except Exception:
        return str(raw_result)
    
def format_bin(val: int) -> str:
    """Return binary string grouped by 8 bits (from right)."""
    b = bin(val)[2:]  # strip '0b'
    # pad to multiple of 8
    pad_len = (8 - len(b) % 8) % 8
    b = "0" * pad_len + b
    # split every 8 bits
    groups = [b[i:i+8] for i in range(0, len(b), 8)]
    return " ".join(groups)

def format_hex(val: int) -> str:
    """Return hex string grouped by 4 digits (16 bits)."""
    h = hex(val)[2:].upper()  # strip '0x'
    # pad to multiple of 4
    pad_len = (4 - len(h) % 4) % 4
    h = "0" * pad_len + h
    # split every 4 digits
    groups = [h[i:i+4] for i in range(0, len(h), 4)]
    return " ".join(groups)