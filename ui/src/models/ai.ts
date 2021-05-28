export interface AI {
  get_ai_id: (callbackFn?: (aiPlayerId: number) => void) => void;

  // Search depth essentially equals the difficulty level (4 = extremely hard!)
  get_optimal_col: (searchDepth?: number, callbackFn?: (optimalCol: number) => void) => void;
}
