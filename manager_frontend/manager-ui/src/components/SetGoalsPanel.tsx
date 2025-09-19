// src/components/SetGoalsPanel.tsx
import React, { useState } from "react"
import type { Goal } from "../types"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

interface SetGoalsPanelProps {
  onFetch: (goals: Goal[]) => void
  loading?: boolean
}

const SetGoalsPanel: React.FC<SetGoalsPanelProps> = ({ onFetch, loading }) => {
  const [selectedGoals, setSelectedGoals] = useState<Goal[]>([])

  const toggleGoal = (goal: Goal) => {
    setSelectedGoals((prev) =>
      prev.includes(goal) ? prev.filter((g) => g !== goal) : [...prev, goal]
    )
  }

  return (
    <Card className="rounded-xl border bg-white/60 backdrop-blur-md shadow-md">
      <CardHeader>
        <CardTitle className="text-lg">Set Goals</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        {(["AOV", "CART_RECOVERY", "CLEAR_STOCK"] as Goal[]).map((goal) => (
          <label
            key={goal}
            className="flex items-center gap-2 cursor-pointer hover:text-primary"
          >
            <input
              type="checkbox"
              checked={selectedGoals.includes(goal)}
              onChange={() => toggleGoal(goal)}
              className="h-4 w-4 accent-primary"
            />
            <span className="text-sm">{goal}</span>
          </label>
        ))}
        <Button
          className="mt-4 w-full"
          onClick={() => onFetch(selectedGoals)}
          disabled={loading}
        >
          {loading ? "Fetching..." : "Fetch"}
        </Button>
      </CardContent>
    </Card>
  )
}

export default SetGoalsPanel
