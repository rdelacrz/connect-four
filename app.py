"""
Starts the application.
"""

from src.core.game import ConnectFourGame

if __name__ == '__main__':
    connect_four = ConnectFourGame(["Player 1", "Player 2"])

    connect_four.drop_disc(1)
    print(connect_four.grid)

    connect_four.drop_disc(0)
    print(connect_four.grid)

    connect_four.drop_disc(2)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)

    connect_four.drop_disc(3)
    print(connect_four.grid)
    