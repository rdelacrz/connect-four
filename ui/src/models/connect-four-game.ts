import { GameState } from './game-state';

export interface ConnectFourGame {
  get_state: (callbackFn?: (state: GameState) => void) => void;
  check_for_discs_in_row: (row: number, col: number, discsInRow: number,
                           callbackFn?: (playerId: number) => void) => void;
  change_player: (playerId?: number, callbackFn?: (newPlayerId: number) => void) => void;
  drop_disc: (colNum: number, callbackFn?: (winningPlayer?: number) => void) => void;
  reset_game: (callbackFn?: (state: GameState) => void) => void;
}
