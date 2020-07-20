from argparse import ArgumentParser
import os
import logging
import json

from helper_code import logger
from word import Word
import test

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_TEST = 'test'
_COMMAND_ANALYZE = 'analyze'
_COMMAND_ANALYZE_FILE = 'analyze-file'
_COMMAND_PHONETIC = 'phonetic'
_COMMAND_RHYME = 'rhyme'
_RHYME_DICTIONARY_PATH_1 = os.path.join('text_files', 'basiswoorden.txt')
_RHYME_DICTIONARY_PATH_2 = os.path.join('text_files', 'Dutch_Word_List.txt')
_RHYME_DICTIONARY_PATH_3 = os.path.join('text_files', 'DutchDictionary.txt')


def test_parser():
    test.phonetic_tester()
    test.split_tester()


def analyze(input_sentence):
    words = input_sentence.split()
    analyze_dict = {}
    letter_analyze_dict = {}
    syllable_count = 0
    letter_count = 0
    for input_word in words:
        word = Word(input_word)
        for letter in word.text:
            letter_count += 1
            if letter not in letter_analyze_dict:
                letter_analyze_dict[letter] = 1
            else:
                letter_analyze_dict[letter] += 1
        for syllable in word.syllables:
            syllable_count += 1
            if syllable.text not in analyze_dict:
                analyze_dict[syllable.text] = 1
            else:
                analyze_dict[syllable.text] += 1
    sorted_dict = {k: v for k, v in sorted(
        analyze_dict.items(), key=lambda item: item[1], reverse=True)}
    letter_sorted_dict = {k: v for k, v in sorted(
        letter_analyze_dict.items(), key=lambda item: item[1], reverse=True)}
    logging.info(
        f'there were a total of {len(analyze_dict)} unique syllables in the text, of {len(words)} words and {syllable_count} total syllables.')
    logging.info(f'there were a total of {letter_count} letters.')
    top10 = {key: value for key, value in list(sorted_dict.items())[0:10]}
    logging.info(f'the {len(top10)} most common syllable(s) was/were {top10}')
    top10letter_dictionaries = {key: value for key, value in list(letter_sorted_dict.items())[0:10]}
    logging.info(
        f'the {len(top10letter_dictionaries)} most common letter(s) was/were {top10letter_dictionaries}')


RHYME_FUNCTIONS = {
    'full': Word.get_rhyme_part,
    'vowel': Word.get_phonetic_vowels
}


def create_phonetic_dictionary_file():
    full_json_file = open('full_dictionary.json', 'w')
    vowel_json_file = open('vowel_dictionary.json', 'w')

    full_dictionary = {}
    vowel_dictionary = {}
    logging.info('Reading dictionaries...')
    for i in range(1, 4):
        dictionary = open(eval(f'_RHYME_DICTIONARY_PATH_{i}'), encoding='utf8').read().split()

        for entry in dictionary:
            if entry not in full_dictionary:
                word = Word(entry)
                rhyme_part = RHYME_FUNCTIONS['full'](word)
                full_dictionary[word.text] = rhyme_part

                phonetic_vowels = RHYME_FUNCTIONS['vowel'](word)
                vowel_dictionary[word.text] = phonetic_vowels

    json.dump(full_dictionary, full_json_file)
    json.dump(vowel_dictionary, vowel_json_file)


def find_rhyme_from_json_file(input_word, rhyme_type):
    logging.info('Finding rhyme words...')
    dictionary = json.load(open('full_dictionary.json')) if rhyme_type == 'full' else json.load(open(
        'vowel_dictionary.json'))
    input_word_rhyme_form = RHYME_FUNCTIONS[rhyme_type](Word(input_word))
    rhyme_words = [entry for entry in dictionary if dictionary[entry] == input_word_rhyme_form]

    logging.info(f'Words that {rhyme_type} rhyme with "{input_word}"')
    for word in rhyme_words:
        print(word, end=',')
    print('')


def find_rhyme(input_word, rhyme_type):
    create_phonetic_dictionary_file()

    find_rhyme_from_json_file(input_word, rhyme_type)

    input_word = Word(input_word)
    logging.debug(
        f'Finding words that {rhyme_type} rhyme with: {RHYME_FUNCTIONS[rhyme_type](input_word)}')
    logging.info(f'Finding words that {rhyme_type} rhyme with "{input_word.text}"...')

    dictionary = open(_RHYME_DICTIONARY_PATH_1).read().split()
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
        print(rhyme_word.text, end=',')
    print('')


def _add_parser_category_split(subparsers):
    parser = subparsers.add_parser(_COMMAND_SPLIT, help='splits the input word in syllables.')
    parser.set_defaults(command=_COMMAND_SPLIT)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


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


def _add_parser_category_pronounce(subparsers):
    parser = subparsers.add_parser(_COMMAND_PRONOUNCE, help='pronounces the input word.')
    parser.set_defaults(command=_COMMAND_PRONOUNCE)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


def _add_parser_category_analyze(subparsers):
    parser = subparsers.add_parser(_COMMAND_ANALYZE, help='analyzes the input word.')
    parser.set_defaults(command=_COMMAND_ANALYZE)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


def _add_parser_category_analyze_file(subparsers):
    parser = subparsers.add_parser(_COMMAND_ANALYZE_FILE, help='analyzes the input file.')
    parser.set_defaults(command=_COMMAND_ANALYZE_FILE)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


def _add_parser_category_phonetic(subparsers):
    parser = subparsers.add_parser(
        _COMMAND_PHONETIC, help='gives the phonetic version of the input word.')
    parser.set_defaults(command=_COMMAND_PHONETIC)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


def _add_parser_category_test(subparsers):
    parser = subparsers.add_parser(_COMMAND_TEST, help='runs all the tests on the parser.')
    parser.set_defaults(command=_COMMAND_TEST)


def _parse_arguments():
    parser = ArgumentParser(description='Console interface for the parser.')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(help='Category')
    _add_parser_category_split(subparsers)
    _add_parser_category_pronounce(subparsers)
    _add_parser_category_test(subparsers)
    _add_parser_category_analyze_file(subparsers)
    _add_parser_category_analyze(subparsers)
    _add_parser_category_phonetic(subparsers)
    _add_parser_category_rhyme(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    elif args.command == _COMMAND_TEST:
        test_parser()

    elif args.command == _COMMAND_SPLIT:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            print(word.get_split_word(), end=" ")

    elif args.command == _COMMAND_PRONOUNCE:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            word.pronounce_word()

    elif args.command == _COMMAND_PHONETIC:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            print(word.pronunciation, end=" ")

    elif args.command == _COMMAND_ANALYZE:
        analyze(args.input)

    elif args.command == _COMMAND_ANALYZE_FILE:
        try:
            f = open(args.input, "r",  encoding='utf8')
        except:
            f = open(args.input, "r")
        analyze(f.read())

    elif args.command == _COMMAND_RHYME:
        find_rhyme(args.input, args.type)

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
