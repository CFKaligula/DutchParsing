import Letters
from Syllable import Syllable
'''
TO BE IMPLEMENTED:
* Sound
* nieuw, duw, hoi, groei, leeuw (just ignore the w)
* oer and uil, vowel pronunciation should be oe-uhr, ui-uhr where uh== schwa
* qu pronounced as kw
* should probably make a pronunciation variable for syllables
* use 'for letter in word' instead of 'for i in range(0,len(word))
'''


class Word:
    def __init__(self, text):
        self.text = text.lower()
        self.length = len(text)
        self.syllables = self.get_syllables(text, 0, [Syllable('')])

    def display_syllable_list(self):
        # prints a list with the syllables
        syllable_list = [syl.text for syl in self.syllables]
        print(syllable_list)

    def get_split_word(self):
        # returns the word split into syllables with dashes
        result = ''
        for i in range(0, len(self.syllables)):
            result += self.syllables[i].text
            if i != len(self.syllables)-1:
                result += Letters.BREAK_SYMBOL
        return result

    def get_syllables(self, word, start, syllable_list):
        syl = Syllable(prev_syl=syllable_list[-1])

        word = self.text
        if start >= self.length:
            return syllable_list[1:]
        for index in range(start, self.length+1):
            if index >= self.length:
                break
            print(f'index letter: {word[index]}, {index}')
            if word[index] == '-':
                index += 1
                break
            elif word[index] in Letters.CONSONANTS:
                syl.add_cons(word[index])
            elif word[index] in (Letters.VOWELS):
                if len(syl.end_cons) > 0:
                    index = syl.fix_end_cons(index)
                    break
                else:
                    next_let = word[index+1] if index < self.length-1 else ''
                    break_bool = syl.add_vowel(word[index], next_let)
                    if break_bool:
                        break
            elif word[index] in Letters.VOWELS_WITH_ACCENTS:
                if len(syl.vowels) == 0:
                    syl.vowels += word[index]
                else:
                    index = syl.fix_end_cons(index)
                    break
            else:
                raise Exception(
                    f'Words should only contain Letters, {word[index]} is not a letter.')
        if syl.vowels in Letters.VOWELS_WITH_ACCENTS:
            print(f' The syllable contains an accent, {syl.vowels}.')
            syl.remove_accents()
        syllable_list.append(syl)
        syl.display_cons_and_vowels()
        syl.check_start_cons()
        syl.update_text()

        return self.get_syllables(word, index, syllable_list)

    def speak_syllables(self):
        for syllable in self.syllables:
            syllable.speak_syllable()
