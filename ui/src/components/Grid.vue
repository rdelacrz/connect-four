<template>
  <div class="grid-wrapper">
    <div class="grid-col-wrapper" v-for="(gridCol, colIndex) in gridSpaces" :key="colIndex" @click.stop="handleColumnClick(colIndex)">
      <div class="grid-space-container" v-for="gridSpace in gridSpaces[colIndex]" :key="gridSpace.y">
        <div v-if="!!gridSpace.disc">
          <span :style="{'backgroundColor': gridSpace.disc.color}">{{gridSpace.disc.color}}</span>
        </div>
        <div v-else>
          <span>{{gridSpace.x}}, {{gridSpace.y}}</span>
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
  },
  data() {
    const gridSpaces = computed(() => this.$props.state?.grid_spaces || []);
    const availableColSpaces = computed(() => this.$props.state?.available_col_spaces || []);
    return {
      gridSpaces,
      availableColSpaces,
      winnerId: -1,
    }
  },
  methods: {
    handleColumnClick(colNum: number) {
      const availableColSpaces = this.availableColSpaces as number[];
      const winnerId = this.winnerId as number;
      if (availableColSpaces[colNum] !== null && winnerId === -1) {
        const callbackFn = (winningPlayer?: number) => {
          if (winningPlayer !== null) {
            this.winnerId = winningPlayer;
          }
        };
        this.$store.dispatch('dropDisc', {colNum, callbackFn});
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
    border: solid 5px black;
    .grid-col-wrapper {
      display: inline-flex;
      flex-direction: column-reverse;
      cursor: pointer;
      .grid-space-container {
        border: solid 2px black;
        height: 80px;
        width: 80px;
      }
    }
  }
</style>
