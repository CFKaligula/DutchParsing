import argparse
import letters
'''
TO BE IMPLEMENTED:
* correct parsing of j, blije should be blij-e where ij is a dipthong, vrijijs should be vrij-ijs, jijeter, jij-eter herfstjuk,
* blije should be blij-e not bli-je
* lachen should be lach-en, not lac-hen
* taxi should be tax-i, not ta-xi
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
                result += '-'
        return result

    def get_syllables(self, rest_word, start, syllable_list):
        start_cons = ''
        vowels = ''
        end_cons = ''
        word = self.text
        if start >= self.length:
            return syllable_list[1:]
        for index in range(start, self.length+1):
            if index >= self.length:
                break
            print(f'index letter: {word[index]}, {index}')
            if word[index] in letters.consonants:  # if we find a consonant
                if len(vowels) > 0:
                    end_cons += word[index]
                else:
                    start_cons += word[index]

            else:  # if we find a vowel
                if len(end_cons) > 0:
                    # if we already have end cons, then this vowel is part of the next syllable
                    if len(end_cons) == 1:
                        # if there is only 1 ending consonant
                        # the cons should go to the next syllable
                        end_cons = ''
                        index -= 1
                    else:
                        # if there are multiple consonants
                        # we give all but the first to the next syllable
                        index -= len(end_cons) - 1
                        end_cons = end_cons[0]
                    break
                else:
                    if len(vowels) == 0:
                        vowels += word[index]
                    elif (vowels + word[index]) in letters.tripthongs:
                        # find a tripthong
                        vowels += word[index]
                        if index < self.length-1 and word[index+1] in vowels:
                            # this is the end of the syllable, if the next letter is a vowel,
                            index += 1
                            break
                    elif index < self.length-1 and (vowels + word[index] + word[index+1]) in letters.tripthongs:
                        # foresee a tripthong
                        vowels += word[index]
                    elif (vowels + word[index]) in letters.dipthongs:
                        # since we won't make a tripthong, we know we can stop the syllable here
                        vowels += word[index]
                    else:
                        # no dipthong or tripthong, so end of syllable
                        break

        print(f'start_cons: {start_cons}')
        print(f'vowels: {vowels}')
        print(f'end_cons: {end_cons}')
        syl = Syllable(start_cons + vowels + end_cons, syllable_list[-1])
        syl.check_start_cons()
        syllable_list.append(syl)
        return self.get_syllables(rest_word, index, syllable_list)


class Syllable:
    def __init__(self, text='', prev_syl=''):
        self.text = text
        self.length = len(self.text)
        self.start_cons = ''
        self.vowels = ''
        self.end_cons = ''
        self.find_cons_and_vowels()
        self.prev_syl = prev_syl

    def find_cons_and_vowels(self):
        # finds the consonant and vowel groups in the syllable
        if self.text == '':
            return '', '', ''
        found_vowel = False
        for i in range(0, self.length):
            if self.text[i] in letters.consonants:
                if not found_vowel:
                    self.start_cons += self.text[i]
                else:
                    self.end_cons += self.text[i]
            else:
                self.vowels += self.text[i]
                found_vowel = True

    def check_start_cons(self):
        if len(self.prev_syl.text) > 0:
            while self.start_cons not in letters.consonant_combinations:
                print(f'start cons {self.start_cons} is not a good group')
                self.prev_syl.end_cons += self.start_cons[0]
                self.start_cons = self.start_cons[1:]
            self.update_text()
            self.prev_syl.update_text()

    def update_text(self):
        self.text = self.start_cons + self.vowels + self.end_cons
        print(f'updated text to {self.text}')

    def display_syllable(self):
        print(self.text)

    def display_cons_and_vowels(self):
        print(f'The cons and vowels for {self.text} are:')
        print(f'start_cons: {self.start_cons}')
        print(f'vowels: {self.vowels}')
        print(f'end_cons: {self.end_cons}')


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str,
                        help='input for the parser', nargs='+')
    args = parser.parse_args()
    print(args.input)
    processed_input = []
    if args.input == ['test']:
        test_parser()
    else:
        for word in args.input:
            hallo = Word(word)
            hallo.display_syllable_list()
            print(hallo.get_split_word())


def test_parser():
    if Word('dromen').get_split_word() == 'dro-men' and \
            Word('leerling').get_split_word() == 'leer-ling' and \
            Word('ambtenaar').get_split_word() == 'amb-te-naar' and \
            Word('koeien').get_split_word() == 'koei-en' and \
            Word('piano').get_split_word() == 'pi-a-no' and \
            Word('niveau').get_split_word() == 'ni-veau' and \
            Word('radio').get_split_word() == 'ra-di-o' and \
            Word('hoofdstad').get_split_word() == 'hoofd-stad':
        print('*********all tests successful************')


def main():
    get_input()


main()
