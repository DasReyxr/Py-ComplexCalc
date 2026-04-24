"""
------ Orlando Reyes ------
--------- Auf Das ---------
------ Das Calculator ------
-------- 15/11/2025 --------
Improvement
NUM
---
DEN
PyInstaller template (run from this folder):
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "DasCalculator" --icon "ALU.ico" --add-data "ALU.ico;." --add-data "ALU.png;." mainUI.py

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
import sys
import ctypes
from pathlib import Path
import tkinter.font as tkfont

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

DIVISIONLINE = "----"
# ---------------- The Calculator GUI ----------------
class EngCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_windows_app_id()
        self.title("Das Calculator")
        self.geometry("900x700")
        self.resizable(False, False)
        self._set_window_icon()

        # ------ THEME SETUP ---------
        self.setup_colors()
        self.current_mode = "dark"
        self.current_colors = self.colors_dark.copy()

        # ------ HISTORY ---------
        self.history = []  # list of (expr, result)
        self.history_index = None
        self.use_degrees = True

        # ------ DISPLAY ---------
        self.display = ctk.CTkTextbox(self, width=860, height=180, font=("Consolas", 28))
        self.display.pack(pady=10)
        self.display.insert("1.0", "")
        # Configure tab-based grid cells so each term can sit in its own "box"
        self.configure_tab_grid(cell_chars=6, max_cells=40)

        # History navigation will be conditional; fractions use arrows locally
        self.display.bind("<Up>", self.on_up)
        self.display.bind("<Down>", self.on_down)
        self.display.bind("<Return>", self.enter)
        # Fraction template on DIVISIONLINE[0]
        self.display.bind("/", self.on_slash)
        # Literal inline division: Ctrl + /
        self.display.bind("<Control-Key-/>", self.on_ctrl_slash)
        self.display.bind("<KP_Divide>", self.on_ctrl_slash)
        # Exit denominator with Right arrow
        self.display.bind("<Right>", self.on_right)
        # Operators on dash line between fractions
        self.display.bind("+", self.on_operator)
        self.display.bind("<KP_Add>", self.on_operator)
        self.display.bind("-", self.on_operator)
        self.display.bind("<KP_Subtract>", self.on_operator)
        self.display.bind("*", self.on_operator)
        self.display.bind("<KP_Multiply>", self.on_operator)
        # Delete entire fraction when deleting a dash
        self.display.bind("<BackSpace>", self.on_backspace)
        self.display.bind("<Delete>", self.on_delete_key)
        # History with Shift + arrows
        self.display.bind("<Shift-Up>", self.load_prev)
        self.display.bind("<Shift-Down>", self.load_next)
        # Shift operators (keyboard < and > insert << and >>)
        self.display.bind("<less>", self.on_less_than)
        self.display.bind("<greater>", self.on_greater_than)
        # Auto-expand division line when typing in numerator
        self.display.bind("<KeyRelease>", self.on_key_release)

        # ------ OUTPUT LABEL ---------
        self.output_label = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.output_label.pack(pady=5)

        # ------ THEME TOGGLE ---------
        self.mode_switch = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="pink"
        )
        self.mode_switch.select()
        self.mode_switch.pack(pady=(10, 6))

        # ------ MODE INDICATOR (always visible above keypad) ---------
        self.mode_indicator = ctk.CTkLabel(self, text="Mode: Degrees", font=("Arial", 14))
        self.mode_indicator.pack(pady=2)

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
        self.apply_dark_mode_colors()
        self.after(100, self._set_window_icon)

    def _set_windows_app_id(self):
        if sys.platform != "win32":
            return
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("AufDas.DasCalculator")
        except Exception:
            pass

    def _set_window_icon(self):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        icon_ico = base_dir / "ALU.ico"
        icon_png = base_dir / "ALU.png"

        try:
            if icon_ico.exists():
                self.iconbitmap(default=str(icon_ico))
                self.iconbitmap(str(icon_ico))
                return
        except Exception:
            pass

        try:
            if not icon_png.exists():
                return

            self._app_icon = tk.PhotoImage(file=str(icon_png))
            w = max(1, self._app_icon.width())
            h = max(1, self._app_icon.height())
            subsample_32 = max(1, min(w // 32, h // 32))
            subsample_16 = max(1, min(w // 16, h // 16))
            self._app_icon_32 = self._app_icon.subsample(subsample_32, subsample_32)
            self._app_icon_16 = self._app_icon.subsample(subsample_16, subsample_16)
            self.iconphoto(True, self._app_icon, self._app_icon_32, self._app_icon_16)
            self.wm_iconphoto(True, self._app_icon, self._app_icon_32, self._app_icon_16)
        except Exception:
            pass

    def configure_tab_grid(self, cell_chars=6, max_cells=40):
        try:
            f = tkfont.Font(font=("Consolas", 28))
            cell_px = f.measure(" " * cell_chars)
            # Build a list of tab stops in pixels
            stops = tuple((i+1) * cell_px for i in range(max_cells))
            # CTkTextbox is tk.Text under the hood; we can set tabs option
            self.display.configure(tabs=stops)
        except Exception:
            pass

    # ---------------- Theme Management ----------------
    def setup_colors(self):
        """Define color palettes for dark and pink modes."""
        self.colors_dark = {
            "bg": "#0f0f10",
            "frame": "#1f1f20",
            "text": "#FFFFFF",
            "button": "#3a3a3a",
            "button_hover": "#4a4a4a",
            "entry": "#191919",
            "entry_text": "#FFFFFF",
            "border": "#333333",
            "textbox": "#141414",
            "label_text": "#FFFFFF",
            "button_text": "#FFFFFF",
        }

        self.colors_pink = {
            "bg": "#FFE4F0",
            "frame": "#FFF0F5",
            "text": "#8B4789",
            "button": "#FF69B4",
            "button_hover": "#FF1493",
            "entry": "#FFFFFF",
            "entry_text": "#8B4789",
            "border": "#FFB6D9",
            "textbox": "#FFFFFF",
            "label_text": "#8B4789",
            "button_text": "#FFFFFF",
        }

    def toggle_theme(self):
        """Switch between dark and pink modes."""
        # If switch text says "Dark Mode", user just switched OFF (to pink)
        # If switch text says "Pink Mode", user just switched ON (to dark)
        if self.current_mode == "dark":
            self.current_mode = "pink"
            self.current_colors = self.colors_pink.copy()
            self.mode_switch.configure(text="Pink Mode")
        else:
            self.current_mode = "dark"
            self.current_colors = self.colors_dark.copy()
            self.mode_switch.configure(text="Dark Mode")

        self.apply_dark_mode_colors()

    def apply_dark_mode_colors(self):
        """Apply current color scheme to all widgets."""
        self.configure(fg_color=self.current_colors["bg"])
        self.mode_switch.configure(
            text="Dark Mode" if self.current_mode == "dark" else "Pink Mode",
            fg_color=self.current_colors["frame"],
            text_color=self.current_colors["text"],
            button_color=self.current_colors["button"],
            progress_color=self.current_colors["button"]
        )

        # Apply colors to all widgets recursively
        for widget in self._get_all_widgets(self):
            if isinstance(widget, ctk.CTkFrame):
                widget.configure(fg_color=self.current_colors["frame"])
            elif isinstance(widget, ctk.CTkLabel):
                widget.configure(
                    fg_color="transparent",
                    text_color=self.current_colors["label_text"]
                )
            elif isinstance(widget, ctk.CTkButton):
                widget.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                    hover_color=self.current_colors["button_hover"]
                )
            elif isinstance(widget, ctk.CTkEntry):
                widget.configure(
                    fg_color=self.current_colors["entry"],
                    text_color=self.current_colors["entry_text"],
                    border_color=self.current_colors["border"]
                )
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(
                    fg_color=self.current_colors["textbox"],
                    text_color=self.current_colors["text"]
                )

    def _get_all_widgets(self, parent):
        """Recursively get all widgets from parent."""
        widgets = []
        for widget in parent.winfo_children():
            widgets.append(widget)
            widgets.extend(self._get_all_widgets(widget))
        return widgets

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
            if hasattr(self, "mode_indicator"):
                self.mode_indicator.configure(text="")
        else:
            if hasattr(self, "base_mode_btn"):
                try:
                    self.base_mode_btn.destroy()
                    del self.base_mode_btn
                except Exception:
                    pass
            self.output_label.configure(text="")
            if hasattr(self, "mode_indicator"):
                mode = "Degrees" if self.use_degrees else "Radians"
                self.mode_indicator.configure(text=f"Mode: {mode}")

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
        if hasattr(self, "mode_indicator"):
            self.mode_indicator.configure(text=f"Mode: {mode}")

    # ---------------- Evaluate ----------------
    def evaluate(self):
        raw_expr = self.display.get("1.0", "end-1c").strip()
        if not raw_expr:
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
            # Provide rect/pol builders that follow current sin/cos (degree/radian)
            local_env.update({
                "rect": lambda x, y: complex(x, y),
                "pol": lambda r, th: r * (complex(local_env["cos"](th), local_env["sin"](th))),
                "toRect": lambda r, th: r * (complex(local_env["cos"](th), local_env["sin"](th)))
            })
        elif self.calc_mode == "DIG":
            try:
                results = self.evaluate_programmer(raw_expr)
                out = f"DEC: {results['DEC']}\nHEX: {results['HEX']}\nOCT: {results['OCT']}\nBIN: {results['BIN']}"
                self.output_label.configure(text=out)
                self.history.append((raw_expr, out))
                self.history_box.insert("end", raw_expr + " = " + results["DEC"] + "\n")
                self.history_box.see("end")
                return
            except Exception as e:
                print("Programmer Mode Error:", e)
                self.output_label.configure(text="Math Error")
                return

        # Preprocess ENG-specific syntaxes: fraction blocks and polar literals
        if self.calc_mode == "ENG":
            print(f"DEBUG raw_expr:\n{repr(raw_expr)}")
            expr_for_history = self.replace_fraction_blocks(raw_expr)
            print(f"DEBUG after replace_fraction_blocks: {repr(expr_for_history)}")
            expr_for_history = polar_literal_to_func(expr_for_history)
            expr = expr_for_history
        else:
            expr = raw_expr

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
            if self.calc_mode == "ENG":
                result_str = eng_format_result(raw_result, self.use_degrees)
            else:
                fmt = MODULES[self.calc_mode]["format_result"]
                result_str = fmt(raw_result, getattr(self, "base_mode", None))
        except Exception:
            result_str = str(raw_result)

        self.output_label.configure(text=result_str)
        # Store RAW expression so recalling history preserves fraction blocks
        self.history.append((raw_expr, result_str))
        # History list shows the processed single-line expression for readability
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
        if key == "/" and self.calc_mode == "ENG":
            self.on_slash()
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

    # ---------------- Fractions UX ----------------
    def on_slash(self, event=None):
        if self.calc_mode != "ENG":
            return  # let normal DIVISIONLINE[0] in DIG
        try:
            pos = self.display.index(tk.INSERT)
            line_s, col_s = pos.split(".")
            line = int(line_s)
            col = int(col_s)

            cur_line_text = self.display.get(f"{line}.0", f"{line}.end")
            prev_line_text = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            next_line_text = self.display.get(f"{line+1}.0", f"{line+1}.end")

            import re as _re
            
            # Check if we're on a numerator line (next line has DIVISIONLINE)
            on_numerator_line = DIVISIONLINE in next_line_text
            
            # Check if we're on a denominator line (previous line has DIVISIONLINE)
            on_denominator_line = DIVISIONLINE in prev_line_text
            
            # If on numerator or denominator line, just insert "/" inline (no new block)
            if on_numerator_line or on_denominator_line:
                self.display.insert(pos, "/")
                self.display.mark_set(tk.INSERT, f"{line}.{col+1}")
                return "break"
            
            # Selection takes priority for numerator
            numerator_sel = None
            if self.display.tag_ranges("sel"):
                numerator_sel = self.display.get("sel.first", "sel.last")
                self.display.delete("sel.first", "sel.last")

            # Detect if we're on a division line (contains DIVISIONLINE anywhere)
            on_dash_line = (DIVISIONLINE in cur_line_text)

            if on_dash_line and line > 1:
                # Inline add another fraction at current column
                # Determine numerator: from selection or from token just left of caret on current line
                if numerator_sel is not None:
                    numerator = numerator_sel
                else:
                    left_segment = self.display.get(f"{line}.0", pos)
                    # Only capture the number (not the operator before it)
                    m = _re.search(r"(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m and m.group(1):
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(numerator)
                        # remove that token from current (dash) line
                        self.display.delete(f"{line}.{start_col}", pos)
                        col = start_col  # align to token start
                    else:
                        numerator = "1"

                # Ensure above and below lines long enough; align by tabs so each term sits in its cell
                def ensure_col(line_no: int, col_no: int):
                    end_idx = self.display.index(f"{line_no}.end")
                    cur_col = int(end_idx.split(".")[1])
                    if cur_col < col_no:
                        self.display.insert(end_idx, " " * (col_no - cur_col))
                # Align cells by matching number of tabs before insertion point
                left_mid = self.display.get(f"{line}.0", f"{line}.{col}")
                tabs_before = left_mid.count("\t")
                # Advance to next cell boundary if we're not at start of one (by inserting a tab)
                if not left_mid.endswith("\t") and not left_mid.endswith(" "):
                    self.display.insert(f"{line}.{col}", "\t")
                    col += 1
                # Ensure top and bottom lines have the same number of tabs
                def ensure_tabs(line_no: int, n_tabs: int):
                    line_text = self.display.get(f"{line_no}.0", f"{line_no}.end")
                    cur_tabs = line_text.count("\t")
                    if cur_tabs < n_tabs:
                        self.display.insert(f"{line_no}.end", "\t" * (n_tabs - cur_tabs))
                ensure_tabs(line-1, tabs_before)
                ensure_tabs(line+1, tabs_before)
                # Fallback padding with spaces if still short by columns
                ensure_col(line-1, col)
                ensure_col(line+1, col)

                # Insert components aligned at column
                self.display.insert(f"{line-1}.{col}", numerator)
                self.display.insert(f"{line}.{col}", DIVISIONLINE)
                self.display.insert(f"{line+1}.{col}", "D")
                # Move caret to denominator position to keep typing
                self.display.mark_set(tk.INSERT, f"{line+1}.{col}")
                return "break"
            else:
                # Fallback: create a new vertical fraction block
                txt = self.get_selection_or_word()
                if txt is None:
                    # Try to capture numeric token immediately before caret on the same line
                    left_segment = self.display.get(f"{line}.0", pos)
                    # Only capture the number (not the operator before it)
                    # Use \d to start, so -5 after 2 becomes just 5, leaving "2-" 
                    m = _re.search(r"(\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m:
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(m.group(1))
                        self.display.delete(f"{line}.{start_col}", pos)
                    else:
                        # Check for standalone negative number at start of line
                        m2 = _re.search(r"^([+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                        if m2:
                            numerator = m2.group(1)
                            start_col = 0
                            self.display.delete(f"{line}.{start_col}", pos)
                        else:
                            numerator = "N"
                else:
                    numerator = txt
                    self.display.delete("sel.first", "sel.last")

                insert_at = self.display.index(tk.INSERT)
                # Indent dash/D lines to current column so the dashes align under the numerator,
                # keeping any left-side terms (e.g., '2-') outside the fraction but parseable.
                if col>4:
                    indent = " " * (col)
                else:
                    indent = ""
                block = f"{numerator}\n{indent}{DIVISIONLINE}\n{indent}D"
                self.display.insert(insert_at, block)
                # place cursor at start of D line at same column
                line2, col2 = map(int, insert_at.split("."))
                den_line_index = f"{line2+2}.{col}"
                self.display.mark_set(tk.INSERT, den_line_index)
                return "break"
        except Exception:
            return "break"

    def on_up(self, event=None):
        # If we're around a fraction block, move to numerator line
        if self.move_between_fraction_lines(direction="up"):
            return "break"
        # default caret move
        return None

    def on_down(self, event=None):
        # If we're around a fraction block, move to denominator line
        if self.move_between_fraction_lines(direction="down"):
            return "break"
        # default caret move
        return None

    def on_ctrl_slash(self, event=None):
        # Insert a literal DIVISIONLINE[0]: allows inline divisions like 1/2/3/4
        try:
            pos = self.display.index(tk.INSERT)
            self.display.insert(pos, "/")
            line, col = map(int, pos.split("."))
            self.display.mark_set(tk.INSERT, f"{line}.{col+1}")
            return "break"
        except Exception:
            return "break"

    def on_less_than(self, event=None):
        # Insert << when user types <
        if self.calc_mode == "DIG":
            self.display.insert(tk.INSERT, "<<")
            return "break"
        return None  # Allow normal < in ENG mode

    def on_greater_than(self, event=None):
        # Insert >> when user types >
        if self.calc_mode == "DIG":
            self.display.insert(tk.INSERT, ">>")
            return "break"
        return None  # Allow normal > in ENG mode

    def on_key_release(self, event=None):
        """Auto-expand division line to match numerator width when typing in numerator."""
        if self.calc_mode != "ENG":
            return None
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            
            # Check if next line has division line (we're on numerator)
            next_line_text = self.display.get(f"{line+1}.0", f"{line+1}.end")
            if DIVISIONLINE in next_line_text:
                cur_line_text = self.display.get(f"{line}.0", f"{line}.end")
                num_len = len(cur_line_text.rstrip())
                
                # Find current division line start and dash count
                div_line = line + 1
                div_text = self.display.get(f"{div_line}.0", f"{div_line}.end")
                
                # Find where dashes start and end
                dash_start = div_text.find('-')
                if dash_start == -1:
                    return None
                dash_end = dash_start
                while dash_end < len(div_text) and div_text[dash_end] == '-':
                    dash_end += 1
                
                current_dash_len = dash_end - dash_start
                needed_dash_len = max(4, num_len)  # At least 4 dashes
                
                if needed_dash_len > current_dash_len:
                    # Expand the division line
                    extra_dashes = '-' * (needed_dash_len - current_dash_len)
                    self.display.insert(f"{div_line}.{dash_end}", extra_dashes)
        except Exception:
            pass
        return None

    def on_right(self, event=None):
        # If caret is at end of a denominator line, jump to dash line end
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            cur_line = self.display.get(f"{line}.0", f"{line}.end")
            # denominator line if previous line starts with '////'
            prev_line = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            if prev_line.lstrip().startswith(DIVISIONLINE):
                # at end?
                line_end = self.display.index(f"{line}.end")
                if pos == line_end:
                    # Move caret to end of dash line; insert a space if not present
                    dash_end = self.display.index(f"{line-1}.end")
                    # ensure a space after dashes if last char isn't space
                    last_char = self.display.get(f"{line-1}.end-1c", f"{line-1}.end")
                    if last_char != " ":
                        self.display.insert(dash_end, " ")
                        dash_end = self.display.index(f"{line-1}.end")
                    self.display.mark_set(tk.INSERT, dash_end)
                    return "break"
        except Exception:
            pass
        # default behavior
        return None

    def move_between_fraction_lines(self, direction: str) -> bool:
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            cur = self.display.get(f"{line}.0", f"{line}.end")
            above = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            below = self.display.get(f"{line+1}.0", f"{line+1}.end")

            # If on middle line '---', jump accordingly
            if cur.lstrip().startswith(DIVISIONLINE):
                target_line = line-1 if direction == "up" else line+1
                self.display.mark_set(tk.INSERT, f"{target_line}.end")
                return True

            # If on numerator with next line '---' and going down
            if below.lstrip().startswith(DIVISIONLINE) and direction == "down":
                self.display.mark_set(tk.INSERT, f"{line+2}.end")
                return True

            # If on denominator with previous line '---' and going up
            if above.lstrip().startswith(DIVISIONLINE) and direction == "up":
                self.display.mark_set(tk.INSERT, f"{line-2}.end")
                return True
        except Exception:
            return False
        return False

    def get_selection_or_word(self):
        try:
            if self.display.tag_ranges("sel"):
                return self.display.get("sel.first", "sel.last")
        except Exception:
            pass
        return None

    def replace_fraction_blocks(self, text: str) -> str:
        """Parse multi-line fractions possibly placed side-by-side.
        For any triplet of lines where the middle contains DIVISIONLINE, scan left-to-right and
        reconstruct an expression by converting each DIVISIONLINE column span into (NUM)/(DEN),
        where NUM and DEN are the contiguous non-space tokens starting at the same column
        on the lines above and below.
        Non-fraction operators/tokens are taken from the middle line.
        Other lines without DIVISIONLINE are appended as-is.
        """
        lines = text.splitlines()
        out_parts = []
        i = 0
        divlen = len(DIVISIONLINE)  # Length of the division marker
        while i < len(lines):
            if i + 2 < len(lines) and DIVISIONLINE in lines[i+1]:
                top = lines[i]
                mid = lines[i+1]
                bot = lines[i+2]
                # Normalize lengths
                maxlen = max(len(top), len(mid), len(bot))
                top = top.ljust(maxlen)
                mid = mid.ljust(maxlen)
                bot = bot.ljust(maxlen)
                j = 0
                expr = []
                while j < maxlen:
                    if mid.startswith(DIVISIONLINE, j):
                        start = j
                        end = j + divlen
                        
                        # Read token that overlaps with the division line region
                        # The token could start before 'start' and extend into/past the ---- region
                        def read_token_around(s, div_start, div_end):
                            # Find the token that covers the division line area
                            # Look backwards from div_start to find token start
                            token_start = div_start
                            while token_start > 0 and s[token_start - 1] != ' ':
                                token_start -= 1
                            # Look forwards from div_start to find token end
                            token_end = div_start
                            while token_end < len(s) and s[token_end] != ' ':
                                token_end += 1
                            token = s[token_start:token_end].strip()
                            return token
                        
                        num = read_token_around(top, start, end)
                        den = read_token_around(bot, start, end)
                            
                        if not num:
                            num = "0"
                        if not den:
                            den = "1"
                        expr.append(f"({num})/({den})")
                        # Skip ALL consecutive dashes (not just divlen)
                        while j < maxlen and mid[j] == '-':
                            j += 1
                    else:
                        ch = mid[j]
                        # Skip dash characters and spaces, only add operators
                        if ch != '-' and not ch.isspace() and ch != '/':
                            expr.append(ch)
                        j += 1
                out_parts.append(''.join(expr))
                i += 3
            else:
                out_parts.append(lines[i])
                i += 1
        return ' '.join([p for p in out_parts if p.strip()])

    # ---------------- Fraction deletion ----------------
    def on_backspace(self, event=None):
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            col = int(pos.split(".")[1])
            # Look at character to the left
            if col == 0:
                return None
            left_char = self.display.get(f"{line}.{col-1}", f"{line}.{col}")
            if left_char == DIVISIONLINE[0]:
                # Identify entire run of slashes around this point
                full_line = self.display.get(f"{line}.0", f"{line}.end")
                if DIVISIONLINE in full_line:
                    start = col-1
                    while start > 0 and full_line[start-1] == DIVISIONLINE[0]:
                        start -= 1
                    end = col
                    while end < len(full_line) and full_line[end] == DIVISIONLINE[0]:
                        end += 1
                    if end - start >= len(DIVISIONLINE):
                        # Also remove numerator and denominator tokens aligned at 'start'
                        def token_span(s, idx):
                            # Expand tabs to spaces like parser
                            s2 = s.replace('\t', '      ')
                            idx2 = idx
                            # Find token start
                            k = idx2
                            while k < len(s2) and s2[k].isspace():
                                k += 1
                            a = k
                            while k < len(s2) and not s2[k].isspace():
                                k += 1
                            b = k
                            return a, b
                        top = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
                        bot = self.display.get(f"{line+1}.0", f"{line+1}.end")
                        a_top, b_top = token_span(top, start)
                        a_bot, b_bot = token_span(bot, start)
                        if line > 1 and b_top > a_top:
                            self.display.delete(f"{line-1}.{a_top}", f"{line-1}.{b_top}")
                        self.display.delete(f"{line}.{start}", f"{line}.{end}")
                        if b_bot > a_bot:
                            self.display.delete(f"{line+1}.{a_bot}", f"{line+1}.{b_bot}")
                        self.display.mark_set(tk.INSERT, f"{line}.{start}")
                        return "break"
        except Exception:
            pass
        return None

    def on_delete_key(self, event=None):
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            col = int(pos.split(".")[1])
            cur_char = self.display.get(f"{line}.{col}", f"{line}.{col+1}")
            if cur_char == DIVISIONLINE[0]:
                full_line = self.display.get(f"{line}.0", f"{line}.end")
                if DIVISIONLINE in full_line:
                    start = col
                    while start > 0 and full_line[start-1] == DIVISIONLINE[0]:
                        start -= 1
                    end = col
                    while end < len(full_line) and full_line[end] == DIVISIONLINE[0]:
                        end += 1
                    if end - start >= len(DIVISIONLINE):
                        # Remove aligned numerator/denominator too
                        def token_span(s, idx):
                            s2 = s.replace('\t', '      ')
                            idx2 = idx
                            k = idx2
                            while k < len(s2) and s2[k].isspace():
                                k += 1
                            a = k
                            while k < len(s2) and not s2[k].isspace():
                                k += 1
                            b = k
                            return a, b
                        top = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
                        bot = self.display.get(f"{line+1}.0", f"{line+1}.end")
                        a_top, b_top = token_span(top, start)
                        a_bot, b_bot = token_span(bot, start)
                        if line > 1 and b_top > a_top:
                            self.display.delete(f"{line-1}.{a_top}", f"{line-1}.{b_top}")
                        self.display.delete(f"{line}.{start}", f"{line}.{end}")
                        if b_bot > a_bot:
                            self.display.delete(f"{line+1}.{a_bot}", f"{line+1}.{b_bot}")
                        self.display.mark_set(tk.INSERT, f"{line}.{start}")
                        return "break"
        except Exception:
            pass
        return None

    def on_operator(self, event=None):
        """Handle +, -, * operators - place them on the division line when in a fraction context."""
        if self.calc_mode != "ENG":
            return None
        
        # Get the operator character from the event
        op = event.char if event and event.char else "+"
        
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            col = int(pos.split(".")[1])
            
            cur_line = self.display.get(f"{line}.0", f"{line}.end")
            prev_line = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            next_line = self.display.get(f"{line+1}.0", f"{line+1}.end")
            
            # Check if we're on numerator line (next line has ----)
            if DIVISIONLINE in next_line:
                # Move to the division line and insert operator there
                div_line = line + 1
                div_line_text = self.display.get(f"{div_line}.0", f"{div_line}.end")
                # Pad numerator, division, and denominator lines
                new_col = max(col, len(cur_line)) + 1
                
                def ensure_col(line_no: int, col_no: int):
                    end_idx = self.display.index(f"{line_no}.end")
                    cur_col = int(end_idx.split(".")[1])
                    if cur_col < col_no:
                        self.display.insert(end_idx, " " * (col_no - cur_col))
                
                ensure_col(line, new_col)      # numerator
                ensure_col(div_line, new_col)  # division line
                ensure_col(line + 2, new_col)  # denominator
                
                # Insert operator on division line
                self.display.insert(f"{div_line}.{new_col}", op)
                self.display.mark_set(tk.INSERT, f"{div_line}.{new_col + 1}")
                return "break"
            
            # Check if we're on denominator line (prev line has ----)
            elif DIVISIONLINE in prev_line:
                # Move to the division line and insert operator there
                div_line = line - 1
                # Pad all three lines
                new_col = max(col, len(cur_line)) + 1
                
                def ensure_col(line_no: int, col_no: int):
                    end_idx = self.display.index(f"{line_no}.end")
                    cur_col = int(end_idx.split(".")[1])
                    if cur_col < col_no:
                        self.display.insert(end_idx, " " * (col_no - cur_col))
                
                ensure_col(line - 2, new_col)  # numerator
                ensure_col(div_line, new_col)  # division line
                ensure_col(line, new_col)      # denominator
                
                # Insert operator on division line
                self.display.insert(f"{div_line}.{new_col}", op)
                self.display.mark_set(tk.INSERT, f"{div_line}.{new_col + 1}")
                return "break"
            
            # Check if we're already on division line
            elif DIVISIONLINE in cur_line:
                # Pad numerator and denominator
                def ensure_col(line_no: int, col_no: int):
                    end_idx = self.display.index(f"{line_no}.end")
                    cur_col = int(end_idx.split(".")[1])
                    if cur_col < col_no:
                        self.display.insert(end_idx, " " * (col_no - cur_col))
                ensure_col(line - 1, col)
                ensure_col(line + 1, col)
                # Let normal insertion happen
                return None
                
        except Exception:
            pass
        # Default insertion of '+' continues
        return None

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
            ("exp(x)", "exp("), ("abs(x)", "abs("), ("pi", "pi"), ("e", "e"),
            ("rect(x,y)", "rect("), ("pol(r,θ)", "pol(")
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
            return "break"
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)
        expr, res = self.history[self.history_index]
        self.display.delete("1.0", "end")
        self.display.insert("1.0", expr)
        self.display.mark_set(tk.INSERT, "end-1c")
        return "break"

    def load_next(self, event=None):
        if not self.history or self.history_index is None:
            return "break"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            expr, res = self.history[self.history_index]
            self.display.delete("1.0", "end")
            self.display.insert("1.0", expr)
            self.display.mark_set(tk.INSERT, "end-1c")
        else:
            self.history_index = None
            self.display.delete("1.0", "end")
        return "break"

    def enter(self, event=None):
        self.evaluate()
        return "break"

    # ---------------- LaTeX Export ----------------
    def expr_to_latex(self, expr: str) -> str:
        """Convert a math expression to LaTeX format."""
        import re as _re
        
        # Convert fractions like (num)/(den) to \frac{num}{den}
        def replace_frac(m):
            num = m.group(1)
            den = m.group(2)
            return f"\\frac{{{num}}}{{{den}}}"
        
        latex = expr
        # Match (...)/(...)
        latex = _re.sub(r'\(([^()]+)\)/\(([^()]+)\)', replace_frac, latex)
        
        # Convert simple a/b fractions
        latex = _re.sub(r'(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)', r'\\frac{\1}{\2}', latex)
        
        # Convert functions
        latex = latex.replace('sqrt(', '\\sqrt{').replace('sin(', '\\sin(').replace('cos(', '\\cos(').replace('tan(', '\\tan(')
        latex = latex.replace('log(', '\\log(').replace('exp(', '\\exp(')
        
        # Convert sqrt closing ) to }
        latex = _re.sub(r'\\sqrt\{([^}]+)\)', r'\\sqrt{\1}', latex)
        
        # Convert pi and e
        latex = latex.replace('pi', '\\pi').replace(' e ', ' e ')
        
        # Convert multiplication
        latex = latex.replace('*', ' \\cdot ')
        
        # Convert angle notation (L angle)
        latex = _re.sub(r'(\d+(?:\.\d+)?(?:[munpkMG])?)\s*L\s*(-?\d+(?:\.\d+)?)', r'\1 \\angle \2^\\circ', latex)
        
        return latex

    def export_latex(self):
        """Export history to LaTeX and copy to clipboard."""
        if not self.history:
            self.output_label.configure(text="No history to export")
            return
        
        latex_lines = ["\\begin{align*}"]
        for expr, result in self.history:
            # Convert multi-line fraction to single line first
            expr_single = self.replace_fraction_blocks(expr)
            latex_expr = self.expr_to_latex(expr_single)
            
            # Parse result - take first line (Rect value)
            result_first = result.split('\n')[0] if '\n' in result else result
            result_first = result_first.replace('Rect:', '').strip()
            
            latex_lines.append(f"  {latex_expr} &= {result_first} \\\\")
        
        latex_lines.append("\\end{align*}")
        latex_output = "\n".join(latex_lines)
        
        # Copy to clipboard
        self.clipboard_clear()
        self.clipboard_append(latex_output)
        
        # Show confirmation
        self.output_label.configure(text="LaTeX copied to clipboard!")
        
        # Also show in a popup
        win = ctk.CTkToplevel(self)
        win.title("LaTeX Export")
        win.geometry("500x400")
        win.transient(self)
        
        ctk.CTkLabel(win, text="LaTeX Output (copied to clipboard):", font=("Arial", 12)).pack(pady=5)
        
        text_box = ctk.CTkTextbox(win, width=460, height=320, font=("Consolas", 11))
        text_box.pack(padx=10, pady=5)
        text_box.insert("1.0", latex_output)
        
        ctk.CTkButton(win, text="Close", command=win.destroy).pack(pady=5)


# ---------------- Run ----------------
if __name__ == "__main__":
    app = EngCalculator()
    app.mainloop()
