import { ActionTree } from 'vuex';
import { ConnectFourGame, GameState } from '../models';
import { RootState } from './state';

const connectFour = (window as any).connectFour as ConnectFourGame;

const actions: ActionTree<RootState, RootState> = {
  getGameState: (context) => {
    connectFour.get_state((state) => {
      context.commit('SET_GAME_STATE', state);
      context.commit('SET_STATE_UPDATE_FLAG', false);
    });
  },
  checkForVictory: (context, payload: {row: number, col: number, callbackFn?: (newPlayerId?: number) => void}) => {
    connectFour.check_for_victory(payload.row, payload.col, (playerId?: number) => {
      if (!!payload.callbackFn) {
        payload.callbackFn(playerId);
      }
      context.dispatch('getGameState');
    });
  },
  changePlayer: (context, payload: { playerId?: number, callbackFn?: (newPlayerId: number) => void }) => {
    if (!context.state.updateInProgress) {
      context.commit('SET_STATE_UPDATE_FLAG', true);
      connectFour.change_player(payload.playerId, (newPlayerId: number) => {
        if (!!payload.callbackFn) {
          payload.callbackFn(newPlayerId);
        }
        context.dispatch('getGameState');
      });
    }
  },
  dropDisc: (context, payload: { colNum: number, callbackFn?: (winningPlayer?: number) => void }) => {
    if (!context.state.updateInProgress) {
      context.commit('SET_STATE_UPDATE_FLAG', true);
      connectFour.drop_disc(payload.colNum, (winningPlayer?: number) => {
        if (!!payload.callbackFn) {
          payload.callbackFn(winningPlayer);
        }
        context.dispatch('getGameState');
      });
    }
  },
  resetGame: (context) => {
    if (!context.state.updateInProgress) {
      context.commit('SET_STATE_UPDATE_FLAG', true);
      connectFour.reset_game((state) => {
        context.commit('SET_GAME_STATE', state);
        context.commit('SET_STATE_UPDATE_FLAG', false);
      });
    }
  }
};

export default actions;
