<template>
  <div class="app-wrapper">
    <div class="grid-outer-container">
      <Grid :state='grid' :winnerId='winnerId' :playerTurn='playerTurn' />
    </div>
    <div class="game-board-wrapper">
      <h1>Players</h1>
      <div v-for="player in players" :key="player.id" class="player-name-container">
        <div class="player-name">
          <div v-show="player.id === currentPlayer" class="current-token" :style="{'backgroundColor': currentTokenColor}" />
          {{player.name}}
          <div v-if="player.id === winnerId" class="winner-message">WINNER!!!</div>
        </div>
      </div>
      <button class="reset-button" @click="resetGame">Reset Game</button>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { mapState } from 'vuex';
import { Options, Vue } from 'vue-class-component';
import Grid from './components/Grid.vue';
import { Disc } from './models';

const App = defineComponent({
  computed: {
    players() {
      return this.$store.state.gameState?.players;
    },
    currentPlayer() {
      return this.$store.state.gameState?.current_player;
    },
    playerTurn() {
      return this.$store.state.aiPlayerId !== this.$store.state.gameState?.current_player;
    },
    currentTokenColor() {
      const discs: Disc[] = this.$store.state.gameState?.discs || [];
      const currentPlayer: number = this.$store.state.gameState?.current_player || 0;
      const playerDisc = discs.find(d => d.player_id === currentPlayer);
      return playerDisc?.color;
    },
    grid() {
      return this.$store.state.gameState?.grid;
    },
    winnerId() {
      return this.$store.state.gameState?.winner_id;
    }
  },
  components: {
    Grid,
  },
  mounted() {
    this.$store.dispatch('getGameState');
    this.$store.dispatch('getAIPlayerId');
  },
  methods: {
    resetGame() {
      this.$store.dispatch('resetGame');
    },
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

.app-wrapper {
  display: flex;
  .grid-outer-container {
    padding: 0 100px;
  }
  .game-board-wrapper {
    .player-name-container {
      position: relative;
      margin-bottom: 15px;
      .player-name {
        position: relative;
        display: inline-flex;
        align-items: center;
        font-size: 20px;
        line-height: 20px;
        .current-token {
          position: absolute;
          left: -20px;
          border: solid 1px black;
          border-radius: 50%;
          height: 10px;
          width: 10px;
          vertical-align: middle;
        }
        .winner-message {
          color: crimson;
          font-size: 20px;
          font-weight: bold;
          margin-left: 20px;
        }
      }
    }
    .reset-button {
      font-size: 30px;
    }
  }
}
</style>
