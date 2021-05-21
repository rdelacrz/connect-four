<template>
  <Grid :state='grid' />
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { mapState } from 'vuex';
import { Options, Vue } from 'vue-class-component';
import Grid from './components/Grid.vue';

const App = defineComponent({
  computed: {
    grid() {
      return this.$store.state.gameState?.grid;
    },
  },
  components: {
    Grid,
  },
  mounted() {
    this.$store.dispatch('getGameState');
  },
})

export default App;

</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
