
consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'j',
              'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
# y should be included for names like jordy, don't know yet if j has to be included for dipthongs
vowels = {'a', 'e', 'i', 'o', 'u'}
dipthongs = {'au', 'ou', 'ei', 'ij', 'oe',
             'ui',  'aa', 'ee', 'ie', 'oo', 'uu', 'oi'}
tripthongs = {'oei', 'eau', 'eeu', 'ooi', 'aai', 'oeu'}
# can only be at the start of words, e.g. auto, never blau, aarde, never laa etc.
start_dipthongs = {'au', 'aa', 'ee', 'oo', 'uu', }
# can only be first group of vowels, e.g. bloei-en, niveau-ijs
end_tripthongs = {'oei', 'eau', 'eeu', 'ooi', 'aai'}
# can only be last group of vowels e.g. oeuvre
start_tripthongs = {'oeu'}
break_symbol = '-'
consonant_combinations = {'',
                          'b', 'bl', 'br',
                          'c', 'cl', 'cr',
                          'd', 'dr', 'dl', 'dr',
                          'f', 'fl', 'fj' 'fr',
                          'g', 'gr', 'gl', 'gr',
                          'h',
                          'k', 'kl', 'kn', 'kr',
                          'l',
                          'j',
                          'm',
                          'n',
                          'p', 'pl', 'pr',
                          'q',
                          'r',
                          's', 'sh', 'sk', 'sl', 'sj', 'sm', 'sn', 'sp', 'sr', 'st', 'sw', 'sch', 'schr', 'schl',
                          't', 'th', 'tr',
                          'v', 'vl', 'vr',
                          'w', 'wr',
                          'x',
                          'y',
                          'z'
                          }
