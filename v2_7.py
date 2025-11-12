import customtkinter as ctk
from tkinter import messagebox, simpledialog
from PIL import Image
import numpy as np
import math
import os


def complejo_a_fasor(z):
    r = abs(z)
    ang = math.degrees(math.atan2(z.imag, z.real))
    return f"{r:.4g}c{ang:.4g}°"


class FasorCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ===== Window setup =====
        self.title("Calculadora de Sistemas con Fasores y Complejos")
        self.geometry("950x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("pink")
        self.current_mode = "dark"

        # ===== Variables =====
        self.size = 3
        self.history = []

        # ===== Load Hello Kitty =====
        kitty_path = os.path.join(os.path.dirname(__file__), "HK.jpg")
        if os.path.exists(kitty_path):
            img = Image.open(kitty_path)
            self.bg_image = ctk.CTkImage(
                light_image=img, dark_image=img, size=(950, 600)
            )
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place_forget()
        else:
            self.bg_label = None
            print("⚠️ No se encontró HK.jpg — fondo deshabilitado.")

        # ===== Top Bar =====
        top_bar = ctk.CTkFrame(self)
        top_bar.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            top_bar, text="🌐 Calculadora de Fasores", font=("Arial", 16, "bold")
        ).pack(side="left", padx=10)

        self.theme_switch = ctk.CTkSwitch(
            top_bar,
            text="Modo Darks",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light",
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="right", padx=10)

        # ===== Main Frame =====
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Left panel -----
        self.left = ctk.CTkFrame(self.main_frame)
        self.left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        instrucciones = (
            "📘 Cómo ingresar valores:\n"
            "Puedes escribir valores como complejos o fasores.\n\n"
            "✅ Complejos: 3+4j, -2j, 5, 1.2-3j\n"
            "✅ Fasores: 10c30, 5c-90, 3c0, 2.5c45deg\n\n"
            "Ángulo en grados. Tamaño máx: 10x10"
        )
        ctk.CTkLabel(self.left, text=instrucciones, justify="left", anchor="w").pack(
            pady=5
        )

        ctk.CTkButton(self.left, text="Cambiar tamaño", command=self.change_size).pack(
            pady=5
        )

        self.frame_matrix = ctk.CTkFrame(self.left)
        self.frame_matrix.pack(pady=10)
        self.build_matrix()

        ctk.CTkButton(self.left, text="Resolver sistema", command=self.solve).pack(
            pady=10
        )

        # ----- Right panel -----
        self.right = ctk.CTkFrame(self.main_frame)
        self.right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.right, text="📜 Historial de soluciones").pack(pady=5)
        self.history_box = ctk.CTkTextbox(self.right, width=400, height=300)
        self.history_box.pack(pady=5, fill="both", expand=True)

        ctk.CTkLabel(self.right, text="Sistemas guardados").pack(pady=5)
        self.listbox = ctk.CTkOptionMenu(
            self.right, values=["(ninguno)"], command=self.load_history
        )
        self.listbox.pack(pady=5)

    # ============================================
    # MATRIX
    # ============================================
    def build_matrix(self):
        for w in self.frame_matrix.winfo_children():
            w.destroy()

        self.entries_A = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                e = ctk.CTkEntry(self.frame_matrix, width=80)
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, "1c0")
                row.append(e)
            self.entries_A.append(row)

        ctk.CTkLabel(self.frame_matrix, text="|").grid(
            row=0, column=self.size, rowspan=self.size, padx=4
        )

        self.entries_b = []
        for i in range(self.size):
            e = ctk.CTkEntry(self.frame_matrix, width=80)
            e.grid(row=i, column=self.size + 1, padx=3, pady=3)
            e.insert(0, "0")
            self.entries_b.append(e)

    def parse_value(self, text):
        text = text.replace(" ", "").replace("∠", "c")
        if "c" in text:
            r, ang = text.split("c")
            r = float(r)
            ang = ang.replace("deg", "").replace("°", "")
            ang = np.deg2rad(float(ang))
            return r * (np.cos(ang) + 1j * np.sin(ang))
        return complex(text)

    def solve(self):
        try:
            A = np.zeros((self.size, self.size), dtype=complex)
            b = np.zeros(self.size, dtype=complex)

            for i in range(self.size):
                for j in range(self.size):
                    A[i, j] = self.parse_value(self.entries_A[i][j].get())
                b[i] = self.parse_value(self.entries_b[i].get())

            x = np.linalg.solve(A, b)
            self.history.append((A.copy(), b.copy(), x.copy()))
            self.update_history_menu()

            result_str = "\n".join(
                [f"x{i+1} = {val:.4f}" for i, val in enumerate(x)]
            )
            messagebox.showinfo("Solución", result_str)

            A_fasor = [
                [complejo_a_fasor(A[i, j]) for j in range(self.size)]
                for i in range(self.size)
            ]
            b_fasor = [complejo_a_fasor(b[i]) for i in range(self.size)]
            x_fasor = [complejo_a_fasor(x[i]) for i in range(self.size)]
            self.add_to_history_view(A_fasor, b_fasor, x_fasor)
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida o matriz singular.\n\n{e}")

    def add_to_history_view(self, A_fasor, b_fasor, x_fasor):
        self.history_box.insert("end", f"\n=== SOLUCIÓN #{len(self.history)} ===\n\n")
        for i, row in enumerate(A_fasor):
            self.history_box.insert("end", f"A{i+1}: {'  '.join(row)}\n")
        self.history_box.insert("end", "\nb: " + "  ".join(b_fasor) + "\n")
        for i, val in enumerate(x_fasor):
            self.history_box.insert("end", f"x{i+1} = {val}\n")
        self.history_box.insert("end", "\n---------------------------------\n")
        self.history_box.see("end")

    def update_history_menu(self):
        items = [
            f"Sistema #{i+1} ({len(b)}x{len(b)})"
            for i, (A, b, x) in enumerate(self.history)
        ]
        self.listbox.configure(values=items)

    def load_history(self, choice):
        if not choice or choice == "(ninguno)":
            return
        idx = int(choice.split("#")[1].split()[0]) - 1
        A, b, _ = self.history[idx]
        self.size = len(b)
        self.build_matrix()
        for i in range(self.size):
            for j in range(self.size):
                self.entries_A[i][j].delete(0, "end")
                self.entries_A[i][j].insert(0, complejo_a_fasor(A[i, j]))
            self.entries_b[i].delete(0, "end")
            self.entries_b[i].insert(0, complejo_a_fasor(b[i]))

    def change_size(self):
        new_size = simpledialog.askinteger(
            "Nuevo tamaño",
            "Ingresa el tamaño de la matriz (máx 10):",
            minvalue=1,
            maxvalue=10,
        )
        if new_size:
            self.size = new_size
            self.build_matrix()

    # ============================================
    # THEME TOGGLE
    # ============================================
    def toggle_theme(self):
        new_mode = self.theme_switch.get()
        ctk.set_appearance_mode(new_mode)
        self.current_mode = new_mode

        if new_mode == "light":  # Modo Rosa
            if self.bg_label:
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.bg_label.lower()
            self.configure(fg_color="white")
            self.theme_switch.configure(text="Modo Rosa")
        else:  # Modo Darks
            if self.bg_label:
                self.bg_label.place_forget()
            self.configure(fg_color="#272727")
            self.theme_switch.configure(text="Modo Darks")


if __name__ == "__main__":
    app = FasorCalculator()
    app.mainloop()
