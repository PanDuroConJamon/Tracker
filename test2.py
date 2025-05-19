import tkinter as tk
import re
import dictionary
import lexer as lex
from tkinter import ttk



class TerminalCLI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terminal CLI")
        self.geometry("800x600")
        self.configure(bg="black")

        # Marco principal
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Contador de líneas
        self.line_numbers = tk.Text(self.main_frame, width=4, bg="gray20", fg="white", font=("Courier", 12),
                                    state="disabled")
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Área de texto principal
        self.text_widget = tk.Text(
            self.main_frame,
            bg="gray",
            fg="white",
            insertbackground="white",
            font=("JetBrains Mono NL", 12),
            wrap="word",
            undo=True,
        )
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.sync_scroll_y)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Consola de errores léxicos (estilo consola)
        self.error_console = tk.Text(self, height=5, bg="black", fg="red", font=("Courier", 10), state="disabled")
        self.error_console.pack(side=tk.BOTTOM, fill=tk.X)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        # Vinculación de eventos
        self.text_widget.bind("<KeyRelease>", self.on_key_release)
        self.text_widget.bind("<MouseWheel>", self.sync_scroll)
        self.text_widget.bind("<Button-1>", self.sync_scroll)

        # Vinculación de atajos de teclado
        self.bind_shortcuts()
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        lines = self.text_widget.index("end-1c").split(".")[0]
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert(tk.END, "\n".join(str(i) for i in range(1, int(lines) + 1)))
        self.line_numbers.config(state="disabled")

    def sync_scroll(self, event):
        self.update_line_numbers()
        self.line_numbers.yview_moveto(self.text_widget.yview()[0])

    def sync_scroll_y(self, *args):
        self.text_widget.yview(*args)
        self.line_numbers.yview(*args)

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_words()

        # Atajos de teclado

    def bind_shortcuts(self):
        self.text_widget.bind("<Control-r>", self.run_command)
        self.text_widget.bind("<Control-g>", self.save_content)
        self.text_widget.bind("<Control-l>", self.load_lexicon)
        self.text_widget.bind("<Control-s>", self.load_syntactic)

    def highlight_words(self):
        # Limpia palabras resaltadas moodificadas
        for tag in self.text_widget.tag_names():
            self.text_widget.tag_remove(tag, "1.0", tk.END)

        #
        text = self.text_widget.get("1.0", tk.END)
        for word, color in dictionary.highlight_words().items():
            self.text_widget.tag_config(word, foreground=color)
            # Busca solo palabras completas
            for match in re.finditer(rf'\b{re.escape(word)}\b', text):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_widget.tag_add(word, start, end)

    def run_command(self, event=None):
        content = self.text_widget.get("1.0", tk.END).strip()
        print("[RUN]:", content)

    def save_content(self, event=None):
        content = self.text_widget.get("1.0", tk.END).strip()
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(content)
        print("[SAVE]: Content saved to output.txt")

    # def load_lexicon(self, event=None):
    #     print("[ACTION]: Ctrl + Shift + L triggered! Lexical Analysis")
    #     text = self.text_widget.get("1.0", "end-1c")
    #     tokens = lex.lex_tree(text, dictionary.tokens())
    #
    #     # Mostrar los tokens en consola
    #     for token in tokens:
    #         print(token)
    #
    #     self.show_symbol_table(tokens)

    def load_lexicon(self, event=None):
        print("[ACTION]: Ctrl + Shift + L triggered! Lexical Analysis")
        text = self.text_widget.get("1.0", "end-1c")
        errors = []
        tokens, errors = lex.lex_tree(text, dictionary.tokens())

        for token in tokens:
            print(token)

        self.show_symbol_table(tokens)

        if errors:
            self.show_lexical_errors(errors)


    def load_syntactic(self, event=None):
        print("[ACTION]: Ctrl + Shift + S triggered! Syntactic Analysis")

    def show_symbol_table(self, symbol_table):
        window = tk.Toplevel()
        window.title("Tabla de Símbolos")
        window.geometry("600x400")

        tree = ttk.Treeview(window, columns=("Lexema", "Tipo", "Línea"), show="headings")
        tree.heading("Lexema", text="Lexema")
        tree.heading("Tipo", text="Tipo")
        tree.heading("Línea", text="Línea")

        tree.column("Lexema", width=200)
        tree.column("Tipo", width=200)
        tree.column("Línea", width=100)

        for symbol in symbol_table:
            tree.insert("", "end", values=(symbol["word"], symbol["component"], symbol["line"]))

        tree.pack(fill="both", expand=True)

    def show_lexical_errors(self, errors):
        # Limpia la consola de errores
        self.error_console.config(state="normal")
        self.error_console.delete("1.0", tk.END)

        if not errors:
            self.error_console.config(state="disabled")
            return

        for error in errors:
            line = error["line"]
            message = error["error"]
            self.error_console.insert(tk.END, f"[Error Línea {line}]: {message}\n")

        self.error_console.config(state="disabled")


if __name__ == "__main__":
    app = TerminalCLI()
    app.mainloop()
