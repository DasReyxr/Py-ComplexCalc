import numpy as np
import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
from ComplexCalc import FasorCalculatorCore
import os
from PIL import Image

CURRENT_PATH = r"C:\Users\dasre\Wkn\Python\gittcloned\Py-ComplexCalc"
PINK_PATH_PHOTO = fr"{CURRENT_PATH}\HK.jpg"
DPINK_PATH_THEME = fr"{CURRENT_PATH}\DarkPink.json"
LPINK_PATH_THEME = fr"{CURRENT_PATH}\LightPink.json"

class FasorCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Calculadora de Sistemas con Fasores y Complejos")
        self.geometry("1200x700")
        
        self.size = 3
        self.history = []  # session history list of tuples (A, b, x, timestamp)
        self.saved_items = []  # loaded saved items from file (list of dicts)
        self.current_mode = "dark"  # Track current mode

        # Files
        self.saved_filename = "saved_systems.txt"
        self.exported_py = "exported_systems.py"

        # core logic (UI-independent)
        self.core = FasorCalculatorCore(saved_filename=self.saved_filename, exported_py=self.exported_py)

        # Set initial theme
        ctk.set_appearance_mode("dark")
        ctk.ThemeManager.load_theme(DPINK_PATH_THEME)
        
        # --- Dark/Light Mode Switch ---
        # self.mode_switch = ctk.CTkSwitch(
        #     self,
        #     text="Modo oscuro",
        #     command=self.toggle_mode,
        #     onvalue="dark",
        #     offvalue="light",
        # )
        # self.mode_switch.select()  # start in dark mode
        # self.mode_switch.pack(pady=(10, 15))

        # --- Hello Kitty background image (hidden by default) ---
        image_path = os.path.join(os.path.dirname(__file__), PINK_PATH_PHOTO) 
        if os.path.exists(image_path):
            self.bg_image = ctk.CTkImage(light_image=Image.open(image_path),
                                        dark_image=Image.open(image_path),
                                        size=(520, 560))
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            # Don't place it yet — we'll only show it in Modo Rosa
        else:
            self.bg_label = None
            print("⚠️ Hello Kitty image not found — background disabled.")

        # ============================
        # MAIN FRAME
        # ============================
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT COLUMN
        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", padx=10, pady=10)

        instrucciones_texto = (
            " Cómo ingresar valores:\n"
            "Puedes escribir valores como complejos o fasores.\n"
            "Complejos: 3+4j, -2j, 5, 1.2-3j\n"
            "Fasores: 10c30°, 5c-90, 3c0°, 2.5c45\n"
            "Ángulo siempre en grados. Máximo tamaño: 10x10."
        )

        ctk.CTkLabel(left, text=instrucciones_texto, justify="left", anchor="w").pack(pady=5)

        ctk.CTkButton(left, text="Cambiar tamaño", command=self.change_size).pack(pady=5)
        ctk.CTkButton(left, text="Cargar ejemplo", command=self.load_default_example).pack(pady=5)

        self.frame_matrix = ctk.CTkFrame(left)
        self.frame_matrix.pack(pady=10)

        self.build_matrix()

        ctk.CTkButton(left, text="Resolver", command=self.solve).pack(pady=10)

        # Buttons for save/load
        btn_frame = ctk.CTkFrame(left)
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="Cargar sistema guardado", command=self.load_saved_menu_popup).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Importar desde archivo...", command=self.import_from_file).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Refrescar lista guardada", command=self.load_saved_systems).grid(row=0, column=2, padx=5)

        # RIGHT COLUMN
        right = ctk.CTkFrame(main_frame)
        right.pack(side="right", padx=10, pady=10)

        ctk.CTkLabel(right, text="Historial de soluciones:").pack()
        self.history_box = ctk.CTkTextbox(right, width=640, height=350)
        self.history_box.pack(pady=10)

        # Saved systems dropdown
        ctk.CTkLabel(right, text="Sistemas guardados:").pack()
        self.saved_menu = ctk.CTkOptionMenu(right, values=["(vacío)"], command=self.load_saved_option)
        self.saved_menu.pack(pady=5)

        # Load saved systems on start
        self.load_saved_systems()
        # Pre-fill a default example (helps users see input format and 'i' support)
        self.load_default_example()

    def toggle_mode(self):
        """Switch between dark and light modes."""
        new_mode = self.mode_switch.get()
        ctk.set_appearance_mode(new_mode)
        self.current_mode = new_mode

        if new_mode == "light":  # Modo Blanco
            ctk.ThemeManager.load_theme(LPINK_PATH_THEME)  # Load white theme
            if self.bg_label:
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bg_label.lower()
            self.configure(fg_color="white")
            self.mode_switch.configure(text="Modo Blanco")
        else:  # Modo Oscuro
            ctk.ThemeManager.load_theme(DPINK_PATH_THEME)  # Load dark theme
            if self.bg_label:
                self.bg_label.place_forget()
            self.configure(fg_color="#272727")
            self.mode_switch.configure(text="Modo Oscuro")

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
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, "1c0")
                row.append(e)
            self.entries_A.append(row)

        # Separator
        sep = ctk.CTkLabel(self.frame_matrix, text="  |  ")
        sep.grid(row=0, column=self.size, rowspan=self.size)

        self.entries_b = []
        for i in range(self.size):
            e = ctk.CTkEntry(self.frame_matrix, width=130)
            e.grid(row=i, column=self.size + 1, padx=3, pady=3)
            e.insert(0, "0")
            self.entries_b.append(e)

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

            # Popup solution (rectangular numeric)
            result_str = "\n".join([f"x{i+1} = {val}" for i, val in enumerate(result["x"])])
            messagebox.showinfo("Solución", result_str)

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
            messagebox.showerror("Error", f"Entrada inválida o matriz singular.\n\n{e}")

    def update_history_menu_session(self):
        # Also update saved systems option menu? No: session history separate from saved files
        pass

    def add_to_history_view(self, A_f, b_f, x_f, A_r, b_r, x_r, timestamp):
        self.history_box.insert("end", "\n=== SOLUCIÓN ===\n")
        self.history_box.insert("end", f"Guardado: {timestamp}\n\n")

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
        self.history_box.insert("end", "\nSolución:\n")
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
            messagebox.showwarning("Advertencia", f"No se pudo guardar el sistema.\n\n{e}")

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
                self.saved_menu.configure(values=["(vacío)"])
                self.saved_menu.set("(vacío)")
                return
            labels = []
            for i, obj in enumerate(self.saved_items, start=1):
                ts = obj.get("timestamp", "unknown time")
                labels.append(f"Sistema guardado #{i} — {ts}")
            self.saved_menu.configure(values=labels)
            self.saved_menu.set(labels[-1])
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo leer {self.saved_filename}.\n\n{e}")
            self.saved_menu.configure(values=["(vacío)"])
            self.saved_menu.set("(vacío)")

    def load_saved_option(self, option_text):
        """Callback when the user selects an item in saved_menu."""
        if not option_text or option_text == "(vacío)":
            return
        try:
            idx = int(option_text.split("#")[1].split(" ")[0]) - 1
            self._load_saved_by_index(idx)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el sistema seleccionado.\n\n{e}")

    def _load_saved_by_index(self, idx):
        if idx < 0 or idx >= len(self.saved_items):
            messagebox.showerror("Error", "Índice de sistema guardado inválido.")
            return

        obj = self.saved_items[idx]
        size = obj.get("size", None)
        if not size:
            messagebox.showerror("Error", "El sistema guardado no contiene información de tamaño.")
            return

        self.size = size
        self.build_matrix()

        # Fill A and b with polar values (A_polar, b_polar)
        A_p = obj.get("A_polar", None)
        b_p = obj.get("b_polar", None)
        if A_p is None or b_p is None:
            messagebox.showerror("Error", "El sistema guardado no contiene A_polar/b_polar.")
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

        messagebox.showinfo("Listo", f"Sistema guardado #{idx+1} cargado en la GUI.")

    def load_saved_menu_popup(self):
        """Alternative popup listing (just to re-open the menu if needed)."""
        # The saved_menu OptionMenu is visible; this function simply refreshes and focuses it.
        self.load_saved_systems()
        messagebox.showinfo("Info", "Lista de sistemas guardados actualizada. Usa el menú desplegable 'Sistemas guardados' para seleccionar uno.")

    def import_from_file(self):
        """Allow user to pick a different saved file and load its entries into the saved menu."""
        file_path = filedialog.askopenfilename(title="Selecciona archivo de sistemas guardados", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not file_path:
            return
        try:
            imported = self.core.import_from_file(file_path)
            if not imported:
                messagebox.showwarning("Advertencia", "No se encontraron entradas válidas en el archivo.")
                return
            self.saved_items = imported
            labels = []
            for i, obj in enumerate(self.saved_items, start=1):
                ts = obj.get("timestamp", "unknown time")
                labels.append(f"Sistema guardado #{i} — {ts}")
            self.saved_menu.configure(values=labels)
            self.saved_menu.set(labels[-1])
            messagebox.showinfo("Importado", f"Se importaron {len(self.saved_items)} sistemas desde {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el archivo.\n\n{e}")

    # ============================
    # SIZE MODIFIER
    # ============================
    def change_size(self):
        dialog = ctk.CTkInputDialog(
            text="Ingresa el tamaño (máx 10):",
            title="Nuevo tamaño"
        )
        
        result = dialog.get_input()
        
        if result:
            try:
                new_size = int(result)
                if 1 <= new_size <= 10:
                    self.size = new_size
                    self.build_matrix()
                    self.dynamic_window_resize()
                else:
                    messagebox.showwarning("Advertencia", "El tamaño debe estar entre 1 y 10.")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa un número válido.")
    
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