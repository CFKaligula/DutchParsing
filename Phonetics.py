import Letters
from Syllable import Syllable


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


def find_start_con_pronunciation(syllable):
    start_con_sound = ''
    if syllable.start_cons == 'tj':
        start_con_sound = 'ð'
    else:
        for i in range(0, len(syllable.start_cons)):
            if syllable.start_cons[i] == 'c':
                if i > 0 and syllable.start_cons[i-1] == 's':
                    continue
                elif i < len(syllable.start_cons)-1 and syllable.start_cons[i+1] == 'h':
                    start_con_sound += 'g'
                elif i < len(syllable.start_cons)-1 or syllable.vowels[0] in {'a', 'o', 'u'} or syllable.start_cons + syllable.vowels[0] == 'sce':
                    start_con_sound += 'k'
                else:
                    start_con_sound += 's'

            elif syllable.start_cons[i] == 's' \
                    and i < len(syllable.start_cons)-1 and syllable.start_cons[i+1] == 'c' \
                    and i < len(syllable.start_cons)-2 and syllable.start_cons[i+2] == 'h':
                if syllable.vowels + syllable.end_cons == 'e' and syllable.next_syl is None:
                    start_con_sound += 's'
                else:
                    start_con_sound += 'sg'
            elif syllable.start_cons[i] == 'c' and i > 0 and syllable.start_cons[i-1] == 's':
                continue
            elif syllable.start_cons[i] == 'q' and syllable.vowels != '' and syllable.vowels[0] == 'u':
                start_con_sound += 'kw'
            elif syllable.start_cons[i] == 'y':
                start_con_sound += 'j'
            elif syllable.start_cons[i] == 'x':
                start_con_sound += 'ks'
            elif syllable.start_cons[i] == 'h' and i > 0 and syllable.start_cons[i-1] == 'c':
                continue
            else:
                start_con_sound += syllable.start_cons[i]
    return start_con_sound


def find_vowel_pronunciation(syllable):
    vowel_sound = ''
    if syllable.start_cons == 'q' and syllable.vowels != '' and syllable.vowels[0] == 'u':
        syl_without_qu = Syllable(
            input_text=syllable.vowels[1:]+syllable.end_cons, prev_syl=syllable.prev_syl, next_syl=syllable.next_syl)
        return find_vowel_pronunciation(syl_without_qu)
    elif syllable.vowels in Letters.VOWELS:
        if not syllable.end_cons:
            if syllable.next_syl is not None and syllable.next_syl.start_cons != '' and syllable.next_syl.start_cons[0] in {'r', 'l'}:
                # if the next syllable starts with an r, some vowels are pronounced differently
                vowel_sound = next_syl_r_or_l(syllable.vowels)
            else:
                vowel_sound = find_open_vowel_pronunciation(syllable)
        elif (syllable.vowels + syllable.end_cons) in {'en', 'er'} and not syllable.next_syl:
            return '0'
        elif syllable.end_cons == 'sch'and syllable.vowels == 'i':
            vowel_sound += add_accent(syllable.vowels)
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


def find_end_con_pronunciation(syllable):
    end_con_sound = ''
    if syllable.end_cons == 'sch':
        end_con_sound = 's'
    else:
        for i in range(0, len(syllable.end_cons)):
            if syllable.end_cons[i] == 'n' and i+1 <= len(syllable.end_cons)-1 and syllable.end_cons[i+1] == 'g':
                end_con_sound += 'ñ'
            elif syllable.end_cons[i] == 's' and i < len(syllable.end_cons)-1 and syllable.end_cons[i+1] == 'c' and i < len(syllable.end_cons)+1 and syllable.end_cons[i+2] == 'h':
                end_con_sound += 's'
            elif syllable.end_cons[i] == 'c' and i > 0 and syllable.end_cons[i-1] == 's':
                continue
            elif i > 0 and syllable.end_cons[i-1] == 'n' and syllable.end_cons[i] == 'g':
                continue
            elif syllable.end_cons[i] == 'y':
                end_con_sound += 'j'
            elif syllable.end_cons[i] == 'x':
                end_con_sound += 'ks'
            elif syllable.end_cons[i] == 'g':
                end_con_sound += 'æ'
            else:
                end_con_sound += syllable.end_cons[i]
    return end_con_sound
