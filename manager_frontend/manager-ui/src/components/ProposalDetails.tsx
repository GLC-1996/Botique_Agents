// src/components/ProposalDetails.tsx
import React from "react";
import type { LLMProposal, Goal } from "../types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface ProposalDetailsProps {
  proposal: LLMProposal | null;
  onApprove: (goal: Goal, index: number) => void;
}

const ProposalDetails: React.FC<ProposalDetailsProps> = ({
  proposal,
  onApprove,
}) => {
  if (!proposal) {
    return (
      <Card className="rounded-xl border bg-white/60 backdrop-blur-md shadow-md">
        <CardHeader>
          <CardTitle className="text-lg">Details</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Select a proposal to view details
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="rounded-xl border bg-white/60 backdrop-blur-md shadow-md">
      <CardHeader>
        <CardTitle className="text-lg">Goal: {proposal.goal}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {proposal.strategies.map((s, idx) => (
            <li
              key={idx}
              className="flex items-center justify-between text-sm border-b pb-2"
            >
              <span>{s.text}</span>
              <Button
                size="sm"
                variant={s.approved ? "secondary" : "default"}
                disabled={s.approved}
                onClick={() => onApprove(proposal.goal, idx)}
              >
                {s.approved ? "Approved ✅" : "Approve"}
              </Button>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};

export default ProposalDetails;
