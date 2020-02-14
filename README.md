# DutchParsing

 A Python Implementation for correctly parsing Dutch words.

## Introductions

 The idea of this parser it to make use of rules as much as possible and to not use word lists.
 First the parser will be used to split up words in syllables
 Then the correct sounds for every syllable should be linked
 After that add an artificial voice to pronounce the words.

 Eventually there will be need for a word list of some sort, as there is no way to know if the syllable 'be' should be pronounced as 'bay' for 'bezem' or  'buh' for 'bezet.

## To-do

For English loanwords, y should be a vowel if there are already starting consonants

## How to Use

You can easily interact with the tool via the Console, with the command `split` you can get a word split up via the way explained above.

``` bash
$WORD= lopen # any word you want to input
C:\...\DutchParsing>python Console.py split $WORD
lo-pen
```

You can input a word together with the command `phonetic` to the console script and it will give a phonetic translation of the word using this program's system,
for info about the pronunciation of each symbol see the PhoneticSystem file:

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

You can also do multiple inputs by enclosing the inputs with double quotation marks.

## Copying

Be free to copy any of the code here, it is just a fun project.
