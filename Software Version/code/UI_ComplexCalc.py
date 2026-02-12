"""
------ Iker Garcia  ------
--------- Auf Das ---------
------ Complex Calc ------
-------- 15/11/2025 -------
"""
# ------- Main Library -------

'''
python -m PyInstaller --onefile --windowed UI_ComplexCalc.py  --add-data "HK.jpg;." --add-data "IE.png;." 

'''
import numpy as np
import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
from ComplexCalc import FasorCalculatorCore, complejo_rect, complejo_a_fasor
import os
import json
from PIL import Image
import sys
import webbrowser


def resource_path(relative):
    # Use PyInstaller temp folder when frozen, otherwise use folder where this file lives
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base_path, relative)

PINK_PATH_PHOTO = resource_path("HK.jpg")
IE_PATH_PHOTO = resource_path("IE.png")

#DPINK_PATH_THEME = resource_path("DarkPink.json")
#LPINK_PATH_THEME = fr"{CURRENT_PATH}\LightPink.json"

class FasorCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Complex Calc v3.00")
        self.geometry("1400x850")  # Adjusted size to show calculator
        
        self.size = 3
        self.history = []  # session history list of tuples (A, b, x, timestamp)
        self.saved_items = []  # loaded saved items from file (list of dicts)
        self.current_mode = "dark"  # Track current mode

        # Files
        self.saved_filename = "saved_systems.txt"
        self.exported_py = "exported_systems.py"

        # core logic (UI-independent)
        self.core = FasorCalculatorCore(saved_filename=self.saved_filename, exported_py=self.exported_py)

        
        # ===== COLOR VARIABLES =====
        self.setup_colors()
        
        # Set initial theme
        #ctk.set_appearance_mode("dark")
        #ctk.ThemeManager.load_theme(DPINK_PATH_THEME)
        
        # --- Theme Selector Frame ---
        theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        theme_frame.pack(pady=(10, 6))
        
        ctk.CTkLabel(theme_frame, text="Theme:", font=("Helvetica", 11)).pack(side="left", padx=(0, 5))
        
        self.theme_selector = ctk.CTkOptionMenu(
            theme_frame,
            values=["Dark", "Light", "Pink", "Mint", "Purple", "Ocean"],
            command=self.change_theme,
            width=120
        )
        self.theme_selector.set("Dark")
        self.theme_selector.pack(side="left")

        # Header area: big title, smaller names header, and small IE image to the right
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10), padx=12)

        # Main title (left)
        self.header_title = ctk.CTkLabel(header_frame, text="Complex Calc 3.00", font=("Helvetica", 28, "bold"))
        self.header_title.pack(side="left", padx=(0, 12))

        # Smaller names subtitle (next to title)
        names_text = "Das Reyes  •  Iker Garcia  •  Roberto Lopez  •  Kevin Lara"
        self.header_names = ctk.CTkLabel(header_frame, text=names_text, font=("Helvetica", 17))
        self.header_names.pack(side="left", padx=(0, 8), pady=(8,0))

        # IE image (small) to the right of the names
        try:
            ie_small = ctk.CTkImage(
                light_image=Image.open(IE_PATH_PHOTO),
                dark_image=Image.open(IE_PATH_PHOTO),
                size=(75, 75)
            )
            self.ie_label = ctk.CTkLabel(header_frame, image=ie_small, text="", fg_color="transparent")
            self.ie_label.image = ie_small
            self.ie_label.pack(side="left", padx=(6,0))
        except Exception:
            # if image missing, keep the header layout without it
            pass

        
    
        # Set initial colors to dark mode
        self.current_colors = self.colors_dark.copy()
        # ============================
        # MAIN FRAME
        # ============================
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

          # LEFT COLUMN
        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", padx=10, pady=10)

        # Create a frame for text and image side by side
        info_frame = ctk.CTkFrame(left)
        info_frame.pack(pady=10)

        # TEXT COLUMN
        text_frame = ctk.CTkFrame(info_frame)
        text_frame.pack(side="left", padx=10)

   
        instrucciones_texto = (
            "For and By Electronics Engineers\n\n\n"
            "How to enter values:\n"
            "You can type values as complex numbers or phasors.\n"
            "Complex: 3+4j, -j2, 5, 1.2-3j\n"
            "Phasors: 10L30°, 5L-90, 3L0°, 2.5L45\n"
            "Angle in degrees. Max size: 10x10."
        )
        ctk.CTkLabel(text_frame, text=instrucciones_texto, justify="left", anchor="w").pack(pady=5)

        # keep references so we can re-style them on mode toggle
        self.btn_change_size = ctk.CTkButton(left, text="Change size", command=self.change_size)
        self.btn_change_size.pack(pady=5)
        self.btn_load_example = ctk.CTkButton(left, text="Load example", command=self.load_default_example)
        self.btn_load_example.pack(pady=5)

        self.frame_matrix = ctk.CTkFrame(left)
        self.frame_matrix.pack(pady=10)

        # Build main matrix area and buttons (unchanged)...
        self.build_matrix()
        self.btn_solve = ctk.CTkButton(left, text="Solve", command=self.solve)
        self.btn_solve.pack(pady=10)

        # Buttons for save/load
        btn_frame = ctk.CTkFrame(left)
        btn_frame.pack(pady=5)

        self.btn_load_saved = ctk.CTkButton(btn_frame, text="Load saved system", command=self.load_saved_menu_popup)
        self.btn_load_saved.grid(row=0, column=0, padx=5)
        self.btn_import = ctk.CTkButton(btn_frame, text="Import from file...", command=self.import_from_file)
        self.btn_import.grid(row=0, column=1, padx=5)
        self.btn_refresh_saved = ctk.CTkButton(btn_frame, text="Refresh saved list", command=self.load_saved_systems)
        self.btn_refresh_saved.grid(row=0, column=2, padx=5)

        # RIGHT COLUMN
        right = ctk.CTkFrame(main_frame)
        right.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(right, text="Solution history:").pack()
        self.history_box = ctk.CTkTextbox(right, width=720, height=280)
        self.history_box.pack(pady=5)
 
        # Saved systems dropdown
        ctk.CTkLabel(right, text="Saved systems:").pack()
        self.saved_menu = ctk.CTkOptionMenu(right, values=["(empty)"], command=self.load_saved_option)
        self.saved_menu.pack(pady=5)

        # ============================
        # CALCULATOR SECTION
        # ============================
        calc_frame = ctk.CTkFrame(right, border_width=1, border_color="#444444", width=300, height=280)
        calc_frame.pack(pady=5, padx=10)
        calc_frame.pack_propagate(False)  # Prevent frame from resizing to content
        
        ctk.CTkLabel(calc_frame, text="🧮 Calculadora:", font=("Helvetica", 12, "bold")).pack(pady=2)
        
        # Calculator display - shows what you're typing
        self.calc_display = ctk.CTkEntry(
            calc_frame, 
            width=260, 
            height=40, 
            font=("Courier New", 14, "bold"),
            justify="right"
        )
        self.calc_display.pack(pady=3, padx=8)
        self.calc_display.insert(0, "0")
        self.calc_display.bind("<Return>", lambda _e: self.calc_button_click("="))
        
        # Calculator state
        self.calc_memory = 0
        self.calc_current = ""
        self.calc_operation = None
        self.calc_first_operand = None
        
        # Button grid
        button_frame = ctk.CTkFrame(calc_frame)
        button_frame.pack(pady=3, padx=8)
        
        # Calculator buttons layout
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', 'j', '+', '=']
        ]
        
        self.calc_buttons = []
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                btn = ctk.CTkButton(
                    button_frame,
                    text=btn_text,
                    width=42,
                    height=32,
                    font=("Helvetica", 11, "bold"),
                    command=lambda t=btn_text: self.calc_button_click(t)
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.calc_buttons.append(btn)
        
        # Add small margin at bottom
        ctk.CTkLabel(calc_frame, text="").pack(pady=2)

        # Load saved systems on start
        self.load_saved_systems()
        # Pre-fill a default example (helps users see input format and 'i' support)
        self.load_default_example()
        # Apply initial dark mode styling
        self.apply_dark_mode_colors()

      
    def apply_dark_mode_colors(self):
        """Apply current theme colors to all widgets on startup."""
        self.configure(fg_color=self.current_colors["bg"])
        
        # Update theme selector colors
        if hasattr(self, 'theme_selector'):
            self.theme_selector.configure(
                fg_color=self.current_colors["button"],
                text_color=self.current_colors.get("label_text", "#FFFFFF"),
                button_color=self.current_colors["button_hover"]
            )
        
        # Apply colors to all widgets
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
            elif isinstance(widget, ctk.CTkOptionMenu):
                # Use palette-driven label color (don't force white)
                widget.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("label_text", self.current_colors.get("text", "#000000")),
                    button_color=self.current_colors["button_hover"]
                )
                # Try to style the underlying tk.Menu used by CTkOptionMenu
                tkmenu = getattr(widget, "_menu", None)
                if tkmenu is not None:
                    try:
                        tkmenu.configure(
                            background=self.current_colors["frame"],
                            foreground=self.current_colors["label_text"],
                            activebackground=self.current_colors["button"],
                            activeforeground=self.current_colors.get("button_text", "#FFFFFF")
                        )
                        # style each entry if supported
                        end = tkmenu.index("end")
                        if end is not None:
                            for i in range(end + 1):
                                try:
                                    tkmenu.entryconfigure(i,
                                                          background=self.current_colors["frame"],
                                                          foreground=self.current_colors["label_text"],
                                                          activebackground=self.current_colors["button"],
                                                          activeforeground=self.current_colors.get("button_text", "#FFFFFF"))
                                except Exception:
                                    pass
                    except Exception:
                        pass
                # Ensure the optionmenu's displayed label/button also uses the palette
                try:
                    for child in widget.winfo_children():
                        if isinstance(child, ctk.CTkLabel):
                            child.configure(text_color=self.current_colors["label_text"])
                        if isinstance(child, ctk.CTkButton):
                            child.configure(text_color=self.current_colors.get("button_text", "#FFFFFF"))
                except Exception:
                    pass
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(
                    fg_color=self.current_colors["textbox"],
                    text_color=self.current_colors["text"]
                )
        # Also style the specific buttons/menus we kept references for (ensures they update)
        for btn in ("btn_change_size", "btn_load_example", "btn_solve", "btn_load_saved", "btn_import", "btn_refresh_saved"):
            if hasattr(self, btn):
                getattr(self, btn).configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                     hover_color=self.current_colors["button_hover"]
                )
        
        # Style calculator buttons if they exist
        if hasattr(self, "calc_buttons"):
            for btn in self.calc_buttons:
                btn.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                    hover_color=self.current_colors["button_hover"]
                )
        
        # Style calculator display
        if hasattr(self, "calc_display"):
            self.calc_display.configure(
                fg_color=self.current_colors["entry"],
                text_color=self.current_colors["entry_text"],
                border_color=self.current_colors["border"]
            )
        
        # Ensure option menu dropdown (tk.Menu) matches theme if available
        if hasattr(self, "saved_menu"):
            # set visible optionmenu colors
            try:
                self.saved_menu.configure(fg_color=self.current_colors["button"], text_color=self.current_colors.get("label_text", "#222222"), button_color=self.current_colors["button_hover"])
            except Exception:
                pass
        if getattr(self.saved_menu, "_menu", None) is not None:
            try:
                self.saved_menu._menu.configure(background=self.current_colors["frame"], foreground=self.current_colors["label_text"], activebackground=self.current_colors["button"], activeforeground=self.current_colors.get("button_text", "#FFFFFF"))
            except Exception:
                pass

    def setup_colors(self):
        """Load color themes from themes.json"""
        theme_path = resource_path("themes.json")
        with open(theme_path, 'r') as f:
            themes = json.load(f)
        
        self.colors_dark = themes["dark"]
        self.colors_light = themes["light"]
        self.colors_pink = themes["pink"]
        self.colors_mint = themes["mint"]
        self.colors_purple = themes["purple"]
        self.colors_ocean = themes["ocean"]
                
    def change_theme(self, theme_name):
        """Change the application theme based on selection."""
        ctk.set_appearance_mode("dark")  # Always use dark appearance for CustomTkinter
        
        # Map theme names to color palettes
        theme_map = {
            "Dark": self.colors_dark,
            "Light": self.colors_light,
            "Pink": self.colors_pink,
            "Mint": self.colors_mint,
            "Purple": self.colors_purple,
            "Ocean": self.colors_ocean
        }
        
        self.current_colors = theme_map.get(theme_name, self.colors_dark).copy()
        self.current_mode = theme_name.lower()
        self.configure(fg_color=self.current_colors["bg"])
        
        # Apply colors to all widgets
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
            elif isinstance(widget, ctk.CTkOptionMenu):
                widget.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("label_text", "#222222"),
                    button_color=self.current_colors["button_hover"]
                )
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(
                    fg_color=self.current_colors["textbox"],
                    text_color=self.current_colors["text"]
                )
        
        # Re-style referenced buttons/menus
        for btn in ("btn_change_size", "btn_load_example", "btn_solve", "btn_load_saved", "btn_import", "btn_refresh_saved"):
            if hasattr(self, btn):
                getattr(self, btn).configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                    hover_color=self.current_colors["button_hover"]
                )
        
        # Style calculator components
        if hasattr(self, "calc_buttons"):
            for calc_btn in self.calc_buttons:
                calc_btn.configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                    hover_color=self.current_colors["button_hover"]
                )
        if hasattr(self, "calc_display"):
            self.calc_display.configure(
                fg_color=self.current_colors["entry"],
                text_color=self.current_colors["entry_text"],
                border_color=self.current_colors["border"]
            )
        
        # Style theme selector
        if hasattr(self, "theme_selector"):
            self.theme_selector.configure(
                fg_color=self.current_colors["button"],
                text_color=self.current_colors.get("label_text", "#222222"),
                button_color=self.current_colors["button_hover"]
            )
        
        if hasattr(self, "saved_menu"):
            self.saved_menu.configure(
                fg_color=self.current_colors["button"],
                text_color=self.current_colors.get("label_text", "#222222"),
                button_color=self.current_colors["button_hover"]
            )
            tkmenu = getattr(self.saved_menu, "_menu", None)
            if tkmenu is not None:
                try:
                    tkmenu.configure(
                        background=self.current_colors["frame"],
                        foreground=self.current_colors["label_text"],
                        activebackground=self.current_colors["button"],
                        activeforeground=self.current_colors.get("button_text", "#FFFFFF")
                    )
                except Exception:
                    pass

    def _get_all_widgets(self, parent):
        """Recursively get all widgets from parent."""
        widgets = []
        for widget in parent.winfo_children():
            widgets.append(widget)
            widgets.extend(self._get_all_widgets(widget))
        return widgets
    # ============================
    # MATRIX BUILDER
    # ============================
    def build_matrix(self):
        for w in self.frame_matrix.winfo_children():
            w.destroy()

        self.entries_A = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                e = ctk.CTkEntry(self.frame_matrix, width=130)
                # apply current theme colors immediately so new entries match current mode
                try:
                    e.configure(
                        fg_color=self.current_colors.get("entry", "#333333"),
                        text_color=self.current_colors.get("entry_text", "#FFFFFF"),
                        border_color=self.current_colors.get("border", "#555555")
                    )
                except Exception:
                    # older customtkinter versions may not support some options
                    pass
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, "1L0")
                row.append(e)
            self.entries_A.append(row)

        # Separator
        sep = ctk.CTkLabel(self.frame_matrix, text="  |  ")
        try:
            sep.configure(text_color=self.current_colors.get("label_text", "#FFFFFF"), fg_color="transparent")
        except Exception:
            pass
        sep.grid(row=0, column=self.size, rowspan=self.size)

        self.entries_b = []
        for i in range(self.size):
            e = ctk.CTkEntry(self.frame_matrix, width=130)
            try:
                e.configure(
                    fg_color=self.current_colors.get("entry", "#333333"),
                    text_color=self.current_colors.get("entry_text", "#FFFFFF"),
                    border_color=self.current_colors.get("border", "#555555")
                )
            except Exception:
                pass
            e.grid(row=i, column=self.size + 1, padx=3, pady=3)
            e.insert(0, "0")
            self.entries_b.append(e)

        # ensure referenced widgets (entries) are styled consistently with the rest of UI
        # In case other global styling is needed (option menus / buttons), call the apply function:
        try:
            self.apply_dark_mode_colors()
        except Exception:
            # fallback: ignore if apply function misbehaves
            pass
        
        # Resize window to fit new matrix size after a short delay
        self.after(100, self.dynamic_window_resize)
    def load_default_example(self):
        """Fill the matrix entries with a helpful default example.
        The example demonstrates rectangular notation with 'i' as imaginary unit.
        """
        sample_size = 3
        # ensure matrix sized correctly
        if self.size != sample_size:
            self.size = sample_size
            self.build_matrix()

        example_A = [
            ["2+1i", "-1", "0"],
            ["-1", "2+0.5i", "-1"],
            ["0", "-1", "2"],
        ]
        example_b = ["1", "0", "1i"]

        for i in range(self.size):
            for j in range(self.size):
                try:
                    self.entries_A[i][j].delete(0, "end")
                    self.entries_A[i][j].insert(0, example_A[i][j])
                except Exception:
                    pass

        for i in range(self.size):
            try:
                self.entries_b[i].delete(0, "end")
                self.entries_b[i].insert(0, example_b[i])
            except Exception:
                pass

    # ============================
    # PARSER
    # ============================
    def parse_value(self, text):
        # delegate to core parser (accepts both 'j' and 'i' for imaginary unit)
        return self.core.parse_value(text)

    # ============================
    # SOLVER
    # ============================
    def solve(self):
        try:
            # Gather strings from UI entries
            A_strings = [[self.entries_A[i][j].get() for j in range(self.size)] for i in range(self.size)]
            b_strings = [self.entries_b[i].get() for i in range(self.size)]

            # Delegate solve + formatting to core
            result = self.core.solve_from_strings(A_strings, b_strings)

            # Save in session history (store numeric arrays)
            self.history.append((result["A"].copy(), result["b"].copy(), result["x"].copy(), result["timestamp"]))
            self.update_history_menu_session()

            '''# Popup solution (rectangular numeric)
            result_sztr = "\n".join([f"x{i+1} = {val}" for i, val in enumerate(result["x"])])
            messagebox.showinfo("Solución", result_str)
            '''
            # Add to GUI history using formatted strings from core
            self.add_to_history_view(result["A_polar"], result["b_polar"], result["x_polar"], result["A_rect"], result["b_rect"], result["x_rect"], result["timestamp"])  

            # Persist using core
            try:
                self.core.save_system(result)
            except Exception as e:
                messagebox.showwarning("Advertencia", f"No se pudo guardar el sistema:\n\n{e}")

            """"
            # Print rectangular in terminal
            print("\n=== RECTANGULAR RESULTS ===")
            print("Matrix A:")
            for row in result["A"]:
                print("  ", [complex(val) for val in row])

            print("\nVector b:")
            for val in result["b"]:
                print(" ", complex(val))

            print("\nSolution x:")
            for i, val in enumerate(result["x"]):
                print(f" x{i+1} = {complex(val)}")
            """
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input or singular matrix.\n\n{e}")

    def update_history_menu_session(self):
        # Also update saved systems option menu? No: session history separate from saved files
        pass

    def add_to_history_view(self, A_f, b_f, x_f, A_r, b_r, x_r, timestamp):
        self.history_box.insert("end", "\n=== SOLUTION ===\n")
        self.history_box.insert("end", f"Saved: {timestamp}\n\n")
        '''
        # A matrix: row by row with side-by-side polar | rect
        self.history_box.insert("end", "A:\n")
        for i in range(self.size):
            left = "  " + "  ".join(A_f[i])
            right = "  " + "  ".join(A_r[i])
            # pad spacing for readability
            self.history_box.insert("end", f"{left}\n{right}\n\n")

        self.history_box.insert("end", "b:\n")
        for i in range(self.size):
            self.history_box.insert("end", f"  {b_f[i]}   |   {b_r[i]}\n")
        '''
        self.history_box.insert("end", "\nSolution:\n")
        for i in range(self.size):
            self.history_box.insert("end", f"  x{i+1} = {x_f[i]}   |   {x_r[i]}\n")

        self.history_box.insert("end", "\n----------------------------\n")

    # ============================
    # PERSISTENCE: Save & Load
    # ============================
    def save_system(self, A_f, b_f, x_f, A_r, b_r, x_r, timestamp):
        # delegate persistence to core
        result = {
            "timestamp": timestamp,
            "size": self.size,
            "A_polar": A_f,
            "b_polar": b_f,
            "x_polar": x_f,
            "A_rect": A_r,
            "b_rect": b_r,
            "x_rect": x_r,
        }
        try:
            self.core.save_system(result)
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not save the system.\n\n{e}")

        # reload saved list for UI
        self.load_saved_systems()

    def _rect_string_to_complex_literal(self, s):
        """
        Convert "a + bj" string to Python complex literal a+bj (as complex) when exporting to .py.
        We'll evaluate safely by replacing 'j' and returning a complex(...) as a Python literal in the file.
        To keep the exported file human-readable, we'll produce a complex() call.
        """
        # UI no longer performs this conversion; core does it when exporting
        raise RuntimeError("_rect_string_to_complex_literal should be called on core module")

    def load_saved_systems(self):
        """Read saved_systems.txt and populate self.saved_items and dropdown menu values."""
        try:
            self.saved_items = self.core.load_saved_items()
            if not self.saved_items:
                self.saved_menu.configure(values=["(empty)"])
                self.saved_menu.set("(empty)")
                return
            labels = []
            for i, obj in enumerate(self.saved_items, start=1):
                ts = obj.get("timestamp", "unknown time")
                labels.append(f"Saved system #{i} — {ts}")
            self.saved_menu.configure(values=labels)
            self.saved_menu.set(labels[-1])
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not read {self.saved_filename}.\n\n{e}")
            self.saved_menu.configure(values=["(empty)"])
            self.saved_menu.set("(empty)")

    def load_saved_option(self, option_text):
        """Callback when the user selects an item in saved_menu."""
        if not option_text or option_text == "(vacío)":
            return
        try:
            idx = int(option_text.split("#")[1].split(" ")[0]) - 1
            self._load_saved_by_index(idx)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load the selected system.\n\n{e}")

    def _load_saved_by_index(self, idx):
        if idx < 0 or idx >= len(self.saved_items):
            messagebox.showerror("Error", "Invalid saved system index.")
            return

        obj = self.saved_items[idx]
        size = obj.get("size", None)
        if not size:
            messagebox.showerror("Error", "The saved system does not contain size information.")
            return

        self.size = size
        self.build_matrix()

        # Fill A and b with polar values (A_polar, b_polar)
        A_p = obj.get("A_polar", None)
        b_p = obj.get("b_polar", None)
        if A_p is None or b_p is None:
            messagebox.showerror("Error", "The saved system does not contain A_polar/b_polar.")
            return

        for i in range(self.size):
            for j in range(self.size):
                try:
                    self.entries_A[i][j].delete(0, "end")
                    self.entries_A[i][j].insert(0, A_p[i][j])
                except Exception:
                    # leave default if mismatch
                    pass

        for i in range(self.size):
            try:
                self.entries_b[i].delete(0, "end")
                self.entries_b[i].insert(0, b_p[i])
            except Exception:
                pass

        messagebox.showinfo("Done", f"Saved system #{idx+1} loaded into the GUI.")

    def load_saved_menu_popup(self):
        """Alternative popup listing (just to re-open the menu if needed)."""
        # The saved_menu OptionMenu is visible; this function simply refreshes and focuses it.
        self.load_saved_systems()
        messagebox.showinfo("Info", "Saved systems list updated. Use the 'Saved systems' dropdown to select one.")

    def import_from_file(self):
        """Allow user to pick a different saved file and load its entries into the saved menu."""
        file_path = filedialog.askopenfilename(title="Select saved systems file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return
        try:
            imported = self.core.import_from_file(file_path)
            if not imported:
                messagebox.showwarning("Warning", "No valid entries found in the file.")
                return
            self.saved_items = imported
            labels = []
            for i, obj in enumerate(self.saved_items, start=1):
                ts = obj.get("timestamp", "unknown time")
                labels.append(f"Saved system #{i} — {ts}")
            self.saved_menu.configure(values=labels)
            self.saved_menu.set(labels[-1])
            messagebox.showinfo("Imported", f"Imported {len(self.saved_items)} systems from {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not import the file.\n\n{e}")

    # ============================
    # SIZE MODIFIER
    # ============================
    def change_size(self):
        """Show a themed modal dialog to change matrix size."""
        result = self._themed_size_dialog(current=self.size)
        if result is None:
            return
        try:
            new_size = int(result)
            if 1 <= new_size <= 10:
                self.size = new_size
                self.build_matrix()
                self.dynamic_window_resize()
            else:
                messagebox.showwarning("Warning", "Size must be between 1 and 10.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def _themed_size_dialog(self, current=None):
        """Create a modal CTkToplevel input dialog using current theme colors.
        Returns the string entered or None if cancelled.
        """
        dlg = ctk.CTkToplevel(self)
        dlg.title("Nuevo tamaño")
        dlg.transient(self)
        
        # Ensure dialog uses current theme colors
        frame_color = self.current_colors.get("frame", "#2d2d2d")
        label_color = self.current_colors.get("label_text", "#FFFFFF")
        entry_bg = self.current_colors.get("entry", "#333333")
        entry_text = self.current_colors.get("entry_text", "#FFFFFF")
        button_bg = self.current_colors.get("button", "#FF69B4")
        button_hover = self.current_colors.get("button_hover", "#FF1493")
        border = self.current_colors.get("border", "#555555")

        dlg.configure(fg_color=frame_color)

        # Content
        ctk.CTkLabel(dlg, text="Enter size (max 10):", text_color=label_color).pack(padx=12, pady=(12,6))

        entry = ctk.CTkEntry(dlg, width=120)
        try:
            entry.configure(fg_color=entry_bg, text_color=entry_text, border_color=border)
        except Exception:
            pass
        entry.pack(padx=12, pady=(0,12))
        if current is not None:
            entry.insert(0, str(current))
        entry.focus_set()

        res = {"value": None}

        def on_ok():
            res["value"] = entry.get()
            dlg.destroy()

        def on_cancel():
            dlg.destroy()

        btn_frame = ctk.CTkFrame(dlg, fg_color=frame_color)
        btn_frame.pack(padx=12, pady=(0,12))

        ok_btn = ctk.CTkButton(btn_frame, text="OK", width=80, command=on_ok,
                               fg_color=button_bg, hover_color=button_hover, text_color="#FFFFFF")
        cancel_btn = ctk.CTkButton(btn_frame, text="Cancelar", width=80, command=on_cancel,
                                   fg_color=button_bg, hover_color=button_hover, text_color="#FFFFFF")
        ok_btn.grid(row=0, column=0, padx=6)
        cancel_btn.grid(row=0, column=1, padx=6)

        # Force immediate styling in case customtkinter deferred theme mapping
        try:
            ok_btn.configure(fg_color=button_bg, hover_color=button_hover, text_color="#FFFFFF")
            cancel_btn.configure(fg_color=button_bg, hover_color=button_hover, text_color="#FFFFFF")
            btn_frame.configure(fg_color=frame_color)
            dlg.configure(fg_color=frame_color)
        except Exception:
            pass

        # Bind Enter/Escape
        dlg.bind("<Return>", lambda e: on_ok())
        dlg.bind("<Escape>", lambda e: on_cancel())

        # Center dialog over parent
        dlg.update_idletasks()
        w = dlg.winfo_reqwidth()
        h = dlg.winfo_reqheight()
        px = self.winfo_rootx()
        py = self.winfo_rooty()
        pw = self.winfo_width()
        ph = self.winfo_height()
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)
        dlg.geometry(f"+{x}+{y}")
        
        # Set grab after window is positioned and visible
        dlg.update()
        dlg.grab_set()

        dlg.wait_window()
        return res["value"]
        
    def dynamic_window_resize(self):
        """Dynamically resize window based on actual content size"""
        # Force update of all widgets
        self.update_idletasks()
        
        # Calculate matrix dimensions based on size
        # Each entry is approximately 130px wide + padding
        matrix_width = (self.size * 130) + ((self.size + 2) * 130) + 100  # A matrix + separator + b vector + padding
        
        # Left panel width (matrix + instructions + buttons)
        left_panel_width = max(matrix_width, 450)  # Minimum for instructions text
        
        # Right panel width (history + saved systems + calculator)
        right_panel_width = 750  # Fixed, enough for history and calculator
        
        # Calculate total width needed
        total_content_width = left_panel_width + right_panel_width + 60  # 60 for padding
        
        # Calculate height based on matrix rows
        matrix_height = (self.size * 35) + 200  # 35px per row + space for buttons and instructions
        
        # Right panel needs space for history (450px) + calculator (250px) + controls
        right_panel_height = 850
        
        total_content_height = max(matrix_height + 300, right_panel_height)  # 300 for header and other controls
        
        # Set bounds
        min_width = 1200
        max_width = 1800
        min_height = 700
        max_height = 1080
        
        # Constrain dimensions
        new_width = max(min_width, min(total_content_width, max_width))
        new_height = max(min_height, min(total_content_height, max_height))
        
        # Get current screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Don't exceed 90% of screen size
        new_width = min(new_width, int(screen_width * 0.9))
        new_height = min(new_height, int(screen_height * 0.9))
        
        # Apply new geometry
        #self.geometry(f"{new_width}x{new_height}")
        
        # Center window on screen after resize
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Ensure window stays on screen
        x = max(0, min(x, screen_width - width))
        y = max(0, min(y, screen_height - height))
        
        #self.geometry(f"{width}x{height}+{x}+{y}")

    # ============================
    # CALCULATOR METHODS
    # ============================
    def calc_button_click(self, btn_text):
        """Handle calculator button clicks."""
        current = self.calc_display.get()
        
        try:
            if btn_text == 'C':
                # Clear
                self.calc_display.delete(0, "end")
                self.calc_display.insert(0, "0")
                self.calc_current = ""
                self.calc_operation = None
                self.calc_first_operand = None
                
            elif btn_text == '=':
                # Evaluate expression
                try:
                    # First try to evaluate as a mathematical expression
                    result = self._evaluate_expression(current)
                    
                    # Format result based on whether it's complex or real
                    if isinstance(result, complex):
                        if abs(result.imag) < 1e-10:
                            # Real number
                            display_result = f"{result.real:.6g}"
                        else:
                            # Complex number - show rectangular form
                            display_result = complejo_rect(result)
                    else:
                        display_result = f"{result:.6g}"
                    
                    self.calc_display.delete(0, "end")
                    self.calc_display.insert(0, display_result)
                    self.calc_operation = None
                    self.calc_first_operand = None
                except Exception as e:
                    messagebox.showerror("Error", f"Expresión inválida:\n{current}\n\n{str(e)}")
                        
            elif btn_text in ['+', '-', '*', '/', '^']:
                # Just add the operator to the display
                if current and current != "0":
                    # If operator is ^ convert to **
                    operator = '**' if btn_text == '^' else btn_text
                    self.calc_display.insert("end", operator)
                    
        
            elif btn_text in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', 'j', '(', ')']:
                # Number or symbol input - show what you're typing
                if current == "0" and btn_text != '.':
                    self.calc_display.delete(0, "end")
                    self.calc_display.insert(0, btn_text)
                else:
                    self.calc_display.insert("end", btn_text)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error en calculadora: {e}")
    
    def _evaluate_expression(self, expr):
        """Safely evaluate a mathematical expression.
        Handles both real and complex numbers, including phasor notation.
        """
        expr = expr.strip()
        if not expr or expr == "0":
            return 0
        
        # Check if it contains phasor notation (L for angle)
        if 'L' in expr.upper():
            # Try to parse as phasor or expression with phasors
            return self.parse_value(expr)
        
        # Replace 'j' with 'J' temporarily to avoid conflicts
        expr_eval = expr.replace('J', 'j')
        expr_eval = expr.replace('i', 'j')
        
        # Check if it's a complex number expression (contains J)
        if 'j' in expr_eval:
            # Replace J back to j and parse as complex
            expr_eval = expr_eval.replace('J', 'j')
            # Try to evaluate as Python expression with complex numbers
            try:
                # Safe evaluation - only allow numbers, operators, and j
                safe_dict = {'__builtins__': {}, 'j': 1j}
                result = eval(expr_eval, safe_dict)
                return result
            except:
                # Fallback to parse_value
                return self.parse_value(expr)
        
        # It's a real number expression - evaluate it
        try:
            # Safe evaluation for real numbers
            safe_dict = {'__builtins__': {}}
            result = eval(expr_eval, safe_dict)
            return result
        except:
            # Last resort - try parse_value
            return self.parse_value(expr)
    
    def _calc_operate(self, a, b, op):
        """Perform operation between two complex numbers."""
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if abs(b) < 1e-10:
                raise ValueError("Division by zero")
            return a / b
        elif op == '^' or op == '**':
            return a ** b
        else:
            raise ValueError(f"Unknown operation: {op}")
        

if __name__ == "__main__":
    app = FasorCalculator()
    app.mainloop()