"""
Contains logic for an AI player to perform minimax strategies.
"""

# Built-in modules
from copy import deepcopy
from math import inf

# User-defined modules
from ..core.game import ConnectFourGame
from .interface import ConnectFourAI
from ..utilities import js_callback

class MinimaxAI(ConnectFourAI):
    """
    AI that uses the Minimax strategy to play Connect Four. Its goal is to minimize the possible loss for a worst-case scenario.
    In other words, minimizing the maximum loss.
    """

    def __init__(self, ai_player_id: int, game: ConnectFourGame):
        super().__init__(ai_player_id, game, "Minimax AI")

    def minimax(self, game_node: ConnectFourGame, search_depth: int):
        if search_depth == 0 or game_node.grid.is_grid_full():
            return self.heuristic_function(game_node)

        # AI player wants to maximize gains while opponent wants to minimize it
        maximizing_player = game_node.current_player == self.ai_player_id
        value = -inf if maximizing_player else inf

        # Determines possible moves in current state
        for col_num, available_row in enumerate(game_node.grid.available_col_spaces):
            if available_row is not None:
                child_node = deepcopy(game_node)
                child_node.drop_disc(col_num)

                # Maximizing player will want to maximize values, minimizing player will want to do the opposite
                if maximizing_player:
                    value = max(value, self.minimax(child_node, search_depth - 1))
                else:
                    value = min(value, self.minimax(child_node, search_depth - 1))

        return value

    def heuristic_function(self, game_node: ConnectFourGame):
        if game_node.winner_id is None:
            return 0
        elif game_node.winner_id == self.ai_player_id:
            return inf      # Means AI player has won
        else:
            return -inf     # Means AI player has lost

    @js_callback
    def get_optimal_col(self, search_depth = 4):
        optimal_col = None
        optimal_value = None

        # Evaluates every available move using minimax
        for col_num, available_row in enumerate(self.game.grid.available_col_spaces):
            if available_row is not None:
                # Tests move as if disc was actually dropped in the current column
                child_node = deepcopy(self.game)
                child_node.drop_disc(col_num)

                if optimal_col is None:
                    optimal_col = col_num
                    optimal_value = self.minimax(child_node, search_depth)
                else:
                    value = self.minimax(child_node, search_depth)

                    # Determines whether current column represents the optimal move
                    if value > optimal_value:
                        optimal_col = col_num
                        optimal_value = value

        return optimal_col