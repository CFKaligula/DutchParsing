# DutchParsing

 A Python Implementation for correctly parsing Dutch words.

## Introductions

The Dutch language has quite a complicated spelling system (also called *orthography*), making it possible in a lot of cases to derive a words pronunciation from its spelling. However, there are also a plethora of exceptions, making it not always possible.

Loan words are probably the first obstacle to come to mind. The fact that *jam* is not pronounced like *yahm* but like *zhem* (like the *s* in *treasure*), is impossible to know, especially because *jam* being pronounced phonetically is also an existing word. You would need a deep learning model to be able to work around such challenges, and those exist. The challenge undertaken in this project, is to only use only deterministic spelling rules and hard-coded exception lists as little as possible.

### Open and Closed Syllables

Here is a simple example of a Dutch spelling rule, to illustrate how this project works. In Dutch there are 2 types of syllables: open and closed. Where an open syllable has no ending consonant and a closed syllable does. So in the word *bomen* there are 2 syllables: *bo* and *men*. The first is open, the second is closed. Vowels in Dutch differ in pronuncation depending on the syllable type. The o in *bo* is the same as the vowel in *boom*, but different from *bom*. To "close" an open syllable, you double the next consonant, so *bommen* has the same *o* as *bom*. This means that in Dutch *boomen* can never occur. This double consonant rule is one of many we can follow to get the correct syllables a word is made up of.

Currently I have found only 1 general problem that seems to be unsolvable without a dictionary where we always split some words incorrectly. this has to do with the fact that there are loanwords from English that use the y as a vowel and then there are a couple of loanwords from other countries, 'yoghurt' and 'yoga', that use y as a consonant. There is simply no way of knowing, without a dictionary, whether babyoppas should be bab-yop-pas or ba-by-op-pas, or if besyoghurt should be-sy-og-hurt or bes-yog-hurt.

## Installation

This project uses `uv` to handles package management.

## How to Use

You can do multiple inputs by enclosing the inputs with double quotation marks.

### Splitting words in syllables

You can easily interact with the tool via the Console, with the command `split` you can get a word split up via the way explained above.

``` powershell
$WORD= lopen # any word you want to input
...\DutchParsing>uv run console.py split $WORD
lo-pen
```

### Getting the pronunciation of a word

You can input a word together with the command `phonetic` to the console script and it will give a phonetic translation of the word using this program's system,
for info about the pronunciation of each symbol see the PhoneticSystem file:

``` powershell
$WORD= lopen # any word you want to input
...\DutchParsing>uv run console.py phonetic $WORD
lóp0n
```

### Finding Rhyme words for a word

You can find all the words that rhyme with a certain words. You can either find words that rhyme fully or words that only have the same vowels. If no rhyme type is specified it does full rhyme by default. Use the following command:

``` powershell
$WORD= lopen # any word you want to input
$TYPE= full # should be either 'full' or 'vowel'
...\DutchParsing>uv run console.py rhyme -t $TYPE $WORD
2020-03-02 21:58:14,253 - [INFO]  Finding words that rhyme with: óp0n
bekopen
bezopen
dopen
dropen
hopen
knopen
kopen
kropen
lopen
nopen
open
slopen
stropen
tropen
zopen
```

### Running tests

Tests are done with the `pytest` module in the `tests/` folder.
