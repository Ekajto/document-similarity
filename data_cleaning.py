import string


def remove_head(txt):
    lines = txt.split("\n")
    index = next((i for i, line in enumerate(lines) if "ISBN" in line), -1)
    if index != -1:
        lines = lines[index + 1 :]  # noqa
    return "\n".join(lines)


def remove_tail(txt):
    lines = txt.split("\n")
    index = next((i for i, line in enumerate(reversed(lines)) if "-----" in line), -1)
    if index != -1:
        lines = lines[: len(lines) - index - 1]

    return "\n".join(lines)


def remove_punctuations(txt):
    punct = string.punctuation + "—…„”"
    return "".join([c for c in txt if c not in punct])


def remove_stopwords(txt):
    STOPWORDS_FILE = "polish_stopwords.txt"
    with open(STOPWORDS_FILE) as file:
        sw = [line.rstrip() for line in file]

    return " ".join([w for w in txt.split() if w.lower() not in sw])


def clean_data(txt) -> list[str]:
    txt = remove_head(txt)
    txt = remove_tail(txt)
    txt = txt.replace("\n", " ").replace("\r", " ").replace("'", "")
    txt = remove_punctuations(txt)
    txt = remove_stopwords(txt)
    return txt.lower().split()
