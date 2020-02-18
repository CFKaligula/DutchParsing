
from Word import Word
import sys


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
        'hoofdstad': 'hoofd-stad',

    }
    for test in test_dict:
        print(test, end=",") if Word(test).get_split_word(
        ) == test_dict[test] else print(f'\nFAILED {test}, GOT "{Word(test).pronunciation}" INSTEAD OF "{test_dict[test]}"')

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
        'herkennen': 'herken0n',
        'denken': 'denk0n',
        'bezem': 'bézem',
        'bezet': 'b0zet',
        'gag': 'gaæ',
        'taxi': 'taksí',
        'yoga': 'jógá',
        'schaar': 'sgá0r',
        'scheren': 'sgiir0n',
        'praatje': 'práð0',
        'quinty': 'kwintí',
        'quasi': 'kwásí',
        'citroen': 'sítrön',
        'appel': 'apel',
        'blokken': 'blok0n'
    }
    for test in test_dict:
        print(test, end=",") if Word(
            test).pronunciation == test_dict[test] else print(f'\nFAILED {test}, GOT "{Word(test).pronunciation}" INSTEAD OF "{test_dict[test]}".')

    print('\n***.***.***Done with phonetic tests***.***.***')