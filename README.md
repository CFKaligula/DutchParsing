# DutchParsing
 A Python Implementation for correctly parsing Dutch words

 The idea of this parser it to make use of rules as much as possible and to not use word lists to parse Dutch sentences and words.
 First the parser will be used to split up words in syllables
 Then the correct sounds for every syllable should be shown
 After that add an artifical voice to pronounce the words.

 The parser currently parses from right to left, I have no idea if this is better than left to right but it works pretty well for now.

 Eventually there will be need for a word list of some sort, as there is no way to know if the syllable 'be' should be pronounced as 'bay' for 'bezem' or  'buh' for 'bezet.
