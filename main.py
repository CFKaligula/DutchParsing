from src.rhyme import RhymeType, get_rhyme_words_from_dictionaries
from src.word import Word


def split(input_word: str) -> None:
    """splits the input word in syllables and prints them"""
    word = Word(input_word)
    print(word.get_split_word(), end=' ')


def get_pronunciation(input_word: str) -> None:
    """gives the phonetic version of the input word"""
    word = Word(input_word)
    print(word.pronunciation, end=' ')


def find_rhyme(input_word: str, rhyme_type: RhymeType) -> None:
    """finds the rhyme words for the input word and prints them"""

    rhyme_words = get_rhyme_words_from_dictionaries(input_word, rhyme_type)
    print(f'Found rhyme words: {", ".join(rhyme_words)}')
