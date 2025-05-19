
def highlight_words():
    return {
        "TRACK": "orange",
        "track": "orange",
        "CYCLE": "orange",
        "cycle": "orange",

        "oscar":"cyan",
        "]": "orange",
        "[": "orange"
    }


def tokens():
    return {
        "TRACK": "track",
        "track": "track",
        "CYCLE": "cycle",
        "cycle": "cycle",
        "{": "left paren",
        "}": "right paren",
        "[": "left block",
        "]": "right block"
    }
