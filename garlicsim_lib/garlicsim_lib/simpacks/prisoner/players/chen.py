# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from ..base_player import BasePlayer


class Chen(BasePlayer):
    
    color = 'Brown'
    
    def make_move(self, round):
        from ..players import *
        if round == 0:
            self.last_play = None
            self.play_on_second_round = None
            self.other_player_type = None
            return False
        elif round == 1:
            self.play_on_second_round = self.last_play
            return True
        elif round == 2:
            if self.play_on_second_round is True:
                if self.last_play is True:
                    self.other_player_type = Angel
                if self.last_play is False:
                    self.other_player_type = TitForTat
            else: # self.play_on_second_round is False
                if self.last_play is True:
                    self.other_player_type = Chen
                if self.last_play is False:
                    self.other_player_type = Devil
        
        if self.other_player_type is Angel:
            return False
        elif self.other_player_type is TitForTat:
            return False
        elif self.other_player_type is Devil:
            return False
        else:
            assert self.other_player_type is Chen
            return True
        

    def other_player_played(self, move):
        self.last_play = move
        

