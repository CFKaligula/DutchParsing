import os

from word import Word
import json

_COMMAND_RHYME = 'rhyme'
_COMMAND_TEST = 'test'
_RHYME_DICTIONARY_PATH_1 = os.path.join('text_files', 'basiswoorden.txt')
_RHYME_DICTIONARY_PATH_2 = os.path.join('text_files', 'Dutch_Word_list.txt')
_RHYME_DICTIONARY_PATH_3 = os.path.join('text_files', 'DutchDictionary.txt')

RHYME_FUNCTIONS = {
    'full': Word.get_rhyme_part,
    'vowel': Word.get_phonetic_vowels
}


def create_phonetic_dictionary_file():
    full_json_file = open('full_dictionary.json', 'w')
    vowel_json_file = open('vowel_dictionary.json', 'w')

    full_dictionary = {}
    vowel_dictionary = {}
    print('Reading dictionaries...')
    for i in range(1, 4):
        dictionary = open(eval(f'_RHYME_DICTIONARY_PATH_{i}'), encoding='utf8').read().split()

        for entry in dictionary:
            if entry not in full_dictionary:
                word = Word(entry)
                rhyme_part = RHYME_FUNCTIONS['full'](word)
                full_dictionary[word.text] = rhyme_part

                phonetic_vowels = RHYME_FUNCTIONS['vowel'](word)
                vowel_dictionary[word.text] = phonetic_vowels

    json.dump(full_dictionary, full_json_file)
    json.dump(vowel_dictionary, vowel_json_file)


def find_rhyme_from_json_file(input_word, rhyme_type):

    dictionary = json.load(open('full_dictionary.json')) if rhyme_type == 'full' else json.load(open(
        'vowel_dictionary.json'))
    input_word_rhyme_form = RHYME_FUNCTIONS[rhyme_type](Word(input_word))
    rhyme_words = [entry for entry in dictionary if dictionary[entry] == input_word_rhyme_form]

    for word in rhyme_words:
        print(word, end=',')
    print('')
    return rhyme_words


create_phonetic_dictionary_file()
find_rhyme_from_json_file('berkterrein', 'full')
