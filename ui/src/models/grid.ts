import { GridSpace } from './grid-space';

export interface Grid {
  height: number;
  width: number;
  total_capacity: number;
  grid_spaces: GridSpace[][];
  available_col_spaces: number;
  inserted_disc_count: number;
}
