"""
Contains logic for an AI player to perform minimax strategies.
"""

# Built-in modules
from copy import deepcopy
from math import ceil, floor, inf

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

    def _determine_near_x_in_a_rows(self, game_node: ConnectFourGame, disc_number_in_row = 4):
        player_four_in_a_rows = {}

        # Checks each column for empty spaces that are one disc away from the given number of discs in a row
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
                        player_id = game_node.check_for_discs_in_row(row, col, disc_number_in_row, test_player_id)
                        if player_id is not None:
                            count = player_four_in_a_rows.get(player_id, 0)
                            player_four_in_a_rows[player_id] = count + 1

        return player_four_in_a_rows

    def heuristic_function(self, game_node: ConnectFourGame, search_depth: int):
        """
        The heuristic function applied to a game node to assign a ranking for how optimal the grid's state is
        for the current AI player.

        :param `game_node`: Node containing an instance of the current game state after a move was performed.

        :return: Integer representing the optimality of a grid's state for the AI player.
        """

        # Victory or defeat with a higher depth value is more desirable, because it means less moves are used to reach it
        depth_points = 2520 / (10 - search_depth)

        if game_node.winner_id is None:
            # Evaluates empty spaces for any player that is one disc away from a victory
            player_four_in_a_rows = self._determine_near_x_in_a_rows(game_node, game_node.victory_condition)
            ai_count = player_four_in_a_rows.get(self.ai_player_id, 0)
            other_player_count = sum([
                player_four_in_a_rows[player_id]
                for player_id in filter(lambda player_id: player_id != self.ai_player_id, player_four_in_a_rows)
            ])
            if ai_count - other_player_count != 0:
                return (ai_count - other_player_count) * 20

            # Evaluates grid positioning, granting bonus points for discs closer to the center of the grid
            max_deviation = floor(game_node.grid.width / 4.0)
            mid = ceil(game_node.grid.width / 2.0)
            ai_count = 0
            other_player_count = 0
            for col in range(mid - max_deviation, mid + max_deviation):
                for row in range(0, game_node.grid.height):
                    curr_space = game_node.grid.grid_spaces[col][row]
                    if curr_space.disc is None:
                        break   # Short-circuits when empty space in a column is reached
                    elif curr_space.disc.player_id == self.ai_player_id:
                        ai_count += 1
                    else:
                        other_player_count += 1
            if ai_count - other_player_count != 0:
                return (ai_count - other_player_count) * 2

            return 0
        elif game_node.winner_id == self.ai_player_id:
            return self.winner_heuristic_value + depth_points      # Means AI player has won
        else:
            return -self.winner_heuristic_value - depth_points     # Means AI player has lost

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
            return self.heuristic_function(game_node, search_depth)

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