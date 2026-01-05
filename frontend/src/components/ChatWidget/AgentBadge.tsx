'use client';

interface AgentBadgeProps {
  agent: string;
}

const AGENT_CONFIG: Record<
  string,
  { label: string; color: string; icon: string; description: string }
> = {
  SUPERVISOR: {
    label: 'Supervisor',
    color: 'bg-purple-600',
    icon: '🎯',
    description: 'Orchestrating response',
  },
  TRIAGE: {
    label: 'Triage Agent',
    color: 'bg-yellow-600',
    icon: '⚡',
    description: 'Alert classification',
  },
  ENRICHMENT: {
    label: 'Enrichment Agent',
    color: 'bg-blue-600',
    icon: '🔍',
    description: 'IOC enrichment',
  },
  THREATINTEL: {
    label: 'Threat Intel',
    color: 'bg-red-600',
    icon: '🎭',
    description: 'Threat analysis',
  },
  DETECTION: {
    label: 'Detection Engineer',
    color: 'bg-green-600',
    icon: '🛡️',
    description: 'Rule generation',
  },
  INCIDENT: {
    label: 'Incident Commander',
    color: 'bg-orange-600',
    icon: '🚨',
    description: 'Response coordination',
  },
  REPORT: {
    label: 'Report Writer',
    color: 'bg-indigo-600',
    icon: '📝',
    description: 'Report generation',
  },
};

export function AgentBadge({ agent }: AgentBadgeProps) {
  const config = AGENT_CONFIG[agent] || {
    label: agent,
    color: 'bg-gray-600',
    icon: '🤖',
    description: 'AI Agent',
  };

  return (
    <div className="flex items-center space-x-2 mb-2">
      <span
        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color} text-white`}
      >
        <span className="mr-1">{config.icon}</span>
        {config.label}
      </span>
      <span className="text-xs text-gray-500">{config.description}</span>
    </div>
  );
}
