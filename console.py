from argparse import ArgumentParser

from src.word import Word

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_PHONETIC = 'phonetic'
_COMMAND_RHYME = 'rhyme'


def _add_parser_category_split(subparsers):
    parser = subparsers.add_parser(_COMMAND_SPLIT, help='splits the input word in syllables.')
    parser.set_defaults(command=_COMMAND_SPLIT)

    parser.add_argument('input', type=str, help='input for the parser')


def _add_parser_category_pronounce(subparsers):
    parser = subparsers.add_parser(_COMMAND_PRONOUNCE, help='pronounces the input word.')
    parser.set_defaults(command=_COMMAND_PRONOUNCE)

    parser.add_argument('input', type=str, help='input for the parser')


def _add_parser_category_phonetic(subparsers):
    parser = subparsers.add_parser(_COMMAND_PHONETIC, help='gives the phonetic version of the input word.')
    parser.set_defaults(command=_COMMAND_PHONETIC)

    parser.add_argument('input', type=str, help='input for the parser')


def _parse_arguments():
    parser = ArgumentParser(description='Console interface for the parser.')
    parser.set_defaults(command=None)

    subparsers = parser.add_subparsers(help='Category')
    _add_parser_category_split(subparsers)
    _add_parser_category_pronounce(subparsers)
    _add_parser_category_phonetic(subparsers)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()

    elif args.command == _COMMAND_SPLIT:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            print(word.get_split_word(), end=' ')

    elif args.command == _COMMAND_PRONOUNCE:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            word.pronounce_word()

    elif args.command == _COMMAND_PHONETIC:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            print(word.pronunciation, end=' ')

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
