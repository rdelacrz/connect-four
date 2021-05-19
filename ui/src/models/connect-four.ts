export interface ConnectFourGame {
    check_for_victory: (row: number, col: number, callback_fn?: (playerId: number) => void) => void;
    change_player: (playerId?: number, callback_fn?: (newPlayerId: number) => void) => void;
    drop_disc: (col_num: number, callback_fn?: (winningPlayer?: number) => void) => void;
}