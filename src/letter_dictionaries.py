CONSONANTS = {'b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'j', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
# y should be included for names like jordy, don't know yet if j has to be included for DIPTHONGS
VOWELS = {'a', 'e', 'i', 'o', 'u'}
VOWELS_WITH_ACCENTS = {'á', 'ä', 'é', 'ë', 'í', 'ï', 'ó', 'ö', 'ú', 'ü'}
DIPTHONGS = {'au', 'ou', 'ei', 'ij', 'oe', 'ui', 'aa', 'ee', 'ie', 'oo', 'uu', 'oi', 'eu'}
TRIPTHONGS = {'oei', 'eau', 'eeu', 'ooi', 'aai', 'oeu', 'ieu'}

VALID_CONSONANT_COMBINATIONS = {
    '',
    'bl',
    'br',
    'cl',
    'cr',
    'dr',
    'dl',
    'dr',
    'fl',
    'fjfr',
    'gr',
    'gl',
    'gr',
    # h
    'kl',
    'kn',
    'kr',
    # l
    # j
    # m
    # n
    'pl',
    'pr',
    # q
    # r
    'sk',
    'sl',
    'sj',
    'sm',
    'sn',
    'sp',
    'sr',
    'st',
    'sw',
    'sch',
    'schr',
    'schl',
    'str',
    'spr',
    'spl',
    'scr',  # sh
    'th',
    'tr',
    'vl',
    'vr',
    'wr',
    # x
    # y
    'zw',
}


PHONETIC_SYSTEM_CONSONANTS = {
    'b',
    'c',
    'd',
    'f',
    'g',
    'h',
    'j',
    'k',
    'l',
    'm',
    'n',
    'p',
    'q',
    'r',
    's',
    't',
    'v',
    'w',
    'x',
    'y',
    'z',
    '®',
    'µ',
    'ß',
    'æ',
    'ð',
    'ñ',
    'þ',
}

PHONETIC_SYSTEM_VOWELS = {
    'a',
    'i',
    'e',
    'o',
    'u',
    'á',
    'í',
    'é',
    'ó',
    'ú',
    'ä',
    'ï',
    'ë',
    'ö',
    'ü',
    'ê',
    'î',
    'A',
    'Á',
    'O',
    'Ö',
    'Ó',
}

PREPOSITION_EXCEPTIONS = {'beter', 'geven', 'ver', 'beven', 'bezem', 'gele'}
