// src/App.tsx
import { useState, useEffect } from "react";
import SetGoalsPanel from "./components/SetGoalsPanel";
import ProposalsList from "./components/ProposalsList";
import ProposalDetails from "./components/ProposalDetails";
import HelpPanel from "./components/HelpPanel";
import type { Goal, LLMProposal } from "./types";

function App() {
  const [proposals, setProposals] = useState<LLMProposal[]>([]);
  const [activeProposal, setActiveProposal] = useState<LLMProposal | null>(null);
  const [loading, setLoading] = useState(false);
  const [fetchedGoals, setFetchedGoals] = useState<Goal[]>([]);
  const [campaignMessage, setCampaignMessage] = useState<string | null>(null);
  const [showLiveMessages, setShowLiveMessages] = useState(false);
  const [liveMessages, setLiveMessages] = useState<string[]>([]);

  const normalizeProposals = (raw: any[]): LLMProposal[] =>
    raw.map((p) => ({
      goal: p.goal,
      strategies: p.strategies.map((s: string) => ({ text: s })),
    }));

  const handleFetch = async (goals: Goal[]) => {
    setLoading(true);
    try {
      const newGoals = goals.filter((g) => !fetchedGoals.includes(g));

      if (newGoals.length === 0) {
        console.log("No new goals to fetch, using cached results");
        return;
      }

      const activateRes = await fetch("http://localhost:8001/agent/activate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newGoals),
      });

      if (!activateRes.ok) throw new Error("Failed to activate agents");
      const activated = await activateRes.json();
      const newProposals = normalizeProposals(activated);

      setProposals((prev) => [...prev, ...newProposals]);
      setFetchedGoals((prev) => [...prev, ...newGoals]);
    } catch (err) {
      console.error("Error fetching proposals:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (goal: Goal) => {
    const proposal = proposals.find((p) => p.goal === goal) || null;
    setActiveProposal(proposal);
  };

  const handleApprove = async (goal: Goal, index: number) => {
    const strategy = proposals.find((p) => p.goal === goal)?.strategies[index];
    if (!strategy) return;

    try {
      const res = await fetch("http://localhost:8001/agent/approve_strategy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal, strategy_text: strategy.text }),
      });

      if (!res.ok) throw new Error("Approval failed");
      const approved = await res.json();

      setProposals((prev) =>
        prev.map((p) =>
          p.goal === goal
            ? {
                ...p,
                strategies: p.strategies.map((s, i) =>
                  i === index
                    ? { ...s, approved: true, strategy_id: approved.strategy_id }
                    : s
                ),
              }
            : p
        )
      );

      if (activeProposal?.goal === goal) {
        setActiveProposal((prev) =>
          prev
            ? {
                ...prev,
                strategies: prev.strategies.map((s, i) =>
                  i === index
                    ? { ...s, approved: true, strategy_id: approved.strategy_id }
                    : s
                ),
              }
            : null
        );
      }
    } catch (err) {
      console.error("Error approving strategy:", err);
    }
  };

  const handleClear = async () => {
    try {
      await fetch("http://localhost:8001/agent/clear_proposals", {
        method: "POST",
      });
    } catch (err) {
      console.error("Backend clear failed:", err);
    }
    setProposals([]);
    setActiveProposal(null);
    setFetchedGoals([]);
  };

  const handleStartCampaign = async () => {
    try {
      const res = await fetch("http://localhost:8002/ua/start-campaign", {
        method: "POST",
      });
      if (!res.ok) throw new Error("Failed to start campaign");
      setCampaignMessage("Campaign started ✅");
    } catch (err) {
      console.error("Error starting campaign:", err);
      setCampaignMessage("Failed to start campaign ❌");
    }
  };

  // Poll live messages if section is visible
  useEffect(() => {
    if (!showLiveMessages) return;

    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://localhost:8003/cart/message");
        if (!res.ok) return;
        const data = await res.json();
        if (data.message) {
          setLiveMessages((prev) => {
            if (prev.includes(data.message)) return prev;
            return [...prev, data.message];
          });
        }
      } catch (err) {
        console.error("Error fetching live message:", err);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [showLiveMessages]);

  // At least one approved?
  const hasApproved = proposals.some((p) =>
    p.strategies.some((s) => s.approved)
  );

  return (
    <div className="flex flex-col min-h-screen w-screen bg-background text-foreground">
      {/* Header */}
      <header className="w-full h-14 flex items-center px-6 bg-gradient-to-r from-primary/80 to-primary text-white shadow-md">
        <h1 className="text-xl font-bold tracking-wide">Stratgen.AI</h1>
      </header>
  
      {/* Body */}
      <div className="flex flex-1">
        {/* Left edge */}
        <div className="w-1/4 p-6 border-r">
          <SetGoalsPanel
            onFetch={handleFetch}
            onClear={handleClear}
            onStartCampaign={handleStartCampaign}
            onShowLiveMessages={() => setShowLiveMessages(true)}
            loading={loading}
            hasApproved={hasApproved}
          />
          {campaignMessage && (
            <p className="mt-2 text-sm text-green-600">{campaignMessage}</p>
          )}
        </div>
  
        {/* Center */}
        <div className="flex-1 p-6 flex flex-col gap-6">
          <ProposalsList proposals={proposals} onSelect={handleSelect} />
          <ProposalDetails proposal={activeProposal} onApprove={handleApprove} />
  
          {showLiveMessages && (
            <div className="mt-6 p-4 border rounded-lg bg-white/50 backdrop-blur-md shadow-md">
              <h3 className="font-bold mb-2">Live Messages</h3>
              {liveMessages.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No messages yet...
                </p>
              ) : (
                <ul className="list-disc pl-6 space-y-1">
                  {liveMessages.map((msg, i) => (
                    <li key={i}>{msg}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
  
        {/* Right edge */}
        <div className="w-1/4 p-6 border-l">
          <HelpPanel />
        </div>
      </div>
    </div>
  );
  
}

export default App;
