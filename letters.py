
CONSONANTS = {'b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'j',
              'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
# y should be included for names like jordy, don't know yet if j has to be included for DIPTHONGS
VOWELS = {'a', 'e', 'i', 'o', 'u'}
DIPTHONGS = {'au', 'ou', 'ei', 'ij', 'oe',
             'ui',  'aa', 'ee', 'ie', 'oo', 'uu', 'oi'}
TRIPTHONGS = {'oei', 'eau', 'eeu', 'ooi', 'aai', 'oeu'}
BREAK_SYMBOL = '-'
VALID_CONSONANT_COMBINATIONS = {'',
                                'bl', 'br',
                                'cl', 'cr',
                                'dr', 'dl', 'dr',
                                'fl', 'fj' 'fr',
                                'gr', 'gl', 'gr',
                                # h
                                'kl', 'kn', 'kr',
                                # l
                                # j
                                # m
                                # n
                                'p', 'pl', 'pr',
                                # q
                                # r
                                'sh', 'sk', 'sl', 'sj', 'sm', 'sn', 'sp', 'sr', 'st', 'sw', 'sch', 'schr', 'schl', 'str',
                                'th', 'tr',
                                'vl', 'vr',
                                'wr',
                                # x
                                # y
                                'z', 'zw'
                                }
