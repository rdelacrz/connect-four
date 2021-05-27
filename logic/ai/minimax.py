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

    def minimax(self, game_node: ConnectFourGame, search_depth: int, alpha: int, beta: int):
        """
        Implements the Minimax algorithm with alpha-beta pruning to improve performance.

        :param `game_node`: Contains state of the game at the time of some move.
        :param `search_depth`: The maximum depth at which the algorithm will be run in order to evaluate 
        the heuristic values of the AI player's possible moves.
        :param `alpha`: Represents the minimum score that the maximizing player is assured of.
        :param `beta`: Represents the maximum score that the minimizing player is assured of.

        :return: Final heuristic value resulting from current state of the game node.
        """

        # Returns heuristic value when game reaches a terminal state
        if search_depth == 0 or game_node.winner_id is not None or game_node.grid.is_grid_full():
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
                    value = max(value, self.minimax(child_node, search_depth - 1, alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break   # Beta cutoff
                else:
                    value = min(value, self.minimax(child_node, search_depth - 1, alpha, beta))
                    beta = min(beta, value)
                    if beta <= alpha:
                        break   # Alpha cutoff

        return value

    def heuristic_function(self, game_node: ConnectFourGame):
        if game_node.winner_id is None:
            # Evaluates results of most recent move
            checked_space = game_node.grid.most_recently_modified_space
            if checked_space is not None:
                # Evaluates whether any player has 3 discs in a row
                player_id = game_node.check_for_discs_in_row(checked_space.y, checked_space.x, 3)
                if player_id is not None:
                    return inf if player_id == self.ai_player_id else -inf

                # Evaluates disc placements on sides and top edges of grid (which are bad positions)
                edge_eval = 0
                if checked_space.x == 0 or checked_space.x == game_node.grid.width - 1:
                    edge_eval += -150 if checked_space.disc.player_id == self.ai_player_id else 150
                if checked_space.y == game_node.grid.height - 1:
                    edge_eval += -300 if checked_space.disc.player_id == self.ai_player_id else 300
                if edge_eval != 0:
                    return edge_eval

            return 0
        elif game_node.winner_id == self.ai_player_id:
            return inf      # Means AI player has won
        else:
            return -inf     # Means AI player has lost

    @js_callback
    def get_optimal_col(self, search_depth = 4):
        # Evaluates every available move using minimax
        col_value_pair = []
        for col_num, available_row in enumerate(self.game.grid.available_col_spaces):
            if available_row is not None:
                # Tests move as if disc was actually dropped in the current column
                child_node = deepcopy(self.game)
                child_node.drop_disc(col_num)
                value = self.minimax(child_node, search_depth, -inf, inf)
                col_value_pair.append((col_num, value))
        
        if len(col_value_pair) > 0:
            col_num, _ = max(col_value_pair, key=lambda x: x[1])
            return col_num

        return None