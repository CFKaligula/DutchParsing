# DutchParsing

 A Python Implementation for correctly parsing Dutch words.

## Introductions

 The idea of this parser it to make use of rules as much as possible and to not use word lists.
 First the parser will be used to split up words in syllables
 Then the correct sounds for every syllable should be linked
 After that add an artificial voice to pronounce the words.

 Eventually there will be need for a word list of some sort, as there is no way to know if the syllable 'be' should be pronounced as 'bay' for 'bezem' or  'buh' for 'bezet.

## Requirements

F or the pronunciation you need to install the [playsound](https://pypi.org/project/playsound/) library:
Can be done with the command `pip install playsound`

## How to Use

### Splitting words in syllables

You can easily interact with the tool via the Console, with the command `split` you can get a word split up via the way explained above.

``` powershell
$WORD= lopen # any word you want to input
C:\...\DutchParsing>python Console.py split $WORD
lo-pen
```

### Getting the pronunciation of a word

You can input a word together with the command `phonetic` to the console script and it will give a phonetic translation of the word using this program's system,
for info about the pronunciation of each symbol see the PhoneticSystem file:

``` powershell
$WORD= lopen # any word you want to input
C:\...\DutchParsing>python Console.py phonetic $WORD
lóp0n
```

### Finding Rhyme words for a word

You can find all the words that rhyme with a certain words. You can either find words that rhyme fully or words that only have the same vowels. If no rhyme type is specified it does full rhyme by default. Use the following command:

``` powershell
$WORD= lopen # any word you want to input
$TYPE= full # should be either 'full' or 'vowels'
C:\...\DutchParsing>python Console.py rhyme -t $TYPE $WORD
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

You can test the tool by running the `test` command which will run a bunch of tests on the splitting to see if they still work correctly.

``` powershell
C:\...\DutchParsing>python Console.py test
***.***.*** All Tests Successful ***.***.***
```

You can analyze a file or a piece of text with the `analyze` command, it will tell you some info about the piece of text.

``` powershell
C:\...\DutchParsing>python Console.py analyze "een lekker stukkie tekst om te lezen."
there were a total of 10 unique syllables in the text, of 7 words and 10 total syllables.
there were a total of 31 letters.
the 10 most common syllables were {'een': 1, 'lek': 1, 'ker': 1, 'stuk': 1, 'kie': 1, 'tekst': 1, 'om': 1, 'te': 1, 'le': 1, 'zen': 1}
the 10 most common letters were {'e': 9, 'k': 5, 't': 4, 'n': 2, 'l': 2, 's': 2, 'r': 1, 'u': 1, 'i': 1, 'o': 1}
```

``` powershell
C:\...\DutchParsing>python Console.py analyze-file TextFiles/Het-Boek.txt
there were a total of 4859 unique syllables in the text, of 761332 words.
the 10 most common syllables were {'de': 65405, '': 33432, 'en': 31476, 'ge': 22602, 'van': 21798, 'te': 19022, 'den': 17583, 'het': 15858, 'ver': 15036, 'u': 14538}
```

You can also do multiple inputs by enclosing the inputs with double quotation marks.
