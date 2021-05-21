import { GridSpace } from './grid-space';

export interface GridState {
  width: number;
  height: number;
  total_capacity: number;
  grid_spaces: GridSpace[][];
  available_col_spaces: number[];
  inserted_disc_count: number;
}
