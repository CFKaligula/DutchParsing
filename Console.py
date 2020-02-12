from argparse import ArgumentParser

from Word import Word

_COMMAND_SPLIT = 'split'
_COMMAND_PRONOUNCE = 'pronounce'
_COMMAND_TEST = 'test'
_COMMAND_ANALYZE = 'analyze'
_COMMAND_ANALYZE_FILE = 'analyze-file'
_COMMAND_PHONETIC = 'phonetic'


def test_parser():
    phonetic_tester()
    split_tester()


def split_tester():
    test_dict = {
        'dromen':  'dro-men',
        'leerling':  'leer-ling',
        'ambtenaar':  'amb-te-naar',
        'koeien':  'koei-en',
        'piano':  'pi-a-no',
        'niveau':  'ni-veau',
        'radio':  'ra-di-o',
        'blije': 'blij-e',
        'taxi': 'tax-i',
        'lachen': 'lach-en',
        'autootje': 'au-too-tje',
        'herfstjuk': 'herfst-juk',
        'beïnvloeden': 'be-in-vloe-den',
        'blok-étagere': 'blok-e-ta-ge-re',
        'blaséeend':  'bla-se-eend',
        'baby': 'ba-by',
        'ijsyoghurt': 'ijs-yog-hurt',
        'sexy': 'sex-y',
        'babby': 'bab-by',
        'yoghurt': 'yog-hurt',
        'quasi': 'qua-si',
        'chronische': 'chro-ni-sche',
        'lange': 'lang-e',
        'hoofdstad': 'hoofd-stad'
    }
    for test in test_dict:
        print(test, end=",") if Word(test).get_split_word(
        ) == test_dict[test] else print(f'\nFAILED {test}')
    print('\n***.***.***Done with split tests***.***.***')


def phonetic_tester():
    test_dict = {
        'ga': 'gá',
        'gas': 'gas',
        'gade': 'gád0',
        'sexy': 'seksí',
        'gaas': 'gás',
        'gaal': 'gá0l',
        'baas': 'bás',
        'lijk': 'lïk',
        'bijl': 'beel',
        'lang': 'lañ',
        'chronische': 'grónís0',
        'chronisch': 'grónís',
        'scepter': 'sept0r',
        'ceder': 'séd0r',
        'casus': 'kásus',
        'herkennen': 'herkenn0n',
        'denken': 'denk0n',
        'bezem': 'bézem',
        'bezet': 'b0zet',
        'gag': 'gaæ',
        'taxi': 'taksí',
        'yoga': 'jógá',
        'schaar': 'sgá0r',
        'scheren': 'sgiir0n',
    }
    for test in test_dict:
        print(test, end=",") if Word(
            test).pronunciation == test_dict[test] else print(f'\nFAILED {test}, GOT {Word(test).pronunciation} INSTEAD')
    print('\n***.***.***Done with phonetic tests***.***.***')


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
