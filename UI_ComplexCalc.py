# fasor_ui.py
import customtkinter as ctk
from tkinter import messagebox, simpledialog, filedialog
from ComplexCalc import FasorSystem
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FasorCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Sistemas con Fasores y Complejos")
        self.core = FasorSystem(size=3)
        self.size = 3
        self.saved_items = []

        # Layout
        main = ctk.CTkFrame(root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        left = ctk.CTkFrame(main)
        left.pack(side="left", padx=10, pady=10)

        instructions = (
            "📌 Cómo ingresar valores:\n"
            "✅ Complejos: 3+4j, -2j, 5, 1.2-3j\n"
            "✅ Fasores: 10c30°, 5c-90, 3c0°, 2.5c45"
        )
        ctk.CTkLabel(left, text=instructions, justify="left").pack()

        ctk.CTkButton(left, text="Cambiar tamaño", command=self.change_size).pack(pady=5)
        self.frame_matrix = ctk.CTkFrame(left)
        self.frame_matrix.pack(pady=10)
        self.build_matrix()

        ctk.CTkButton(left, text="Resolver", command=self.solve).pack(pady=5)
        ctk.CTkButton(left, text="Cargar sistema guardado", command=self.load_saved_menu).pack(pady=5)

        right = ctk.CTkFrame(main)
        right.pack(side="right", padx=10)
        self.history_box = ctk.CTkTextbox(right, width=600, height=400)
        self.history_box.pack()
        self.saved_menu = ctk.CTkOptionMenu(right, values=["(vacío)"], command=self.load_selected)
        self.saved_menu.pack(pady=5)
        self.refresh_saved()

    def build_matrix(self):
        for w in self.frame_matrix.winfo_children():
            w.destroy()
        self.entries_A = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                e = ctk.CTkEntry(self.frame_matrix, width=120)
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "1c0")
                row.append(e)
            self.entries_A.append(row)
        ctk.CTkLabel(self.frame_matrix, text="|").grid(row=0, column=self.size, rowspan=self.size)
        self.entries_b = []
        for i in range(self.size):
            e = ctk.CTkEntry(self.frame_matrix, width=120)
            e.grid(row=i, column=self.size + 1, padx=2, pady=2)
            e.insert(0, "0")
            self.entries_b.append(e)

    def solve(self):
        try:
            A_text = [[e.get() for e in row] for row in self.entries_A]
            b_text = [e.get() for e in self.entries_b]
            A, b, x = self.core.solve_system(A_text, b_text)
            data = self.core.export_results(A, b, x)
            self.core.save_system(data)
            self.show_result(data)
            self.refresh_saved()
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver: {e}")

    def show_result(self, data):
        self.history_box.insert("end", "\n=== NUEVA SOLUCIÓN ===\n")
        self.history_box.insert("end", f"{data['timestamp']}\n\n")
        for i, val in enumerate(data["x_polar"]):
            self.history_box.insert("end", f"x{i+1} = {val}   |   {data['x_rect'][i]}\n")

    def refresh_saved(self):
        items = self.core.load_saved_systems()
        self.saved_items = items
        if not items:
            self.saved_menu.configure(values=["(vacío)"])
            self.saved_menu.set("(vacío)")
            return
        labels = [f"Sistema #{i+1} - {it['timestamp']}" for i, it in enumerate(items)]
        self.saved_menu.configure(values=labels)
        self.saved_menu.set(labels[-1])

    def load_selected(self, label):
        if not self.saved_items or label == "(vacío)":
            return
        idx = int(label.split("#")[1].split(" ")[0]) - 1
        obj = self.saved_items[idx]
        self.size = obj["size"]
        self.build_matrix()
        A = obj["A_polar"]
        b = obj["b_polar"]
        for i in range(self.size):
            for j in range(self.size):
                self.entries_A[i][j].delete(0, "end")
                self.entries_A[i][j].insert(0, A[i][j])
            self.entries_b[i].delete(0, "end")
            self.entries_b[i].insert(0, b[i])
        messagebox.showinfo("Listo", "Sistema cargado correctamente.")

    def change_size(self):
        new_size = simpledialog.askinteger("Tamaño", "Nuevo tamaño (máx 10):", minvalue=1, maxvalue=10)
        if new_size:
            self.size = new_size
            self.build_matrix()

    def load_saved_menu(self):
        self.refresh_saved()
        messagebox.showinfo("Info", "Lista de sistemas actualizada.")

if __name__ == "__main__":
    root = ctk.CTk()
    app = FasorCalculatorApp(root)
    root.mainloop()
