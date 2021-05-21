import { Disc } from './disc';
import { GridState } from './grid-state';
import { Player } from './player';

export interface GameState {
  players: Player[];
  current_player: number;
  discs: Disc[];
  grid: GridState;
  victory_condition: number;
}
