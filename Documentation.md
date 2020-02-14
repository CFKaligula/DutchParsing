# Documentation

This will be the design document that covers the implementation of this tool.

## Words

Words are transformed into Word objects that contain a couple of properties:

* **String** `text`, the actual text of the word.
* **Integer** `length`, the length of the word.
* **\[Syllable\]** `syllables`, the syllables which the word is made up of.
* **String** `pronunciation`, a phonetic way saying exactly how the word should be pronounced.

## Syllables

Syllables also have objects that contain the following properties:

* **Word** `word`, the word object that the syllable is a part of.
* **String** `start_cons`, the consonants at the start of the syllable.
* **String** `vowels`, the vowels making up the vowel sound in the syllable.
* **String** `end_cons`, the consonants at the end of the syllable.
* **Syllable** `prev_syl`, the syllable (object) that comes previously in teh word.
* **Syllable** `next_syl`, the syllable (object) that comes next in teh word.

Realize that `start_cons` and `end_cons` can both be empty strings for example in the word 'otto' the syllables would be 'la' and 'te' and the first syllable would have no starting consonants and the second syllable would have no ending consonants.

## Splitting Words in Syllables

SHOULD PROBABLY EXPLAIN MORE ABOUT WHAT SPLITTING ACTUALLY DOES AND WHAT SYLLABLES ARE

The first challenge for this program is splitting words into syllables. This is a useful feature for text editors for automatically hyphenating words at the end of sentences, but we want to split the word into syllables to be able to find the pronunciation of the word. Dutch is a language with a lot of rules that make words not phonetic, but their pronunciation can, in most cases, be derived from the letters around it. For example 'o' is pronounced differently in an open or a closed syllable, open means there is no ending consonant. The word 'dromen' should be split like dro-men as there is only 1 consonant and the word 'drommen' should be split like 'drom-men' as there are 2 consonants. This double consonant rule is one of many we can follow to get the correct syllables a word is made up of. Currently I have found only 1 general problem that seems to be unsolvable without a dictionary where we always split some words incorrectly. this has to do with the fact that there are loanwords from English that use the y as a vowel and then there are a couple of loanwords from other countries, 'yoghurt' and 'yoga', that use y as a consonant. There is simply no way of knowing, without a dictionary, whether babyoppas should be bab-yop-pas or ba-by-op-pas, or if besyoghurt should be-sy-og-hurt or bes-yog-hurt.

Dutch has its own rules for splitting up words in syllables that do not conform the actual syllables that make up the word. For example, starting syllables without starting consonants, should not be split, so the word 'eten' should not be split like 'e-ten' but should stay 'eten'. For this tool we want to parse the words like they should actually be pronounced so we can later give the correct pronunciation of the words. Moreover, adapting the current implementation to follow the actual Dutch syllable splitting rules would not be difficult at all. We will now continue the way the actual syllable splitting is implemented.

When we create a word object, it will find its own syllables when it is instantiated. The function used for this is the `initialize_syllables` function. This function is actually recursive and takes 2 arguments the current index called `start` of the word from where it still has to find syllables and the current list of syllables called `syllable_list`. When we first call the function `start` is of course 0 and `syllable_list` is a list containing an empty syllable, we have to do this otherwise our first Syllable will have a None object assigned for its `prev_syl` property.

The first thing we do is check if start is  higher than the length of the word, if that is the case, we assign the `next_syl` property to every syllable in the syllable list, as we now know them all, and we return the list of syllables without the first empty Syllable we added when we called the function for the first time.

Otherwise we loop over the letters in the word from the index `start` to the end of the word. There is a high chance we will break the loop before the end of the word as we will break this loop once we found the end of our syllable. First we check if our current index is not higher than the length of the word, if that is the case we of course break the for loop. We then make a variable called `next_let` which is equal to the letter that comes after the current one in the word. This variable will be useful later on. Otherwise we have a couple of cases, I will first explain the trivial cases. Firstly if the letter we are currently analyzing is a dash we break, since a dash automatically means the end of the syllable. The other trivial case is when we find a character that is not in the alphabet, we then do nothing and just look at the next letter. Then we have 3 cases left, the letter is either: a consonant, a vowel with an accent or a vowel without an accent.

