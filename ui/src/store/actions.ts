import { ActionTree } from 'vuex';
import { AI, ConnectFourGame } from '../models';
import { RootState } from './state';

const connectFour = (window as any).connectFour as ConnectFourGame;
const ai = (window as any).ai as AI;

const actions: ActionTree<RootState, RootState> = {
  // Main game actions
  getGameState: (context, postDiscDrop = false) => {
    connectFour.get_state((state) => {
      context.commit('SET_GAME_STATE', state);
      context.commit('SET_STATE_UPDATE_FLAG', false);

      // Executes AI action after player disc drop (if an AI exists)
      if (postDiscDrop && state.winner_id === null && state.current_player === context.state.aiPlayerId) {
        // Encapsulated in setTimeout to prevent function call from stopping render
        setTimeout(() => {
          context.dispatch('getAIOptimalCol', {
            searchDepth: 4,
            callbackFn: (colNum: number) => {
              context.dispatch('dropDisc', { colNum });
            },
          });
        }, 500);
      }
    });
  },
  checkForVictory: (context, payload: {row: number, col: number, discsInRow: number,
      callbackFn?: (newPlayerId?: number) => void}) => {
    connectFour.check_for_discs_in_row(payload.row, payload.col, payload.discsInRow, (playerId?: number) => {
      if (payload.callbackFn) {
        payload.callbackFn(playerId);
      }
      context.dispatch('getGameState');
    });
  },
  changePlayer: (context, payload: { playerId?: number, callbackFn?: (newPlayerId: number) => void }) => {
    if (!context.state.updateInProgress) {
      context.commit('SET_STATE_UPDATE_FLAG', true);
      connectFour.change_player(payload.playerId, (newPlayerId: number) => {
        if (payload.callbackFn) {
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
        if (payload.callbackFn) {
          payload.callbackFn(winningPlayer);
        }
        context.dispatch('getGameState', true);
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
  },

  // AI actions
  getAIPlayerId: (context) => {
    ai.get_ai_id((aiPlayerId) => {
      context.commit('SET_AI_PLAYER_ID', aiPlayerId);
    });
  },
  getAIOptimalCol: (context, payload: { searchDepth?: number, callbackFn?: (optimalCol?: number) => void }) => {
    ai.get_optimal_col(payload.searchDepth || 4, payload.callbackFn);
  },
};

export default actions;
