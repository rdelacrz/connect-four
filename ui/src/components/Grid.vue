<template>
  <div class="grid-wrapper">
    <div class="grid-col-wrapper" v-for="(gridCol, colIndex) in gridSpaces" :key="colIndex" @click="handleColumnClick(colIndex)">
      <div class="grid-space-container" v-for="gridSpace in gridSpaces[colIndex]" :key="gridSpace.y">
        <div v-if="!!gridSpace.disc">
          <div class="token" :style="{'backgroundColor': gridSpace.disc.color}" />
        </div>
        <div v-else>
          <div class="token empty" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent } from 'vue';
import { Options, Vue } from 'vue-class-component';
import { GridState } from '../models';

const Grid = defineComponent({
  props: {
    state: Object as () => GridState,
    winnerId: Number,
    playerTurn: Boolean,
  },
  data() {
    const gridSpaces = computed(() => this.$props.state?.grid_spaces || []);
    const availableColSpaces = computed(() => this.$props.state?.available_col_spaces || []);
    return {
      gridSpaces,
      availableColSpaces,
    }
  },
  methods: {
    handleColumnClick(colNum: number) {
      const playerTurn = this.playerTurn as boolean;
      const availableColSpaces = this.availableColSpaces as number[];
      const winnerId = this.winnerId as number | null;
      if (playerTurn && availableColSpaces[colNum] !== null && winnerId === null) {
        this.$store.dispatch('dropDisc', {colNum}).then(() => {
          this.$emit('playerClick', colNum);
        });
      }
    },
  }
})

export default Grid;
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  .grid-wrapper {
    display: inline-block;
    background-color: #A08C64;
    border: solid 5px black;
    .grid-col-wrapper {
      display: inline-flex;
      flex-direction: column-reverse;
      cursor: pointer;
      .grid-space-container {
        padding: 10px;
        .token {
          background-color: white;
          border: solid 2px black;
          border-radius: 50%;
          height: 80px;
          width: 80px;
        }
      }
    }
  }
</style>
