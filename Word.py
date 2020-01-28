import Letters
from Syllable import Syllable
'''
TO BE IMPLEMENTED:
* ijs-yog-hurt but ba-by-opera, probably impossible
* Sound
* nieuw, duw, hoi, groei, leeuw (just ignore the w)
* oer and uil, vowel pronunciation should be oe-uhr, ui-uhr where uh== schwa
* qu pronounced as kw
* should probably make a pronunciation variable for syllables
'''


class Word:
    def __init__(self, text):
        self._text = text.lower()
        self._length = len(text)
        self._syllables = self.initialize_syllables(text, 0, [Syllable('')])

    @property
    def text(self):
        return self._text

    @property
    def length(self):
        return self._length

    @property
    def syllables(self):
        return self._syllables

    def display_syllable_list(self):
        # prints a list with the syllables
        syllable_list = [syl.text for syl in self._syllables]
        print(syllable_list)

    def get_split_word(self):
        # returns the word split into syllables with dashes
        result = ''
        for syllable in self._syllables:
            result += syllable.text + Letters.BREAK_SYMBOL
        result = result[:-1]    # we remove the last break symbol
        return result

    def initialize_syllables(self, word, start, syllable_list):
        syl = Syllable(prev_syl=syllable_list[-1])

        word = self.text
        if start >= self.length:
            return syllable_list[1:]
        for index in range(start, self._length+1):
            if index >= self._length:
                break
            # print(f'index letter: {word[index]}, {index}')
            next_let = word[index+1] if index < self._length-1 else ''
            if word[index] == '-':
                index += 1
                break

            elif word[index] in Letters.CONSONANTS:
                if word[index] == 'y' and index == self.length-1:
                    if len(syl.end_cons) > 0:
                        index = syl.fix_end_cons(index)
                        break
                    else:
                        print(syl.end_cons)
                        syl.add_y()
                else:
                    syl.add_cons(word[index])
            elif word[index] in (Letters.VOWELS):
                if len(syl.end_cons) > 0:
                    index = syl.fix_end_cons(index)
                    break
                else:
                    break_bool = syl.add_vowel(word[index], next_let)
                    if break_bool:
                        break
            elif word[index] in Letters.VOWELS_WITH_ACCENTS:
                if len(syl.vowels) == 0:
                    break_bool = syl.add_vowel(word[index], next_let)
                    if break_bool:
                        break
                else:
                    index = syl.fix_end_cons(index)
                    break
            else:
                # print(f'"{word[index]}" is not a letter.')
                pass
        if syl.vowels in Letters.VOWELS_WITH_ACCENTS:
            #print(f' The syllable contains an accent, {syl.vowels}.')
            syl.remove_accents()
        syllable_list.append(syl)
        #syl.display_cons_and_vowels()
        syl.check_start_cons()

        return self.initialize_syllables(word, index, syllable_list)

    def pronounce_word(self):
        for syllable in self._syllables:
            syllable.pronounce_syllable()
