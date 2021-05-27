"""
Contains the basic class for a Connect Four AI, which is to be extended and implemented by the various different AI
types that make use of its functions.
"""

from ..core.game import ConnectFourGame
from ..utilities import js_callback

class ConnectFourAI:
    """
    Class for Connect Four AI.
    """

    def __init__(self, ai_player_id: int, game: ConnectFourGame, ai_type: str):
        self.ai_player_id = ai_player_id
        self.game = game
        self.ai_type = ai_type

    @js_callback
    def get_ai_id(self):
        return self.ai_player_id

    def heuristic_function(self, game_node: ConnectFourGame):
        """
        The heuristic function applied to a game node to assign a ranking for how optimal the grid's state is
        for the current AI player.

        :param `game_node`: Node containing an instance of the current game state after a move was performed.

        :return: Integer representing the optimality of a grid's state for the AI player.
        """

        raise NotImplementedError("This function must be implemented by AI.")

    def get_optimal_col(self, search_depth = 4):
        """
        Gets the number of the column that is most optimal for the AI player to drop a disc in.

        :param `search_depth`: The maximum depth at which the algorithm will be run in order to evaluate 
        the heuristic values of the AI player's possible moves and get the optimal column number based on the
        highest value.

        :return: Number of the column that is most optimal for the AI player to drop a disc in.
        """

        raise NotImplementedError("This function must be implemented by AI.")
