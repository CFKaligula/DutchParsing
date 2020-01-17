import letters
from Syllable import Syllable
'''
TO BE IMPLEMENTED:
* Sound
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
                result += letters.BREAK_SYMBOL
        return result

    def get_syllables(self, rest_word, start, syllable_list):
        syl = Syllable(prev_syl=syllable_list[-1])

        word = self.text
        if start >= self.length:
            return syllable_list[1:]
        for index in range(start, self.length+1):
            if index >= self.length:
                break
            print(f'index letter: {word[index]}, {index}')
            if word[index] in letters.CONSONANTS:
                syl.add_cons(word[index])
            elif word[index] in letters.VOWELS:
                if len(syl.end_cons) > 0:
                    index = syl.fix_end_cons(index)
                    break
                else:
                    next_let = word[index+1] if index < self.length-1 else ''
                    break_bool = syl.add_vowel(word[index], next_let)
                    if break_bool:
                        break
            else:
                raise Exception(
                    f'Words should only contain letters, {word[index]} is not a letter.')

        syllable_list.append(syl)
        syl.display_cons_and_vowels()
        syl.check_start_cons()
        syl.update_text()

        return self.get_syllables(rest_word, index, syllable_list)
