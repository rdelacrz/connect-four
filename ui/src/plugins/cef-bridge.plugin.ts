/***
 * Plugin responsible for connecting to data sent to the global state by CEFPython.
 */

import { Plugin } from 'vue';
import { ConnectFourGame } from '../models';

export const CEFBridgePlugin: Plugin = {
    install: (app, options) => {
        const connectFour = (window as any).connectFour as ConnectFourGame;

        app.config.globalProperties.$getState = connectFour.get_state;
        app.config.globalProperties.$changePlayer = connectFour.change_player;
        app.config.globalProperties.$checkForVictory = connectFour.check_for_victory;
        app.config.globalProperties.$dropDisc = connectFour.drop_disc;
    },
};
