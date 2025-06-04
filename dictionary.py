
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
        "PISTA": "pista",
        "NOTA": "nota",
        "REPETIR": "repetir",
        "FRECUENCIA":"frecuencia",
        "RETRASO":"retraso",
        "INSTRUMENTO":"instrumento",
        "COMPONER":"componer",

        # Delimitadores
        "(": "paren_izq",
        ")": "paren_der",
        "[": "bloq_izq",
        "]": "bloq_der",
        ",": "coma",
        ".": "punto",
        ":": "double_punto",

        # Tipos
        "DO": "tipo_nota",
        "RE": "tipo_nota",
        "MI": "tipo_nota",
        "FA": "tipo_nota",
        "SOL": "tipo_nota",
        "LA": "tipo_nota",
        "SI": "tipo_nota",
        "DI": "tipo_nota",

        "FLAUTA": "tipo_instrumento",
        "PLATO": "tipo_instrumento",
        "TAMBOR": "tipo_instrumento",
        "GUITARRA": "tipo_instrumento",
        "BAJO": "tipo_instrumento",

        "SEN": "tipo_frecuencia",
        "TRI": "tipo_frecuencia",
        "CUA": "tipo_frecuencia",
        "REC": "tipo_frecuencia",
    }
