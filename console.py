from argparse import ArgumentParser
import os
import logging

from helper_code import logger
from word import Word
import test


_COMMAND_RHYME = 'rhyme'
_COMMAND_TEST = 'test'
_RHYME_DICTIONARY_PATH = os.path.join('text_files', 'basiswoorden.txt')


RHYME_FUNCTIONS = {
    'full': Word.get_rhyme_part,
    'vowel': Word.get_phonetic_vowels
}


def find_rhyme(input_word, rhyme_type):
    input_word = Word(input_word)
    logging.debug(
        f'Finding words that {rhyme_type} rhyme with: {RHYME_FUNCTIONS[rhyme_type](input_word)}')
    logging.info(f'Finding words that {rhyme_type} rhyme with "{input_word.text}"...')

    dictionary = open(_RHYME_DICTIONARY_PATH).read().split()
    rhyme_words = []
    for dictionary_entry in dictionary:
        word = Word(dictionary_entry)
        if RHYME_FUNCTIONS[rhyme_type](word) == RHYME_FUNCTIONS[rhyme_type](input_word):
            if rhyme_type == 'vowel' and len(word.syllables) < len(RHYME_FUNCTIONS[rhyme_type](word)):
                # haar becomes ha0r phonetically, so for vowel rhyme it will rhyme with varen
                # so we check that there are atleast as many syllables as vowels so haar doesn't rhyme with varen anymore
                continue

            rhyme_words.append(word)
    for rhyme_word in rhyme_words:
        print(rhyme_word.text)
