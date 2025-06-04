import re
#
# def lex_tree(text: str, dictionary: dict):
#     result = []
#     lines = text.split("\n")
#
#     # Patrones
#     number_pattern = re.compile(r'^\d+(\.\d+)?$')
#     identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')  # Comienza con letra o _, seguido de letras/números/_
#
#     for line_num, line in enumerate(lines, start=1):
#         # Separar comentarios
#         line = line.strip()
#         if '//' in line:
#             comment_index = line.find('//')
#             code_part = line[:comment_index]
#             comment = line[comment_index:]
#         else:
#             code_part = line
#             comment = ""
#
#         # Analizar código sin comentario
#         words = re.findall(r'\w+|\S', code_part)
#         for word in words:
#             if word in dictionary:
#                 component = dictionary[word]
#             elif number_pattern.match(word):
#                 component = "number"
#             elif identifier_pattern.match(word):
#                 component = "identifier"
#             else:
#                 component = "symbol"
#             result.append({
#                 "word": word,
#                 "component": component,
#                 "line": line_num
#             })
#
#         # Analizar comentario si existe
#         if comment:
#             result.append({
#                 "word": comment.strip(),
#                 "component": "comment",
#                 "line": line_num
#             })
#
#     return result
errors = []
def lex_tree(text: str, dictionary: dict):
    result = []
    errors = []
    lines = text.split("\n")

    number_pattern = re.compile(r'^\d+(\.\d+)?$')  # enteros o decimales
    identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')

    for line_num, line in enumerate(lines, start=1):
        if '//' in line:
            comment_index = line.find('//')
            code_part = line[:comment_index]
            comment = line[comment_index:]
        else:
            code_part = line
            comment = ""

        words = re.findall(r'\w+|[^\s\w]', code_part)

        for word in words:
            if word in dictionary:
                component = dictionary[word]
            elif number_pattern.match(word):
                component = "numero"
            elif identifier_pattern.match(word):
                component = "identificador"
            else:
                component = "simbolo_desconocido"
                errors.append({
                    "error": f"Símbolo desconocido: '{word}'",
                    "line": line_num
                })

            result.append({
                "palabra": word,
                "componente": component,
                "linea": line_num
            })

        if comment:
            result.append({
                "palabra": comment.strip(),
                "componente": "comentario",
                "linea": line_num
            })

    return result, errors



# import re
#
#
# def lex_tree(text: str, dictionary: dict):
#     result = []
#     lines = text.split("\n")
#
#     # Patrones para reconocer números e identificadores
#     number_pattern = re.compile(r'^\d+(\.\d+)?$')  # enteros o decimales
#     identifier_pattern = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
#
#     for line_num, line in enumerate(lines, start=1):
#         # Separar comentarios
#         if '//' in line:
#             comment_index = line.find('//')
#             code_part = line[:comment_index]
#             comment = line[comment_index:]
#         else:
#             code_part = line
#             comment = ""
#
#         # Extrae palabras y símbolos individuales
#         words = re.findall(r'\w+|[^\s\w]', code_part)
#
#         for word in words:
#             if word in dictionary:
#                 component = dictionary[word]
#             elif number_pattern.match(word):
#                 component = "number"
#             elif identifier_pattern.match(word):
#                 component = "identifier"
#             else:
#                 component = "unknown_symbol"
#
#             result.append({
#                 "word": word,
#                 "component": component,
#                 "line": line_num
#             })
#
#         if comment:
#             result.append({
#                 "word": comment.strip(),
#                 "component": "comment",
#                 "line": line_num
#             })
#
#     return result
