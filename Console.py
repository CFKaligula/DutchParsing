import argparse
from Word import Word


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str,
                        help='input for the parser', nargs='+')
    args = parser.parse_args()
    print(args.input)
    processed_input = []
    if args.input == ['test']:
        test_parser()
    else:
        for word in args.input:
            hallo = Word(word)
            hallo.display_syllable_list()
            print(hallo.get_split_word())


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
            Word('hoofdstad').get_split_word() == 'hoofd-stad':
        print('*********All Tests Successful************')


def main():
    get_input()


main()
