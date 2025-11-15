# engineering_calculator_fixed_with_modules.py
import customtkinter as ctk
import tkinter as tk
import cmath
import math
import re
import traceback

# ---------------- Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- Base functions & prefixes ----------------
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
    "j": 1j,     # allow complex literal
}

ENG_PREFIXES = {
    'T': 1e12, 'G': 1e9, 'M': 1e6, 'k': 1e3,
    'm': 1e-3, 'u': 1e-6, 'n': 1e-9,
    'p': 1e-12, 'f': 1e-15
}

def deg_wrap(fn):
    return lambda x: fn(math.radians(x))

# ---------------- Safe engineering-input converter ----------------
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

# ---------------- Engineering-format output ----------------
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


def DIG_IN(self, ch):
    if self.base_mode == "HEX":
        return ch.upper() in "0123456789ABCDEF"
    if self.base_mode == "DEC":
        return ch in "0123456789"
    if self.base_mode == "OCT":
        return ch in "01234567"
    if self.base_mode == "BIN":
        return ch in "01"
    return False

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

# ---------------- CTkTextbox index helpers ----------------
def text_index_to_abs(textbox: tk.Text, index: str) -> int:
    full = textbox.get("1.0", "end-1c")
    try:
        line_str, col_str = index.split(".")
        line = int(line_str)
        col = int(col_str)
    except Exception:
        return len(full)
    if line <= 1:
        return min(max(col, 0), len(full))
    lines = full.split("\n")
    abs_idx = 0
    for i in range(line - 1):
        if i < len(lines):
            abs_idx += len(lines[i]) + 1
        else:
            abs_idx += 1
    abs_idx += col
    return max(0, min(abs_idx, len(full)))

def abs_to_text_index(textbox: tk.Text, abs_index: int) -> str:
    full = textbox.get("1.0", "end-1c")
    abs_index = max(0, min(abs_index, len(full)))
    lines = full.split("\n")
    running = 0
    for i, ln in enumerate(lines):
        if running + len(ln) >= abs_index:
            col = abs_index - running
            return f"{i+1}.{col}"
        running += len(ln) + 1
    return f"{len(lines)}.{len(lines[-1])}"

#--- Implicit Multiplication ------
def insert_implicit_multiplication(expr: str):
    expr = re.sub(r'(\d|\))\s*\(', r'\1*(', expr)
    expr = re.sub(r'\)\s*(\d|[a-zA-Z])', r')*\1', expr)
    expr = re.sub(r'(\d)\s*([a-zA-Z])', r'\1*\2', expr)
    expr = expr.replace("pi", "*pi") if re.search(r'\dpi', expr) else expr
    expr = expr.replace("e", "*e") if re.search(r'\de', expr) else expr
    expr = expr.replace("*pi", "pi", 1) if expr.startswith("*pi") else expr
    expr = expr.replace("*e", "e", 1) if expr.startswith("*e") else expr
    return expr

# helper: convert number-like tokens to decimal strings depending on chosen base
def prog_token_to_decimal(token: str, base_mode: str):
    """
    Convert a token (digits/letters) to a decimal string according to base_mode.
    Raises ValueError if token invalid for the base.
    """
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
    # DEC
    if base_mode == "DEC":
        if re.fullmatch(r"[0-9]+", tok):
            return str(int(tok, 10))
        raise ValueError(f"Invalid DEC token: {token}")
    # fallback: try decimal parse
    return token


# ---------------- MODULES FRAMEWORK ----------------
# Each module defines: layout (list of rows), and a function `prepare_env(local_env)` that mutates local_env for that mode,
# and a `format_result(raw_result, current_base)` function (for programmer mode we'll provide base formatting).
# MODULES keys are mode names. Default mode is 'engineering' (the existing behavior).
def engineering_prepare_env(local_env):
    # use existing BASE_FUNCS behavior (complex math)
    local_env.update(BASE_FUNCS.copy())

