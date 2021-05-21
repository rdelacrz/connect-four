import { GameState } from '../models';

export interface RootState {
  gameState?: GameState;
  updateInProgress: boolean;
}
