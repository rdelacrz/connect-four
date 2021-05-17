<template>
  <div class="grid-wrapper">
    <div>
      Grids
    </div>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue';
import { Options, Vue } from 'vue-class-component';

@Options({
  props: {
    height: Number,
    width: Number,
  }
})
export default class Grid extends Vue {
  height!: number;
  width!: number;


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  .grid-wrapper {
    background: gray;
  }
</style>
