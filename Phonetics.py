import Letters
from Syllable import Syllable
import StartPronunciations
import EndPronunciations

LETTER_FUNCTIONS = {
    'find_start_c_pronunciation': StartPronunciations.find_start_c_pronunciation,
    'find_start_h_pronunciation': StartPronunciations.find_start_h_pronunciation,
    'find_start_j_pronunciation': StartPronunciations.find_start_j_pronunciation,
    'find_start_s_pronunciation': StartPronunciations.find_start_s_pronunciation,
    'find_start_q_pronunciation': StartPronunciations.find_start_q_pronunciation,


    'find_end_g_pronunciation': EndPronunciations.find_end_g_pronunciation,
    'find_end_c_pronunciation': EndPronunciations.find_end_c_pronunciation,
    'find_end_h_pronunciation': EndPronunciations.find_end_h_pronunciation,
    'find_end_n_pronunciation': EndPronunciations.find_end_n_pronunciation
}


def find_start_con_pronunciation(syllable):
    start_con_sound = ''
    if syllable.start_cons == 'tj':
        # autootje
        start_con_sound = 'ð'
    else:
        for i in range(0, len(syllable.start_cons)):
            if i == 0 and syllable.start_cons[i] == syllable.prev_syl.end_cons[-1:]:
                # blokken = bloken
                continue
            if i > 0 and syllable.start_cons[i] == syllable.start_cons[i-1]:
                # pppas = pas
                continue
            function_name = f'find_start_{syllable.start_cons[i]}_pronunciation'
            if function_name in LETTER_FUNCTIONS:
                start_con_sound += LETTER_FUNCTIONS[function_name](syllable, i)
            else:
                start_con_sound += default_consonant_replacement(syllable.start_cons[i])
    return start_con_sound


def find_end_con_pronunciation(syllable):
    end_con_sound = ''
    if syllable.end_cons == 'sch':
        # logisch
        end_con_sound = 's'
    else:
        for i in range(0, len(syllable.end_cons)):
            if i > 0 and syllable.end_cons[i] == syllable.end_cons[i-1]:
                # bakk = bak
                continue
            function_name = f'find_end_{syllable.end_cons[i]}_pronunciation'
            if function_name in LETTER_FUNCTIONS:
                end_con_sound += LETTER_FUNCTIONS[function_name](syllable, i)
            else:
                end_con_sound += default_consonant_replacement(syllable.end_cons[i])
    return end_con_sound


def find_vowel_pronunciation(syllable):
    vowel_sound = ''
    if syllable.start_cons == 'q' and syllable.vowels != '' and syllable.vowels[0] == 'u':
        # qua = kwa
        syl_without_qu = Syllable(
            input_text=syllable.vowels[1:]+syllable.end_cons, prev_syl=syllable.prev_syl, next_syl=syllable.next_syl)
        return find_vowel_pronunciation(syl_without_qu)
    elif syllable.start_cons == 'c' and syllable.vowels == 'i':
        # citroen
        vowel_sound = add_accent(syllable.vowels)
    elif syllable.vowels in Letters.VOWELS:
        if not syllable.end_cons:
            if syllable.next_syl is not None and syllable.next_syl.start_cons != '' and syllable.next_syl.start_cons[0] in {'r', 'l'}:
                # if the next syllable starts with an r, some vowels are pronounced differently
                vowel_sound = next_syl_r_or_l(syllable.vowels)
            else:
                vowel_sound = find_open_vowel_pronunciation(syllable)
        elif (syllable.vowels + syllable.end_cons) in {'en', 'er'} and not syllable.next_syl:
            # lopen and loper
            return '0'
        elif syllable.end_cons == 'sch'and syllable.vowels == 'i':
            # logisch
            vowel_sound = add_accent(syllable.vowels)
        else:
            vowel_sound = syllable.vowels

    elif syllable.end_cons is not '' and syllable._end_cons[0] in {'r', 'l'}:
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


def add_accent(vowel):
    switcher = {
        'a': 'á',  # la = laa
        'e': 'é',  # beter
        'i': 'í',  # never happens, only in simon i think
        'o': 'ó',  # boven
        'u': 'ú'   #
    }
    return switcher.get(vowel, f'Could not find a replacement for {vowel}, add_accent()')


def ending_vowel(vowel):
    switcher = {
        'e': '0',  # blij-e
        'y': 'í'   # sexy
    }
    return switcher.get(vowel, add_accent(vowel))


def default_phonetic_symbol(dipthong):
    15
    switcher = {
        'aa': 'á',
        'ee': 'é',
        'ie': 'í',
        'oo': 'ó',
        'uu': 'ú',
        'au': 'ä',
        'ou': 'ä',
        'ij': 'ï',
        'ei': 'ï',
        'eu': 'ë',
        'oe': 'ö',
        'ui': 'ü',
        'ai': 'A',
        'oi': 'O',
        'aai': 'Á',
        'ooi': 'Ó',
        'oei': 'Ö',
        'oeu': 'uu',
        'y': 'í'   # sexy

    }
    return switcher.get(dipthong, f'Could not find a replacement for {dipthong}, default_phonetic_symbol()')


def r_or_l_phonetic_symbol(dipthong):
    switcher = {
        'aa': 'á0',
        'ee': 'ii',
        'ie': 'í0',
        'oo': 'o0',
        'uu': 'ú0',
        'ij': 'ee',
        'ei': 'ee',
        'oe': 'ö0',
        'ui': 'ü0'

    }
    return switcher.get(dipthong, default_phonetic_symbol(dipthong))


def next_syl_r_or_l(vowel):
    switcher = {
        'o': 'oo',  # voren
        'i': 'íí',  # gieren hypothetically
        'e': 'ii'  # scheren
    }
    return switcher.get(vowel, add_accent(vowel))


def default_consonant_replacement(consonants):
    switcher = {
        'y': 'j',
        'x': 'ks',
    }
    return switcher.get(consonants, consonants)
