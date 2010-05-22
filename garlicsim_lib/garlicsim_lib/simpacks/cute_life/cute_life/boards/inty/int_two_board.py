def combine_four_to_int_four_board(nw, ne, sw, se):
    return nw + (ne << 4) + (sw << 8) + (se << 12)
