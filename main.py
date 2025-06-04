import tkinter as tk
import re
import dictionary
import lexer as lex
import parser
from tkinter import ttk



class TerminalCLI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker Terminal")
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

# SECCIÓN DE COMANDOS
    def run_command(self, event=None):
        def run_command(self, event=None):
            content = self.text_widget.get("1.0", tk.END).strip()
            print(
                f"[RUN Command Activated ({self.title()})]: Iniciando análisis completo...")  # Mensaje para la consola de Python

            # 1. Limpiar la consola de errores del IDE al inicio
            self.clear_error_console()
            self.error_console.config(state="normal")  # Asegurar que esté habilitada para inserción

            if not content:
                self.show_message_in_console("No hay código para analizar.")
                self.error_console.config(state="disabled")  # Deshabilitar al final
                return

            # 2. Realizar Análisis Léxico
            print("Ejecutando análisis léxico...")
            tokens, lexical_errors = lex.lex_tree(content, dictionary.tokens())

            # Mostrar errores léxicos si existen
            if lexical_errors:
                self.show_lexical_errors(lexical_errors)
                print(f"Errores léxicos encontrados: {len(lexical_errors)}")
            else:
                print("Análisis léxico completado sin errores.")

            # 3. Realizar Análisis Sintáctico (incluso si hay errores léxicos)
            # El parser recibirá los tokens que el lexer haya podido generar.
            # Si el lexer falló catastróficamente y 'tokens' es vacío o muy incorrecto,
            # el parser probablemente generará muchos errores, lo cual es esperado en este flujo.
            print("Ejecutando análisis sintáctico...")
            parser_obj = sintactico.Parser(tokens)  # Pasamos los tokens, sean cuales sean
            ast_resultado = parser_obj.parse()
            syntactic_errors = parser_obj.errors  # Acceder a los errores del parser

            # Mostrar errores sintácticos si existen
            if syntactic_errors:
                self.show_syntactic_errors(syntactic_errors)
                print(f"Errores sintácticos encontrados: {len(syntactic_errors)}")
            else:
                # Solo se considera éxito sintáctico si el AST se generó y no hay errores explícitos
                if ast_resultado:
                    print("Análisis sintáctico completado sin errores.")
                else:
                    # Esto puede pasar si parse() devuelve None sin añadir errores a parser_obj.errors
                    # o si los tokens eran completamente inutilizables.
                    print(
                        "Análisis sintáctico finalizó pero no generó un AST válido (posiblemente debido a tokens inutilizables).")


            if not lexical_errors and not syntactic_errors and ast_resultado:
                self.show_message_in_console(
                    "¡Análisis completo exitoso! El código es léxica y sintácticamente correcto.", is_error_header=True)

            elif lexical_errors or syntactic_errors:
                self.show_message_in_console("El análisis encontró errores. Por favor, revísalos.",
                                             is_error_header=True)
            else:  # Ni errores, ni AST (ej. código válido pero vacío después de comentarios)
                if not tokens:  # Si el lexer no produjo tokens (ej. solo comentarios o vacío)
                    self.show_message_in_console("Análisis completo: El código está vacío o solo contiene comentarios.",
                                                 is_error_header=True)
                else:  # Tokens producidos pero el parser no generó AST ni errores (caso raro)
                    self.show_message_in_console(
                        "Análisis completo finalizado. No se generó AST ni se reportaron errores explícitos.",
                        is_error_header=True)

            # 5. Deshabilitar la consola de errores al final de todas las operaciones de inserción
            self.error_console.config(state="disabled")
            print("Proceso de run_command finalizado.")

    def save_content(self, event=None):
        content = self.text_widget.get("1.0", tk.END).strip()
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(content)
        print("[SAVE]: Content saved to output.txt")

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
        print("[ACTION]: Ctrl + S triggered! Syntactic Analysis")  # O tu atajo actual
        self.clear_error_console()  # Limpia la consola de errores primero

        text_content = self.text_widget.get("1.0", "end-1c")

        # 1. Análisis Léxico
        tokens, lexical_errors = lex.lex_tree(text_content, dictionary.tokens())

        if lexical_errors:
            self.show_lexical_errors(lexical_errors)
            self.show_message_in_console("Corrija los errores léxicos antes del análisis sintáctico.")
            return

        if not tokens:
            self.show_message_in_console(
                "No hay tokens para el análisis sintáctico (código fuente vacío o solo comentarios).")
            return


        parser_obj = parser.Parser(tokens)
        ast_resultado = parser_obj.parse()

        if parser_obj.errors:
            self.show_syntactic_errors(parser_obj.errors)
            self.show_message_in_console("El análisis sintáctico encontró errores.")
        elif ast_resultado:
            self.show_message_in_console("¡Análisis Sintáctico Exitoso!")
            self.display_ast_in_treeview(ast_resultado)
        else:
            self.show_message_in_console("El análisis sintáctico no produjo un resultado o falló inesperadamente.")

