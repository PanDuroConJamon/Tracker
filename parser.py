# parser.py (Versión Actualizada)

class Parser:
    def __init__(self, tokens):
        self.tokens = [token for token in tokens if token['component'] != 'comentario']  # Ignorar comentarios
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.errors = []

    def _advance(self):
        """Avanza al siguiente token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def _consume(self, expected_component, error_message=None):
        """Consume el token actual si es del tipo esperado, sino registra un error."""
        if self.current_token and self.current_token['component'] == expected_component:
            token = self.current_token
            self._advance()
            return token
        else:
            if not error_message:
                error_message = f"Se esperaba token '{expected_component}' pero se encontró '{self.current_token['component'] if self.current_token else 'EOF'}'"
            line = self.current_token['line'] if self.current_token else 'desconocida'
            column = self.current_token.get('column', 'desconocida') if self.current_token else ''
            self.errors.append({"error": error_message, "line": line, "column": column})
            raise SyntaxError(error_message)

    def _match_token_word(self, expected_component, expected_word, error_message=None):
        """Consume el token actual si es del tipo y palabra esperada."""
        if self.current_token and \
                self.current_token['component'] == expected_component and \
                self.current_token['word'] == expected_word:
            token = self.current_token
            self._advance()
            return token
        else:
            if not error_message:
                error_message = f"Se esperaba token '{expected_component}' con valor '{expected_word}' pero se encontró '{self.current_token['word'] if self.current_token else 'EOF'}'"
            line = self.current_token['line'] if self.current_token else 'desconocida'
            column = self.current_token.get('column', 'desconocida') if self.current_token else ''
            self.errors.append({"error": error_message, "line": line, "column": column})
            raise SyntaxError(error_message)

    def parse(self):
        """Método principal para iniciar el análisis."""
        if not self.tokens:
            return {"type": "programa", "lista_instrucciones": []}

        ast = self.parse_programa()
        if self.current_token is not None and not self.errors:
            self.errors.append({
                "error": f"Tokens inesperados al final del programa, comenzando con '{self.current_token['word']}'",
                "line": self.current_token['line'],
                "column": self.current_token.get('column', '')
            })
        if self.errors:
            return None
        return ast

    # GRAMMAR RULES PARSING METHODS

    def parse_programa(self):
        try:
            lista_instrucciones_node = self.parse_lista_instrucciones()
            return {"type": "programa", "lista_instrucciones": lista_instrucciones_node}
        except SyntaxError:
            return None

    def parse_lista_instrucciones(self):
        instructions = []
        while self.current_token and self._can_start_instruccion(self.current_token['component']):
            try:
                instruccion = self.parse_instrucciones()
                if instruccion:
                    instructions.append(instruccion)
            except SyntaxError:
                # Si una instrucción falla, detenemos la lista o intentamos recuperación.
                # Por ahora, un error en una instrucción detiene el parseo de más instrucciones en esta lista.
                break
        return instructions

    def _can_start_instruccion(self, token_component):
        """Verifica si un token puede iniciar una regla de 'instrucciones'."""
        return token_component in [
            "retraso", "nota", "frecuencia", "pista",
            "bloq_izq", "repetir", "componer",
            "identificador"  # Añadido para referencias de pista
        ]

    def parse_tipo_nota(self):
        if self.current_token and self.current_token['component'] == 'tipo_nota':
            token_word = self.current_token['word']
            self._advance()
            return {"type": "tipo_nota", "value": token_word}
        else:
            self._consume('tipo_nota', "Se esperaba un tipo de nota (DO, RE, etc.)")

    def parse_tipo_instrumento(self):
        if self.current_token and self.current_token['component'] == 'tipo_instrumento':
            token_word = self.current_token['word']
            self._advance()
            return {"type": "tipo_instrumento", "value": token_word}
        else:
            self._consume('tipo_instrumento', "Se esperaba un tipo de instrumento (FLAUTA, etc.)")

    def parse_tipo_frecuencia(self):
        if self.current_token and self.current_token['component'] == 'tipo_frecuencia':
            token_word = self.current_token['word']
            self._advance()
            return {"type": "tipo_frecuencia", "value": token_word}
        else:
            self._consume('tipo_frecuencia', "Se esperaba un tipo de frecuencia (SEN, etc.)")

    def parse_modificador_retraso(self):
        # Se asume que el '.' ya fue consumido o verificado
        self._consume('retraso', "Se esperaba la palabra clave 'RETRASO' después de '.'")
        self._consume('paren_izq', "Se esperaba '(' después de 'RETRASO'")
        numero_token = self._consume('numero', "Se esperaba un número para el valor de RETRASO")
        self._consume('paren_der', "Se esperaba ')' después del número de RETRASO")
        return {"type": "modificador_retraso", "value": float(numero_token['word'])}

    def parse_modificador_instrumento(self):
        # Se asume que el '.' ya fue consumido o verificado
        self._consume('instrumento', "Se esperaba la palabra clave 'INSTRUMENTO' después de '.'")
        self._consume('paren_izq', "Se esperaba '(' después de 'INSTRUMENTO'")
        tipo_instrumento_node = self.parse_tipo_instrumento()
        self._consume('paren_der', "Se esperaba ')' después del tipo de instrumento")
        return {"type": "modificador_instrumento", "value": tipo_instrumento_node['value']}

    def parse_instrucciones(self):
        if not self.current_token:
            self.errors.append(
                {"error": "Se esperaba una instrucción, pero se encontró fin de archivo.", "line": "EOF", "column": ""})
            raise SyntaxError("EOF inesperado")

        token_comp = self.current_token['component']
        node = None

        if token_comp == 'retraso':  # 'RETRASO' '(' numero ')'
            self._advance()
            self._consume('paren_izq')
            numero_token = self._consume('numero')
            self._consume('paren_der')
            node = {"type": "comando_retraso", "value": float(numero_token['word'])}

        elif token_comp == 'nota':  # 'NOTA' '(' tipo_nota ',' numero ',' numero ')' [modificadores]
            self._advance()
            self._consume('paren_izq')
            tipo_nota_node = self.parse_tipo_nota()
            self._consume('coma')
            numero1_token = self._consume('numero')
            self._consume('coma')
            numero2_token = self._consume('numero')
            self._consume('paren_der')

            node_nota = {
                "type": "nota_musical",
                "nota": tipo_nota_node['value'],
                "param1": float(numero1_token['word']),
                "param2": float(numero2_token['word']),
                "instrumento": None,
                "retraso": None
            }

            # Manejo de modificadores opcionales: .INSTRUMENTO() y/o .RETRASO()
            # Asumimos que si ambos están, .INSTRUMENTO va primero, luego .RETRASO
            # Check for '.INSTRUMENTO'
            if self.current_token and self.current_token['component'] == 'punto':
                # Guardamos el estado por si el modificador no es el esperado o falla
                idx_backup = self.current_token_index
                try:
                    token_punto = self.current_token  # Guardamos el token '.'
                    self._advance()  # Avanzamos después del '.'

                    if self.current_token and self.current_token['component'] == 'instrumento':
                        node_nota['instrumento'] = self.parse_modificador_instrumento()
                        # Después de un instrumento, podría venir un retraso
                        if self.current_token and self.current_token['component'] == 'punto':
                            idx_backup_2 = self.current_token_index
                            try:
                                self._advance()  # Avanzamos después del segundo '.'
                                if self.current_token and self.current_token['component'] == 'retraso':
                                    node_nota['retraso'] = self.parse_modificador_retraso()
                                else:  # No es .RETRASO, retroceder el '.' y el token siguiente
                                    self.current_token_index = idx_backup_2
                                    self.current_token = self.tokens[self.current_token_index]
                            except SyntaxError:
                                self.current_token_index = idx_backup_2
                                self.current_token = self.tokens[self.current_token_index]
                                if self.errors and self.errors[-1]['line'] == self.current_token[
                                    'line']: self.errors.pop()

                    elif self.current_token and self.current_token['component'] == 'retraso':
                        node_nota['retraso'] = self.parse_modificador_retraso()

                    else:  # No es ni .INSTRUMENTO ni .RETRASO, retroceder al estado antes del primer '.'
                        self.current_token_index = idx_backup
                        self.current_token = self.tokens[self.current_token_index]
                except SyntaxError:
                    self.current_token_index = idx_backup
                    self.current_token = self.tokens[self.current_token_index]
                    # Si hubo un error intentando parsear el modificador, lo eliminamos de la lista de errores
                    # para no reportar un error por un modificador opcional que no estaba o estaba malformado.
                    if self.errors and self.errors[-1]['line'] == (
                    token_punto['line'] if token_punto else 'desconocida'): self.errors.pop()

            node = node_nota

        elif token_comp == 'frecuencia':
            self._advance()
            self._consume('paren_izq')
            tipo_frecuencia_node = self.parse_tipo_frecuencia()
            self._consume('coma')
            numero1_token = self._consume('numero')
            self._consume('coma')
            numero2_token = self._consume('numero')
            self._consume('coma')
            numero3_token = self._consume('numero')
            self._consume('paren_der')

            node_frec = {
                "type": "frecuencia_cmd",
                "frec_type": tipo_frecuencia_node['value'],
                "param1": float(numero1_token['word']),
                "param2": float(numero2_token['word']),
                "param3": float(numero3_token['word']),
                "retraso": None
            }
            if self.current_token and self.current_token['component'] == 'punto':
                idx_backup = self.current_token_index
                token_punto = self.current_token
                try:
                    self._advance()
                    if self.current_token and self.current_token['component'] == 'retraso':
                        node_frec['retraso'] = self.parse_modificador_retraso()
                    else:
                        self.current_token_index = idx_backup
                        self.current_token = self.tokens[self.current_token_index]
                except SyntaxError:
                    self.current_token_index = idx_backup
                    self.current_token = self.tokens[self.current_token_index]
                    if self.errors and self.errors[-1]['line'] == (
                    token_punto['line'] if token_punto else 'desconocida'): self.errors.pop()
            node = node_frec

        elif token_comp == 'pista':  # 'PISTA' identificador ':' lista_instrucciones
            self._advance()
            id_token = self._consume('identificador', "Se esperaba un nombre de identificador para PISTA")
            self._consume('double_punto', "Se esperaba ':' después del nombre de PISTA")
            # CAMBIO: Ahora se espera una lista_instrucciones
            lista_instrucciones_pista = self.parse_lista_instrucciones()
            node = {"type": "pista_definicion", "name": id_token['word'], "body": lista_instrucciones_pista}

        elif token_comp == 'bloq_izq':  # '[' lista_instrucciones ']'
            self._advance()
            instrucciones_internas_node = self.parse_lista_instrucciones()  # Ya estaba así, correcto
            self._consume('bloq_der', "Se esperaba ']' para cerrar el bloque de instrucciones")
            node = {"type": "bloque_instrucciones", "body": instrucciones_internas_node}

        elif token_comp == 'repetir':
            self._advance()
            self._consume('paren_izq')
            numero_token = self._consume('numero')
            self._consume('paren_der')
            node = {"type": "repetir_cmd", "count": int(numero_token['word'])}

        elif token_comp == 'componer':  # 'COMPONER' ':' lista_instrucciones
            self._advance()
            self._consume('double_punto', "Se esperaba ':' después de 'COMPONER'")
            # CAMBIO: Ahora se espera una lista_instrucciones
            lista_instrucciones_componer = self.parse_lista_instrucciones()
            node = {"type": "componer_bloque", "body": lista_instrucciones_componer}

        elif token_comp == 'identificador':  # NUEVA REGLA: identificador (como referencia a pista)
            id_token = self.current_token
            self._advance()  # Consume el identificador
            node = {"type": "referencia_pista", "name": id_token['word']}
            # Aquí podrías, en una etapa semántica, verificar si esta pista ha sido definida.

        else:
            err_msg = f"Instrucción desconocida o inesperada comenzando con token '{self.current_token['word']}' ({self.current_token['component']})"
            self.errors.append({
                "error": err_msg,
                "line": self.current_token['line'],
                "column": self.current_token.get('column', '')
            })
            raise SyntaxError(err_msg)

        return node