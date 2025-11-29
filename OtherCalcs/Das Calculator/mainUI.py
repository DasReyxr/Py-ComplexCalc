"""
------ Orlando Reyes ------
--------- Auf Das ---------
------ Das Calculator ------
-------- 15/11/2025 --------
Improvement
NUM
---
DEN

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


# ---------------- The Calculator GUI ----------------
class EngCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Das Calculator")
        self.geometry("900x700")
        self.resizable(False, False)

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
        # Fraction template on '/'
        self.display.bind("/", self.on_slash)
        # Literal inline division: Ctrl + /
        self.display.bind("<Control-Key-/>", self.on_ctrl_slash)
        self.display.bind("<KP_Divide>", self.on_ctrl_slash)
        # Exit denominator with Right arrow
        self.display.bind("<Right>", self.on_right)
        # Align '+' on dash line between fractions
        self.display.bind("+", self.on_plus)
        self.display.bind("<KP_Add>", self.on_plus)
        # Delete entire fraction when deleting a dash
        self.display.bind("<BackSpace>", self.on_backspace)
        self.display.bind("<Delete>", self.on_delete_key)
        # History with Shift + arrows
        self.display.bind("<Shift-Up>", self.load_prev)
        self.display.bind("<Shift-Down>", self.load_next)

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
            expr_for_history = self.replace_fraction_blocks(raw_expr)
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
            return  # let normal '/' in DIG
        try:
            pos = self.display.index(tk.INSERT)
            line_s, col_s = pos.split(".")
            line = int(line_s)
            col = int(col_s)

            cur_line_text = self.display.get(f"{line}.0", f"{line}.end")
            prev_line_text = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            next_line_text = self.display.get(f"{line+1}.0", f"{line+1}.end")

            import re as _re
            # Selection takes priority for numerator
            numerator_sel = None
            if self.display.tag_ranges("sel"):
                numerator_sel = self.display.get("sel.first", "sel.last")
                self.display.delete("sel.first", "sel.last")

            # Detect if we're on a dash line (contains '-----' anywhere)
            on_dash_line = ("-----" in cur_line_text)

            if on_dash_line and line > 1:
                # Inline add another fraction at current column
                # Determine numerator: from selection or from token just left of caret on current line
                if numerator_sel is not None:
                    numerator = numerator_sel
                else:
                    left_segment = self.display.get(f"{line}.0", pos)
                    m = _re.search(r"([+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m and m.group(1):
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(m.group(1))
                        # remove that token from current (dash) line
                        self.display.delete(f"{line}.{start_col}", pos)
                        col = start_col  # align to token start
                    else:
                        numerator = "NUM"

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
                self.display.insert(f"{line}.{col}", "-----")
                self.display.insert(f"{line+1}.{col}", "DEN")
                # Move caret to denominator position to keep typing
                self.display.mark_set(tk.INSERT, f"{line+1}.{col}")
                return "break"
            else:
                # Fallback: create a new vertical fraction block
                txt = self.get_selection_or_word()
                if txt is None:
                    # Try to capture numeric token immediately before caret on the same line
                    left_segment = self.display.get(f"{line}.0", pos)
                    m = _re.search(r"([+\-]?\d+(?:\.\d+)?(?:[eE][+\-]?\d+)?i?)$", left_segment)
                    if m:
                        numerator = m.group(1)
                        start_col = len(left_segment) - len(m.group(1))
                        self.display.delete(f"{line}.{start_col}", pos)
                    else:
                        numerator = "NUM"
                else:
                    numerator = txt
                    self.display.delete("sel.first", "sel.last")

                insert_at = self.display.index(tk.INSERT)
                # Indent dash/den lines to current column so the dashes align under the numerator,
                # keeping any left-side terms (e.g., '2-') outside the fraction but parseable.
                indent = " " * col
                block = f"{numerator}\n{indent}-----\n{indent}DEN"
                self.display.insert(insert_at, block)
                # place cursor at start of DEN line at same column
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
        # Insert a literal '/': allows inline divisions like 1/2/3/4
        try:
            pos = self.display.index(tk.INSERT)
            self.display.insert(pos, "/")
            line, col = map(int, pos.split("."))
            self.display.mark_set(tk.INSERT, f"{line}.{col+1}")
            return "break"
        except Exception:
            return "break"

    def on_right(self, event=None):
        # If caret is at end of a denominator line, jump to dash line end
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            cur_line = self.display.get(f"{line}.0", f"{line}.end")
            # denominator line if previous line starts with '-----'
            prev_line = self.display.get(f"{line-1}.0", f"{line-1}.end") if line > 1 else ""
            if prev_line.lstrip().startswith("-----"):
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
            if cur.lstrip().startswith("-----"):
                target_line = line-1 if direction == "up" else line+1
                self.display.mark_set(tk.INSERT, f"{target_line}.end")
                return True

            # If on numerator with next line '---' and going down
            if below.lstrip().startswith("-----") and direction == "down":
                self.display.mark_set(tk.INSERT, f"{line+2}.end")
                return True

            # If on denominator with previous line '---' and going up
            if above.lstrip().startswith("-----") and direction == "up":
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
        For any triplet of lines where the middle contains '-----', scan left-to-right and
        reconstruct an expression by converting each '-----' column span into (NUM)/(DEN),
        where NUM and DEN are the contiguous non-space tokens starting at the same column
        on the lines above and below.
        Non-fraction operators/tokens are taken from the middle (dashes) line.
        Other lines without '-----' are appended as-is.
        """
        lines = text.splitlines()
        out_parts = []
        i = 0
        while i < len(lines):
            if i + 2 < len(lines) and "-----" in lines[i+1]:
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
                # Preserve any prefix text that appears on the top line before the first dash span
                first_dash = mid.find("-----")
                if first_dash > 0:
                    prefix_text = top[:first_dash].strip()
                    if prefix_text:
                        expr.append(prefix_text)
                while j < maxlen:
                    if mid.startswith("-----", j):
                        start = j
                        end = j + 5
                        # Extract numerator and denominator tokens starting at 'start'
                        def read_token(s, idx):
                            k = idx
                            # Skip spaces
                            while k < len(s) and s[k] == ' ':
                                k += 1
                            t = []
                            while k < len(s) and s[k] != ' ':
                                t.append(s[k])
                                k += 1
                            return ''.join(t)

                        num = read_token(top, start)
                        den = read_token(bot, start)
                        if not num:
                            num = "0"
                        if not den:
                            den = "1"
                        expr.append(f"({num})/({den})")
                        j = end
                    else:
                        ch = mid[j]
                        if not ch.isspace():
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
            if left_char == '-':
                # Identify entire run of dashes around this point
                full_line = self.display.get(f"{line}.0", f"{line}.end")
                if '-----' in full_line:
                    start = col-1
                    while start > 0 and full_line[start-1] == '-':
                        start -= 1
                    end = col
                    while end < len(full_line) and full_line[end] == '-':
                        end += 1
                    if end - start >= 5:
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
            if cur_char == '-':
                full_line = self.display.get(f"{line}.0", f"{line}.end")
                if '-----' in full_line:
                    start = col
                    while start > 0 and full_line[start-1] == '-':
                        start -= 1
                    end = col
                    while end < len(full_line) and full_line[end] == '-':
                        end += 1
                    if end - start >= 5:
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

    def on_plus(self, event=None):
        if self.calc_mode != "ENG":
            return None
        try:
            pos = self.display.index(tk.INSERT)
            line = int(pos.split(".")[0])
            col = int(pos.split(".")[1])
            cur_line = self.display.get(f"{line}.0", f"{line}.end")
            if "-----" in cur_line and line > 1:
                # Ensure top and bottom lines padded to this column
                def ensure_col(line_no: int, col_no: int):
                    end_idx = self.display.index(f"{line_no}.end")
                    cur_col = int(end_idx.split(".")[1])
                    if cur_col < col_no:
                        self.display.insert(end_idx, " " * (col_no - cur_col))
                ensure_col(line-1, col)
                ensure_col(line+1, col)
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


# ---------------- Run ----------------
if __name__ == "__main__":
    app = EngCalculator()
    app.mainloop()
