import tkinter as tk


class TerminalCLI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terminal CLI")
        self.geometry("800x600")
        self.configure(bg="black")

        # Crear marco principal
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear un widget para el contador de líneas
        self.line_numbers = tk.Text(self.main_frame, width=4, bg="gray20", fg="white", font=("Courier", 12), state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Crear el widget principal de texto
        self.text_widget = tk.Text(
            self.main_frame,
            bg="gray",
            fg="white",
            insertbackground="white",
            font=("Courier", 12),
            wrap="word",
            undo=True,
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Sincronizar el desplazamiento entre widgets
        self.text_widget.bind("<KeyRelease>", self.update_line_numbers)
        self.text_widget.bind("<MouseWheel>", self.sync_scroll)
        self.text_widget.bind("<Button-1>", self.sync_scroll)
        self.text_widget.config(yscrollcommand=self.sync_scroll_y)

        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll_y)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Vincular comandos por teclas
        self.bind_shortcuts()

        # Actualizar contador de líneas al inicio
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        """Actualiza el contador de líneas en la barra lateral."""
        lines = self.text_widget.index("end-1c").split(".")[0]
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        line_numbers_text = "\n".join(str(i) for i in range(1, int(lines) + 1))
        self.line_numbers.insert(tk.END, line_numbers_text)
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, event):
        """Sincroniza el scroll entre el widget de texto y la barra de líneas."""
        self.update_line_numbers()
        self.line_numbers.yview_moveto(self.text_widget.yview()[0])

    def sync_scroll_y(self, *args):
        """Sincroniza el desplazamiento vertical de ambos widgets."""
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)

    def bind_shortcuts(self):
        """Vincula combinaciones de teclas a métodos específicos."""
        self.text_widget.bind("<Control-r>", self.run_command)     # Ctrl + R
        self.text_widget.bind("<Control-s>", self.save_content)    # Ctrl + S
        self.text_widget.bind("<Control-Shift-F>", self.custom_action)  # Ctrl + Shift + F
        # Aquí puedes seguir agregando más combinaciones

    def run_command(self, event=None):
        """Método para ejecutar un comando (Ctrl + R)."""
        content = self.text_widget.get("1.0", tk.END).strip()
        print("[RUN]:", content)
        # Aquí puedes conectar con tu lenguaje propio

    def save_content(self, event=None):
        """Método para guardar el contenido del CLI(Ctrl + S)."""
        content = self.text_widget.get("1.0", tk.END).strip()
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(content)
        print("[SAVE]: Content saved to output.txt")

    def custom_action(self, event=None):
        """Acción personalizada para Ctrl + Shift + F."""
        print("[ACTION]: Ctrl + Shift + F triggered!")
        content = self.text_widget.get("1.0", tk.END).strip()
        print("Current content:", content)
        # Aquí puedes hacer otra acción personalizada


if __name__ == "__main__":
    app = TerminalCLI()
    app.mainloop()
