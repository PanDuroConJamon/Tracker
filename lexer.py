import re


def lex_tree(text: str, dictionary: dict):
    result = []
    lines = text.split("\n")

    for line_num, line in enumerate(lines, start=1):
        # Extrae palabras usando una expresión regular
        words = re.findall(r'\w+|\S', line)

        for word in words:
            component = dictionary.get(word, "identifier")
            result.append({
                "word": word,
                "component": component,
                "line": line_num
            })

    return result
