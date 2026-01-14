import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: SOC Foundations',
      items: [
        'module-1-soc-foundations/index',
        'module-1-soc-foundations/introduction',
        'module-1-soc-foundations/team-roles',
        'module-1-soc-foundations/alert-triage',
        'module-1-soc-foundations/tools',
        'module-1-soc-foundations/incident-response',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Agentic AI',
      items: [
        'module-2-agentic-ai/index',
        'module-2-agentic-ai/introduction',
        'module-2-agentic-ai/architecture',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: AI-SOC Workflows',
      items: [
        'module-3-ai-soc-workflows/index',
        'module-3-ai-soc-workflows/ai-triage',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: AI Security',
      items: [
        'module-4-ai-security/index',
        'module-4-ai-security/risks',
      ],
    },
    {
      type: 'category',
      label: 'Fundamentals',
      items: [
        'fundamentals/soc-overview',
        'fundamentals/threat-landscape',
        'fundamentals/security-frameworks',
      ],
    },
    {
      type: 'category',
      label: 'Detection Engineering',
      items: [
        'detection/sigma-rules',
      ],
    },
    {
      type: 'category',
      label: 'Incident Response',
      items: [
        'incident-response/ir-process',
      ],
    },
    {
      type: 'category',
      label: 'Module 6: Advanced Implementation',
      items: [
        'module-6-advanced-implementation/index',
        'module-6-advanced-implementation/01-ransomware-simulation',
        'module-6-advanced-implementation/02-accuracy-deep-dive',
        'module-6-advanced-implementation/03-detection-rules',
        'module-6-advanced-implementation/04-compliance',
        'module-6-advanced-implementation/05-reporting',
      ],
    },
    {
      type: 'category',
      label: 'Module 7: Future-Proofing',
      items: [
        'module-7-future-proofing/index',
        'module-7-future-proofing/01-continuous-learning',
        'module-7-future-proofing/02-zero-day-detection',
        'module-7-future-proofing/03-threat-actor-evolution',
        'module-7-future-proofing/04-global-soc',
      ],
    },
  ],
};

export default sidebars;