def programmer_prepare_env(local_env):
    # programmer env: prefer real math + bitwise. Provide int() and bit ops as available via Python.
    # Keep a minimal safe environment allowing numeric literals and functions we want.
    # We'll allow int conversion and bit ops use Python operators in eval.
    allowed = {
        "int": int,
        "bin": bin,
        "hex": hex,
        "abs": abs,
        "pow": pow
    }
    local_env.update(allowed)

def programmer_format_result(raw_result, base):
    # base: "DEC", "hex", "bin"
    try:
        if isinstance(raw_result, complex):
            # fallback to complex textual form
            real = raw_result.real; imag = raw_result.imag
            if abs(imag) < 1e-12: imag = 0
            if abs(real) < 1e-12: real = 0
            if imag == 0:
                return str(int(real)) if float(real).is_integer() else str(real)
            if real == 0:
                return f"{imag}i"
            sign = "+" if imag >= 0 else "-"
            return f"{real} {sign} {abs(imag)}i"
        # if numeric real
        if isinstance(raw_result, (int,)) or (isinstance(raw_result, float) and float(raw_result).is_integer()):
            val = int(raw_result)
            if base == "DEC":
                return str(val)
            elif base == "hex":
                return hex(val)
            elif base == "bin":
                return bin(val)
        else:
            # float -> show as DECimal with Eng formatting
            return Eng_Num_OUT(float(raw_result))
    except Exception:
        return str(raw_result)

MODULES = {
    "ENG": {
        "layout": [
            ["DEG", "Modes", "funct", "(", ")"],
            ["7", "8", "9", "/", "^"],
            ["4", "5", "6", "*", "DEL"],
            ["1", "2", "3", "-", "CLR"],
            [".", "0", "i", "+", "="]
        ],
        "prepare_env": engineering_prepare_env,
        "format_result": lambda raw, base=None: (  # engineering formatting ignores base
            (lambda r: (  # inline formatting: complex or real
                (lambda real, imag: (f"{real}" if imag==0 else (f"{imag}i" if real==0 else f"{real} {'+' if imag>=0 else '-'} {abs(imag)}i")))(raw.real, raw.imag)
            ))(raw) if isinstance(raw, complex) else Eng_Num_OUT(float(raw))
        )
    },
    "DIG": {
        "layout": [
            ["HEX", "<",">", "(", ")"],
            ["7", "8", "9", "A", ""],
            ["4", "5", "6", "B", "DEL"],
            ["1", "2", "3", "C", "CLR"],
            ["F", "0", "E", "D", "="]
        ],
        "prepare_env": programmer_prepare_env,
        "format_result": programmer_format_result
    }
}

