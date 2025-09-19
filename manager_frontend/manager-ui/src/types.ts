// src/types.ts

export type Goal = "AOV" | "CART_RECOVERY" | "CLEAR_STOCK";

export interface Strategy {
  text: string
  approved?: boolean
  strategy_id?: string
}

export interface LLMProposal {
  goal: Goal
  strategies: Strategy[]
}