### The letter is a consonant

If the letter is a consonant we first check if the letter is the last letter of the word and a 'y'. This is a kind of quick fix so that at least non-compound english loanwords are still split correctly like 'baby'. If our letter is indeed the last letter and a y, we check if we we already found some ending consonants, since that would mean that our y is the vowel in the second syllable. See the word 'lazy', when we start parsing we find the  'l' as a starting consonant then the 'a' as a vowel then the 'z' as an ending consonant then the 'y'. Since we found that 'y' we realized that 'z' is not an ending consonant of 'laz' but actually the starting consonant of the syllable 'zy'  otherwise the word would be split as 'laz-y' instead of 'la-zy'. But to fix this we should actually start looping again from the 'z' so we start with as a new syllable. To do this we call a function `fix_end_cons()` which we give our `index` in the loop but which will also return our `index` as it will fix the index to be set to the 'z' again. After calling that function we of course break out of the loop since we found the end of our syllable, The syllable that will now be added to the syllable list is 'la' and we call the function `initialize_syllables()` again with the index of the 'z' and the syllable list appended with the syllable `la`. The reason that we used the `fix_end_cons()` function and did not just decrement the index by one, is that in cases with words with multiple ending consonants, finding what consonants belong to what syllable are a bit more complicated. First of all, if the word would have been 'hutsky', we would have wanted the second syllable to start from 's' and thus the index would have been decremented by 2 instead of 1. This is why in the general case we have to call `fix_end_cons()` which will sort this all out and take care of some edge cases. This function will be explained later on in more detail.

If we did not yet have any ending consonants, we call the `add_y()` function. If we already have vowels, we hope/predict/pray the 'y' is a consonant and thus we call `add_cons` with our letter. If we have any starting consonants we call `add_vowels()`, this is for example for 'by' since we have a starting consonant, we know that the 'y' should be a vowel. Then there is the last case, when there are no starting consonants or vowels, then we add 'y' as a vowel. The only case up until now for this has been the word 'sexy' as this is pronounced as 'sex-y' so the 'y' alone will be its own syllable.

Anyway, when the letter is not a 'y', we call the function `add_cons()` that belongs to the syllable object that will add the consonant to our syllable. This function works quite easily, if the syllable already contains some vowels, then we add the letter to our ending consonants, else we add it to our starting consonants. However, if we found that we already have vowels, and that the vowels + the current letter actually make up the letter combination 'ij', we add the letter to our vowels. This is because in Dutch, 'j' is usually a consonant pronounced like the 'y' in 'you' in English, but when an 'i' comes in front of it, the 'ij'  will be pronounced as a certain vowel. This is, for now, the only edge case in the `add_cons()` function.

#### `fix_end_cons()`

We call the function `fix_end_cons()` to fix up the index for the next syllable and the ending consonants of our syllable. Firstly we check for the case if there is only one ending consonant in that case we remove it from `end_cons` and decrement the index by 1. So for example when we have the word bomen, for our first syllable we will find 'm' to be our ending consonant, but it should actually be 'bo-men' so we decrement the index by 1 so that the next syllable will start with the 'm'. There is only one exception, if our ending consonant is 'x', since we want a word like 'taxi' for example to not be 'ta-xi' but 'tax-i' as the x is pronounced as 'ks' making it kind of a secret double consonant.

Otherwise, if there are multiple ending consonats, we remove all but the first one from `end_cons` and decrement the index by the number of consonants we removed from `end_cons`. There are only a couple exceptions to this, which come in the form of consonants that appear grouped. The first group is 'ch', 'kw', 'th' and 'ng' these consonants groups make one sound so they should not be split up, 'lachen' for example should be split like 'lach-en' as 'ch' is actually just one sound, it is however still a double consonant, so it should not be 'la-chen'. If `end_cons` is empty or one of these 4 groups, we do nothing and just return the index as it was given. The other exceptions are the group 'tj', this is also a consonant group that should stay grouped, however it should only be a group of starting consonants. This group only appears in words in the diminutive case, for example 'autootje' which is split like 'au-too-tje' not 'au-tootj-e' or 'au-toot-je'. So if we find that `end_cons` is equal to 'tj' we  decrement the index by 2 and make `end_cons` empty. The last exception is if we have 'sch' as ending consonants, this is the same as for 'tj', we want 'sch' to be the start if the next syllabe, not the end of this one, for example in the word 'logische' it should be split like 'lo-gi-sche' not 'lo-gi-s-che' or 'lo-gisch-e'

