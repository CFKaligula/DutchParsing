import Phonetics
import Letters
import time
from playsound import playsound


class Syllable:

    def __init__(self, input_text='', prev_syl=None, next_syl=None, word=None):
        self._word = word
        self._start_cons = ''
        self._vowels = ''
        self._end_cons = ''
        self.find_cons_and_vowels(input_text.lower())
        self._prev_syl = prev_syl
        self._next_syl = next_syl

    @property
    def word(self):
        return self._word

    @property
    def text(self):
        return self._start_cons + self._vowels + self._end_cons

    @property
    def length(self):
        return len(self._start_cons + self._vowels + self._end_cons)

    @property
    def start_cons(self):
        return self._start_cons

    @property
    def vowels(self):
        return self._vowels

    @property
    def end_cons(self):
        return self._end_cons

    @property
    def prev_syl(self):
        return self._prev_syl

    @property
    def next_syl(self):
        return self._next_syl

    def find_cons_and_vowels(self, input_text):
        # finds the consonant and vowel groups in the syllable
        found_vowel = False
        for letter in input_text:
            if letter in Letters.CONSONANTS:
                if not found_vowel:
                    self._start_cons += letter
                else:
                    self._end_cons += letter
            else:
                self._vowels += letter
                found_vowel = True

    def fix_start_cons(self):
        if self._prev_syl.text and not (self._start_cons + self._vowels == 'tje'):
            # if we have a previous syllable and our syllable does not contain the diminutive 'tje' (as in autootje)
            while self._start_cons not in (Letters.VALID_CONSONANT_COMBINATIONS | Letters.CONSONANTS):
                # print(f'start cons {self._start_cons} is not a valid consonant combination')
                self._prev_syl._end_cons += self._start_cons[0]
                self._start_cons = self._start_cons[1:]

    def fix_end_cons(self, index):
        if len(self.end_cons) == 1 and self.end_cons != 'x':
            # if there is only 1 ending consonant the cons should go to the next syllable
            # except if the end_cons == x, as taxi is pronounced tax-i not ta-xi
            self._end_cons = ''
            index -= 1
        else:
            if self.end_cons == 'tj':
                # for diminutives the 'tj' will be the start of the next one e.g. au-too-tje
                self._end_cons = ''
                index -= 2
            if self.end_cons == 'sch':
                # for diminutives the 'tj' will be the start of the next one e.g. au-too-tje
                self._end_cons = ''
                index -= 3
            elif self._end_cons not in ['', 'ch', 'kw', 'th', 'ng']:
                # if there are multiple consonants (that are not one of the fixed ones) we give all but the first to the next syllable
                index -= len(self.end_cons) - 1
                self._end_cons = self.end_cons[0]
            # if we already have end cons, then this vowel is part of the next syllable
        return index

    def add_cons(self, cons):
        if self.vowels is not '':
            if self.vowels + cons == 'ij':
                # special check for dipthong 'ij'
                self._vowels += cons
            else:
                self._end_cons += cons
        else:
            self._start_cons += cons

    def add_vowel(self, vowel, next_letter):
        break_bool = False
        if self.vowels is '':
            self._vowels += vowel
        elif (self.start_cons + self.vowels == 'qu'):
            self._vowels += vowel
        elif (self.vowels + vowel) in Letters.TRIPTHONGS:
            # find a tripthong
            self._vowels += vowel
        elif (self.vowels + vowel + next_letter) in Letters.TRIPTHONGS:
            # foresee a tripthong
            self._vowels += vowel
        elif (self.vowels + vowel) in Letters.DIPTHONGS:
            # since we won't make a tripthong, we know we can stop the syllable here
            self._vowels += vowel
        else:
            # no dipthong or tripthong, so end of syllable
            break_bool = True
        return break_bool

    def add_y(self):
        if self.vowels is not '':
            self.add_cons('y')
        elif self.start_cons is not '':
            self.add_vowel('y', '')
        else:
            self.add_vowel('y', '')

    def remove_accents(self):
        self._vowels = ''.join(list(map(Letters.remove_accent, self._vowels)))

    def display_cons_and_vowels(self):
        print(f'The cons and vowels for {self.text} are:')
        print(f'start_cons: {self._start_cons}')
        print(f'vowels: {self._vowels}')
        print(f'end_cons: {self._end_cons}')

    def pronounce_syllable(self):
        print(f'pronounceing syllable {self.text}')
        # playsound('soundFiles/consonants/processed/d1.mp3')
        for letter in self._start_cons:
            if self._start_cons.index(letter) == 0 and self._prev_syl.end_cons and self._prev_syl.end_cons[-1] == self._start_cons[0]:
                print('skipping first cons as it is the same as previous ending cons')
            else:
                playsound(f'soundFiles/consonants/processed/d.mp3')
        # time.sleep(0.08)
        if self._vowels:
            self.pronounce_vowel()

        for letter in self._end_cons:
            print('play end')
            playsound(f'soundFiles/consonants/processed/{letter}.mp3')
        time.sleep(0.1)

    def pronounce_vowel(self):
        file_name = None
        if not self._end_cons:
            if self._vowels in {'a', 'e', 'o', 'u'}:
                file_name = self._vowels + self._vowels
            elif self._vowels == 'i':
                file_name = 'ie'
        else:  # if the syllable is closed
            if self._end_cons[0] in {'r', 'l'}:
                # if the end cons start with an r or an l, some vowels are pronounced differently
                if self._vowels == 'oo':
                    file_name == 'o'
                if self._vowels == 'ee':
                    file_name == 'i'
                if self._vowels == 'ei' or self._vowels == 'ij':
                    file_name == 'e'
        if self._vowels == 'ij':
            file_name = 'ei'
        if self._vowels == 'oeu':
            file_name = 'eu'
        if self._vowels == 'ou':
            file_name = 'au'
        if file_name == None:
            file_name = self._vowels
        vowel_file_path = f'soundFiles/vowels/processed/{file_name}.mp3'
        print(f'playing {vowel_file_path} ', )
        playsound(vowel_file_path)
        # time.sleep(0.1)
