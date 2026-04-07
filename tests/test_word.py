import pytest

from src.word import Word


@pytest.mark.parametrize(
    'word,expected',
    [
        ('ambtenaar', 'amb-te-naar'),
        ('autootje', 'au-too-tje'),
        ('beïnvloeden', 'be-in-vloe-den'),
        ('blok-étagere', 'blok-e-ta-ge-re'),
        ('blaséeend', 'bla-se-eend'),
        ('babby', 'bab-by'),
        ('baby', 'ba-by'),
        ('blije', 'blij-e'),
        ('chronische', 'chro-ni-sche'),
        ('dromen', 'dro-men'),
        ('hoofdstad', 'hoofd-stad'),
        ('ijsyoghurt', 'ijs-yog-hurt'),
        ('lachen', 'lach-en'),
        ('leerling', 'leer-ling'),
        ('lange', 'lang-e'),
        ('koeien', 'koei-en'),
        ('piano', 'pi-a-no'),
        ('niveau', 'ni-veau'),
        ('radio', 'ra-di-o'),
        ('taxi', 'tax-i'),
        ('herfstjuk', 'herfst-juk'),
        ('sexy', 'sex-y'),
        ('quasi', 'qua-si'),
        ('yoghurt', 'yog-hurt'),
    ],
)
def test_get_split_word(word, expected):
    assert Word(word).get_split_word() == expected


@pytest.mark.parametrize(
    'word,expected',
    [
        # a
        ('appel', 'apel'),
        # b
        ('baas', 'bás'),
        ('bijl', 'beel'),
        ('bezem', 'bézem'),
        ('bezet', 'b0zet'),
        ('blokken', 'blok0n'),
        # c
        ('citroen', 'sítrön'),
        ('chronische', 'grónís0'),
        ('chronisch', 'grónís'),
        ('ceder', 'séd0r'),
        ('casus', 'kásus'),
        # d
        ('denken', 'denk0n'),
        # e
        # f
        # g
        ('gaas', 'gás'),
        ('ga', 'gá'),
        ('gas', 'gas'),
        ('gade', 'gád0'),
        ('gaal', 'gá0l'),
        ('gag', 'gaæ'),
        # h
        ('herkennen', 'herken0n'),
        # i
        # j
        # k
        # l
        ('lijk', 'lïk'),
        ('lang', 'laµ'),
        # m
        ('motie', 'mótsí'),
        ('moties', 'mótsís'),
        # n
        # o
        ('oranje', 'oorañ0'),
        # p
        ('pen', 'pen'),
        ('perfectie', 'perfeksí'),
        ('praatje', 'práð0'),
        # q
        ('quincy', 'kwinsí'),
        ('quasi', 'kwásí'),
        # r
        # s
        ('sexy', 'seksí'),
        ('scepter', 'sept0r'),
        ('schaar', 'sgá0r'),
        ('scheren', 'sgiir0n'),
        ('sjaal', 'ßá0l'),
        # t
        ('taxi', 'taksí'),
        ('tieten', 'tít0n'),
        # u
        # v
        # w
        ('wordt', 'wort'),
        ('wondtas', 'wontas'),
        # x
        # y
        ('yoga', 'jógá'),
        # z
    ],
)
def test_pronunciation(word, expected):
    assert Word(word).pronunciation == expected
