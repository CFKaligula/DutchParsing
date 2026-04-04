from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import logbasic

from src.letter_dictionaries import CONSONANTS, DIPTHONGS, TRIPTHONGS, VALID_CONSONANT_COMBINATIONS

if TYPE_CHECKING:
    from src.word import Word


class Syllable:
    def __init__(
        self,
        input_text: str = '',
        prev_syl: Optional[Syllable] = None,
        next_syl: Optional[Syllable] = None,
        word: Optional[Word] = None,
    ):
        self.prev_syl = prev_syl
        self.next_syl = next_syl
        self.word = word

        self.start_cons, self.vowels, self.end_cons = self.find_cons_and_vowels(input_text.lower())

    @property
    def text(self):
        return self.start_cons + self.vowels + self.end_cons

    @property
    def length(self):
        return len(self.start_cons + self.vowels + self.end_cons)

    def find_cons_and_vowels(self, input_text) -> tuple[str, str, str]:
        start_cons = ''
        vowels = ''
        end_cons = ''
        # finds the consonant and vowel groups in the syllable
        found_vowel = False
        for letter in input_text:
            if letter in CONSONANTS:
                if not found_vowel:
                    start_cons += letter
                else:
                    end_cons += letter
            else:
                vowels += letter
                found_vowel = True

        return start_cons, vowels, end_cons

    def fix_start_cons(self):
        """
        fixes the start cons of the syllable if they are not valid.
        we keep moving the first letter of the start cons to the end cons of the previous syllable until we have a valid start cons
        """
        # if we have a previous syllable and our syllable does not contain the diminutive 'tje' (as in autootje)
        if self.prev_syl and self.prev_syl.text != '' and not (self.start_cons + self.vowels == 'tje'):
            while self.start_cons not in (VALID_CONSONANT_COMBINATIONS | CONSONANTS):
                logbasic.debug(f'start cons {self.start_cons} is not a valid consonant combination')
                self.prev_syl.end_cons += self.start_cons[0]
                self.start_cons = self.start_cons[1:]

    def fix_end_cons(self, index):
        """
        fixes the end cons of the syllable if they are not valid.
        """
        # if there is only 1 ending consonant, the cons should go to the next syllable (e.g. vaker: vak -> va)
        # except if the end_cons == x, e.g taxi is pronounced tax-i not ta-xi
        if len(self.end_cons) == 1 and self.end_cons != 'x':
            self.end_cons = ''
            index -= 1

        # for diminutives, the 'tj' will be the start of the next one
        #  e.g. au-too-tje. "tootj" -> "too"
        elif self.end_cons == 'tj':
            self.end_cons = ''
            index -= 2

        elif self.end_cons == 'sch':
            self.end_cons = ''
            index -= 3

        # if there are multiple consonants (that are not one of the fixed ones) we give all but the first to the next syllable
        # e.g. brander -> bran-der
        elif self.end_cons not in ['', 'ch', 'kw', 'th', 'ng']:
            index -= len(self.end_cons) - 1
            self.end_cons = self.end_cons[0]
        # if we already have end cons, then this vowel is part of the next syllable
        return index

    def add_cons(self, cons):
        if self.vowels != '':
            if self.vowels + cons == 'ij' and len(self.end_cons) == 0:
                # special check for dipthong 'ij'
                self.vowels += cons
            else:
                self.end_cons += cons
        else:
            self.start_cons += cons

    def add_vowel(self, vowel, next_letter):
        break_bool = False
        if self.vowels == '':
            self.vowels += vowel
        elif self.start_cons + self.vowels == 'qu':
            self.vowels += vowel
        elif (self.vowels + vowel) in TRIPTHONGS:
            # find a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel + next_letter) in TRIPTHONGS:
            # foresee a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel) in DIPTHONGS:
            # since we won't make a tripthong, we know we can stop the syllable here
            self.vowels += vowel
        else:
            # no dipthong or tripthong, so end of syllable
            break_bool = True
        return break_bool

    def add_y(self):
        if self.vowels != '':
            self.add_cons('y')
        elif self.start_cons != '':
            self.add_vowel('y', '')
        else:
            self.add_vowel('y', '')

    def remove_accents_from_vowels(self):
        self.vowels = ''.join([remove_accent(char) for char in self.vowels])

    def display_cons_and_vowels(self):
        logbasic.info(f'The cons and vowels for {self.text} are:')
        logbasic.info(f'\t*start_cons: {self.start_cons}')
        logbasic.info(f'\t*vowels: {self.vowels}')
        logbasic.info(f'\t*end_cons: {self.end_cons}')


def remove_accent(letter: str) -> str:
    if letter in {'á', 'ä'}:
        return 'a'
    if letter in {'é', 'ë'}:
        return 'e'
    if letter in {'í', 'ï'}:
        return 'i'
    if letter in {'ó', 'ö'}:
        return 'o'
    if letter in {'ú', 'ü'}:
        return 'u'
    else:
        return letter
