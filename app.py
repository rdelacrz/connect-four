"""
Starts the application.
"""

from src.game.grid import Disc, ConnectFourGrid

if __name__ == '__main__':
    connect_four = ConnectFourGrid()
    print(connect_four)

    player1_disc = Disc(1, 'yellow')
    player2_disc = Disc(2, 'red')

    connect_four.drop_disc(player1_disc, 0)
    print(connect_four)

    connect_four.drop_disc(player2_disc, 0)
    print(connect_four)

    connect_four.drop_disc(player1_disc, 2)
    print(connect_four)