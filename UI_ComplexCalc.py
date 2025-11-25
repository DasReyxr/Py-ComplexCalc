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
from ComplexCalc import FasorCalculatorCore
import os
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
        
        self.title("Complex Calc v2.7")
        self.geometry("1200x780")
        
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
        
        
        # --- Dark/Light Mode Switch ---
        self.mode_switch = ctk.CTkSwitch(
            self,
            text="Dark Mode",
            command=self.toggle_mode,
            onvalue="dark",
            offvalue="light",
        )
        self.mode_switch.select()  # start in dark mode
        self.mode_switch.pack(pady=(10, 6))

        # Header area: big title, smaller names header, and small IE image to the right
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10), padx=12)

        # Main title (left)
        self.header_title = ctk.CTkLabel(header_frame, text="Complex Calc 2.7", font=("Helvetica", 28, "bold"))
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
        right.pack(side="right", padx=10, pady=10)

        ctk.CTkLabel(right, text="Solution history:").pack()
        self.history_box = ctk.CTkTextbox(right, width=720, height=450)
        self.history_box.pack(pady=10)
 
        # Saved systems dropdown
        ctk.CTkLabel(right, text="Saved systems:").pack()
        self.saved_menu = ctk.CTkOptionMenu(right, values=["(empty)"], command=self.load_saved_option)
        self.saved_menu.pack(pady=5)

        # Load saved systems on start
        self.load_saved_systems()
        # Pre-fill a default example (helps users see input format and 'i' support)
        self.load_default_example()
        # Apply initial dark mode styling
        self.apply_dark_mode_colors()

      

       
       

    def apply_dark_mode_colors(self):
        """Apply dark mode colors to all widgets on startup."""
        self.configure(fg_color=self.current_colors["bg"])
        self.mode_switch.configure(
            text="Dark Mode" if self.current_mode == "dark" else "Light Mode",
            fg_color=self.current_colors["frame"],
            text_color=self.current_colors["text"],
            button_color=self.current_colors["button"],
            progress_color=self.current_colors["button"]
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
            """Define all color variables for easy customization."""
            # Dark Mode Colors (Gray / White)
            self.colors_dark = {
                "bg": "#0f0f10",           # deep dark background
                "frame": "#1f1f20",        # frame dark gray
                "text": "#FFFFFF",         # primary text white
                "button": "#3a3a3a",       # button gray
                "button_hover": "#4a4a4a", # button hover
                "entry": "#191919",        # entry bg
                "entry_text": "#FFFFFF",   # entry text
                "border": "#333333",       # borders
                "textbox": "#141414",      # textbox bg
                "label_text": "#FFFFFF",   # labels
                "button_text": "#FFFFFF",  # button label color (dark theme)
            }

            # Light Mode Colors (Light Gray / White)
            self.colors_light = {
                "bg": "#f7f7f8",           # light background
                "frame": "#ffffff",        # frame white
                "text": "#222222",         # dark text
                "button": "#e0e0e0",       # light button
                "button_hover": "#cccccc", # button hover
                "entry": "#ffffff",        # entry bg
                "entry_text": "#222222",   # entry text
                "border": "#dddddd",       # borders
                "textbox": "#ffffff",      # textbox bg
                "label_text": "#222222",   # labels
                "button_text": "#222222",  # button label color (light theme: dark text)
            }

            # preserved previous pink palette (kept commented for reference)
            # self.colors_pink = {
            #     "bg": "#FFE4F0",
            #     "frame": "#FFF0F5",
            #     "text": "#8B4789",
            #     "button": "#FF69B4",
            #     "button_hover": "#FF1493",
            #     "entry": "#FFFFFF",
            #     "entry_text": "#8B4789",
            #     "border": "#FFB6D9",
            #     "textbox": "#FFFFFF",
            #     "label_text": "#8B4789",
            #     "button_text": "#FFFFFF",
            # }
            
    def toggle_mode(self):
        """Switch between dark mode and pink mode with full color changes."""
        new_mode = self.mode_switch.get()
        ctk.set_appearance_mode("dark")  # Always use dark appearance for CustomTkinter
        self.current_mode = new_mode

        if new_mode == "light":
            # PINK MODE - Set HK image as background with transparent frames
            self.current_colors = self.colors_light.copy()
            '''
            try:
                # Get window dimensions
                self.update_idletasks()
                width = self.winfo_width()
                height = self.winfo_height()
                
                hk_bg_image = ctk.CTkImage(
                    light_image=Image.open(PINK_PATH_PHOTO),
                    dark_image=Image.open(PINK_PATH_PHOTO),
                    size=(width, height)
                )
                
                # Set main window background to light pink
                self.configure(fg_color=self.current_colors["bg"])
                
                # Create background label that fills entire window
                if hasattr(self, 'bg_label'):
                    self.bg_label.destroy()
                
                self.bg_label = ctk.CTkLabel(self, image=hk_bg_image, text="", fg_color=self.current_colors["bg"])
                self.bg_label.image = hk_bg_image
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bg_label.lower()  # Send to back
            except Exception as e:
                print(f"Error setting background image: {e}")
            '''
            self.configure(fg_color=self.current_colors["bg"])
            
            # Update switch with pink colors
            self.mode_switch.configure(
                text="Light Mode",
                fg_color=self.current_colors["button"],  # Pink background for switch
                text_color=self.current_colors["text"],  # Dark text
                button_color=self.current_colors["button_hover"],  # Deep pink dot
                progress_color=self.current_colors["button"]  # Pink progress bar
            )

        else:
            # DARK MODE - Clean dark theme
            self.current_colors = self.colors_dark.copy()
            
            # Remove background image if it exists
            if hasattr(self, 'bg_label'):
                self.bg_label.destroy()
            
            self.configure(fg_color=self.current_colors["bg"])
            
            # Update switch with dark colors
            self.mode_switch.configure(
                text="Dark Mode",
                fg_color=self.current_colors["frame"],  # Dark gray background
                text_color=self.current_colors["text"],  # White text
                button_color=self.current_colors["button"],  # Pink dot for contrast
                progress_color=self.current_colors["button"]  # Pink progress
            )
            
        # Apply colors to all widgets
        for widget in self._get_all_widgets(self):
            if isinstance(widget, ctk.CTkFrame):
                if new_mode == "light":
                    widget.configure(fg_color="transparent")  # Transparent frames in pink mode
                else:
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
                    text_color="#FFFFFF",
                    button_color=self.current_colors["button_hover"]
                )
            elif isinstance(widget, ctk.CTkTextbox):
                widget.configure(
                    fg_color=self.current_colors["textbox"],
                    text_color=self.current_colors["text"]
                )
        # Re-style referenced buttons/menus to ensure visual consistency
        for btn in ("btn_change_size", "btn_load_example", "btn_solve", "btn_load_saved", "btn_import", "btn_refresh_saved"):
            if hasattr(self, btn):
                getattr(self, btn).configure(
                    fg_color=self.current_colors["button"],
                    text_color=self.current_colors.get("button_text", "#FFFFFF"),
                     hover_color=self.current_colors["button_hover"]
                )
        if hasattr(self, "saved_menu"):
            self.saved_menu.configure(fg_color=self.current_colors["button"], text_color=self.current_colors.get("label_text", "#222222"), button_color=self.current_colors["button_hover"])
            tkmenu = getattr(self.saved_menu, "_menu", None)
            if tkmenu is not None:
                try:
                    tkmenu.configure(background=self.current_colors["frame"], foreground=self.current_colors["label_text"], activebackground=self.current_colors["button"], activeforeground=self.current_colors.get("button_text", "#FFFFFF"))
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
            result_str = "\n".join([f"x{i+1} = {val}" for i, val in enumerate(result["x"])])
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
        dlg.grab_set()

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

        dlg.wait_window()
        return res["value"]
        
    def dynamic_window_resize(self):
        """Dynamically resize window based on actual content size"""
        # Force update of all widgets
        self.update_idletasks()
        
        # Get the required size from the main frame
        main_frame = self.winfo_children()[1]  # Assuming main_frame is the second child (after mode_switch)
        
        # Calculate required dimensions with some padding
        req_width = main_frame.winfo_reqwidth() + 40  # Add padding
        req_height = main_frame.winfo_reqheight() + 100  # Add padding for mode switch and margins
        
        # Set minimum dimensions
        min_width = 1000
        min_height = 600
        
        new_width = max(req_width, min_width)
        new_height = max(req_height, min_height)
        
        # Apply new geometry
        self.geometry(f"{new_width}x{new_height}")
        
        # Center window on screen after resize
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        

if __name__ == "__main__":
    app = FasorCalculator()
    app.mainloop()