import letters
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
    * find start pron and the find_end_pron do not copy paste, make generic func
    * change trema to ^ so ä should be â á ä
    * ontdek = ondek ( maybe not?)
    * blokken = bloken 
    * motie = mótsí? but still 'tieten' you can atleast check motie/moties so when its the last syllable
'''


class Word:
    def __init__(self, text):
        self._text = text.lower()
        self._length = len(text)
        self._syllables = self.initialize_syllables(0, [Syllable('')])
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

    def display_syllable_list(self):
        # prints a list with the syllables
        syllable_list = [syl.text for syl in self._syllables]
        print(syllable_list)

    def get_split_word(self):
        # returns the word split into syllables with dashes
        result = ''
        for syllable in self._syllables:
            result += syllable.text + letters.BREAK_SYMBOL
        result = result[:-1]    # we remove the last break symbol
        return result

    def initialize_syllables(self,  start, syllable_list):
        syl = Syllable(prev_syl=syllable_list[-1], word=self)

        if start >= self.length:
            for i in range(0, len(syllable_list)-1):
                syllable_list[i]._next_syl = syllable_list[i+1]
            return syllable_list[1:]
        for index in range(start, self._length+1):
            if index >= self._length:
                break
            #print(f'index letter: {self.text[index]}, {index}')
            next_let = self.text[index+1] if index < self._length-1 else ''
            if self.text[index] == '-':
                index += 1
                break

            elif self.text[index] in letters.CONSONANTS:
                if self.text[index] == 'y' and index == self.length-1:
                    if len(syl.end_cons) > 0:
                        index = syl.fix_end_cons(index)
                        break
                    else:
                        syl.add_y()
                else:
                    syl.add_cons(self.text[index])
            elif self.text[index] in letters.VOWELS:
                if len(syl.end_cons) > 0:
                    index = syl.fix_end_cons(index)
                    break
                else:
                    break_bool = syl.add_vowel(self.text[index], next_let)
                    if break_bool:
                        break
            elif self.text[index] in letters.VOWELS_WITH_ACCENTS:
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
        if syl.vowels in letters.VOWELS_WITH_ACCENTS:
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
