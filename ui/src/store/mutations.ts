import { MutationTree } from 'vuex';
import { GameState } from '../models';
import { RootState } from './state';

const mutations: MutationTree<RootState> = {
  SET_GAME_STATE: (state, gameState: GameState) => {
    state.gameState = gameState;
  },
  SET_STATE_UPDATE_FLAG: (state, updateInProgress: boolean) => {
    state.updateInProgress = updateInProgress;
  },
};

export default mutations;
