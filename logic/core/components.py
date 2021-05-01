"""
Contains the basic physical components of the Connect Four grid. The classes here will only encapsulate the basic
variables and methods required to setup and interact with the grid. Functional logic related to the actual rules of
Connect Four will be implemented elsewhere, allowing for a clear separation between game logic and data structure.
"""

from .exceptions import IllegalAction

class Disc:
    def __init__(self, player_id: int, color: str):
        self.player_id = player_id
        self.color = color

class GridSpace:
    def __init__(self, x: int, y: int):
        self.disc: Disc = None
        self.x = x
        self.y = y

    def __repr__(self):
        return '_' if self.disc is None else str(self.disc.player_id)

class ConnectFourGrid:
    def __init__(self, width=7, height=6):
        self.width = width
        self.height = height
        self.total_capacity = width * height
        self.setup_grid()

    def __repr__(self):
        """
        Produces visual representation of the Connect Four grid (from top to bottom), displaying _ for empty spaces,
        and player ids wherever a player's disc is inserted.

        :return: String representing state of the Connect Four grid.
        """
        board_repr = ""
        for y in range(self.height - 1, -1, -1):
            row = [self.grid_spaces[x][y] for x in range(self.width)]
            board_repr += ' '.join([str(grid_space) for grid_space in row]) + '\n'
        return board_repr

    def setup_grid(self):
        """
        Initializes both the grid and a simple list for the next available row for each column in the grid.

        The grid is comprised of a list of lists, with the top level list indices representing the different column
        numbers within the grid, and the bottom level lists representing the different rows within a given column.
        """

        self.grid_spaces = [[GridSpace(x, y) for y in range(self.height)] for x in range(self.width)]
        self.available_col_spaces = [0 for _ in range(self.width)]
        self.inserted_disc_count = 0

    def is_grid_full(self):
        """
        Checks whether grid has been completely filled with discs.

        :return: True if number of discs has reached the total capacity within the grid, False otherwise.
        """

        return self.inserted_disc_count >= self.total_capacity

    def drop_disc(self, disc: Disc, col_num: int):
        """
        Drops a player disc within a given column on the grid.

        :param `disc`: Object for disc containing player id and disc color.
        :param `col_num`: Column number that disc is being dropped in (corresponds to the x coordinate on the grid).

        :return: Row number that the disc was placed in.
        """

        if self.is_grid_full():
            raise IllegalAction('Grid has reached the maximum number of allowable discs!')

        row_num = self.available_col_spaces[col_num]
        
        if row_num is None:
            raise IllegalAction('Cannot place a disc in a grid column that is completely full!')
        else:
            self.grid_spaces[col_num][row_num].disc = disc

            # Sets next available row to None if it exceeds height of the grid
            next_available_row = row_num + 1
            self.available_col_spaces[col_num] = next_available_row if next_available_row < self.height else None

            self.inserted_disc_count += 1

            return row_num
        