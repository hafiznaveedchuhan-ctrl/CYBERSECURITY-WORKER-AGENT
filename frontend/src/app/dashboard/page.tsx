'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { ChatWidget } from '@/components/ChatWidget';

interface ApprovalRequest {
  id: string;
  action_type: string;
  target: string;
  reason: string;
  risk_level: string;
  requested_at: string;
  expires_at: string;
}

interface AgentStats {
  total_runs: number;
  successful_runs: number;
  failed_runs: number;
  avg_duration_ms: number;
  by_agent: Record<string, number>;
}

interface RecentAlert {
  id: string;
  title: string;
  severity: string;
  status: string;
  timestamp: string;
}

export default function DashboardPage() {
  const { user, token, isLoading } = useAuth();
  const router = useRouter();
  const [pendingApprovals, setPendingApprovals] = useState<ApprovalRequest[]>([]);
  const [agentStats, setAgentStats] = useState<AgentStats | null>(null);
  const [recentAlerts, setRecentAlerts] = useState<RecentAlert[]>([]);
  const [showChat, setShowChat] = useState(false);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login');
    }
  }, [user, isLoading, router]);

  useEffect(() => {
    if (token) {
      fetchDashboardData();
    }
  }, [token]);

  const fetchDashboardData = async () => {
    try {
      // Fetch pending approvals
      const approvalsRes = await fetch('/api/approvals', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (approvalsRes.ok) {
        const data = await approvalsRes.json();
        setPendingApprovals(data.approvals || []);
      }

      // Fetch agent stats
      const statsRes = await fetch('/api/agent-runs/stats/summary', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (statsRes.ok) {
        setAgentStats(await statsRes.json());
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const handleApproval = async (approvalId: string, approved: boolean) => {
    try {
      const endpoint = approved
        ? `/api/approvals/${approvalId}/approve`
        : `/api/approvals/${approvalId}/reject`;

      await fetch(endpoint, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });

      // Refresh data
      fetchDashboardData();
    } catch (error) {
      console.error('Approval action failed:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">SOC Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-400">Welcome, {user.email}</span>
            <button
              onClick={() => setShowChat(!showChat)}
              className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors"
            >
              {showChat ? 'Hide AI Assistant' : 'Open AI Assistant'}
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Main Content */}
        <main className={`flex-1 p-6 ${showChat ? 'mr-96' : ''}`}>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Pending Approvals"
              value={pendingApprovals.length}
              icon="⚠️"
              color="yellow"
            />
            <StatCard
              title="Agent Runs Today"
              value={agentStats?.total_runs || 0}
              icon="🤖"
              color="blue"
            />
            <StatCard
              title="Success Rate"
              value={
                agentStats
                  ? `${Math.round((agentStats.successful_runs / agentStats.total_runs) * 100 || 0)}%`
                  : '0%'
              }
              icon="✅"
              color="green"
            />
            <StatCard
              title="Avg Response Time"
              value={agentStats ? `${Math.round(agentStats.avg_duration_ms)}ms` : '0ms'}
              icon="⚡"
              color="purple"
            />
          </div>

          {/* Pending Approvals */}
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Pending Approvals</h2>
            {pendingApprovals.length === 0 ? (
              <div className="bg-gray-800 rounded-lg p-6 text-center text-gray-400">
                No pending approvals
              </div>
            ) : (
              <div className="space-y-4">
                {pendingApprovals.map((approval) => (
                  <ApprovalCard
                    key={approval.id}
                    approval={approval}
                    onApprove={() => handleApproval(approval.id, true)}
                    onReject={() => handleApproval(approval.id, false)}
                  />
                ))}
              </div>
            )}
          </section>

          {/* Agent Activity */}
          <section className="mb-8">
            <h2 className="text-xl font-semibold mb-4">Agent Activity</h2>
            <div className="bg-gray-800 rounded-lg p-6">
              {agentStats?.by_agent ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {Object.entries(agentStats.by_agent).map(([agent, count]) => (
                    <div key={agent} className="text-center">
                      <div className="text-2xl font-bold text-blue-400">{count}</div>
                      <div className="text-sm text-gray-400">{agent}</div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400 text-center">No agent activity recorded</p>
              )}
            </div>
          </section>

          {/* Quick Actions */}
          <section>
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <QuickActionButton
                label="Analyze Alert"
                icon="🔍"
                onClick={() => {
                  setShowChat(true);
                  alert('AI Assistant opened! Paste your security alert for analysis.');
                }}
              />
              <QuickActionButton
                label="Generate Report"
                icon="📝"
                onClick={() => {
                  setShowChat(true);
                  alert('AI Assistant opened! Ask to generate an incident report.');
                }}
              />
              <QuickActionButton
                label="Search IOCs"
                icon="🎯"
                onClick={() => setShowChat(true)}
              />
              <QuickActionButton
                label="View Textbook"
                icon="📚"
                onClick={() => window.open('https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/', '_blank')}
              />
            </div>
          </section>
        </main>

        {/* Chat Sidebar */}
        {showChat && (
          <aside className="fixed right-0 top-0 h-screen w-96 bg-gray-800 border-l border-gray-700">
            <ChatWidget className="h-full" />
          </aside>
        )}
      </div>
    </div>
  );
}

function StatCard({
  title,
  value,
  icon,
  color,
}: {
  title: string;
  value: string | number;
  icon: string;
  color: string;
}) {
  const colorClasses = {
    yellow: 'bg-yellow-900/30 border-yellow-600',
    blue: 'bg-blue-900/30 border-blue-600',
    green: 'bg-green-900/30 border-green-600',
    purple: 'bg-purple-900/30 border-purple-600',
  };

  return (
    <div className={`rounded-lg p-6 border ${colorClasses[color as keyof typeof colorClasses]}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-400">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </div>
  );
}

function ApprovalCard({
  approval,
  onApprove,
  onReject,
}: {
  approval: ApprovalRequest;
  onApprove: () => void;
  onReject: () => void;
}) {
  const riskColors = {
    low: 'text-green-400',
    medium: 'text-yellow-400',
    high: 'text-orange-400',
    critical: 'text-red-400',
  };

  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-medium">{approval.action_type}</span>
            <span
              className={`text-sm ${riskColors[approval.risk_level as keyof typeof riskColors]}`}
            >
              ({approval.risk_level})
            </span>
          </div>
          <p className="text-gray-400 text-sm mt-1">Target: {approval.target}</p>
          <p className="text-gray-500 text-sm mt-1">{approval.reason}</p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={onReject}
            className="px-3 py-1 bg-gray-700 text-white rounded hover:bg-gray-600"
          >
            Reject
          </button>
          <button
            onClick={onApprove}
            className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
          >
            Approve
          </button>
        </div>
      </div>
    </div>
  );
}

function QuickActionButton({
  label,
  icon,
  onClick,
}: {
  label: string;
  icon: string;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="bg-gray-800 rounded-lg p-4 border border-gray-700 hover:border-blue-500 transition-colors text-center"
    >
      <span className="text-2xl block mb-2">{icon}</span>
      <span className="text-sm">{label}</span>
    </button>
  );
}
