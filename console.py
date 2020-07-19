from argparse import ArgumentParser
import os
import logging

from helper_code import logger
from word import Word
import test


_COMMAND_RHYME = 'rhyme'
_COMMAND_TEST = 'test'
_RHYME_DICTIONARY_PATH = os.path.join('text_files', 'basiswoorden.txt')


def test_parser():
    test.phonetic_tester()
    test.split_tester()


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


def _add_parser_category_rhyme(subparsers):
    parser = subparsers.add_parser(_COMMAND_RHYME, help='finds rhyme words for the input word.')
    parser.set_defaults(command=_COMMAND_RHYME)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')

    parser.add_argument(
        '-t',
        '--type',
        type=str,
        default='full',
        choices=RHYME_FUNCTIONS.keys()
    )


def _add_parser_category_test(subparsers):
    parser = subparsers.add_parser(_COMMAND_TEST, help='runs all the tests on the parser.')
    parser.set_defaults(command=_COMMAND_TEST)


def _parse_arguments():
    parser = ArgumentParser(description='Console interface for the parser.')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(help='Category')
    _add_parser_category_test(subparsers)
    _add_parser_category_rhyme(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    elif args.command == _COMMAND_TEST:
        test_parser()

    elif args.command == _COMMAND_RHYME:
        find_rhyme(args.input, args.type)

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
