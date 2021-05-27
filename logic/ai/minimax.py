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

    def _get_game_node_children(self, game_node: ConnectFourGame):
        """
        Gets the resulting states of every available move from the current game node, alongside the column
        numbers associated with the moves that created these states.

        :param `game_node`: Contains the current state of the game.

        :return: List of tuples (col_num, child_node), where col_num is the column number associated with a
        move, while the child_node is the resulting game state of that move.
        """

        children = []
        for col_num, available_row in enumerate(game_node.grid.available_col_spaces):
            if available_row is not None:
                child_node = deepcopy(game_node)
                child_node.drop_disc(col_num)
                children.append((col_num, child_node))

        return children

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

        # Maximizing player will want to maximize values, minimizing player will want to do the opposite
        if maximizing_player:
            value = -inf
            for _, child_node in self._get_game_node_children(game_node):
                value = max(value, self.minimax(child_node, search_depth - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break   # Beta cutoff
        else:
            value = inf
            for _, child_node in self._get_game_node_children(game_node):
                value = min(value, self.minimax(child_node, search_depth - 1, alpha, beta))
                beta = min(beta, value)
                if beta <= alpha:
                    break   # Alpha cutoff

        return value

    def _determine_near_four_in_a_rows(self, game_node: ConnectFourGame):
        player_four_in_a_rows = {}

        # Checks each column for empty spaces that are one disc away from a 4 in a row
        for col, available_row in enumerate(game_node.grid.available_col_spaces):
            if available_row is not None:
                for row in range(available_row, self.game.grid.height):
                    # Short circuits if empty space has no nearby discs; checks next column afterwards
                    left_side_empty = col == 0 \
                        or (available_row == 0 and game_node.grid.grid_spaces[col - 1][available_row].disc is None) \
                        or (available_row > 0 and game_node.grid.grid_spaces[col - 1][available_row - 1].disc is None)
                    right_side_empty = col == game_node.grid.width - 1 \
                        or (available_row == 0 and game_node.grid.grid_spaces[col + 1][available_row].disc is None) \
                        or (available_row > 0 and game_node.grid.grid_spaces[col + 1][available_row - 1].disc is None)
                    if left_side_empty and right_side_empty:
                        break

                    # Tests empty space for each player
                    for test_player_id in [player.id for player in game_node.players]:
                        player_id = game_node.check_for_discs_in_row(row, col, 4, test_player_id)
                        if player_id is not None:
                            count = player_four_in_a_rows.get(player_id, 0)
                            player_four_in_a_rows[player_id] = count + 1

        return player_four_in_a_rows

    def heuristic_function(self, game_node: ConnectFourGame):
        if game_node.winner_id is None:
            # Evaluates results of most recent move
            checked_space = game_node.grid.most_recently_modified_space
            if checked_space is not None:
                # Evaluates empty spaces for any player that is one disc away from 4 in a row
                player_four_in_a_rows = self._determine_near_four_in_a_rows(game_node)
                ai_count = player_four_in_a_rows.get(self.ai_player_id, 0)
                other_player_count = sum([
                    player_four_in_a_rows[player_id]
                    for player_id in filter(lambda player_id: player_id != self.ai_player_id, player_four_in_a_rows)
                ])
                return (ai_count - other_player_count) * 20

            return 0
        elif game_node.winner_id == self.ai_player_id:
            return inf      # Means AI player has won
        else:
            return -inf     # Means AI player has lost

    @js_callback
    def get_optimal_col(self, search_depth = 4):
        col_value_pair = []

        # Evaluates every available move using minimax
        for col_num, child_node in self._get_game_node_children(self.game):
            value = self.minimax(child_node, search_depth, -inf, inf)
            col_value_pair.append((col_num, value))
        
        if len(col_value_pair) > 0:
            col_num, _ = max(col_value_pair, key=lambda x: x[1])
            return col_num

        return None