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
        'module-1-soc-foundations/tools',
        'module-1-soc-foundations/alert-triage',
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
  ],
};

export default sidebars;
