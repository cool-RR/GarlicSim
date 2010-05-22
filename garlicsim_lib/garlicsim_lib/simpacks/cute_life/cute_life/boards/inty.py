
def _bit_count(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    # return ((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
    return (((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) & 0xffffffff) >> 24

def _int_four_board_coords_to_cell_number(x, y):
    
    a, b = divmod(x, 2)
    c, d = divmod(y, 2)
    
    big_exponent = a + 2 * c
    small_exponent = b + 2 * d
    
    exponent = small_exponent + 4 * big_exponent

    return 2 ** exponent 
    
    
    # tododoc optimization: can bundle these to few lines

    
def int_four_board_get(int_four_board, x, y):
    
    return bool(int_four_board & _coords_to_cell_number(x, y))



def int_four_board_get_with_cell_change_to_true(int_four_board, x, y):
    
    return int_four_board | _coords_to_cell_number(x, y)



def int_four_board_get_with_cell_change_to_false(int_four_board, x, y):
    
    return int_four_board & ~_coords_to_cell_number(x, y)



def int_four_board_get_with_cell_toggle(int_four_board, x, y):
    
    return int_four_board ^ _coords_to_cell_number(x, y)


def int_four_board_get_next_sub_int_two_board(int_four_board):

    int_two_board = 0
    
    n_neighbours_of_nw = _bit_count(4951 & int_four_board)
    if n_neighbours_of_nw == 3:
        int_two_board += 1
    elif n_neighbours_of_nw == 2:
        if 8 & int_four_board:
            int_two_board += 1
            
    n_neighbours_of_ne = _bit_count(9902 & int_four_board)
    if n_neighbours_of_ne == 3:
        int_two_board += 2
    elif n_neighbours_of_ne == 2:
        if 64 & int_four_board:
            int_two_board += 2
            
    n_neighbours_of_sw = _bit_count(23884 & int_four_board)
    if n_neighbours_of_sw == 3:
        int_two_board += 4
    elif n_neighbours_of_sw == 2:
        if 512 & int_four_board:
            int_two_board += 4
            
    n_neighbours_of_se = _bit_count(47768 & int_four_board)
    if n_neighbours_of_se == 3:
        int_two_board += 8
    elif n_neighbours_of_se == 2:
        if 4096 & int_four_board:
            int_two_board += 8
            
    return int_two_board
     

            
def int_four_board_to_string(int_four_board):
    return '\n'.join(''.join(('#' if get(int_four_board, x, y) else ' ') for x in xrange(0, 4))
                     for y in xrange(0, 4))

def combine_int_two_boards_to_int_four_boards(nw, ne, sw, se):
    return nw + (ne << 4) + (sw << 8) + (se << 12)
    

import array

a=array.array(
    'b',
    (
        int_four_board_get_next_sub_int_two_board(int_four_board)
        for int_four_board in xrange(0, 65536)
    )
)