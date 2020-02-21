import letter_dictionaries
from syllable import Syllable
import phonetic
'''
TO BE IMPLEMENTED:
* Split
    * ijs-yog-hurt but ba-by-opera, probably impossible. can do something for analyse where you see y has no vowels around it so it must be the vowel.
* Sound
    * sound files for consonants and some dipthongs
    * nieuw, duw, hoi, groei, leeuw (just ignore the w)
* Rhyme inventory
    * full rhyme and only vowel rhyme 
* phonetic
    * ieuw, duw, eeuw
    * change trema to ^ so ä should be â á ä
    * ontdek = ondek ( maybe not?)
    * motie = mótsí also when not last syllable
    * jasje maybe jaße? not sure so implement ,ß for end_con s
    * different r's 
    * d,b,z,v at the end should be t,p,s,f
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
            #print(f'index letter: {self.text[index]}, {index}')
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
                # print(f'"{self.text[index]}" is not a letter.')
                pass
        if syl.vowels in letter_dictionaries.VOWELS_WITH_ACCENTS:
            #print(f' The syllable contains an accent, {syl.vowels}.')
            syl.remove_accents()
        # syl.display_cons_and_vowels()
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
