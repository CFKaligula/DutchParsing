import enum
import json
import os

import logbasic  # type: ignore

from src.word import Word


class RhymeType(enum.Enum):
    FULL = 'full'
    VOWEL = 'vowel'


RHYME_FUNCTIONS = {
    RhymeType.FULL: Word.get_rhyme_part,
    RhymeType.VOWEL: Word.get_phonetic_vowels,
}

OUTPUT_FOLDER_PATH = 'output'

FULL_DICTIONARY_PATH = os.path.join(OUTPUT_FOLDER_PATH, 'full_dictionary.json')
VOWEL_DICTIONARY_PATH = os.path.join(OUTPUT_FOLDER_PATH, 'vowel_dictionary.json')
N_SYLLABLES_DICTIONARY_PATH = os.path.join(OUTPUT_FOLDER_PATH, 'n_syllables_dictionary.json')


def create_rhyme_dictionaries() -> None:
    """
    Creates the rhyme dictionaries from the input text files and saves them as json files."""

    if not os.path.exists(OUTPUT_FOLDER_PATH):
        os.makedirs(OUTPUT_FOLDER_PATH, exist_ok=True)

    input_dictionary_paths = [
        os.path.join('assets', 'text_files', 'basiswoorden.txt'),
        os.path.join('assets', 'text_files', 'Dutch_Word_List.txt'),
        os.path.join('assets', 'text_files', 'DutchDictionary.txt'),
    ]

    full_dictionary = {}
    vowel_dictionary = {}
    n_syllables_dictionary = {}
    logbasic.info('Reading dictionaries...')
    for dictionary_path in input_dictionary_paths:
        logbasic.info(f'Reading dictionary from {dictionary_path}...')
        with open(dictionary_path, 'r', encoding='utf-8') as dictionary_file:
            dictionary = dictionary_file.read().split()

        for entry in dictionary:
            if entry not in full_dictionary or entry not in vowel_dictionary:
                word = Word(entry)

                rhyme_part = word.get_rhyme_part()
                full_dictionary[word.text] = rhyme_part

                phonetic_vowels = word.get_phonetic_vowels()
                vowel_dictionary[word.text] = phonetic_vowels

                n_syllables = len(word.syllables)
                n_syllables_dictionary[word.text] = n_syllables

    with open(FULL_DICTIONARY_PATH, 'w') as full_json_file:
        json.dump(full_dictionary, full_json_file)

    with open(VOWEL_DICTIONARY_PATH, 'w') as vowel_json_file:
        json.dump(vowel_dictionary, vowel_json_file)

    with open(N_SYLLABLES_DICTIONARY_PATH, 'w') as n_syllables_json_file:
        json.dump(n_syllables_dictionary, n_syllables_json_file)


def get_rhyme_words_from_dictionaries(input_word: str, rhyme_type: RhymeType) -> list[str]:
    logbasic.info('Finding rhyme words...')
    dictionary_file_path = FULL_DICTIONARY_PATH if rhyme_type == RhymeType.FULL else VOWEL_DICTIONARY_PATH

    if not os.path.exists(dictionary_file_path):
        logbasic.info('Phonetic dictionary file not found, creating it...')
        create_rhyme_dictionaries()

    dictionary = json.load(open(dictionary_file_path))

    input_word_rhyme_form = RHYME_FUNCTIONS[rhyme_type](Word(input_word))

    rhyme_words = []
    for entry in dictionary:
        if dictionary[entry] == input_word_rhyme_form:
            # haar becomes ha0r phonetically, so for vowel rhyme it will rhyme with varen
            # so we check that there are atleast as many syllables as vowels so haar doesn't rhyme with varen anymore
            if rhyme_type == RhymeType.FULL or len(Word(entry).syllables) >= len(Word(input_word).syllables):
                rhyme_words.append(entry)
    rhyme_words = [entry for entry in dictionary if dictionary[entry] == input_word_rhyme_form]

    return rhyme_words
