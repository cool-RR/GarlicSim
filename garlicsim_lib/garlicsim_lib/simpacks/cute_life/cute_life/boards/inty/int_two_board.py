def combine_int_two_boards_to_int_four_boards(nw, ne, sw, se):
    return nw + (ne << 4) + (sw << 8) + (se << 12)
