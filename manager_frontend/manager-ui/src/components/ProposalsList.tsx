// src/components/ProposalsList.tsx
import React from "react"
import type { LLMProposal, Goal } from "../types"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

interface ProposalsListProps {
  proposals: LLMProposal[]
  onSelect: (goal: Goal) => void
}

const ProposalsList: React.FC<ProposalsListProps> = ({ proposals, onSelect }) => {
  return (
    <Card className="rounded-xl border bg-white/60 backdrop-blur-md shadow-md">
      <CardHeader>
        <CardTitle className="text-lg">Proposals</CardTitle>
      </CardHeader>
      <CardContent>
        {proposals.length === 0 ? (
          <p className="text-sm text-muted-foreground">No proposals yet</p>
        ) : (
          <ul className="divide-y rounded-lg border">
            {proposals.map((p) => (
              <li
                key={p.goal}
                className="cursor-pointer px-3 py-2 hover:bg-accent hover:text-accent-foreground transition-colors"
                onClick={() => onSelect(p.goal)}
              >
                {p.goal}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}

export default ProposalsList
