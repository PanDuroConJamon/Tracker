
def highlight_words():
    return {
        "TRACK": "orange",
        "track": "orange",
        "CYCLE": "orange",
        "cycle": "orange",

        "PISTA": "orange",
        "NOTA": "orange",
        "REPETIR": "orange",
        "FRECUENCIA": "orange",
        "RETRASO": "orange",
        "INSTRUMENTO": "orange",
        "COMPONER": "orange",

        "FLAUTA": "red",
        "PLATO": "red",
        "TAMBOR": "red",
        "GUITARRA": "red",
        "BAJO": "red",

        "SEN": "light blue",
        "TRI": "light blue",
        "CUA": "light blue",
        "REC": "light blue",

    }


def tokens():
    return {
        # Palabras reservadas
        "PISTA": "PISTA",
        "NOTA": "NOTA",
        "REPETIR": "REPETIR",
        "FRECUENCIA":"FRECUENCIA",
        "RETRASO":"RETRASO",
        "INSTRUMENTO":"INSTRUMENTO",
        "COMPONER":"COMPONER",

        # Delimitadores
        "(": "_paren",
        ")": "right_paren",
        "[": "left_block",
        "]": "right_block",
        ",": "comma",
        ".": "dot",
        ":": "double_dot",

        # Tipos
        "DO": "TIPO_NOTA",
        "RE": "TIPO_NOTA",
        "MI": "TIPO_NOTA",
        "FA": "TIPO_NOTA",
        "SOL": "TIPO_NOTA",
        "LA": "TIPO_NOTA",
        "SI": "TIPO_NOTA",
        "DI": "TIPO_NOTA",

        "FLAUTA": "TIPO_INSTRUMENTO",
        "PLATO": "TIPO_INSTRUMENTO",
        "TAMBOR": "TIPO_INSTRUMENTO",
        "GUITARRA": "TIPO_INSTRUMENTO",
        "BAJO": "TIPO_INSTRUMENTO",

        "SEN": "TIPO_FRECUENCIA",
        "TRI": "TIPO_FRECUENCIA",
        "CUA": "TIPO_FRECUENCIA",
        "REC": "TIPO_FRECUENCIA",
    }
