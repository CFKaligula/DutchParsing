from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional

import logbasic  # type: ignore

import src.letter_dictionaries as letter_dictionaries

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

        self.start_cons = ''
        self.vowels = ''
        self.end_cons = ''
        self.find_cons_and_vowels(input_text.lower())

    @property
    def text(self):
        return self.start_cons + self.vowels + self.end_cons

    @property
    def length(self):
        return len(self.start_cons + self.vowels + self.end_cons)

    def find_cons_and_vowels(self, input_text):
        # finds the consonant and vowel groups in the syllable
        found_vowel = False
        for letter in input_text:
            if letter in letter_dictionaries.CONSONANTS:
                if not found_vowel:
                    self.start_cons += letter
                else:
                    self.end_cons += letter
            else:
                self.vowels += letter
                found_vowel = True

    def fix_start_cons(self):
        """
        fixes the start cons of the syllable if they are not valid.
        we keep moving the first letter of the start cons to the end cons of the previous syllable until we have a valid start cons
        """
        # if we have a previous syllable and our syllable does not contain the diminutive 'tje' (as in autootje)
        if self.prev_syl and self.prev_syl.text != '' and not (self.start_cons + self.vowels == 'tje'):
            while self.start_cons not in (letter_dictionaries.VALID_CONSONANT_COMBINATIONS | letter_dictionaries.CONSONANTS):
                logbasic.debug(f'start cons {self.start_cons} is not a valid consonant combination')
                self.prev_syl.end_cons += self.start_cons[0]
                self.start_cons = self.start_cons[1:]

    def fix_end_cons(self, index):
        """
        fixes the end cons of the syllable if they are not valid.
        """
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
            elif self.end_cons == 'sch':
                # for diminutives the 'tj' will be the start of the next one e.g. au-too-tje
                self.end_cons = ''
                index -= 3
            elif self.end_cons not in ['', 'ch', 'kw', 'th', 'ng']:
                # if there are multiple consonants (that are not one of the fixed ones) we give all but the first to the next syllable
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
        elif (self.vowels + vowel) in letter_dictionaries.TRIPTHONGS:
            # find a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel + next_letter) in letter_dictionaries.TRIPTHONGS:
            # foresee a tripthong
            self.vowels += vowel
        elif (self.vowels + vowel) in letter_dictionaries.DIPTHONGS:
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
        self.vowels = ''.join([letter_dictionaries.remove_accent(char) for char in self.vowels])

    def display_cons_and_vowels(self):
        logbasic.info(f'The cons and vowels for {self.text} are:')
        logbasic.info(f'\t*start_cons: {self.start_cons}')
        logbasic.info(f'\t*vowels: {self.vowels}')
        logbasic.info(f'\t*end_cons: {self.end_cons}')

    def pronounce_syllable(self):
        logbasic.debug(f'pronouncing syllable {self.text}')
        for letter in self.start_cons:
            if self.start_cons.index(letter) == 0 and self.prev_syl and self.prev_syl.end_cons[-1:] == self.start_cons[0]:
                logbasic.debug('skipping first cons as it is the same as previous ending cons')
            else:
                logbasic.debug(f'playing start letter {letter}')
                # sound_path = f'soundFiles/consonants/processed/{letter}.mp3'
        # time.sleep(0.08)
        if self.vowels:
            self.pronounce_vowel()

        for letter in self.end_cons:
            logbasic.debug(f'playing end letter {letter}')
            # sound_path = f'soundFiles/consonants/processed/{letter}.mp3'

        time.sleep(0.1)

    def pronounce_vowel(self):
        file_name = None
        if not self.end_cons:
            if self.vowels in {'a', 'e', 'o', 'u'}:
                file_name = self.vowels + self.vowels
            elif self.vowels == 'i':
                file_name = 'ie'
        else:  # if the syllable is closed
            if self.end_cons[0] in {'r', 'l'}:
                # if the end cons start with an r or an l, some vowels are pronounced differently
                if self.vowels == 'oo':
                    file_name = 'o'
                if self.vowels == 'ee':
                    file_name = 'i'
                if self.vowels == 'ei' or self.vowels == 'ij':
                    file_name = 'e'
        if self.vowels == 'ij':
            file_name = 'ei'
        if self.vowels == 'oeu':
            file_name = 'eu'
        if self.vowels == 'ou':
            file_name = 'au'
        if file_name is None:
            file_name = self.vowels

        # vowel_file_path = f'soundFiles/vowels/processed/{file_name}.mp3'
        logbasic.debug('playing vowel')
        logbasic.debug('playing vowel')
        logbasic.debug('playing vowel')
        logbasic.debug('playing vowel')
