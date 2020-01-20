import Letters
import time
from playsound import playsound


class Syllable:
    def __init__(self, text='', prev_syl=''):
        self.text = text.lower()
        self.length = len(self.text)
        self.start_cons = ''
        self.vowels = ''
        self.end_cons = ''
        self.find_cons_and_vowels()
        self.prev_syl = prev_syl

    def find_cons_and_vowels(self):
        # finds the consonant and vowel groups in the syllable
        found_vowel = False
        for i in range(0, self.length):
            if self.text[i] in Letters.CONSONANTS:
                if not found_vowel:
                    self.start_cons += self.text[i]
                else:
                    self.end_cons += self.text[i]
            else:
                self.vowels += self.text[i]
                found_vowel = True

    def check_start_cons(self):
        if len(self.prev_syl.text) > 0 and not (self.start_cons + self.vowels == 'tje'):
            # if we have a previous syllable and our syllable does not contain the diminutive 'tje' (as in autootje)
            while self.start_cons not in (Letters.VALID_CONSONANT_COMBINATIONS | Letters.CONSONANTS):
                print(
                    f'start cons {self.start_cons} is not a valid consonant combination')
                self.prev_syl.end_cons += self.start_cons[0]
                self.start_cons = self.start_cons[1:]
            self.update_text()
            self.prev_syl.update_text()

    def fix_end_cons(self, index):
        if len(self.end_cons) == 1 and self.end_cons != 'x':
            # if there is only 1 ending consonant the cons should go to the next syllable
            # except if the end_cons == x, as taxi is pronounced tax-i not ta-xi
            self.end_cons = ''
            index -= 1
        else:
            if self.end_cons == 'tj':
                # for diminutives the 'tj' will be the start of the next one e.g. au-too-tje
                self.end_cons = ''
                index -= 2
            elif self.end_cons not in ['', 'ch', 'kw', 'th', ]:
                # if there are multiple consonants (that are not one of the fixed ones) we give all but the first to the next syllable
                index -= len(self.end_cons) - 1
                self.end_cons = self.end_cons[0]
            # if we already have end cons, then this vowel is part of the next syllable
        return index

    def update_text(self):
        self.text = self.start_cons + self.vowels + self.end_cons
        print(f'updated text to {self.text}')

    def add_cons(self, cons):
        if len(self.vowels) > 0:
            if self.vowels + cons == 'ij':
                # special check for dipthong 'ij'
                self.vowels += cons
            else:
                self.end_cons += cons
        else:
            self.start_cons += cons

    def add_vowel(self, vowel, next_letter):
        break_bool = False
        if len(self.vowels) == 0:
            self.vowels += vowel

        elif (self.vowels + vowel) in Letters.TRIPTHONGS:
            # find a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel + next_letter) in Letters.TRIPTHONGS:
            # foresee a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel) in Letters.DIPTHONGS:
            # since we won't make a tripthong, we know we can stop the syllable here
            self.vowels += vowel
        else:
            # no dipthong or tripthong, so end of syllable

            break_bool = True
        return break_bool

    def remove_accents(self):
        for i in range(0, len(self.vowels)):
            if self.vowels[i] in Letters.VOWELS_WITH_ACCENTS:
                self.vowels = Letters.remove_accent_in_string(self.vowels, i)

    def display_syllable(self):
        print(self.text)

    def display_cons_and_vowels(self):
        print(f'The cons and vowels for {self.text} are:')
        print(f'start_cons: {self.start_cons}')
        print(f'vowels: {self.vowels}')
        print(f'end_cons: {self.end_cons}')

    def speak_syllable(self):
        print(f'speaking syllable {self.text}')
        # playsound('soundFiles/consonants/processed/d1.mp3')

        for i in range(0, len(self.start_cons)):
            if i == 0 and len(self.prev_syl.end_cons) > 0 and self.prev_syl.end_cons[-1] == self.start_cons[0]:
                print('skipping first cons as it is the same as previous ending cons')
            else:
                playsound(
                    f'soundFiles/consonants/processed/d.mp3')
        time.sleep(0.2)
        if len(self.vowels) > 0:
            self.speak_vowel()

        for i in range(0, len(self.end_cons)):
            print('play end')
            playsound(
                f'soundFiles/consonants/processed/{self.end_cons[i]}.mp3')
        time.sleep(0.1)

    def speak_vowel(self):
        file_name = None
        if len(self.end_cons) == 0:
            if self.vowels in {'a', 'e', 'o', 'u'}:
                file_name = self.vowels + self.vowels
            elif self.vowels == 'i':
                file_name = 'ie'
        else:  # if the syllable is closed
            if self.end_cons[0] in {'r', 'l'}:
                # if the end cons start with an r or an l, some vowels are pronounced differently
                if self.vowels == 'oo':
                    file_name == 'o'
                if self.vowels == 'ee':
                    file_name == 'i'
                if self.vowels == 'ei' or self.vowels == 'ij':
                    file_name == 'e'
        if self.vowels == 'ij':
            file_name = 'ei'
        if self.vowels == 'oeu':
            file_name = 'eu'
        if self.vowels == 'ou':
            file_name = 'au'
        if file_name == None:
            file_name = self.vowels
        vowel_file_path = f'soundFiles/vowels/processed/{file_name}.mp3'
        print(f'playing {vowel_file_path} ', )
        playsound(vowel_file_path)
        time.sleep(0.1)