### The letter is a vowel (without an accent)

If we find a vowel, but we already have ending consonants, we call `fix_end_cons` and break. This is because a syllable can only contain 1 group of vowels and if we already have ending consonants, then there must already be vowels, so the new vowels must be part of the next syllable. We just have to fix the ending consonants as some might be part of that second syllable as well. If we do not yet have ending consonants, we call the function `add_vowel` that is part of the syllable class, we pass it our letter, the `next_let` variable and this function `add_vowel` will return a boolean `break_bool` that will tell us whether or not we should break the loop, which we will do if the returned `break_bool` is True.

The reason we pass `next_let` is all about finding dipthong and tripthongs. Our definition of these words is a bit different than the actual meaning. What in linguistics is usually meant with a dipthong is a vowel that is actually going from one vowel to another, an example in english is the i in 'like' it is actually pronounced as 'laik' where the tongue in the mouth goes from one place to another. In Dutch there are some dipthongs that are actually written with two vowels, for example 'au' or 'ei', but there are also some vowel groups that are actually not dipthongs, for example 'aa' or 'oe'. So when we talk about a dipthong in this document we simply mean 2 vowels that make up a sound together. So for example in the word 'viaduct' 'ia' is not a dipthong as 'ia' is not a dipthong in the dutch language, the word should be split like 'vi-a-duct', but the word 'koeken' does contain a dipthong 'oe' so we split like 'koe-ken'. To make it even harder we have the dipthong 'ij' which is actually made up of the vowel 'i' and the consonant 'j', but it is still a dipthong as we explained earlier. Now that you understand the intricacies of the dutch orthography of vowels, the `add_vowel` function will be explained.

The first case is really easy, if there are not yet any vowels, we add our vowel to `vowels` and leave `break_bool` false when we return it. The second case is if the starting consonants and vowels we already have equal 'qu' this is a special case for loanwords from lating like 'quasi' and 'aquaduct' basically this u is unpronounced so every vowel that comes after it should be added to the `vowels`. The third case is if `vowels` + this letter together make a tripthong, if that is the case we add the vowel to `vowels`. The fourth case is if we can make a tripthong with `vowels`, our letter and the next letter, we of course also add our letter to `vowels`. The fifth case is if we can make a dipthong with `vowels` and our letter, we again add our letter to `vowels` if this is the case. If our letter didn't go through any of these cases, that means we won't add it to the vowels of this syllable and we set `break_bool` to True. This way the next syllable will start at this vowel. The reason that we do not break if we find a tripthong or a dipthong is that we would also have to change the index then, this would make the code rather ugly as we would also have to give the index to add_vowel. We would rather continue the loop and break then, than be slightly faster, but have also slightly less ugly code.

### The letter is a vowel with an accent

If the letter is a vowel with an accent, we know that if there already vowels, we can never add this vowel with an accent. So when there are already vowels we call `fix_endcons()` and break. The reason we know that we can break is because an accent is either a forward dash, a backwards dash or an ampersand/umlaut. an ampersand in dutch by definition means a syllable split like in the woord 'ideeën' which should be 'idee-en'. A letter with a forward dash, also acccent aigu, or a backwards dash, accent grave, are never used in dipthongs so we know we can split the syllable. The only times these would come after another vowel is in compound words like 'laétagere' which should be 'la-e-ta-ge-re'. There is one exception, but it only appears in French, for the female form of some adjectives like 'blasé' which becomes 'blasée', but this never appears in Dutch, as far as I know. We could implement so that if we already have 'é' as our vowel and then we find an 'e' we just add it, but there could be a case where we have a compound word from a word that ends on 'é' and the other word starts with  'e' like for example 'blaséeend', which is a lot more likely than this French feminine case.

If there are not yet any vowels, we just call add_vowel where it will fall into the first case so it will be added.

### After the syllable is complete

