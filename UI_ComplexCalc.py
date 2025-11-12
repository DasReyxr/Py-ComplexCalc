import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
import numpy as np
import json, os
from datetime import datetime

# Import logic
from ComplexCalc import complejo_a_fasor, complejo_rect, FasorCalculatorLogic

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FasorCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Sistemas con Fasores y Complejos")

        self.logic = FasorCalculatorLogic()
        self.size = 3
        self.history = []
        self.saved_items = []

        self.saved_filename = "saved_systems.txt"
        self.exported_py = "exported_systems.py"

        # ====== MAIN FRAME ======
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT
        left = ctk.CTkFrame(main_frame)
        left.pack(side="left", padx=10, pady=10)

        instrucciones = (
            "📌 Cómo ingresar valores:\n"
            "✅ Complejos: 3+4j, -2j, 5, 1.2-3j\n"
            "✅ Fasores: 10c30°, 5c-90, 3c0°, 2.5c45\n"
            "Ángulo en grados. Máx tamaño: 10x10."
        )
        ctk.CTkLabel(left, text=instrucciones, justify="left").pack(pady=5)
        ctk.CTkButton(left, text="Cambiar tamaño", command=self.change_size).pack(pady=5)

        self.frame_matrix = ctk.CTkFrame(left)
        self.frame_matrix.pack(pady=10)
        self.build_matrix()

        ctk.CTkButton(left, text="Resolver", command=self.solve).pack(pady=10)

        # RIGHT
        right = ctk.CTkFrame(main_frame)
        right.pack(side="right", padx=10, pady=10)

        ctk.CTkLabel(right, text="Historial de soluciones:").pack()
        self.history_box = ctk.CTkTextbox(right, width=640, height=350)
        self.history_box.pack(pady=10)

    # ==== MATRIX ====
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

        ctk.CTkLabel(self.frame_matrix, text="  |  ").grid(row=0, column=self.size, rowspan=self.size)

        self.entries_b = []
        for i in range(self.size):
            e = ctk.CTkEntry(self.frame_matrix, width=130)
            e.grid(row=i, column=self.size + 1, padx=3, pady=3)
            e.insert(0, "0")
            self.entries_b.append(e)

    # ==== SOLVE ====
    def solve(self):
        try:
            A = np.zeros((self.size, self.size), dtype=complex)
            b = np.zeros(self.size, dtype=complex)
            for i in range(self.size):
                for j in range(self.size):
                    A[i, j] = self.logic.parse_value(self.entries_A[i][j].get())
                b[i] = self.logic.parse_value(self.entries_b[i].get())

            x = self.logic.solve_system(A, b)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result_str = "\n".join([f"x{i+1} = {val:.4f}" for i, val in enumerate(x)])
            messagebox.showinfo("Solución", result_str)

            A_f = [[complejo_a_fasor(A[i, j]) for j in range(self.size)] for i in range(self.size)]
            b_f = [complejo_a_fasor(b[i]) for i in range(self.size)]
            x_f = [complejo_a_fasor(x[i]) for i in range(self.size)]

            A_r = [[complejo_rect(A[i, j]) for j in range(self.size)] for i in range(self.size)]
            b_r = [complejo_rect(b[i]) for i in range(self.size)]
            x_r = [complejo_rect(x[i]) for i in range(self.size)]

            self.add_to_history(A_f, b_f, x_f, A_r, b_r, x_r, timestamp)

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida o matriz singular.\n\n{e}")

    def add_to_history(self, A_f, b_f, x_f, A_r, b_r, x_r, timestamp):
        box = self.history_box
        box.insert("end", f"\n=== {timestamp} ===\nA:\n")
        for i in range(self.size):
            box.insert("end", "  " + "  ".join(A_f[i]) + "\n")
            box.insert("end", "  " + "  ".join(A_r[i]) + "\n\n")
        box.insert("end", "b:\n")
        for i in range(self.size):
            box.insert("end", f"  {b_f[i]} | {b_r[i]}\n")
        box.insert("end", "Solución:\n")
        for i in range(self.size):
            box.insert("end", f"  x{i+1} = {x_f[i]} | {x_r[i]}\n")
        box.insert("end", "----------------------------\n")

    def change_size(self):
        new_size = simpledialog.askinteger("Nuevo tamaño", "Tamaño (1–10):", minvalue=1, maxvalue=10)
        if new_size:
            self.size = new_size
            self.build_matrix()


if __name__ == "__main__":
    root = ctk.CTk()
    app = FasorCalculatorApp(root)
    root.mainloop()
