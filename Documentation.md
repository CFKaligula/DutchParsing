# Documentation

This will be the design document that covers the implementation of this tool.

## Words

Words are transformed into Word objects that contain a couple of properties:

* **String** `text`, the actual text of the word.
* **Integer** `length`, the length of teh word.
* **\[Syllable\]** `syllables`, the syllables which the word is made up of.
* **String** `pronunciation`, a phonetic way saying exactly how the word should be pronounced.

## Syllables

Syllables also have are objects that contain the following properties:

* **Word** `word`, the word object that the syllable is a part of.
* **String** `start_cons`, the consonants at the start of the syllable.
* **String** `vowels`, the vowels making up the vowel sound in the syllable.
* **String** `end_cons`, the consonants at the end of the syllable.
* **Syllable** `prev_syl`, the syllable (object) that comes previously in teh word.
* **Syllable** `next_syl`, the syllable (object) that comes next in teh word.

Realize that `start_cons` and `end_cons` can both be empty strings for example in the word 'otto' the syllables would be 'la' and 'te' and the first syllable would have no starting consonants and the second syllable would have no ending consonants.

## Splitting Words in Syllables

SHOULD PROBABLY EXPLAIN MORE ABOUT WHAT SPLITTING ACTUALLY DOES AND WHAT SYLLABLES ARE

The first challenge for this program is splitting words into syllables. This is a useful feature for text editors for automatically hyphenating words at the end of sentences, but we want to split the word into syllables to be able to find the pronunciation of the word. Dutch is a language with a lot of rules that make words not phonetic, but their pronunciation can, in most cases, be derived from the letters around it. For example 'o' is pronounced differently in an open or a closed syllable, open means there is no ending consonant. The word 'dromen' should be split like dro-men as there is only 1 consonant and the word 'drommen' shoud be split like 'drom-men' as there are 2 consonants. This double consonant rule is one of many we can follow to get the correct syllables a word is made up of. Currently I have found only 1 general problem that seems to be unsolvable without a dictionary where we always split some words incorrectly. this has to do with the fact that there are loanwords from English that use the y as a vowel and then there are a couple of loanwords from other countries, 'yoghurt' and 'yoga', that use y as a consonant. There is simply no way of knowing, without a dictionary, whether babyoppas should be bab-yop-pas or ba-by-op-pas, or if besyoghurt should be-sy-og-hurt or bes-yog-hurt.

Dutch has its own rules for splitting up words in syllables that do not conform the actual syllables that make up the word. For example, starting syllables without starting consonants, should not be split, so the word 'eten' should not be split like 'e-ten' but should stay 'eten'. For this tool we want to parse the words like they should actually be pronounced so we can later give the correct pronunciation of the words. Moreover, adapting the current implementation to follow the actual Dutch syllable splitting rules would not be difficult at all. We will now continue the way the actual syllable splitting is implemented.

When we create a word object, it will find its own syllables when it is instantiated. The function used for this is the `initialize_syllables` function. This function is actually recursve and takes 2 arguments the current index called `start` of the word from where it still has to find syllables and the current list of syllables called `syllable_list`. When we first call the function `start` is of course 0 and `syllable_list` is a list containing an empty syllable, we have to do this otherwise our first Syllable will have a None object assigned for its `prev_syl` property.

The first thing we do is check if start is  higher than the length of the word, if that is the case, we assign the `next_syl` property to every syllable in the syllable list, as we now know them all, and we return the list of syllables without the first empty Syllable we added when we called the function for the first time.

Otherwise we loop over the letters in the word from the index `start` to the end of the word. There is a high chance we will break the loop before the end of the word as we will break this loop once we found the end of our syllable. First we check if our current index is not higher than the length of the word, if that is the case we of course break the for loop. We then make a variable called `next_let` which is equal to the letter that comes after the current one in the word. This variable will be useful later on. Otherwise we have a couple of cases, I will first explain the trivial cases. Firstly if the letter we are currently analyzing is a dash we break, since a dash automatically means the end of the syllable. The other trivial case is when we find a character that is not in the alphabet, we then do nothing and just look at the next letter. Then we have 3 cases left, the letter is either: a consonant, a vowel with an accent or a vowel without an accent.

### The letter is a consonant

If the letter is a consonant we first check if the letter is the last letter of the word and a 'y'. This is a kind of quick fix so that atleast non-compound english loanwords are still split correctly like 'baby'. If our letter is indeed the last letter and a y, we check if we we already found some ending consonants, since that would mean that our y is the vowel in the second syllable. See the word 'lazy', when we start parsing we find the  'l' as a starting consonant then the 'a' as a vowel then the 'z' as an ending consonant then the 'y'. Since we found that 'y' we realized that 'z' is not an ending consonant of 'laz' but actually the starting consonant of the syllable 'zy'  otherwise the word would be split as 'laz-y' instead of 'la-zy'. But to fix this we should actually start looping again from the z so we start with as a new syllable. To do this we call a function `fix_end_cons()` which we give our `index` in the loop but which will also return our `index` as it will fix the index to be set to the 'z' again. After calling that function we of course break out of the loop since we found the end of our syllable, The syllable that will now be added to the syllable list is 'la' and we call the function `initialize_syllables()` again with the index of the 'z' and the syllable list appended with the syllable `la`. The reason that we used the `fix_end_cons()` function and did not just decrement the index by one, is that in cases with words with multiple ending consonants, finding what consonants belong to what syllable are a bit more complicated. First of all, if the word would have been 'hutsky', we would have wanted the second syllable to start from 's' and thus the index would have been decremented by 2 instead of 1. This is why in the general case we have to call `fix_end_cons()` which will sort this all out and take care of some edge cases. This function will be explained later on in more detail.

If we did not yet have any ending consonants, we call the `add_y()` function. If we have already have vowels, we hope/predict/pray the 'y' is a consonant and thus we call `add_cons` with our letter. If we have any starting consonants we call `add_vowels()`, this is for example for 'by' since we have a starting consonant, we know that the 'y' should be a vowel. Then there is the last case, when there are no starting consonants or vowels, then we add 'y' as a vowel. The only case up until now for this has been the word 'sexy' as this is pronounced as 'sex-y' so the 'y' alone will be its own syllable.

Anyway, when the letter is not a 'y', we call the function `add_cons()` that belongs to the syllable object that will add the consonant to our syllable. This function works quite easily, if the syllable already contains some vowels, then we add the letter to our ending consonants, else we add it to our starting consonants. However, if we found that we already have vowels, and that the vowels + the current letter actually make up the letter combination 'ij', we add the letter to our vowels. This is because in Dutch, 'j' is usually a consonant pronounced like the 'y' in 'you' in English, but when an 'i' comes in front of it, the 'ij'  will be pronounced as a certain vowel. This is, for now, the only edge case in the `add_cons()` function.

With that we have covered the following edge cases in this part:

* baby
* babby
* sexy
* lijk

### The letter is a vowel (with an accent)

### The letter is a vowel with an accent

### `fix_end_cons()`

## Pronunciation

The largest problem has to do with the prefixes 'be', 'ge', 'te' and 'ver'. Usually when a word would start with an open syllable like 'we' like in the word 'wezen' it will be pronounced with a long ee sound, like it should be in an ope syllable. However, these prefixes do not follow the open/closed syllable rules and the e is always pronounced as a schwa sound (sounds like 'eh'), so 'bezeten' should be pronounced 'buh-zeten' while some other words that do not use 'be' as a prefix, like 'bezem' it will be pronunced like 'bay' in English.