# ---------------- The Calculator GUI ----------------
class EngCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Das Calculator")
        self.geometry("820x600")
        self.resizable(False, False)

        #------ HISTORY ---------
        self.history = []  # list of (expr, eng_result)
        self.history_index = None  # None means not browsing
        self.use_degrees = True


        self.display = ctk.CTkTextbox(self, width=780, height=70, font=("Consolas", 28))
        self.display.pack(pady=10)
        self.display.insert("1.0", "")

        #------ KEY BINDINGS ---------
        self.display.bind("<Up>", self.load_prev)
        self.display.bind("<Down>", self.load_next)
        self.display.bind("<Return>", self.enter)
        
        #------ GUI ---------
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.output_label.pack(pady=5)

        # Main frames
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack()

        self.keypad_frame = ctk.CTkFrame(self.main_frame)
        self.keypad_frame.grid(row=0, column=0, padx=10)

        history_frame = ctk.CTkFrame(self.main_frame)
        history_frame.grid(row=0, column=1)

        ctk.CTkLabel(history_frame, text="History", font=("Arial", 16)).pack()
        self.history_box = ctk.CTkTextbox(history_frame, width=300, height=420, font=("Consolas", 11))
        self.history_box.pack(padx=4, pady=4)
        self.history_box.bind("<Button-1>", self.select_history)

        # modular mode
        self.calc_mode = "ENG"
        self.base_mode = "DEC"  # only used in programmer mode ("DEC","hex","bin")

        # Mode button
        mode_text = "Mode: Degrees" if self.use_degrees else "Mode: Radians"
        self.mode_btn = ctk.CTkButton(self, text=mode_text, width=200, command=self.toggle_mode)
        self.mode_btn.pack(pady=5)

        # initial keypad build from calc_mode
        self.build_keypad_for_mode(self.calc_mode)

    # ---------------- Mode management ----------------
    def open_modes_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Select Mode")
        win.geometry("300x220")
        win.transient(self)
        ctk.CTkLabel(win, text="Choose a mode", font=("Arial", 14)).pack(pady=8)
        for name in MODULES.keys():
            b = ctk.CTkButton(win, text=name.capitalize(), command=lambda n=name, w=win: self.select_mode(n, w))
            b.pack(fill="x", padx=12, pady=6)
        win.grab_set()

    def select_mode(self, name, win):
        # switch internal calc_mode and rebuild keypad
        self.calc_mode = name
        self.build_keypad_for_mode(name)

        # PROGRAMMER MODE
        if name == "DIG":
            # show base toggle button
            if not hasattr(self, "base_mode_btn"):
                self.base_mode_btn = ctk.CTkButton(
                    self, 
                    text=f"Base: {self.base_mode.upper()}",
                    width=120,
                    command=self.toggle_base_mode
                )
                self.base_mode_btn.pack(pady=4)
            else:
                self.base_mode_btn.configure(text=f"Base: {self.base_mode.upper()}")

            self.output_label.configure(text="PROGRAMMER MODE")


        else:
            # normal engineering mode
            if hasattr(self, "base_mode_btn"):
                try:
                    self.base_mode_btn.destroy()
                    del self.base_mode_btn
                except Exception:
                    pass

            self.output_label.configure(text="")

        win.destroy()


    def build_keypad_for_mode(self, mode_name):
        for child in self.keypad_frame.winfo_children():
            child.destroy()
        layout = MODULES[mode_name]["layout"]
        for r, row in enumerate(layout):
            for c, txt in enumerate(row):
                if txt == "":
                    continue
                # special behavior for DIG mode's base button
                if mode_name == "DIG" and txt == "HEX":
                    cmd = lambda: self.toggle_base_mode()
                elif mode_name == "DIG" and txt in ("DEL", "CLR", "="):
                    # use existing handlers
                    if txt == "DEL":
                        cmd = lambda: self.button_press("DEL")
                    elif txt == "CLR":
                        cmd = lambda: self.button_press("CLR")
                    else:
                        cmd = lambda: self.button_press("=")
                else:
                    # default: insert text label when pressed
                    cmd = lambda val=txt: self.button_press(val)
                b = ctk.CTkButton(self.keypad_frame, text=txt, width=90, command=cmd)
                b.grid(row=r, column=c, padx=5, pady=5)

    def toggle_mode(self):
        self.use_degrees = not self.use_degrees
        mode = "Degrees" if self.use_degrees else "Radians"
        self.mode_btn.configure(text=f"Mode: {mode}")
        self.output_label.configure(text=f"Mode: {'DEG' if self.use_degrees else 'RAD'}")


    # ---------------- Evaluate ----------------
    def evaluate(self):
        expr = self.display.get("1.0", "end-1c")
        expr = Input_Clean(expr)
        if not expr:
            return

        # base local env
        local_env = {}
        # allow numbers and minimal math
        # each module can mutate local_env
        MODULES[self.calc_mode]["prepare_env"](local_env)

        # angle-aware trig: for engineering module we use BASE_FUNCS, for programmer we left trig out
        if self.calc_mode == "ENG":
            if self.use_degrees:
                local_env.update({
                    "sin": deg_wrap(math.sin),
                    "cos": deg_wrap(math.cos),
                    "tan": deg_wrap(math.tan),
                })
            else:
                local_env.update({
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                })
        if self.calc_mode == "DIG":
            try:
                expr = self.display.get("1.0", "end-1c").strip()
                expr = expr.replace(" ", "")

                results = self.evaluate_programmer(expr)

                out = (
                    f"DEC: {results['DEC']}\n"
                    f"HEX: {results['HEX']}\n"
                    f"OCT: {results['OCT']}\n"
                    f"BIN: {results['BIN']}"
                )

                self.output_label.configure(text=out)

                # history
                self.history.append((expr, out))
                self.history_box.insert("end", expr + " = " + results["DEC"] + "\n")
                self.history_box.see("end")

                return

            except Exception as e:
                print("Programmer Mode Error:", e)
                self.output_label.configure(text="Math Error")
                return

        # conversions common to all
        expr_for_eval = expr.replace("^", "**")
        expr_for_eval = Eng_Num_IN(expr_for_eval)
        expr_for_eval = expr_for_eval.replace("i", "j")

        # implicit multiplication
        expr_for_eval = insert_implicit_multiplication(expr_for_eval)

        try:
            raw_result = eval(expr_for_eval, {"__builtins__": None}, local_env)
        except ZeroDivisionError:
            print("=== Math Error: Division by Zero ===")
            self.output_label.configure(text="Math Error")
            return
        except Exception:
            print("=" * 24)
            print("=== Evaluation Error ===")
            traceback.print_exc()
            print("=" * 24)
            self.output_label.configure(text="Error")
            return

        # format based on module
        try:
            if self.calc_mode == "DIG":
                result_str = MODULES["DIG"]["format_result"](raw_result, self.base_mode)
            else:
                # engineering formatting: complex or real
                if isinstance(raw_result, complex):
                    real = raw_result.real; imag = raw_result.imag
                    if abs(imag) < 1e-12: imag = 0
                    if abs(real) < 1e-12: real = 0
                    if imag == 0:
                        result_str = f"{real}"
                    elif real == 0:
                        result_str = f"{imag}i"
                    else:
                        sign = "+" if imag >= 0 else "-"
                        result_str = f"{real} {sign} {abs(imag)}i"
                else:
                    result_str = Eng_Num_OUT(float(raw_result))
        except Exception:
            result_str = str(raw_result)

        # update UI & history
        self.output_label.configure(text=result_str)
        history_line = f"{expr} = {result_str}"
        self.history.append((expr, result_str))
        self.history_box.insert("end", history_line + "\n")
        self.history_box.see("end")
        self.history_index = len(self.history)

    
    # ---------------- Button press handler ----------------
    def button_press(self, key: str):
        # Special module buttons
        if key == "Modes":
            # open popup to select modules
            self.open_modes_popup()
            return

        if key == "funct":
            self.show_functions_popup()
            return

        # module-specific special keys
        if self.calc_mode == "DIG" and key == "MODE":
            # cycle base as convenience
            self.toggle_base_mode()
            return
        if key == "<":
            self.insert_text("<<")
        if key == ">":
            self.insert_text(">>")
        # keep DEG button behavior for engineering mode
        if key == "DEG":
            if self.calc_mode == "ENG":
                self.toggle_mode()
            return

        # CLR / DEL / = and others reuse previous behaviour
        if key == "CLR":
            self.display.delete("1.0", "end")
            self.output_label.configure(text="")
            return

        if key == "DEL":
            try:
                if self.display.tag_ranges("sel"):
                    start = self.display.index("sel.first")
                    end = self.display.index("sel.last")
                    self.display.delete(start, end)
                    self.display.mark_set(tk.INSERT, start)
                else:
                    cursor = self.display.index(tk.INSERT)
                    abs_idx = text_index_to_abs(self.display, cursor)
                    if abs_idx <= 0:
                        return
                    full = self.display.get("1.0", "end-1c").replace("\n", "")
                    new_abs = max(0, abs_idx - 1)
                    new_text = full[:new_abs] + full[abs_idx:]
                    self.display.delete("1.0", "end")
                    self.display.insert("1.0", new_text)
                    new_index = abs_to_text_index(self.display, new_abs)
                    self.display.mark_set(tk.INSERT, new_index)
            except Exception:
                traceback.print_exc()
            return

   


        if key == "=":
            self.evaluate()
            return

        # otherwise insert text
        self.insert_text(str(key))

    # ---------- insert text at cursor (handles selection) ----------
    def insert_text(self, s: str):
        raw = self.display.get("1.0", "end")
        raw = raw.replace("\r", "").replace("\n", "")
        self.display.delete("1.0", "end")
        self.display.insert("1.0", raw)

        try:
            if self.display.tag_ranges("sel"):
                start = self.display.index("sel.first")
                end = self.display.index("sel.last")
                self.display.delete(start, end)
                insert_pos = start
            else:
                insert_pos = self.display.index(tk.INSERT)
        except Exception:
            insert_pos = self.display.index(tk.INSERT)

        abs_pos = text_index_to_abs(self.display, insert_pos)
        full = self.display.get("1.0", "end-1c").replace("\n", "")
        new_full = full[:abs_pos] + s + full[abs_pos:]

        self.display.delete("1.0", "end")
        self.display.insert("1.0", new_full)
        new_abs = abs_pos + len(s)
        new_index = abs_to_text_index(self.display, new_abs)
        self.display.mark_set(tk.INSERT, new_index)
        self.display.focus_set()

    # ---------- functions popup ----------
    def show_functions_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Functions")
        win.geometry("320x400")
        win.transient(self)

        # functions list can be extended per mode in future; keep same list for now
        funcs = [
            ("sin(x)", "sin("),
            ("cos(x)", "cos("),
            ("tan(x)", "tan("),
            ("sqrt(x)", "sqrt("),
            ("ln(x)", "ln("),
            ("log10(x)", "log("),
            ("log(base,x)", "log(x, base)"),
            ("exp(x)", "exp("),
            ("abs(x)", "abs("),
            ("pi", "pi"),
            ("e", "e")
        ]
        for name, ins in funcs:
            b = ctk.CTkButton(win, text=name, command=lambda t=ins: self.insert_func_from_popup(t, win))
            b.pack(pady=6, padx=8, fill="x")

    def insert_func_from_popup(self, s: str, win):
        try:
            self.insert_text(s)
        except Exception:
            traceback.print_exc()
        finally:
            win.destroy()

    # ---------- history click ----------
    def select_history(self, event):
        try:
            idx = self.history_box.index(f"@{event.x},{event.y}")
            line_no = idx.split(".")[0]
            line_text = self.history_box.get(f"{line_no}.0", f"{line_no}.end").strip()
            if not line_text:
                return
            expr_part = line_text.split(" = ", 1)[0] if " = " in line_text else line_text
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr_part)
            self.display.mark_set(tk.INSERT, "end-1c")
            for i, (e, r) in enumerate(self.history):
                if e == expr_part:
                    self.history_index = i
                    break
            else:
                self.history_index = len(self.history)
        except Exception:
            traceback.print_exc()

    # ---------- arrow navigation ----------
    def load_prev(self, event=None):
        if not self.history:
            return
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)
        expr, res = self.history[self.history_index]
        self.display.delete("1.0", "end")
        self.display.insert("1.0", expr)
        self.display.mark_set(tk.INSERT, "end-1c")
        try:
            self.history_box.see(f"{self.history_index+1}.0")
        except Exception:
            pass

    def load_next(self, event=None):
        if not self.history:
            return
        if self.history_index is None:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            expr, res = self.history[self.history_index]
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr)
            self.display.mark_set(tk.INSERT, "end-1c")
            try:
                self.history_box.see(f"{self.history_index+1}.0")
            except Exception:
                pass
        else:
            self.history_index = None
            self.display.delete("1.0", "end")

    def enter(self, event=None):
        self.evaluate()
        return "break"

    # ---------- Programmer --------
    def toggle_base_mode(self):
        order = ["DEC", "HEX", "OCT", "BIN"]
        idx = order.index(self.base_mode)
        self.base_mode = order[(idx + 1) % len(order)]
        # update button label (if exists)
        if hasattr(self, "base_mode_btn"):
            self.base_mode_btn.configure(text=f"Base: {self.base_mode}")
        self.output_label.configure(text=f"Switched to {self.base_mode}")
        # try to reformat last result shown (best-effort)
        if self.history:
            last_expr, last_res = self.history[-1]
            try:
                if isinstance(last_res, str) and last_res.isdigit():
                    val = int(last_res)
                    # if you have MODULES key "DIG" keep that; use DIG format_result if present
                    if "DIG" in MODULES:
                        fmt = MODULES["DIG"]["format_result"]
                        self.output_label.configure(text=fmt(val, self.base_mode))
            except Exception:
                pass


    def evaluate_programmer(self, expr):
        """
        Evaluate a programmer expression according to self.base_mode.
        - Single '<' becomes 1<<1 (=> 2)
        - Single '>' becomes 1>>1 (=> 0)
        - Converts numeric tokens from selected base into decimal integer literals
        so Python eval with bitwise operators works correctly.
        Returns dict with DEC/HEX/OCT/BIN strings.
        """
        expr = expr.replace(" ", "")
        # --- 1. temporarily protect the real shift operators ---
        expr = expr.replace("<<", " __SHIFT_L__ ").replace(">>", " __SHIFT_R__ ")

        # --- 2. now safely space single operators < and > ---
        expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)<", " < ", expr)
        expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)>", " > ", expr)

        # --- 3. restore shift operators ---
        expr = expr.replace("__SHIFT_L__", "<<").replace("__SHIFT_R__", ">>")

        # special single-char shortcuts
        if expr == "<":
            val = 1 << 1
            return {"DEC": str(val), "HEX": format_hex(val)[2:].upper(), "OCT": oct(val)[2:], "BIN": format_bin(val)[2:]}
        if expr == ">":
            val = 1 >> 1
            return {"DEC": str(val), "HEX": format_hex(val)[2:].upper(), "OCT": oct(val)[2:], "BIN": format_bin(val)[2:]}

 
        # tokenization: capture hex-like tokens and operators (<<, >>, &, |, ^, +, -, *, /, parentheses)
        token_re = re.compile(r"([0-9A-Fa-f]+|<<|>>|<|>|[&\|\^\+\-\*\/\(\)])")

        tokens = token_re.findall(expr)

        if not tokens:
            raise ValueError("Empty expression")

        out_tokens = []
        i = 0
        while i < len(tokens):
            t = tokens[i]
            if t in ("<<", ">>", "&", "|", "^", "+", "-", "*", "/", "(", ")"):
                out_tokens.append(t)
                i += 1
                continue

            # numeric-like token: convert to decimal string based on base_mode
            try:
                dec = prog_token_to_decimal(t, self.base_mode)
            except ValueError as ve:
                # If token invalid, raise for caller to show Math Error
                raise ve
            out_tokens.append(dec)
            i += 1

        py_expr = " ".join(out_tokens)

        # Evaluate safely; Python bitwise operators work on ints
        raw = eval(py_expr, {"__builtins__": None}, {})
        # Normalize to int if possible
        if isinstance(raw, bool):
            raw = int(raw)
        elif isinstance(raw, float) and float(raw).is_integer():
            raw = int(raw)
        elif not isinstance(raw, int):
            raw = int(raw)

        value = int(raw)
        return {
            "DEC": str(value),
            "HEX": format_hex(value)[2:].upper(),
            "OCT": oct(value)[2:],
            "BIN": format_bin(value)[2:],
        }


    def load_programmer_layout(self):
        # delete existing keypad
        for w in self.keypad_frame.winfo_children():
            w.destroy()

        prog_buttons = [
            ["HEX", "<",">", "(", ")"],
            ["7", "8", "9", "A", ""],
            ["4", "5", "6", "B", "DEL"],
            ["1", "2", "3", "C", "CLR"],
            ["F", "0", "E", "D", "="]
        ]

        for r, row in enumerate(prog_buttons):
            for c, name in enumerate(row):
                if not name:
                    continue

                if name in ["HEX", "DEC", "BIN", "OCT"]:
                    # base mode switch
                    cmd = lambda m=name: self.set_prog_base(m)
                elif name == "=":
                    cmd = self.evaluate
                elif name == "DEL":
                    cmd = self.delete_char
                elif name == "CLR":
                    cmd = self.clear_display
                else:
                    cmd = lambda t=name: self.insert_text(t)

                b = ctk.CTkButton(self.keypad_frame, text=name, command=cmd)
                b.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

# ---------------- Run ----------------
if __name__ == "__main__":
    app = EngCalculator()
    app.mainloop()
