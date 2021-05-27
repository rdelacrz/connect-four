export interface AI {
  get_ai_id: (callback_fn?: (aiPlayerId: number) => void) => void;
  get_optimal_col: (search_depth?: number, callback_fn?: (optimalCol: number) => void) => void;
}
