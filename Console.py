from argparse import ArgumentParser

from Word import Word

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_TEST = 'test'
_COMMAND_ANALYZE = 'analyze'
_COMMAND_ANALYZE_FILE = 'analyze-file'
_COMMAND_PHONETIC = 'phonetic'


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
            Word('quasi').get_split_word() == 'qua-si' and \
            Word('hoofdstad').get_split_word() == 'hoofd-stad':
        print('***.***.*** All Tests Successful ***.***.*** ')
    else:
        print('***Test failed ***')


def analyze(input_sentence):
    words = input_sentence.split('\n')
    analyze_dict = {}
    for input_word in words:
        word = Word(input_word)
        for syllable in word.syllables:
            if syllable.text not in analyze_dict:
                analyze_dict[syllable.text] = 1
            else:
                analyze_dict[syllable.text] += 1
    sorted_dict = {k: v for k, v in sorted(
        analyze_dict.items(), key=lambda item: item[1], reverse=True)}
    print(
        f'there were a total of {len(analyze_dict)} unique syllables in the text, of {len(words)} words.')
    top10 = {key: value for key, value in list(sorted_dict.items())[0:100]}
    print(f'the most common syllables were {top10}')


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
            word.display_syllable_list()
            print(word.get_split_word())
    elif args.command == _COMMAND_PRONOUNCE:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            word = Word(args.input)
            word.pronounce_word()
    elif args.command == _COMMAND_PHONETIC:
        input_words = args.input.split()
        for input_word in input_words:
            word = Word(input_word)
            print(word.pronunciation)
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
