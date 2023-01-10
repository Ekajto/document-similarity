from dataclasses import dataclass
from pickle import PickleError

from loguru import logger
from nltk.metrics import edit_distance

from util import load_groups, save_groups

logger.add("logs", rotation="500 MB", format="{time} | {level} | {message}", level="DEBUG")


@dataclass
class WordsRepresentative:
    words: set[str]
    representative: str | None = None  # type: ignore


def levenshtein_groups(tokens: list[str], threshold=0.38) -> list[WordsRepresentative]:
    groups = []
    try:
        groups = load_groups()
    except (FileNotFoundError, PickleError):
        pass
    bow = set(tokens)
    representatives = [group.representative for group in groups]
    bow |= set(representatives)

    for i, word in enumerate(bow):
        logger.debug(f"Proccesing ({word}) {i+1}/{len(bow)}")
        tmp_group = next((group for group in groups if word in group.words), None)
        if tmp_group:
            logger.debug(f"Word ({word}) already in group {tmp_group.words}")
            continue
        min_ld = float("inf")
        similar_word = None
        for other_word in bow - {word}:
            ld = edit_distance(word, other_word)
            if ld < min_ld:
                min_ld = ld
                similar_word = other_word
        # If there is representative then we are going to check if relative max_distance is enough to add it to the subgroup and if not then it will not be added if there is no representative we are going to compare inf to 0 so it will directly add orphan member # noqa
        max_distance = (len(word) + len(similar_word)) * threshold / 2 if similar_word else 0
        if min_ld <= max_distance:
            if word in representatives:
                group = next(group for group in groups if group.representative == word)
                group.words.add(similar_word)  # type: ignore
                logger.debug(f"Word ({similar_word}) added to group ({group})")
            elif similar_word in representatives:
                group = next(group for group in groups if group.representative == similar_word)
                group.words.add(word)
                logger.debug(f"Word ({word}) added to group ({group})")
            else:
                groups.append(WordsRepresentative(words={word, similar_word}))  # type: ignore
                logger.debug(f"Added new group with ({word, similar_word})")
        else:
            groups.append(WordsRepresentative(words={word}))
            logger.debug(f"Added new group with ({word})")
    save_groups(groups)
    return groups


def most_similar(words: set[str]) -> str:
    if len(words) == 1:
        return next(iter(words))

    distances = {}
    for word1 in words:
        distances[word1] = 0
        for word2 in words:
            if word1 == word2:
                continue
            distance = edit_distance(word1, word2)
            distances[word1] += distance

    def avg_distance(word):
        return distances[word] / (len(words) - 1)

    return min(words, key=avg_distance)


def define_representatives(groups: list[WordsRepresentative] | None = None) -> list[WordsRepresentative]:  # type: ignore # noqa
    if not groups:
        try:
            groups = load_groups()
        except (FileNotFoundError) as e:
            raise e

    for group in groups:  # type: ignore
        words = group.words
        representative = most_similar(words)
        group.representative = representative
        logger.debug(f"{representative} is representative of {words}")
    save_groups(groups)
    return groups  # type: ignore


def replace_with_representatives(tokens: list[str], groups: list[WordsRepresentative] | None = None) -> list[str]:  # type: ignore # noqa
    if not groups:
        try:
            groups = load_groups()
        except (FileNotFoundError, PickleError) as e:
            raise e
    for i, token in enumerate(tokens):
        for group in groups:  # type: ignore
            words = group.words
            if token in words:
                tokens[i] = group.representative  # type: ignore
                logger.debug(f"Replacing ({token}) with its representative ({group.representative})")
    return tokens  # type: ignore


def process_data(tokens: list[str]):
    try:
        tokens = replace_with_representatives(tokens)
    except FileNotFoundError:
        pass
    levenshtein_groups(tokens=tokens)
    define_representatives()
    replaced_tokens = replace_with_representatives(tokens)
    return replaced_tokens
