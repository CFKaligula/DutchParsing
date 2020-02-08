import Letters


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


def find_start_con_pronunciation(syllable):
    start_con_sound = ''

    for i in range(0, len(syllable.start_cons)):
        if syllable.start_cons[i] == 'c':
            if i < len(syllable.start_cons)-1 and syllable.start_cons[i+1] == 'h':
                start_con_sound += 'g'
            elif i < len(syllable.start_cons)-1 or syllable.vowels[0] in {'a', 'o', 'u'} or syllable.start_cons + syllable.vowels[0] == 'sce':
                start_con_sound += 'k'
            else:
                start_con_sound += 's'

        elif syllable.start_cons[i] == 'y':
            start_con_sound += 'j'
        elif syllable.start_cons[i] == 'h' and syllable.start_cons[i-1] is not None and syllable.start_cons[i-1] == 'c':
            continue
        else:
            start_con_sound += syllable.start_cons[i]
    return start_con_sound


def find_vowel_pronunciation(syllable):
    vowel_sound = ''
    if syllable.vowels in Letters.VOWELS:
        if not syllable.end_cons:
            vowel_sound = find_open_vowel_pronunciation(syllable)
        elif (syllable.vowels + syllable.end_cons) in {'en', 'er'} and not syllable.next_syl:
            return '0'
        else:
            vowel_sound = syllable.vowels

    elif syllable._end_cons and syllable._end_cons[0] in {'r', 'l'}:
        # if the end cons start with an r or an l, some dipthongs are pronounced differently
        vowel_sound = r_or_l_phonetic_symbol(syllable.vowels)
    else:
        vowel_sound = default_phonetic_symbol(syllable.vowels)
    # print(f'Vowel sound for vowel {syllable.vowels}: {vowel_sound}')
    return vowel_sound


def find_open_vowel_pronunciation(syllable):
    if syllable.text in {'ge', 'be', } and syllable.word.text not in Letters.PREPOSITION_EXCEPTIONS:
        return '0'
    elif syllable.next_syl:
        return add_accent(syllable.vowels)
    else:
        return ending_vowel(syllable.vowels)


def find_end_con_pronunciation(syllable):
    end_con_sound = ''
    if syllable.end_cons == 'sch':
        end_con_sound = 's'
    else:
        for i in range(0, len(syllable.end_cons)):
            if syllable.end_cons[i] == 'n' and syllable.end_cons[i+1] == 'g':
                end_con_sound += 'ñ'
            elif syllable.end_cons[i-1] is not None and syllable.end_cons[i-1] == 'n' and syllable.end_cons[i] == 'g':
                print('skipping for ng')
                continue
            elif syllable.end_cons[i] == 'y':
                end_con_sound += 'j'
            else:
                end_con_sound += syllable.end_cons[i]
    return end_con_sound
