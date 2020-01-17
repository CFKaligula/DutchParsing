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

You can input a word (or multiple) to the console script and it will split it up in syllables for you:

``` bash
C:\...\DutchParsing>python Console.py voorbeeld
```

## Copying

Be free to copy any of the code here, it is just a fun project.