# FIN SECCI

    def clear_error_console(self):
        """Limpia la consola de errores."""
        self.error_console.config(state="normal")
        self.error_console.delete("1.0", tk.END)
        self.error_console.config(state="disabled")

    def show_message_in_console(self, message):
        """Muestra un mensaje general en la consola de errores."""
        self.error_console.config(state="normal")
        self.error_console.insert(tk.END, message + "\n")
        self.error_console.config(state="disabled")

    def show_syntactic_errors(self, errors):
        """Muestra los errores sintácticos en la consola de errores."""
        self.error_console.config(state="normal")

        if not errors:
            self.error_console.config(state="disabled")
            return

        self.error_console.insert(tk.END, "--- Errores Sintácticos ---\n")
        for error_info in errors:
            line = error_info.get("line", "N/A")
            column_info = f", Columna {error_info['column']}" if error_info.get('column') and error_info[
                'column'] != 'desconocida' else ""
            message = error_info.get("error", "Error desconocido.")
            self.error_console.insert(tk.END, f"[Error Línea {line}{column_info}]: {message}\n")

        self.error_console.config(state="disabled")

    def display_ast_in_treeview(self, ast_node, parent_item=""):
        """Muestra el AST en una nueva ventana con un ttk.Treeview.
           Llama a esta función recursivamente para construir el árbol.
        """
        # Crear la ventana y el Treeview solo la primera vez (cuando parent_item está vacío)
        if parent_item == "":
            # Si ya existe una ventana de AST, la destruimos para crear una nueva
            if hasattr(self, 'ast_window') and self.ast_window.winfo_exists():
                self.ast_window.destroy()

            self.ast_window = tk.Toplevel(self)
            self.ast_window.title("Árbol de Sintaxis Abstracta (AST)")
            self.ast_window.geometry("800x600")  # Ajusta el tamaño según necesites

            self.ast_tree = ttk.Treeview(self.ast_window)
            self.ast_tree.pack(expand=True, fill=tk.BOTH)

        # Procesar el nodo actual del AST
        if isinstance(ast_node, dict):
            node_type = ast_node.get("type", "NodoDiccionario")

            # Construir el texto del item, mostrando otros atributos clave
            attributes_display = []
            for key, value in ast_node.items():
                if key != "type" and not isinstance(value, (dict, list)):
                    attributes_display.append(f"{key}: {value}")

            item_text = f"{node_type}"
            if attributes_display:
                item_text += f"  ({', '.join(attributes_display)})"

            current_tree_item = self.ast_tree.insert(parent_item, "end", text=item_text, open=True)

            # Recorrer los hijos del diccionario que son diccionarios o listas
            for key, value in ast_node.items():
                if key == "type":  # Ya se usó
                    continue
                if isinstance(value, dict):
                    # Para un hijo que es un diccionario, crear un nodo que represente la clave
                    key_item = self.ast_tree.insert(current_tree_item, "end", text=f"<{key}>", open=True)
                    self.display_ast_in_treeview(value, key_item)  # Llamada recursiva para el valor (dict)
                elif isinstance(value, list):
                    # Para un hijo que es una lista, crear un nodo que represente la clave
                    key_item = self.ast_tree.insert(current_tree_item, "end", text=f"<{key} (lista)>", open=True)
                    self.display_ast_in_treeview(value, key_item)  # Llamada recursiva para el valor (list)

        elif isinstance(ast_node, list):
            for i, item in enumerate(ast_node):
                self.display_ast_in_treeview(item, parent_item)



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
