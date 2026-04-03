# DutchParsing

 A Python Implementation for correctly parsing Dutch words.

## Introductions

 The idea of this parser it to make use of rules as much as possible and to not use word lists. First the parser will be used to split up words in syllables. Then the correct sounds for every syllable should be linked
 After that add an artificial voice to pronounce the words.

 Eventually there will be need for a word list of some sort, as there is no way to know if the syllable 'be' should be pronounced as 'bay' for 'bezem' or  'buh' for 'bezet.

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
