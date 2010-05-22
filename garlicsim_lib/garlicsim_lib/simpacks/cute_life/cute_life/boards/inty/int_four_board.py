from garlicsim.general_misc import binary_tools

def _coords_to_cell_number(x, y):
    
    a, b = divmod(x, 2)
    c, d = divmod(y, 2)
    
    big_exponent = a + 2 * c
    small_exponent = b + 2 * d
    
    exponent = small_exponent + 4 * big_exponent

    return 2 ** exponent 
    
    # tododoc optimization: can bundle these to few lines

    
def get(int_four_board, x, y):
    return bool(int_four_board & _coords_to_cell_number(x, y))



def get_with_cell_change_to_true(int_four_board, x, y):
    return int_four_board | _coords_to_cell_number(x, y)



def get_with_cell_change_to_false(int_four_board, x, y):
    return int_four_board & ~_coords_to_cell_number(x, y)



def get_with_cell_toggle(int_four_board, x, y):
    return int_four_board ^ _coords_to_cell_number(x, y)


def get_next_sub_int_two_board(int_four_board):

    int_two_board = 0
    
    n_neighbours_of_nw = binary_tools.bit_count(4951 & int_four_board)
    if n_neighbours_of_nw == 3:
        int_two_board += 1
    elif n_neighbours_of_nw == 2:
        if 8 & int_four_board:
            int_two_board += 1
            
    n_neighbours_of_ne = binary_tools.bit_count(12986 & int_four_board)
    if n_neighbours_of_ne == 3:
        int_two_board += 2
    elif n_neighbours_of_ne == 2:
        if 64 & int_four_board:
            int_two_board += 2
            
    n_neighbours_of_sw = binary_tools.bit_count(23884 & int_four_board)
    if n_neighbours_of_sw == 3:
        int_two_board += 4
    elif n_neighbours_of_sw == 2:
        if 512 & int_four_board:
            int_two_board += 4
            
    n_neighbours_of_se = binary_tools.bit_count(60104 & int_four_board)
    if n_neighbours_of_se == 3:
        int_two_board += 8
    elif n_neighbours_of_se == 2:
        if 4096 & int_four_board:
            int_two_board += 8
            
    return int_two_board
     

            
def to_string(int_four_board):
    return '\n'.join(
        ''.join(
            ('#' if get(int_four_board, x, y) else ' ')
            for x in xrange(0, 4)
        )
        for y in xrange(0, 4)
    )

def combine_int_two_boards_to_int_four_board(nw, ne, sw, se):
    return nw + (ne << 4) + (sw << 8) + (se << 12)
    
def combine_four(nw, ne, sw, se):
    return (nw >> 12) + \
           ((ne & 3840) >> 4) + \
           ((sw & 240) << 4) + \
           ((se & 15) << 12)

def combine_two_horizontally(w, e):
    return ((w & 61680) >> 4) + \
           ((e & 3855) << 4)

def combine_two_vertically(n, s):
    return ((n & 65280) >> 8) + \
           ((s & 255) << 8)
           

def get_cells_tuple(int_four_board, value=True):
    coords_list = []
    for x in xrange(4):
        for y in xrange(4):
            if get(int_four_board, x, y) is value:
                coords_list.append((x, y))
    return tuple(coords_list)
                


###############################################################################


def make_nw_piece_for_nw_bloated_kid(int_four_board):
    return ((int_four_board & 34952) >> 3) + \
           ((int_four_board & 16448 ) >> 5) + \
           ((int_four_board & 8704) >> 7) + \
           ((int_four_board & 4096) >> 9)

def make_ne_piece_for_nw_bloated_kid(int_four_board):
    return ((int_four_board & 1028) << 3) + \
           ((int_four_board & 256) >> 1)

def make_sw_piece_for_nw_bloated_kid(int_four_board):
    return ((int_four_board & 34) << 9) + \
           ((int_four_board & 16) << 7)

def make_se_piece_for_nw_bloated_kid(int_four_board):
    return ((int_four_board & 1) << 15)



def make_nw_piece_for_ne_bloated_kid(int_four_board):
    return ((int_four_board & 32896) >> 7) + \
           ((int_four_board & 8192) >> 11)

def make_ne_piece_for_ne_bloated_kid(int_four_board):
    return ((int_four_board & 17476) >> 1) + \
           ((int_four_board & 2056) << 1) + \
           ((int_four_board & 4352) >> 5) + \
           ((int_four_board & 512) >> 3)

def make_sw_piece_for_ne_bloated_kid(int_four_board):
    return ((int_four_board & 32) >> 5)

def make_se_piece_for_ne_bloated_kid(int_four_board):
    return ((int_four_board & 17) << 11) + \
           ((int_four_board & 2) << 13)



def make_nw_piece_for_sw_bloated_kid(int_four_board):
    return ((int_four_board & 34816) >> 11) + \
           ((int_four_board & 16384) >> 13)

def make_ne_piece_for_sw_bloated_kid(int_four_board):
    return ((int_four_board & 1024) >> 5)

def make_sw_piece_for_sw_bloated_kid(int_four_board):
    return ((int_four_board & 8738) << 1) + \
           ((int_four_board & 4112) >> 1) + \
           ((int_four_board & 136) << 5) + \
           ((int_four_board & 64) << 3)

def make_se_piece_for_sw_bloated_kid(int_four_board):
    return ((int_four_board & 257) << 7) + \
           ((int_four_board & 4) << 11)



def make_nw_piece_for_se_bloated_kid(int_four_board):
    return ((int_four_board & 32768) >> 15)

def make_ne_piece_for_se_bloated_kid(int_four_board):
    return ((int_four_board & 17408) >> 9) + \
           ((int_four_board & 2048) >> 7)

def make_sw_piece_for_se_bloated_kid(int_four_board):
    return ((int_four_board & 8224) >> 3) + \
           ((int_four_board & 128) << 1)

def make_se_piece_for_se_bloated_kid(int_four_board):
    return ((int_four_board & 4369) << 3) + \
           ((int_four_board & 514) << 5) + \
           ((int_four_board & 68) << 7) + \
           ((int_four_board & 8) << 9)

###############################################################################