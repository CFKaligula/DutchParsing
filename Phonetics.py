def add_accent(vowel):
    switcher = {
        'a': 'á',  # la = laa
        'e': 'é',  # beter
        'i': 'í',  # never happens, only in simon i think
        'o': 'ó',  # boven
        'u': 'ú'   #
    }
    return switcher.get(vowel, 'Could not find a replacement')


def ending_vowel(vowel):
    switcher = {
        'a': 'á',  # la = laa
        'e': '0',  # blij-e
        'i': 'í',  #
        'o': 'ó',  # boven
        'u': 'ú'   #
    }
    return switcher.get(vowel, 'Could not find a replacement')


def default_phonetic_symbol(dipthong):
    switcher = {
        'aa': 'á',
        'ee': 'é',
        'ie': 'í',
        'oo': 'ó',
        'uu': 'ú',
        'au': 'ä',
        'ij': 'ë',
        'ei': 'ë',
        'oe': 'ö',

    }
    return switcher.get(dipthong, 'Could not find a replacement')


def r_or_l_phonetic_symbol(dipthong):
    switcher = {
        'aa': 'á0',
        'ee': 'i',
        'ie': 'í0',
        'oo': 'o0',
        'uu': 'ú0',
        'ij': 'ee',
        'ei': 'ee',

    }
    return switcher.get(dipthong, default_phonetic_symbol(dipthong))
