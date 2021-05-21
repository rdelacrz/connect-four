import { createStore } from 'vuex';
import actions from './actions';
import mutations from './mutations';
import { RootState } from './state';

export default createStore<RootState>({
  state: {
    updateInProgress: false,
  },
  actions,
  mutations,
});
