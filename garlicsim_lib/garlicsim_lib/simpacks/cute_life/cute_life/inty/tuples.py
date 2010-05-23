import int_four_board


live_cells_tuple = tuple(
    int_four_board.get_cells_tuple(my_int_four_board, True)
    for my_int_four_board in xrange(0, 65536)
) # tododoc optimization: should really optimize these


#dead_cells_tuple = tuple(
    #int_four_board.get_cells_tuple(my_int_four_board, False)
    #for my_int_four_board in xrange(0, 65536)
#)
