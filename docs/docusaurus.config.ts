import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'AI-SOC Platform',
  tagline: 'AI-Powered Security Operations Center - Intelligent Threat Detection & Response',
  favicon: 'img/favicon.ico',

  // GitHub Pages URL
  url: 'https://hafiznaveedchuhan-ctrl.github.io',
  baseUrl: '/CYBERSECURITY-WORKER-AGENT/',

  organizationName: 'hafiznaveedchuhan-ctrl',
  projectName: 'CYBERSECURITY-WORKER-AGENT',
  trailingSlash: false,
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: '/',
          editUrl: 'https://github.com/hafiznaveedchuhan-ctrl/CYBERSECURITY-WORKER-AGENT/tree/master/docs/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Professional color mode settings
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    // Announcement bar for new features
    announcementBar: {
      id: 'ai_soc_launch',
      content: '🚀 <strong>AI-SOC Platform</strong> - Transform your Security Operations with AI-powered agents!',
      backgroundColor: '#0ea5e9',
      textColor: '#ffffff',
      isCloseable: true,
    },
    image: 'img/social-card.jpg',
    navbar: {
      title: 'AI-SOC Platform',
      logo: {
        alt: 'AI-SOC Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: '📚 Learn',
        },
        {
          to: '/module-1-soc-foundations/',
          label: '🛡️ SOC Foundations',
          position: 'left',
        },
        {
          to: '/module-2-agentic-ai/',
          label: '🤖 AI Agents',
          position: 'left',
        },
        {
          href: 'https://github.com/hafiznaveedchuhan-ctrl/CYBERSECURITY-WORKER-AGENT',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '📖 Documentation',
          items: [
            {
              label: 'Introduction',
              to: '/',
            },
            {
              label: 'SOC Foundations',
              to: '/module-1-soc-foundations/',
            },
            {
              label: 'AI Agents',
              to: '/module-2-agentic-ai/',
            },
          ],
        },
        {
          title: '🔧 Platform',
          items: [
            {
              label: 'AI-SOC Workflows',
              to: '/module-3-ai-soc-workflows/',
            },
            {
              label: 'AI Security',
              to: '/module-4-ai-security/',
            },
          ],
        },
        {
          title: '🌐 Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/hafiznaveedchuhan-ctrl/CYBERSECURITY-WORKER-AGENT',
            },
            {
              label: 'Issues',
              href: 'https://github.com/hafiznaveedchuhan-ctrl/CYBERSECURITY-WORKER-AGENT/issues',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} AI-SOC Platform. Built with ❤️ for Security Professionals.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml', 'typescript', 'javascript'],
    },
    // Algolia search (optional - can be configured later)
    // algolia: {
    //   appId: 'YOUR_APP_ID',
    //   apiKey: 'YOUR_API_KEY',
    //   indexName: 'ai-soc',
    // },
  } satisfies Preset.ThemeConfig,
};

export default config;
