from argparse import ArgumentParser

from word import Word
import test

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_TEST = 'test'
_COMMAND_ANALYZE = 'analyze'
_COMMAND_ANALYZE_FILE = 'analyze-file'
_COMMAND_PHONETIC = 'phonetic'


def test_parser():
    Test.phonetic_tester()
    Test.split_tester()


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
    print(
        f'there were a total of {len(analyze_dict)} unique syllables in the text, of {len(words)} words and {syllable_count} total syllables.')
    print(f'there were a total of {letter_count} letters.')
    top10 = {key: value for key, value in list(sorted_dict.items())[0:10]}
    print(f'the 10 most common syllables were {top10}')
    top10letters = {key: value for key, value in list(letter_sorted_dict.items())[0:10]}
    print(f'the 10 most common letters were {top10letters}')


def _add_parser_category_split(subparsers):
    parser = subparsers.add_parser(_COMMAND_SPLIT, help='splits the input word in syllables.')
    parser.set_defaults(command=_COMMAND_SPLIT)

    parser.add_argument(
        'input',
        type=str,
        help='input for the parser')


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

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
