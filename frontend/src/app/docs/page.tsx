'use client';

import { useState } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  ChevronRight,
  ChevronDown,
  Shield,
  Brain,
  Workflow,
  Lock,
  Clock,
  CheckCircle2,
  Users,
  AlertTriangle,
  Wrench,
  Zap,
  Target,
  Bot,
  FileText
} from 'lucide-react';

// Module data structure
const modules = [
  {
    id: 'module-1-soc-foundations',
    title: 'Module 1: SOC Foundations',
    description: 'Learn the foundational concepts of Security Operations Centers and their role in modern cybersecurity.',
    icon: Shield,
    color: 'cyan',
    duration: '4-6 hours',
    chapters: [
      {
        id: '01-introduction',
        title: 'Introduction to SOC',
        description: 'What is a SOC, SOC models, tiers, and key metrics',
        content: `
# Introduction to Security Operations Centers

A **Security Operations Center (SOC)** is a centralized facility where an organization's security team monitors, detects, analyzes, and responds to cybersecurity incidents.

## What is a SOC?

The SOC is responsible for:
- **Continuous Monitoring**: 24/7 surveillance of security events
- **Threat Detection**: Identifying potential security incidents
- **Incident Response**: Coordinating responses to confirmed incidents
- **Threat Intelligence**: Gathering and analyzing threat data

## SOC Models

### In-house SOC
An internal team dedicated to the organization's security with full control over operations.

### Managed SOC (MSSP)
Outsourced security operations to a Managed Security Service Provider.

### Hybrid SOC
A combination of in-house and managed services.

## SOC Tiers

| Tier | Role | Responsibilities |
|------|------|-----------------|
| Tier 1 | Alert Analyst | Initial triage, classification, false positive identification |
| Tier 2 | Incident Responder | Deep dive analysis, forensics, containment |
| Tier 3 | Threat Hunter | Proactive hunting, malware analysis, tool development |

## Key Metrics

- **MTTD**: Mean Time to Detect (Target: < 1 hour)
- **MTTR**: Mean Time to Respond (Target: < 4 hours)
- **False Positive Rate**: (Target: < 20%)
        `
      },
      {
        id: '02-team-roles',
        title: 'SOC Team Roles',
        description: 'Understanding the different positions in a SOC team',
        content: `
# SOC Team Roles

A well-functioning SOC requires a diverse team with specialized skills.

## Core Roles

### SOC Manager
- Overall responsibility for SOC operations
- Resource allocation and team management
- Strategic planning and reporting

### Security Analyst (Tiers 1-3)
- Monitor security alerts and events
- Investigate and respond to incidents
- Document findings and procedures

### Threat Intelligence Analyst
- Monitor threat landscape
- Produce threat reports
- Update detection rules based on new threats

### Incident Response Lead
- Coordinate major incident responses
- Develop and maintain IR playbooks
- Interface with other departments

### Security Engineer
- Maintain and tune security tools
- Develop automation and integrations
- Implement new security technologies

## Skills Required

| Role | Technical Skills | Soft Skills |
|------|-----------------|-------------|
| Analyst | SIEM, Log Analysis, Networking | Communication, Attention to Detail |
| IR Lead | Forensics, Malware Analysis | Leadership, Decision Making |
| Engineer | Scripting, API Development | Problem Solving, Documentation |
        `
      },
      {
        id: '03-alert-triage',
        title: 'Alert Triage Process',
        description: 'Learn how to classify and prioritize security alerts',
        content: `
# Alert Triage Process

Effective alert triage is critical for SOC efficiency.

## Triage Workflow

1. **Alert Ingestion**: Receive alert from security tools
2. **Initial Assessment**: Quick evaluation of alert details
3. **Classification**: Categorize by type and severity
4. **Enrichment**: Gather additional context
5. **Decision**: Escalate, investigate, or close

## Severity Classification

| Severity | Description | Response Time |
|----------|-------------|---------------|
| Critical | Active breach, data exfiltration | Immediate |
| High | Confirmed malicious activity | < 1 hour |
| Medium | Suspicious activity requiring investigation | < 4 hours |
| Low | Informational, policy violations | < 24 hours |

## Common Alert Types

- **Malware Detection**: AV/EDR alerts for malicious files
- **Network Anomalies**: Unusual traffic patterns
- **Authentication Issues**: Failed logins, impossible travel
- **Policy Violations**: Unauthorized access attempts
- **Vulnerability Alerts**: New CVEs affecting systems

## Reducing False Positives

1. Tune detection rules based on environment
2. Create whitelists for known-good activity
3. Use threat intelligence for context
4. Implement machine learning for anomaly detection
        `
      },
      {
        id: '04-tools',
        title: 'SOC Tools and Technologies',
        description: 'Overview of common security tools used in SOC operations',
        content: `
# SOC Tools and Technologies

Modern SOCs rely on a variety of security tools.

## Core Tools

### SIEM (Security Information and Event Management)
- Log aggregation and correlation
- Real-time alerting
- Examples: Splunk, Microsoft Sentinel, Elastic SIEM

### EDR (Endpoint Detection and Response)
- Endpoint visibility and protection
- Threat hunting capabilities
- Examples: CrowdStrike, Carbon Black, SentinelOne

### SOAR (Security Orchestration, Automation, and Response)
- Playbook automation
- Case management
- Examples: Splunk SOAR, Palo Alto XSOAR, IBM Resilient

### Threat Intelligence Platforms
- IOC management
- Threat feed aggregation
- Examples: MISP, ThreatConnect, Anomali

## Network Security Tools

- **Firewall**: Network traffic filtering
- **IDS/IPS**: Intrusion detection and prevention
- **NDR**: Network detection and response
- **Proxy**: Web traffic filtering and inspection

## Tool Integration

Modern SOCs integrate tools for:
- Automated alert enrichment
- Coordinated response actions
- Unified visibility across the environment
        `
      },
      {
        id: '05-incident-response',
        title: 'Incident Response Basics',
        description: 'Fundamental concepts of incident response procedures',
        content: `
# Incident Response Basics

Incident response is the process of handling security incidents.

## IR Lifecycle (NIST Framework)

1. **Preparation**: Develop plans, train team, acquire tools
2. **Detection & Analysis**: Identify and investigate incidents
3. **Containment, Eradication, Recovery**: Stop, clean, restore
4. **Post-Incident Activity**: Learn and improve

## Incident Classification

| Type | Examples |
|------|----------|
| Malware | Ransomware, trojans, viruses |
| Phishing | Email compromise, credential theft |
| Data Breach | Unauthorized data access |
| DDoS | Service disruption attacks |
| Insider Threat | Malicious employee actions |

## Response Actions

### Containment
- Isolate affected systems
- Block malicious IPs/domains
- Disable compromised accounts

### Eradication
- Remove malware
- Patch vulnerabilities
- Reset credentials

### Recovery
- Restore from backups
- Monitor for recurrence
- Validate system integrity

## Documentation

Every incident should be documented:
- Timeline of events
- Actions taken
- Evidence collected
- Lessons learned
        `
      }
    ]
  },
  {
    id: 'module-2-agentic-ai',
    title: 'Module 2: Agentic AI for Security',
    description: 'Understand how autonomous AI agents can enhance security operations.',
    icon: Brain,
    color: 'purple',
    duration: '3-4 hours',
    chapters: [
      {
        id: '01-introduction',
        title: 'Introduction to Agentic AI',
        description: 'What is agentic AI and how does it differ from traditional AI',
        content: `
# Introduction to Agentic AI

Agentic AI represents a new paradigm in artificial intelligence.

## What is Agentic AI?

**Agentic AI** refers to AI systems that can:
- Take autonomous actions
- Make decisions based on goals
- Interact with external systems
- Learn from feedback

## Traditional AI vs Agentic AI

| Aspect | Traditional AI | Agentic AI |
|--------|---------------|------------|
| Interaction | Single input/output | Multi-step workflows |
| Autonomy | Passive response | Active decision making |
| Tools | None | Can use external tools |
| Memory | Stateless | Maintains context |

## Core Concepts

### Agents
Autonomous entities that perceive their environment and take actions.

### Tools
External capabilities agents can use (APIs, databases, services).

### Planning
The ability to break down complex tasks into steps.

### Memory
Short-term (conversation) and long-term (knowledge) storage.

## Benefits in Security

1. **24/7 Operations**: Agents don't need sleep
2. **Consistency**: Same analysis quality every time
3. **Speed**: Instant response to alerts
4. **Scale**: Handle thousands of alerts simultaneously
        `
      },
      {
        id: '02-architecture',
        title: 'Agent Architecture',
        description: 'Understanding how AI agents are structured and operate',
        content: `
# Agent Architecture

Understanding agent architecture is key to building effective AI systems.

## Core Components

### 1. Language Model (Brain)
The LLM that powers reasoning and decision-making.

### 2. System Prompt
Instructions that define the agent's role and behavior.

### 3. Tools
External capabilities the agent can invoke:
- API calls
- Database queries
- File operations
- Security tool integrations

### 4. Memory Systems
- **Working Memory**: Current conversation context
- **Long-term Memory**: Persistent knowledge base

### 5. Orchestration Layer
Manages the agent's execution flow and tool usage.

## Agent Patterns

### ReAct Pattern
Reason → Act → Observe → Repeat

### Plan-and-Execute
Create plan → Execute steps → Verify results

### Multi-Agent Systems
Multiple specialized agents working together.

## Our AI Employ Architecture

The AI-SOC platform uses specialized agents:
- **Supervisor**: Routes requests to specialists
- **Triage**: Classifies and prioritizes alerts
- **Enrichment**: Gathers IOC context
- **ThreatIntel**: Maps to MITRE ATT&CK
- **Detection**: Generates Sigma/YARA rules
- **Incident**: Coordinates response
- **Report**: Creates documentation
        `
      }
    ]
  },
  {
    id: 'module-3-ai-soc-workflows',
    title: 'Module 3: AI-SOC Workflows',
    description: 'Practical workflows combining AI agents with SOC processes.',
    icon: Workflow,
    color: 'green',
    duration: '3-4 hours',
    chapters: [
      {
        id: '01-ai-triage',
        title: 'AI-Powered Triage',
        description: 'Using AI agents to automate alert triage',
        content: `
# AI-Powered Alert Triage

AI agents can dramatically improve the triage process.

## Traditional vs AI Triage

| Aspect | Manual Triage | AI Triage |
|--------|--------------|-----------|
| Speed | Minutes per alert | Seconds |
| Consistency | Variable | Uniform |
| Scale | Limited by staff | Unlimited |
| Availability | Business hours | 24/7 |

## AI Triage Workflow

1. **Alert Ingestion**
   - Receive alert from SIEM/EDR
   - Parse alert into structured format

2. **Initial Classification**
   - Identify alert type
   - Extract key indicators (IOCs)
   - Assess initial severity

3. **Enrichment**
   - Query threat intelligence
   - Check IOC reputation
   - Gather asset context

4. **Severity Assessment**
   - Apply classification rules
   - Consider business context
   - Assign final severity

5. **Routing Decision**
   - Auto-close false positives
   - Route to appropriate team
   - Trigger response playbooks

## Example Prompts

\`\`\`
Analyze this security alert and provide:
1. Alert classification (malware/phishing/recon/etc)
2. Severity rating (critical/high/medium/low)
3. Key IOCs identified
4. Recommended next steps
\`\`\`

## Measuring Success

- Reduction in MTTD
- False positive rate improvement
- Analyst time savings
- Consistent classification accuracy
        `
      }
    ]
  },
  {
    id: 'module-4-ai-security',
    title: 'Module 4: AI Security & Governance',
    description: 'Understanding risks and best practices for AI in security.',
    icon: Lock,
    color: 'red',
    duration: '2-3 hours',
    chapters: [
      {
        id: '01-risks',
        title: 'AI Security Risks',
        description: 'Understanding the risks of AI in security operations',
        content: `
# AI Security Risks

Deploying AI in security operations introduces new risks.

## Prompt Injection

Attackers may try to manipulate AI agents through:
- Malicious input in alerts
- Crafted log entries
- Social engineering via chat

### Mitigations
- Input sanitization
- Output validation
- Least privilege access
- Human approval for sensitive actions

## Data Privacy

AI systems may process sensitive data:
- PII in logs
- Credentials in alerts
- Internal system details

### Mitigations
- Data anonymization
- Access controls
- Audit logging
- Data retention policies

## Model Reliability

AI models can:
- Hallucinate information
- Miss edge cases
- Produce inconsistent results

### Mitigations
- Human-in-the-loop for critical decisions
- Confidence thresholds
- Regular validation testing
- Multiple model consensus

## Governance Best Practices

1. **Define Clear Boundaries**
   - What can agents do autonomously?
   - What requires approval?

2. **Implement Audit Trails**
   - Log all agent actions
   - Track decision rationale

3. **Regular Testing**
   - Red team AI systems
   - Test edge cases

4. **Incident Response for AI**
   - Plan for AI failures
   - Ability to disable agents
        `
      }
    ]
  }
];

