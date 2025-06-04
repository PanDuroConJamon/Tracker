import re

def lex_tree(text: str, dictionary_definitions: dict):
    tokens = []
    errors = []

    # Patrones de Expresiones Regulares Nombradas
    # El orden aquí es importante para la captura con re.finditer
    token_patterns = [
        ('COMMENT', r'//.*'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('WORD', r'[A-Za-z_][A-Za-z0-9_]*'),
        ('SPECIAL_CHAR', r'[][().,:]'),
        ('WHITESPACE', r'\s+'),
        ('MISMATCH', r'.')
    ]

    master_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns))
    lines = text.splitlines() # Usar splitlines() para manejar diferentes finales de línea

    for line_num, line_content in enumerate(lines, start=1):
        for match in master_regex.finditer(line_content):
            token_type = match.lastgroup    # Nombre del grupo que coincidió
            value = match.group(token_type) # El texto coincidente
            column = match.start() + 1      # Columna inicial (1-indexed)

            if token_type == 'COMMENT':
                tokens.append({
                    "word": value,
                    "component": "comentario",
                    "line": line_num,
                    "column": column
                })
            elif token_type == 'NUMBER':
                tokens.append({
                    "word": value,
                    "component": "numero",
                    "line": line_num,
                    "column": column
                })
            elif token_type == 'WORD':
                if value in dictionary_definitions:
                    component = dictionary_definitions[value]
                else:
                    component = "identificador"
                tokens.append({
                    "word": value,
                    "component": component,
                    "line": line_num,
                    "column": column
                })
            elif token_type == 'SPECIAL_CHAR':
                # Verificar si el carácter especial está en el diccionario de definiciones
                if value in dictionary_definitions:
                    component = dictionary_definitions[value]
                    tokens.append({
                        "word": value,
                        "component": component,
                        "line": line_num,
                        "column": column
                    })
                else:
                    # Si es un carácter especial no definido en el diccionario, es un error
                    errors.append({
                        "error": f"Símbolo especial desconocido: '{value}'",
                        "line": line_num,
                        "column": column
                    })
            elif token_type == 'WHITESPACE':
                pass  # Ignorar espacios en blanco
            elif token_type == 'MISMATCH':
                # Cualquier otro carácter que no haya coincidido con las reglas anteriores
                # es un símbolo desconocido/error.
                errors.append({
                    "error": f"Símbolo desconocido: '{value}'",
                    "line": line_num,
                    "column": column
                })
            else: # Esto no debería ocurrir si MISMATCH es el último
                 errors.append({
                    "error": f"Error de tokenización inesperado con '{value}'",
                    "line": line_num,
                    "column": column
                })


    return tokens, errors