from argparse import ArgumentParser

from src.rhyme import RhymeType, get_rhyme_words_from_dictionaries
from src.word import Word

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_RHYME = 'rhyme'


def get_split(input_word: str) -> None:
    """splits the input word in syllables and prints them"""
    word = Word(input_word)
    print(word.get_split_word())


def get_pronunciation(input_word: str) -> None:
    """gives the phonetic version of the input word"""
    word = Word(input_word)
    print(word.pronunciation)


def find_rhyme(input_word: str, rhyme_type: RhymeType) -> None:
    """finds the rhyme words for the input word and prints them"""

    rhyme_words = get_rhyme_words_from_dictionaries(input_word, rhyme_type)
    print(f'Found rhyme words: {"\n\t- ".join(rhyme_words)}')


def _add_parser_category_split(subparsers):
    parser = subparsers.add_parser(_COMMAND_SPLIT, help='splits the input word in syllables.')
    parser.set_defaults(command=_COMMAND_SPLIT)

    parser.add_argument('input', type=str, help='input for the parser')


def _add_parser_category_pronounce(subparsers):
    parser = subparsers.add_parser(_COMMAND_PRONOUNCE, help='pronounces the input word.')
    parser.set_defaults(command=_COMMAND_PRONOUNCE)

    parser.add_argument('input', type=str, help='input for the parser')


def _add_parser_category_rhyme(subparsers):
    parser = subparsers.add_parser(_COMMAND_RHYME, help='finds rhyme words for the input word.')
    parser.set_defaults(command=_COMMAND_RHYME)

    parser.add_argument('input', type=str, help='input for the parser')

    parser.add_argument('-t', '--type', type=str, default='full', choices=['full', 'vowel'])


def _parse_arguments():
    parser = ArgumentParser(description='Console interface for the parser.')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(help='Category')
    _add_parser_category_split(subparsers)
    _add_parser_category_pronounce(subparsers)
    _add_parser_category_rhyme(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    elif args.command == _COMMAND_SPLIT:
        input_words = args.input.split()
        for input_word in input_words:
            get_split(input_word)

    elif args.command == _COMMAND_PRONOUNCE:
        input_words = args.input.split()
        for input_word in input_words:
            get_pronunciation(input_word)

    elif args.command == _COMMAND_RHYME:
        input_words = args.input.split()
        for input_word in input_words:
            find_rhyme(input_word, RhymeType(args.type))

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