const colorClasses: Record<string, { bg: string; border: string; text: string; icon: string }> = {
  cyan: { bg: 'from-cyan-500/20 to-cyan-600/5', border: 'border-cyan-500/30', text: 'text-cyan-400', icon: 'bg-cyan-500/20' },
  purple: { bg: 'from-purple-500/20 to-purple-600/5', border: 'border-purple-500/30', text: 'text-purple-400', icon: 'bg-purple-500/20' },
  green: { bg: 'from-green-500/20 to-green-600/5', border: 'border-green-500/30', text: 'text-green-400', icon: 'bg-green-500/20' },
  red: { bg: 'from-red-500/20 to-red-600/5', border: 'border-red-500/30', text: 'text-red-400', icon: 'bg-red-500/20' },
};

export default function DocsPage() {
  const [expandedModule, setExpandedModule] = useState<string | null>('module-1-soc-foundations');
  const [selectedChapter, setSelectedChapter] = useState<{ moduleId: string; chapterId: string } | null>({
    moduleId: 'module-1-soc-foundations',
    chapterId: '01-introduction'
  });

  const currentModule = modules.find(m => m.id === selectedChapter?.moduleId);
  const currentChapter = currentModule?.chapters.find(c => c.id === selectedChapter?.chapterId);

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Header */}
      <div className="border-b border-cyan-500/20 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center gap-4 mb-4">
            <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
              <BookOpen className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold gradient-text">AI-SOC Textbook</h1>
              <p className="text-slate-400">Comprehensive guide to AI-powered security operations</p>
            </div>
          </div>
          <div className="flex items-center gap-6 text-sm text-slate-400">
            <span className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" /> 4 Modules
            </span>
            <span className="flex items-center gap-2">
              <FileText className="h-4 w-4" /> 10+ Chapters
            </span>
            <span className="flex items-center gap-2">
              <Clock className="h-4 w-4" /> ~15 hours total
            </span>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar - Module Navigation */}
          <div className="lg:w-80 flex-shrink-0">
            <div className="sticky top-24 space-y-4">
              {modules.map((module) => {
                const Icon = module.icon;
                const colors = colorClasses[module.color];
                const isExpanded = expandedModule === module.id;

                return (
                  <div key={module.id} className={`rounded-xl border ${colors.border} bg-gradient-to-br ${colors.bg} overflow-hidden`}>
                    <button
                      onClick={() => setExpandedModule(isExpanded ? null : module.id)}
                      className="w-full p-4 flex items-center gap-3 hover:bg-white/5 transition-colors"
                    >
                      <div className={`h-10 w-10 rounded-lg ${colors.icon} flex items-center justify-center`}>
                        <Icon className={`h-5 w-5 ${colors.text}`} />
                      </div>
                      <div className="flex-1 text-left">
                        <h3 className="font-semibold text-white text-sm">{module.title}</h3>
                        <p className="text-xs text-slate-400">{module.chapters.length} chapters</p>
                      </div>
                      {isExpanded ? (
                        <ChevronDown className="h-5 w-5 text-slate-400" />
                      ) : (
                        <ChevronRight className="h-5 w-5 text-slate-400" />
                      )}
                    </button>

                    {isExpanded && (
                      <div className="border-t border-white/10 p-2">
                        {module.chapters.map((chapter) => {
                          const isSelected = selectedChapter?.moduleId === module.id && selectedChapter?.chapterId === chapter.id;
                          return (
                            <button
                              key={chapter.id}
                              onClick={() => setSelectedChapter({ moduleId: module.id, chapterId: chapter.id })}
                              className={`w-full p-3 rounded-lg text-left transition-colors ${
                                isSelected
                                  ? `bg-white/10 ${colors.text}`
                                  : 'text-slate-400 hover:bg-white/5 hover:text-white'
                              }`}
                            >
                              <span className="text-sm font-medium">{chapter.title}</span>
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 min-w-0">
            {currentChapter ? (
              <div className="cyber-card p-8">
                {/* Chapter Header */}
                <div className="mb-8 pb-6 border-b border-cyan-500/20">
                  <div className="flex items-center gap-2 text-sm text-cyan-400 mb-2">
                    {currentModule && <currentModule.icon className="h-4 w-4" />}
                    <span>{currentModule?.title}</span>
                  </div>
                  <h2 className="text-2xl font-bold text-white mb-2">{currentChapter.title}</h2>
                  <p className="text-slate-400">{currentChapter.description}</p>
                </div>

                {/* Chapter Content */}
                <div className="prose prose-invert prose-cyan max-w-none">
                  <div
                    className="markdown-content"
                    dangerouslySetInnerHTML={{
                      __html: formatMarkdown(currentChapter.content)
                    }}
                  />
                </div>

                {/* Navigation */}
                <div className="mt-8 pt-6 border-t border-cyan-500/20 flex justify-between">
                  <PrevNextButton
                    direction="prev"
                    modules={modules}
                    currentModule={currentModule!}
                    currentChapter={currentChapter}
                    onNavigate={setSelectedChapter}
                  />
                  <PrevNextButton
                    direction="next"
                    modules={modules}
                    currentModule={currentModule!}
                    currentChapter={currentChapter}
                    onNavigate={setSelectedChapter}
                  />
                </div>
              </div>
            ) : (
              <div className="cyber-card p-8 text-center">
                <BookOpen className="h-16 w-16 text-cyan-400 mx-auto mb-4" />
                <h2 className="text-xl font-bold text-white mb-2">Select a Chapter</h2>
                <p className="text-slate-400">Choose a module and chapter from the sidebar to start learning.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <style jsx global>{`
        .markdown-content h1 { font-size: 1.75rem; font-weight: 700; color: white; margin-top: 2rem; margin-bottom: 1rem; }
        .markdown-content h2 { font-size: 1.5rem; font-weight: 600; color: white; margin-top: 1.75rem; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(6, 182, 212, 0.2); padding-bottom: 0.5rem; }
        .markdown-content h3 { font-size: 1.25rem; font-weight: 600; color: #e2e8f0; margin-top: 1.5rem; margin-bottom: 0.5rem; }
        .markdown-content p { color: #94a3b8; line-height: 1.75; margin-bottom: 1rem; }
        .markdown-content ul, .markdown-content ol { color: #94a3b8; margin-left: 1.5rem; margin-bottom: 1rem; }
        .markdown-content li { margin-bottom: 0.5rem; }
        .markdown-content strong { color: #22d3ee; }
        .markdown-content code { background: rgba(6, 182, 212, 0.1); color: #22d3ee; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.875rem; }
        .markdown-content pre { background: #0f172a; border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 0.5rem; padding: 1rem; overflow-x: auto; margin-bottom: 1rem; }
        .markdown-content pre code { background: transparent; padding: 0; }
        .markdown-content table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; }
        .markdown-content th { background: rgba(6, 182, 212, 0.1); color: #22d3ee; padding: 0.75rem; text-align: left; border: 1px solid rgba(6, 182, 212, 0.2); }
        .markdown-content td { padding: 0.75rem; border: 1px solid rgba(6, 182, 212, 0.1); color: #94a3b8; }
        .markdown-content blockquote { border-left: 4px solid #22d3ee; padding-left: 1rem; color: #94a3b8; font-style: italic; margin: 1rem 0; }
      `}</style>
    </div>
  );
}

function formatMarkdown(content: string): string {
  // Simple markdown to HTML conversion
  let html = content
    // Headers
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    // Bold
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Code blocks
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Tables (basic support)
    .replace(/\|(.+)\|/g, (match) => {
      const cells = match.split('|').filter(c => c.trim());
      if (cells.some(c => c.match(/^[-:]+$/))) {
        return ''; // Skip separator row
      }
      const isHeader = match.includes('---');
      const tag = 'td';
      return `<tr>${cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('')}</tr>`;
    })
    // Lists
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.*$)/gm, '<li>$2</li>')
    // Paragraphs
    .replace(/\n\n/g, '</p><p>')
    // Line breaks
    .replace(/\n/g, '<br/>');

  // Wrap lists
  html = html.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>');

  // Wrap tables
  if (html.includes('<tr>')) {
    html = html.replace(/(<tr>.*?<\/tr>)+/gs, '<table>$&</table>');
  }

  return `<p>${html}</p>`;
}

function PrevNextButton({
  direction,
  modules,
  currentModule,
  currentChapter,
  onNavigate
}: {
  direction: 'prev' | 'next';
  modules: typeof modules;
  currentModule: typeof modules[0];
  currentChapter: typeof modules[0]['chapters'][0];
  onNavigate: (nav: { moduleId: string; chapterId: string }) => void;
}) {
  // Find prev/next chapter
  const currentModuleIndex = modules.findIndex(m => m.id === currentModule.id);
  const currentChapterIndex = currentModule.chapters.findIndex(c => c.id === currentChapter.id);

  let targetModule: typeof modules[0] | undefined;
  let targetChapter: typeof modules[0]['chapters'][0] | undefined;

  if (direction === 'prev') {
    if (currentChapterIndex > 0) {
      targetModule = currentModule;
      targetChapter = currentModule.chapters[currentChapterIndex - 1];
    } else if (currentModuleIndex > 0) {
      targetModule = modules[currentModuleIndex - 1];
      targetChapter = targetModule.chapters[targetModule.chapters.length - 1];
    }
  } else {
    if (currentChapterIndex < currentModule.chapters.length - 1) {
      targetModule = currentModule;
      targetChapter = currentModule.chapters[currentChapterIndex + 1];
    } else if (currentModuleIndex < modules.length - 1) {
      targetModule = modules[currentModuleIndex + 1];
      targetChapter = targetModule.chapters[0];
    }
  }

  if (!targetModule || !targetChapter) {
    return <div />;
  }

  return (
    <button
      onClick={() => onNavigate({ moduleId: targetModule!.id, chapterId: targetChapter!.id })}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg border border-cyan-500/30 hover:bg-cyan-500/10 transition-colors ${
        direction === 'prev' ? '' : 'flex-row-reverse'
      }`}
    >
      {direction === 'prev' ? (
        <ChevronRight className="h-4 w-4 text-cyan-400 rotate-180" />
      ) : (
        <ChevronRight className="h-4 w-4 text-cyan-400" />
      )}
      <div className={direction === 'prev' ? 'text-left' : 'text-right'}>
        <span className="text-xs text-slate-500 block">{direction === 'prev' ? 'Previous' : 'Next'}</span>
        <span className="text-sm text-white">{targetChapter.title}</span>
      </div>
    </button>
  );
}
