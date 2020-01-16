import argparse

'''
TO BE IMPLEMENTED:
* correct parsing of j, blije should be blij-e where ij is a dipthong, vrijijs should be vrij-ijs, jijeter, jij-eter herfstjuk, 
* correct parsing of ch,th etc.  e.g. la-chen
* apparently if there is only 1 x word is not split up, so taxi is taxi, not ta-xi, you would have to check the last 
'''

consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'j',
              'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
# y should be included for names like jordy, don't know yet if j has to be included for dipthongs
vowels = {'a', 'e', 'i', 'o', 'u'}
dipthongs = {'au', 'ou', 'ei', 'ij', 'oe',
             'ui',  'aa', 'ee', 'ie', 'oo', 'uu', 'oi'}
tripthongs = {'oei', 'eau', 'eeu', 'ooi', 'aai', 'oeu'}
# can only be at the start of words, e.g. auto, never blau, aarde, never laa etc.
start_dipthongs = {'au', 'aa', 'ee', 'oo', 'uu', }
# can only be first group of vowels, e.g. bloei-en, niveau-ijs
end_tripthongs = {'oei', 'eau', 'eeu', 'ooi', 'aai'}
start_tripthongs = {'oeu'}  # can only be last group of vowels e.g. oeuvre
break_symbol = '·'
consonant_combinations = {'',
                          'b', 'bl', 'br',
                          'c', 'cl', 'cr',
                          'd', 'dr', 'dl', 'dr',
                          'f', 'fl', 'fj' 'fr',
                          'g', 'gr', 'gl', 'gr',
                          'h',
                          'k', 'kl', 'kn', 'kr',
                          'l',
                          'j',
                          'm',
                          'n',
                          'p', 'pl', 'pr',
                          'q',
                          'r',
                          's', 'sh', 'sk', 'sl', 'sj', 'sm', 'sn', 'sp', 'sr', 'st', 'sw', 'sch', 'schr', 'schl',
                          't', 'th', 'tr',
                          'v', 'vl', 'vr',
                          'w', 'wr',
                          'x',
                          'y',
                          'z'
                          }


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str,
                        help="input for the parser", nargs='+')
    args = parser.parse_args()
    print(args.input)
    processed_input = []
    for word in args.input:
        processed_input.append(split_word(word))
    print(processed_input)


def split_word(word):
    word = split_syllable_dictionary(word, len(word)-1)
    print(f'finished working: {word}')
    return word
    

def split_syllable_dictionary(word, start):
    start_cons_group = ''
    vowel_group = ''
    end_cons_group = ''
    rest_word = word[:start+1]
    finished_part = word[start+1:]
    found_vowel = False

    if start <= 0:
        return word
    for index in range(start, -1, -1):
        print(f'index letter: {word[index]}')
        if word[index] in consonants:
            if found_vowel:
                start_cons_group = word[index] + start_cons_group
                rest_word = remove_last_letter(rest_word)
            else:
                end_cons_group = word[index] + end_cons_group
                rest_word = remove_last_letter(rest_word)
        else:
            if len(start_cons_group) > 0:
                if len(start_cons_group) > 1:
                    rest_word += start_cons_group[0]
                    start_cons_group = start_cons_group[1:]
                    index += 1
                break
            else:
                vowel_group = word[index] + vowel_group
                rest_word = remove_last_letter(rest_word)
                found_vowel = True

    print(f'start cons: {start_cons_group}')
    start_cons_group, rest_word, index = check_start_cons(
        start_cons_group, rest_word, index)
    print(f'vowels: {vowel_group}')
    vowel_group = check_vowel_group(vowel_group)
    print(f'end cons: {end_cons_group}')
    print(f'rest: {rest_word}')
    syllable = start_cons_group + vowel_group + end_cons_group
    if len(rest_word) <= 1:
        word = rest_word + syllable + finished_part
    else:
        word = rest_word + '·' + syllable + finished_part
    return split_syllable_dictionary(word, index)


def check_start_cons(start_cons_group, rest_word, index):
    while start_cons_group not in consonant_combinations:
        rest_word += start_cons_group[0]
        start_cons_group = start_cons_group[1:]
        index += 1
        print(f"start cons {start_cons_group} is not a good group")
    return start_cons_group, rest_word, index


def check_vowel_group(vowel_group):
    vowel_group = check_tripthongs(vowel_group)
    if '·' not in vowel_group:
        vowel_group = check_dipthongs(vowel_group)
    return vowel_group


def check_tripthongs(vowel_group):
    i = 0
    while i+2 < len(vowel_group)-1:
        print(
            f'evaluating {vowel_group[i] + vowel_group[i+1] + vowel_group[i+2]}')
        if vowel_group[i] + vowel_group[i+1] + vowel_group[i+2] in tripthongs:
            if len(vowel_group)-1 > i+2:
                vowel_group = insert_break(vowel_group, i+3)
                i += 3
            i += 1
        else:
            vowel_group = insert_break(vowel_group, i+1)
            i += 2
    return vowel_group


def check_dipthongs(vowel_group):
    i = 0
    while i < len(vowel_group)-1:
        print('evaluating')
        print(vowel_group[i] + vowel_group[i+1])
        if vowel_group[i] + vowel_group[i+1] in dipthongs:
            if len(vowel_group)-1 > i+1:
                vowel_group = insert_break(vowel_group, i+2)
                i += 2
            i += 1
        else:
            vowel_group = insert_break(vowel_group, i+1)
            i += 2

    return vowel_group


def remove_last_letter(word):
    return word[:-1]


def insert_break(string, index):
    print(f"insterting break {string[:index] + '·' + string[index:]}")
    return string[:index] + '·' + string[index:]


def test_parser():
    if split_word("dromen") == "dro·men" and \
        split_word("leerling") == "leer·ling" and \
        split_word("ambtenaar") == "amb·te·naar" and \
        split_word("koeien") == "koei·en" and \
        split_word("piano") == "pi·a·no" and \
            split_word("hoofdstad") == "hoofd·stad":
        print("tests successful")
    else:
        print("test failed")


def main():
    get_input()
    # test_parser()


main()
