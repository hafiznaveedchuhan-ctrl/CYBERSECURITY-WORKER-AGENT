import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
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
        'detection/detection-strategies',
        'detection/log-analysis',
      ],
    },
    {
      type: 'category',
      label: 'Incident Response',
      items: [
        'incident-response/ir-process',
        'incident-response/playbooks',
        'incident-response/containment',
      ],
    },
    {
      type: 'category',
      label: 'Threat Intelligence',
      items: [
        'threat-intel/intelligence-lifecycle',
        'threat-intel/ioc-analysis',
        'threat-intel/threat-actors',
      ],
    },
    {
      type: 'category',
      label: 'AI Agents',
      items: [
        'agents/supervisor',
        'agents/triage',
        'agents/enrichment',
        'agents/threat-intel',
        'agents/detection-engineer',
        'agents/incident-commander',
        'agents/report-writer',
      ],
    },
  ],
};

export default sidebars;
