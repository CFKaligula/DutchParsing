import logging

import letter_dictionaries
from syllable import Syllable
from phonetic_code import phonetic

'''
TO BE IMPLEMENTED:
* Programming:
    * logger still isnt imported via __init__.py have to do it via console
* Split
    * ijs-yog-hurt but ba-by-opera, probably impossible. can do something for analyse where you see y has no vowels around it so it must be the vowel.
    * when y is seen as an end cosonant it should be a vowel for next syllable (really hard as we would have to have found a second vowel)

* Sound
    * sound files for consonants and some dipthongs
    * nieuw, duw, hoi, groei, leeuw (just ignore the w)
* Rhyme inventory
    * full rhyme only do stressed part?
    * vader now rhymes with 'vaal' because both have vowels a0 maybe special symbol for aa infront of l/r
* phonetic
    * ieuw, duw, eeuw
    * change trema to ^ so ä should be â á ä
    * ontdek = ondek ( maybe not?) (then also onbedoeld = ombedoeld), anker = angker, research all these combinations
    * jasje maybe jaße? not sure so implement ,ß for end_con s
    * different r's 
    * dommeriken = domm0riken so fix both e and i, same volkeren, kalveren shouldn't be volkiiren
    * maybe make previous_letter() and next_letter() functions so you don't have to do i>0 and end_cons[i-1] everytime
'''


class Word:
    def __init__(self, text):
        self._text = text.lower()
        self._length = len(text)
        self._syllables = self.initialize_syllables(0, [])
        self._pronunciation = ''
        self.initialize_pronunciation()

    @property
    def text(self):
        return self._text

    @property
    def length(self):
        return self._length

    @property
    def syllables(self):
        return self._syllables

    @property
    def pronunciation(self):
        return self._pronunciation

    def get_split_word(self):
        # returns the word split into syllables with dashes
        result = ''
        for syllable in self._syllables:
            result += syllable.text + letter_dictionaries.BREAK_SYMBOL
        result = result[:-1]    # we remove the last break symbol
        return result

    def initialize_syllables(self,  start, syllable_list):
        # Check if we are done recursing
        if start >= self.length:
            for i in range(0, len(syllable_list)-1):
                syllable_list[i]._next_syl = syllable_list[i+1]
            return syllable_list
        # Create a syllable
        if len(syllable_list) == 0:
            syl = Syllable(prev_syl=Syllable(''), word=self)
        else:
            syl = Syllable(prev_syl=syllable_list[-1], word=self)
        # Loop over the word to create the syllable
        for index in range(start, self._length+1):
            if index >= self._length:
                break
            logging.debug(f'index letter: {self.text[index]}, {index}')
            next_let = self.text[index+1] if index < self._length-1 else ''
            if self.text[index] == '-':
                index += 1
                break

            elif self.text[index] in letter_dictionaries.CONSONANTS:
                if self.text[index] == 'y' and index == self.length-1:
                    if len(syl.end_cons) > 0:
                        index = syl.fix_end_cons(index)
                        break
                    else:
                        syl.add_y()
                else:
                    syl.add_cons(self.text[index])
            elif self.text[index] in letter_dictionaries.VOWELS:
                if len(syl.end_cons) > 0:
                    index = syl.fix_end_cons(index)
                    break
                else:
                    break_bool = syl.add_vowel(self.text[index], next_let)
                    if break_bool:
                        break
            elif self.text[index] in letter_dictionaries.VOWELS_WITH_ACCENTS:
                if len(syl.vowels) == 0:
                    break_bool = syl.add_vowel(self.text[index], next_let)
                    if break_bool:
                        break
                else:
                    index = syl.fix_end_cons(index)
                    break
            else:
                logging.debug(f'"{self.text[index]}" is not a letter.')
                pass
        if syl.vowels in letter_dictionaries.VOWELS_WITH_ACCENTS:
            logging.debug(f' The syllable contains an accent, {syl.vowels}.')
            syl.remove_accents()

        syl.fix_start_cons()
        syllable_list.append(syl)
        return self.initialize_syllables(index, syllable_list)

    def initialize_pronunciation(self):
        for syllable in self.syllables:
            if syllable.start_cons:
                self._pronunciation += phonetic.find_start_con_pronunciation(syllable)
            if syllable.vowels:
                self._pronunciation += phonetic.find_vowel_pronunciation(syllable)
            if syllable.end_cons:
                self._pronunciation += phonetic.find_end_con_pronunciation(syllable)

    def pronounce_word(self):
        for syllable in self._syllables:
            syllable.pronounce_syllable()

    def get_phonetic_vowels(self):
        vowels = ''
        for letter in self._pronunciation:
            if letter not in letter_dictionaries.PHONETIC_SYSTEM_CONSONANTS:
                vowels += letter
        logging.debug(vowels)
        return vowels

    def get_rhyme_part(self):
        start_length = 0
        for letter in self._pronunciation:
            if letter in letter_dictionaries.PHONETIC_SYSTEM_CONSONANTS or letter == '0':
                # take the part after the first consonats and schwas, so gepakt will find words that also end on akt
                start_length += 1
            else:
                break
        return self._pronunciation[start_length:]
