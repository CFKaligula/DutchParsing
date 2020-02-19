def find_start_c_pronunciation(syllable, i):
    start_con_sound = ''
    if i > 0 and syllable.start_cons[i-1] == 's':
        # scepter
        pass
    elif i < len(syllable.start_cons)-1 and syllable.start_cons[i+1] == 'h':
        # ch, should not appear at the start but just in case
        start_con_sound += 'g'
    elif i < len(syllable.start_cons)-1 \
            or len(syllable.vowels) > 0 and (syllable.vowels[0] in {'a', 'o', 'u'} or syllable.start_cons + syllable.vowels[0] == 'sce'):
        # casus
        start_con_sound += 'k'
    else:
        # citrus
        start_con_sound += 's'

    return start_con_sound


def find_start_h_pronunciation(syllable, i):
    start_con_sound = ''
    if i > 0 and syllable.start_cons[i-1] == 'c':
         # ch
        pass
    else:
        start_con_sound += 'h'
    return start_con_sound


def find_start_j_pronunciation(syllable, i):
    start_con_sound = ''
    if syllable.prev_syl.end_cons != '' and syllable.prev_syl.end_cons[-1] == 'n':
         # nj as in oranje, already handled with the n
        pass
    else:
        start_con_sound += 'j'
    return start_con_sound


def find_start_s_pronunciation(syllable, i):
    start_con_sound = ''
    if i < len(syllable.start_cons)-1 and syllable.start_cons[i+1] == 'c' \
            and i < len(syllable.start_cons)-2 and syllable.start_cons[i+2] == 'h':
        if syllable.vowels + syllable.end_cons == 'e' and syllable.next_syl is None:
            # word ending on sche like logische
            start_con_sound += 's'
        else:
            # scheen
            start_con_sound += 'sg'
    else:
        start_con_sound += 's'
    return start_con_sound


def find_start_q_pronunciation(syllable, i):
    start_con_sound = ''
    if syllable.vowels != '' and syllable.vowels[0] == 'u':
        # qua = kwa
        start_con_sound += 'kw'
    else:
        start_con_sound += 'k'
    return start_con_sound