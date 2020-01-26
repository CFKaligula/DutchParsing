from argparse import ArgumentParser
from Word import Word

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_TEST = 'test'


def test_parser():
    if Word('dromen').get_split_word() == 'dro-men' and \
            Word('leerling').get_split_word() == 'leer-ling' and \
            Word('ambtenaar').get_split_word() == 'amb-te-naar' and \
            Word('koeien').get_split_word() == 'koei-en' and \
            Word('piano').get_split_word() == 'pi-a-no' and \
            Word('niveau').get_split_word() == 'ni-veau' and \
            Word('radio').get_split_word() == 'ra-di-o' and \
            Word('blije').get_split_word() == 'blij-e' and \
            Word('taxi').get_split_word() == 'tax-i' and \
            Word('lachen').get_split_word() == 'lach-en' and \
            Word('autootje').get_split_word() == 'au-too-tje' and \
            Word('herfstjuk').get_split_word() == 'herfst-juk' and \
            Word('beïnvloeden').get_split_word() == 'be-in-vloe-den' and \
            Word('blok-étagere').get_split_word() == 'blok-e-ta-ge-re' and \
            Word('blaséeend').get_split_word() == 'bla-se-eend' and \
            Word('baby').get_split_word() == 'ba-by' and \
            Word('ijsyoghurt').get_split_word() == 'ijs-yog-hurt' and \
            Word('sexy').get_split_word() == 'sex-y' and \
            Word('yoghurt').get_split_word() == 'yog-hurt' and \
            Word('quasi').get_split_word() == 'quasi' and \
            Word('hoofdstad').get_split_word() == 'hoofd-stad':
        print('*********All Tests Successful************')


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
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()

    elif args.command == _COMMAND_TEST:
        test_parser()
    elif args.command == _COMMAND_SPLIT:
        word = Word(args.input)
        word.display_syllable_list()
        print(word.get_split_word())
    elif args.command == _COMMAND_PRONOUNCE:
        word = Word(args.input)
        word.pronounce_word()
        print(word.get_split_word())

    return (args.command, args)


def main():
    (command, args) = _parse_arguments()


main()
