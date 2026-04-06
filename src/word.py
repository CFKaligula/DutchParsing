import logbasic  # type: ignore

from src.letter_dictionaries import CONSONANTS, PHONETIC_SYSTEM_CONSONANTS, VOWELS, VOWELS_WITH_ACCENTS
from src.phonetic import phonetic
from src.syllable import Syllable

"""
error: flikje  rhymes with zeiden...
TO BE IMPLEMENTED:
* Programming:
    * logger still isnt imported via __init__.py have to do it via console
* Split
    * ijs-yog-hurt but ba-by-opera, probably impossible. can do something for analyse where you see y has no vowels around it so it must be the vowel.
    * when y is seen as an end cosonant it should be a vowel for next syllable (really hard as we would have to have found a second vowel)

* Sound
    * sound files for consonants and some dipthongs
    * nieuw, duw, hoi, groei, leeuw (just ignore the w)
* Rhyme inventory
    * full rhyme only do stressed part?
    * vader now rhymes with 'vaal' because both have vowels a0 maybe special symbol for aa infront of l/r
* phonetic
    * ieuw, duw, eeuw
    * change trema to ^ so ä should be â á ä
    * ontdek = ondek ( maybe not?) (then also onbedoeld = ombedoeld), anker = angker, research all these combinations
    * jasje maybe jaße? not sure so implement ,ß for end_con s
    * different r's 
    * dommeriken = domm0riken so fix both e and i, same volkeren, kalveren shouldn't be volkiiren
    * maybe make previous_letter() and next_letterter() functions so you don't have to do i>0 and end_cons[i-1] everytime
"""


class Word:
    def __init__(self, text: str):
        self.text = text.lower()
        self.length = len(text)
        self.syllables = self.compute_syllables()
        self.pronunciation = self.compute_pronunciation()

    def compute_pronunciation(self):
        pronunciation = ''

        for syllable in self.syllables:
            if syllable.start_cons:
                pronunciation += phonetic.find_start_con_pronunciation(syllable)
            if syllable.vowels:
                pronunciation += phonetic.find_vowel_pronunciation(syllable)
            if syllable.end_cons:
                pronunciation += phonetic.find_end_con_pronunciation(syllable)
        return pronunciation

    def compute_syllables(self) -> list[Syllable]:
        pos = 0
        syllable_list = []

        while pos < self.length:
            # Create a syllable
            if len(syllable_list) == 0:
                syl = Syllable(prev_syl=Syllable(''), word=self)
            else:
                syl = Syllable(prev_syl=syllable_list[-1], word=self)

            index = pos
            # Build this syllable by advancing index until we should stop
            while index < self.length:
                logbasic.debug(f'index letter: {self.text[index]}, {index}')

                current_letter = self.text[index]
                next_letter = self.text[index + 1] if index + 1 < self.length else '-'

                if current_letter == '-':
                    index += 1
                    break

                # CONSONANTS
                elif current_letter in CONSONANTS:
                    if current_letter == 'y' and index == self.length - 1:
                        if len(syl.end_cons) > 0:
                            index = syl.fix_end_cons(index)
                            break
                        else:
                            syl.add_y()
                    else:
                        syl.add_cons(current_letter)
                    index += 1

                # VOWELS
                elif current_letter in VOWELS:
                    if len(syl.end_cons) > 0:
                        index = syl.fix_end_cons(index)
                        break
                    else:
                        break_bool = syl.add_vowel(current_letter, next_letter)
                        if break_bool:
                            break
                        index += 1

                # VOWELS WITH ACCENTS
                elif current_letter in VOWELS_WITH_ACCENTS:
                    if len(syl.vowels) == 0:
                        break_bool = syl.add_vowel(current_letter, next_letter)
                        if break_bool:
                            break
                        index += 1
                    else:
                        index = syl.fix_end_cons(index)
                        break

                else:
                    logbasic.warning(f'"{current_letter}" is not a letter.')
                    index += 1

            if syl.vowels in VOWELS_WITH_ACCENTS:
                logbasic.debug(f' The syllable contains an accent, {syl.vowels}.')
                syl.remove_accents_from_vowels()

            syl.fix_start_cons()
            syllable_list.append(syl)

            pos = index

        # add the next_syl to all syllables
        for i in range(0, len(syllable_list) - 1):
            syllable_list[i].next_syl = syllable_list[i + 1]

        return syllable_list

    def get_split_word(self) -> str:
        """
        returns the word split into syllables with dashes
        """
        result = ''
        for syllable in self.syllables:
            result += syllable.text + '-'
        result = result[:-1]  # we remove the last break symbol
        return result

    def get_phonetic_vowels(self) -> str:
        """
        returns the vowels in the pronunciation of the word, for rhyming purposes.
        """
        vowels = ''
        for letter in self.pronunciation:
            # TODO why not "in vowels"?
            if letter not in PHONETIC_SYSTEM_CONSONANTS:
                vowels += letter
        logbasic.debug(vowels)
        return vowels

    def get_rhyme_part(self) -> str:
        """
        returns the part of the pronunciation that is relevant for rhyming, so the part after the last stressed vowel.
        For example, for 'gepakt' it would return 'akt', so it would rhyme with words that also end on 'akt' like 'verpakt'.
        """
        start_length = 0
        for letter in self.pronunciation:
            if letter in PHONETIC_SYSTEM_CONSONANTS or letter == '0':
                # take the part after the first consonants and schwas, so gepakt will find words that also end on akt
                start_length += 1
            else:
                break

        return self.pronunciation[start_length:]
