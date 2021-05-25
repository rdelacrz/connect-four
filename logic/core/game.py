"""
Contains the logic needed to run a game of Connect Four.
"""

# Third-party modules
from cefpython3 import cefpython as cef

# User-defined modules
from .components import ConnectFourGrid, Disc
from .exceptions import IllegalAction, IllegalState, InvalidSpace

DISC_COLORS = [
    '#F5473E',  # red
    '#FEEC49',  # yellow
    '#048B44',  # green
    '#293777',  # blue
]

def js_callback(func):
    """
    Takes the return value of the function being wrapped and passes it through the callback function (if any).
    It is meant for JavaScript callback purposes, which cannot return a value because inter-process messaging 
    is asynchronous.
    """

    def wrapper(*args):
        # Grabs callback function from positional arguments (if one is provided)
        callback_fn = None
        func_args = args
        if type(args[-1]) is cef.JavascriptCallback:
            callback_fn = args[-1]
            func_args = args[:-1]

        # Passes return value from function accordingly (depending on whether a callback function is passed or not)
        ret = func(*func_args)
        if callback_fn is not None:
            callback_fn.Call(ret)
        else:
            return ret

    return wrapper
 
class Player:
    def __init__(self, player_id: int, name: str):
        self.id = player_id
        self.name = name

    @property
    def state(self):
        return { 'id' : self.id, 'name' : self.name }

class ConnectFourGame:
    """
    Encapsulates logic for setting up the initial parameters of a Connect Four game and establishing its rules.
    """

    def __init__(self, player_names:'list[str]'=['Player One', 'Player Two'], width=7, height=6, victory_condition=4):
        """
        Sets up a game of Connect Four.

        :param `player_names`: List of the names of the players participating in this game.
        :param `width`: Width of the grid.
        :param `height`: Height of the grid.
        :param `victory_condition`: Number of discs that need to line up horizontally, 
        vertically, or diagonally on the grid for a single player to win the game.
        """

        # Checks for valid number of players
        if len(player_names) < 2:
            raise IllegalState('Game cannot be setup without at least two players.')
        elif len(player_names) > len(DISC_COLORS):
            raise IllegalState('Game cannot be setup with more than {0} players.'.format(len(DISC_COLORS)))

        self.players = [Player(index, name) for index, name in enumerate(player_names)]
        self.current_player = 0     # Starts with first player
        self.discs = [Disc(player.id, DISC_COLORS[index]) for index, player in enumerate(self.players)]
        self.grid = ConnectFourGrid(width, height)
        self.victory_condition = victory_condition
        self.winner_id = None

    def __repr__(self):
        """
        Produces visual representation of the Connect Four grid (from top to bottom), displaying _ for empty spaces,
        and player ids wherever a player's disc is inserted. It will also show the id of the player who is next to move.

        :return: String representing state of the Connect Four grid.
        """

        board_repr = str(self.grid)
        board_repr += '-------------------------\n'
        board_repr += 'Next Player: {0}'.format(self.players[self.current_player].name)
        return board_repr

    @js_callback
    def get_state(self):
        state = {
            'players' : [player.state for player in self.players],
            'current_player' : self.current_player,
            'discs' : [disc.state for disc in self.discs],
            'grid' : self.grid.state,
            'victory_condition' : self.victory_condition,
            'winner_id' : self.winner_id
        }
        return state

    def _get_player_chain(self, player_id: int, start_row: int, start_col: int, row_inc: int, col_inc: int):
        """
        Gets a list of discs that belong to the given player, starting from the given start row and column,
        continuing into a given direction based on the given row and column increments, and ending once either a disc
        belonging to a different player is reached or the edge of the grid is reached.

        :param `player_id`: Player id whose discs are being checked for.
        :param `start_row`: Starting row to check for discs.
        :param `start_col`: Starting column to check for discs.
        :param `row_inc`: Increments the row after every check is made for a disc.
        :param `col_inc`: Increments the column after every check is made for a disc.

        :return: A list of discs belonging to the given player, within a direction determined by the row and column
        increments.
        """

        chain = []

        row = start_row
        col = start_col

        while row >= 0 and row < self.grid.height and col >= 0 and col < self.grid.width:
            disc = self.grid.grid_spaces[col][row].disc
            if disc is not None and disc.player_id == player_id:
                chain.append(self.grid.grid_spaces[col][row].disc)
                row += row_inc
                col += col_inc
            else:
                break

        return chain

    @js_callback
    def check_for_victory(self, row: int, col: int):
        """
        Checks for a line of horizontal, vertical, or diagonal discs that meet the victory condition for
        a single player.

        :param `row`: Starting row to check for victory from.
        :param `col`: Starting column to check for victory from.

        :return: Player id meeting victory condition, or None if victory condition is not met.
        """

        if row < 0 or row > self.grid.height or col < 0 or col > self.grid.width:
            raise InvalidSpace("Attempted to check a space that doesn't exist on the grid!")

        player_id = self.grid.grid_spaces[col][row].disc.player_id

        # Checks for vertical line of discs
        upper = self._get_player_chain(player_id, row + 1, col, 1, 0)
        lower = self._get_player_chain(player_id, row - 1, col, -1, 0)
        if len(upper) + len(lower) + 1 >= self.victory_condition:
            self.winner_id = player_id
            return self.winner_id
        
        # Checks for horizontal line of discs
        left = self._get_player_chain(player_id, row, col - 1, 0, -1)
        right = self._get_player_chain(player_id, row, col + 1, 0, 1)
        if len(left) + len(right) + 1 >= self.victory_condition:
            self.winner_id = player_id
            return self.winner_id

        # Checks for downward-right diagonal line of discs
        upper_left = self._get_player_chain(player_id, row + 1, col - 1, 1, -1)
        lower_right = self._get_player_chain(player_id, row - 1, col + 1, -1, 1)
        if len(upper_left) + len(lower_right) + 1 >= self.victory_condition:
            self.winner_id = player_id
            return self.winner_id

        # Checks for upward-right diagonal line of discs
        lower_left = self._get_player_chain(player_id, row - 1, col - 1, -1, -1)
        upper_right = self._get_player_chain(player_id, row + 1, col + 1, 1, 1)
        if len(lower_left) + len(upper_right) + 1 >= self.victory_condition:
            self.winner_id = player_id
            return self.winner_id

        return None

    @js_callback
    def change_player(self, player_id: int = None):
        """
        Changes player. If player id is given, that player id is explicitly set, otherwise goes to the next
        player in the list of players.

        :param `player_id`: Id of player to set.
        :return: Id of player being changed to.
        """

        if player_id is None:
            self.current_player = self.current_player + 1 if self.current_player + 1 < len(self.players) else 0
        else:
            if player_id >= len(self.players):
                raise IllegalAction('Player id does not exist in the list of players')
            self.current_player = player_id

        return self.current_player

    @js_callback
    def drop_disc(self, col_num: int):
        """
        Drops disc belonging to the current player in the given column, and switches to the next player.

        :return: Player id if player has won the game, None otherwise.
        """

        disc = self.discs[self.current_player]
        row_num = self.grid.drop_disc(disc, col_num)
        player_id = self.check_for_victory(row_num, col_num)

        # Has next player make move if current player has not won
        if player_id is None:
            self.change_player()

        return player_id

    @js_callback
    def reset_game(self):
        """
        Starts a new game, reverting grid and game conditions to their initial states.

        :return: State of game after reset.
        """

        self.grid.setup_grid()
        self.current_player = 0
        self.winner_id = None

        return self.get_state()