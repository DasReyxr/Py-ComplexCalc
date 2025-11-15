"""
------ Orlando Reyes ------
--------- Auf Das ---------
------ Das Calculator ------
-------- 15/11/2025 --------
"""
# ------- Main Library -------
# --------- Function ---------
# ---------- Class ----------
# -------- Variables --------
# ----------- Main -----------


import customtkinter as ctk
import tkinter as tk
import traceback
import re

from Eng import *
from Dig import *


MODULES = {
    "ENG": {
        "layout": ENG_LAYOUT,
        "prepare_env": engineering_prepare_env,
        "format_result": eng_format_result
    },
    "DIG": {
        "layout": DIG_LAYOUT,
        "prepare_env": programmer_prepare_env,
        "format_result": programmer_format_result
    }
}

# ---------------- CTk Appearance ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ---------------- The Calculator GUI ----------------
class EngCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Das Calculator")
        self.geometry("820x600")
        self.resizable(False, False)

        # ------ HISTORY ---------
        self.history = []  # list of (expr, result)
        self.history_index = None
        self.use_degrees = True

        # ------ DISPLAY ---------
        self.display = ctk.CTkTextbox(self, width=780, height=70, font=("Consolas", 28))
        self.display.pack(pady=10)
        self.display.insert("1.0", "")

        self.display.bind("<Up>", self.load_prev)
        self.display.bind("<Down>", self.load_next)
        self.display.bind("<Return>", self.enter)

        # ------ OUTPUT LABEL ---------
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.output_label.pack(pady=5)

        # ------ FRAMES ---------
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

        # ----- MODES ---------
        self.calc_mode = "ENG"
        self.base_mode = "DEC"  # only used in programmer mode

        self.mode_btn = ctk.CTkButton(
            self,
            text="Mode: Degrees",
            width=200,
            command=self.toggle_mode
        )
        self.mode_btn.pack(pady=5)

        self.build_keypad_for_mode(self.calc_mode)

    # ---------------- Mode Management ----------------
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
        self.calc_mode = name
        self.build_keypad_for_mode(name)

        if name == "DIG":
            if not hasattr(self, "base_mode_btn"):
                self.base_mode_btn = ctk.CTkButton(
                    self,
                    text=f"Base: {self.base_mode}",
                    width=120,
                    command=self.toggle_base_mode
                )
                self.base_mode_btn.pack(pady=4)
            else:
                self.base_mode_btn.configure(text=f"Base: {self.base_mode}")
            self.output_label.configure(text="PROGRAMMER MODE")
        else:
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
                cmd = lambda val=txt: self.button_press(val)
                if mode_name == "DIG" and txt in ("DEL", "CLR", "="):
                    if txt == "DEL": cmd = lambda val=txt: self.button_press("DEL")
                    if txt == "CLR": cmd = lambda val=txt: self.button_press("CLR")
                    if txt == "=": cmd = lambda val=txt: self.button_press("=")
                elif mode_name == "DIG" and txt == "HEX":
                    cmd = lambda: self.toggle_base_mode()
                b = ctk.CTkButton(self.keypad_frame, text=txt, width=90, command=cmd)
                b.grid(row=r, column=c, padx=5, pady=5)

    def toggle_mode(self):
        self.use_degrees = not self.use_degrees
        mode = "Degrees" if self.use_degrees else "Radians"
        self.mode_btn.configure(text=f"Mode: {mode}")

    # ---------------- Evaluate ----------------
    def evaluate(self):
        expr = self.display.get("1.0", "end-1c").strip()
        if not expr:
            return

        local_env = {}
        MODULES[self.calc_mode]["prepare_env"](local_env)

        if self.calc_mode == "ENG":
            if self.use_degrees:
                local_env.update({"sin": deg_wrap(math.sin),
                                  "cos": deg_wrap(math.cos),
                                  "tan": deg_wrap(math.tan)})
            else:
                local_env.update({"sin": math.sin,
                                  "cos": math.cos,
                                  "tan": math.tan})
        elif self.calc_mode == "DIG":
            try:
                results = self.evaluate_programmer(expr)
                out = f"DEC: {results['DEC']}\nHEX: {results['HEX']}\nOCT: {results['OCT']}\nBIN: {results['BIN']}"
                self.output_label.configure(text=out)
                self.history.append((expr, out))
                self.history_box.insert("end", expr + " = " + results["DEC"] + "\n")
                self.history_box.see("end")
                return
            except Exception as e:
                print("Programmer Mode Error:", e)
                self.output_label.configure(text="Math Error")
                return

        expr_for_eval = insert_implicit_multiplication(Input_Clean(Eng_Num_IN(expr)))
        try:
            raw_result = eval(expr_for_eval, {"__builtins__": None}, local_env)
        except ZeroDivisionError:
            self.output_label.configure(text="Math Error")
            return
        except Exception:
            self.output_label.configure(text="Error")
            return

        try:
            fmt = MODULES[self.calc_mode]["format_result"]
            result_str = fmt(raw_result, getattr(self, "base_mode", None))
        except Exception:
            result_str = str(raw_result)

        self.output_label.configure(text=result_str)
        self.history.append((expr, result_str))
        self.history_box.insert("end", f"{expr} = {result_str}\n")
        self.history_box.see("end")
        self.history_index = len(self.history)

    # ---------------- Button Press ----------------
    def button_press(self, key: str):
        if key == "Modes":
            self.open_modes_popup()
            return
        if key == "funct":
            self.show_functions_popup()
            return
        if self.calc_mode == "DIG" and key == "MODE":
            self.toggle_base_mode()
            return
        if key == "<":
            self.insert_text("<<")
            return
        if key == ">":
            self.insert_text(">>")
            return
        if key == "DEG" and self.calc_mode == "ENG":
            self.toggle_mode()
            return
        if key == "CLR":
            self.display.delete("1.0", "end")
            self.output_label.configure(text="")
            return
        if key == "DEL":
            self.delete_char()
            return
        if key == "=":
            self.evaluate()
            return
        self.insert_text(str(key))

    # ---------------- Insert Text ----------------
    def insert_text(self, s: str):
        self.display.insert(tk.INSERT, s)
        self.display.focus_set()

    # ---------------- Delete Char ----------------
    def delete_char(self):
        try:
            if self.display.tag_ranges("sel"):
                start = self.display.index("sel.first")
                end = self.display.index("sel.last")
                self.display.delete(start, end)
            else:
                pos = self.display.index(tk.INSERT)
                if pos != "1.0":
                    self.display.delete(f"{pos}-1c")
        except Exception:
            traceback.print_exc()

    # ---------------- Programmer Mode Base ----------------
    def toggle_base_mode(self):
        order = ["DEC", "HEX", "OCT", "BIN"]
        idx = order.index(self.base_mode)
        self.base_mode = order[(idx + 1) % len(order)]
        if hasattr(self, "base_mode_btn"):
            self.base_mode_btn.configure(text=f"Base: {self.base_mode}")
        self.output_label.configure(text=f"Switched to {self.base_mode}")

    # ---------------- Programmer Evaluation ----------------
    def evaluate_programmer(self, expr):
        expr = expr.replace(" ", "")
        expr = expr.replace("<<", " __SHIFT_L__ ").replace(">>", " __SHIFT_R__ ")
        expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)<", " < ", expr)
        expr = re.sub(r"(?<!__SHIFT_L__)(?<!__SHIFT_R__)>", " > ", expr)
        expr = expr.replace("__SHIFT_L__", "<<").replace("__SHIFT_R__", ">>")

        if expr == "<":
            val = 1 << 1
            return {"DEC": str(val), "HEX": format_hex(val), "OCT": oct(val)[2:], "BIN": format_bin(val)}
        if expr == ">":
            val = 1 >> 1
            return {"DEC": str(val), "HEX": format_hex(val), "OCT": oct(val)[2:], "BIN": format_bin(val)}

        token_re = re.compile(r"([0-9A-Fa-f]+|<<|>>|<|>|[&\|\^\+\-\*\/\(\)])")
        tokens = token_re.findall(expr)
        out_tokens = []

        for t in tokens:
            if t in ("<<", ">>", "&", "|", "^", "+", "-", "*", "/", "(", ")"):
                out_tokens.append(t)
            else:
                out_tokens.append(prog_token_to_decimal(t, self.base_mode))

        py_expr = " ".join(out_tokens)
        raw = eval(py_expr, {"__builtins__": None}, {})
        val = int(raw)
        return {"DEC": str(val), "HEX": format_hex(val), "OCT": oct(val)[2:], "BIN": format_bin(val)}

    # ---------------- Functions Popup ----------------
    def show_functions_popup(self):
        win = ctk.CTkToplevel(self)
        win.title("Functions")
        win.geometry("320x400")
        win.transient(self)

        funcs = [
            ("sin(x)", "sin("), ("cos(x)", "cos("), ("tan(x)", "tan("),
            ("sqrt(x)", "sqrt("), ("ln(x)", "log("), ("log10(x)", "log("),
            ("exp(x)", "exp("), ("abs(x)", "abs("), ("pi", "pi"), ("e", "e")
        ]
        for name, ins in funcs:
            b = ctk.CTkButton(win, text=name, command=lambda t=ins: self.insert_func_from_popup(t, win))
            b.pack(pady=6, padx=8, fill="x")

    def insert_func_from_popup(self, s: str, win):
        try:
            self.insert_text(s)
        finally:
            win.destroy()

    # ---------------- History Selection ----------------
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

    # ---------------- Arrow Navigation ----------------
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

    def load_next(self, event=None):
        if not self.history or self.history_index is None:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            expr, res = self.history[self.history_index]
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr)
            self.display.mark_set(tk.INSERT, "end-1c")
        else:
            self.history_index = None
            self.display.delete("1.0", "end")

    def enter(self, event=None):
        self.evaluate()
        return "break"


# ---------------- Run ----------------
if __name__ == "__main__":
    app = EngCalculator()
    app.mainloop()