After our loop is complete you would think we are done and can just call the function again with the next letter as our index. However, this is not the case we first have to do 3 things. Firstly if there was a vowel with an accent in the word, we remove it from the syllable, then we call the function `fix_start_cons()` to fix up our starting consonants. It is probably quite unexpected that we also need to fix the starting consonants if we already fixed the ending consonants. This is because you have to split Dutch words so that the starting consonants are a so-called "valid consonant combination". This means that the group of starting consonants has to be a group of consonants that actually appears at the start of a Dutch word. Say we have the word 'herfstig', while processing we find the first syllable to be 'herfst' when we find the 'i', then since we found a vowel we called `fix_end_cons()` and this removed all but the first consonant of `end_cons` from 'herfst', so the first syllable is 'her' we then call the function again from the 'f' and find that the second syllable is 'fstig'. 'fst' is an invalid consonant combination as there are no Dutch words that start with 'fst'. To fix this, we check if there is a previous syllable to whose ending consonants we can add our leftover starting consonants.  We also check if our starting consonants + our vowels make 'tje' as 'tj' is normally not a valid consonant combinatino, but it is when used in the diminutive case 'tje' as in 'autootje'. If there is no previous syllable or if we do have 'tje', we do nothing, otherwise we keep removing the starting consonant at the beginning of the starting consonant group until we our starting consonants are a valid consonant combination, we of course add the removed starting consonants to the previous syllables ending consonant. So in the case of 'her-fstig', It becomes 'herf-stig' and since 'st' is a valid consonant combination, for example in the word 'storm' we stop and have now fixed the starting consonants. To check if the starting consonants are valid we have a list of all of the valid consonant combinations. It is easy to find all of these as there are only a couple of consonants which can occur in groups. Of course every single consonant is also a valid consonant combination so if our group of starting consonants only has size 1 it is automatically valid.

Now that we have fixed the starting consonants our syllable is officially complete and we append it to the syllable list, then we call the function again with the index that our loop ended with as `start` and the current syllable list as `syllable_list` as parameters to `initialize_syllables()`. This will eventually lead to the entire word being split into syllables at which point our recursion will end and our syllable list is finished and our word should be successfully and correctly split.

## Pronunciation

The largest problem has to do with the prefixes 'be', 'ge', 'te' and 'ver'. Usually when a word would start with an open syllable like 'we' like in the word 'wezen' it will be pronounced with a long ee sound, like it should be in an ope syllable. However, these prefixes do not follow the open/closed syllable rules and the e is always pronounced as a schwa sound (sounds like 'eh'), so 'bezeten' should be pronounced 'buh-zeten' while some other words that do not use 'be' as a prefix, like 'bezem' it will be pronounced like 'bay' in English.

## Console

You can easily interact with the tool via the Console, with the command `split` you can get a word split up via the way explained above.

``` bash
$WORD= lopen # any word you want to input
C:\...\DutchParsing>python Console.py split $WORD
lo-pen
```

You can input a word (or multiple) to the console script and it will give a phonetic translation of the word using this program's system:

``` bash
$WORD= lopen # any word you want to input
C:\...\DutchParsing>python Console.py phonetic $WORD
lóp0n
```

You can test the tool by running the `test` command which will run a bunch of tests on the splitting to see if they still work correctly.

``` bash
C:\...\DutchParsing>python Console.py test
***.***.*** All Tests Successful ***.***.***
```

You can analyze a file or a piece of text with the `analyze` command, it will tell you some info about the piece of text.

``` bash
C:\...\DutchParsing>python Console.py analyze "een lekker stukkie tekst om te analyzeren."
there were a total of 11 unique syllables in the text, of 7 sentences.
the 10 most common syllables were {'een': 1, 'lek': 1, 'ker': 1, 'stuk': 1, 'kie': 1, 'tekst': 1, 'om': 1, 'te': 1, 'be': 1, 'kij': 1}
```

``` bash
C:\...\DutchParsing>python Console.py analyze-file TextFiles/Het-Boek.txt
there were a total of 4859 unique syllables in the text, of 761332 words.
the 10 most common syllables were {'de': 65405, '': 33432, 'en': 31476, 'ge': 22602, 'van': 21798, 'te': 19022, 'den': 17583, 'het': 15858, 'ver': 15036, 'u': 14538}
```
