/***
 * Plugin responsible for connecting to data sent to the global state by CEFPython.
 */

import { Plugin } from 'vue';

export const CEFBridgePlugin: Plugin = {
    install: (app, options) => {
        app.config.globalProperties.$connectFour = (window as any).connectFour;
    }
};

