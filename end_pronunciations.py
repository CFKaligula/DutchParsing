
def find_end_n_pronunciation(syllable, i):
    end_con_sound = ''
    if i+1 <= len(syllable.end_cons)-1 and syllable.end_cons[i+1] == 'g':
        end_con_sound += 'µ'
    elif syllable.next_syl is not None and syllable.next_syl.start_cons[0] == 'j':
        end_con_sound += 'ñ'
    else:
        end_con_sound += 'n'
    return end_con_sound


def find_end_g_pronunciation(syllable, i):
    end_con_sound = ''
    if i > 0 and syllable.end_cons[i-1] == 'n':
        # ng is already processed with the n
        pass
    else:
        # voiceless g at the end
        end_con_sound += 'æ'
    return end_con_sound


def find_end_c_pronunciation(syllable, i):
    end_con_sound = ''
    if i < len(syllable.end_cons)-1 and syllable.end_cons[i+1] == 'h':
        # ch, should not appear at the start but just in case
        end_con_sound += 'g'
    else:
        # lac? not sure if always k
        end_con_sound += 'k'

    return end_con_sound


def find_end_h_pronunciation(syllable, i):
    end_con_sound = ''
    if i > 0 and syllable.end_cons[i-1] == 'c':
         # ch
        pass
    else:
        end_con_sound += 'h'
    return end_con_sound