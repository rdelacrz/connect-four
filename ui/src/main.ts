import { createApp } from 'vue'
import App from './App.vue'
import { CEFBridgePlugin } from './plugins';
import store from './store'

const app = createApp(App);

app.use(CEFBridgePlugin);
app.use(store);

app.mount('#app');
