import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/intro">
            Get Started
          </Link>
          <Link
            className="button button--outline button--lg"
            to="/module-1-soc-foundations"
            style={{marginLeft: '1rem', borderColor: '#38bdf8', color: '#38bdf8'}}>
            View Modules
          </Link>
        </div>
      </div>
    </header>
  );
}

const FeatureList = [
  {
    title: 'SOC Foundations',
    icon: '🛡️',
    description: 'Learn the fundamentals of Security Operations Centers, alert triage, and incident response.',
    link: '/module-1-soc-foundations',
  },
  {
    title: 'AI-Powered Agents',
    icon: '🤖',
    description: 'Understand how AI agents enhance security workflows with intelligent automation.',
    link: '/module-2-agentic-ai',
  },
  {
    title: 'AI-SOC Workflows',
    icon: '⚡',
    description: 'Master AI-assisted triage, threat detection, and automated response strategies.',
    link: '/module-3-ai-soc-workflows',
  },
  {
    title: 'AI Security',
    icon: '🔒',
    description: 'Learn about AI security risks, adversarial attacks, and defense strategies.',
    link: '/module-4-ai-security',
  },
];

function Feature({title, icon, description, link}) {
  return (
    <div className={clsx('col col--3')}>
      <Link to={link} className={styles.featureCard}>
        <div className={styles.featureIcon}>{icon}</div>
        <h3>{title}</h3>
        <p>{description}</p>
      </Link>
    </div>
  );
}

function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}

function AgentSection() {
  const agents = [
    { name: 'SUPERVISOR', role: 'Routes requests to specialists', color: '#38bdf8' },
    { name: 'TRIAGE', role: 'Alert classification & severity', color: '#dc2626' },
    { name: 'ENRICHMENT', role: 'IOC reputation gathering', color: '#2563eb' },
    { name: 'THREATINTEL', role: 'MITRE ATT&CK mapping', color: '#ea580c' },
    { name: 'DETECTION', role: 'Sigma & YARA rules', color: '#16a34a' },
    { name: 'INCIDENT-COMMANDER', role: 'Response coordination', color: '#be185d' },
    { name: 'REPORT-WRITER', role: 'Automated reporting', color: '#0891b2' },
  ];

  return (
    <section className={styles.agentSection}>
      <div className="container">
        <h2 className={styles.sectionTitle}>Domain Expert Agents</h2>
        <p className={styles.sectionSubtitle}>Seven specialized AI agents for security operations</p>
        <div className={styles.agentGrid}>
          {agents.map((agent, idx) => (
            <div key={idx} className={styles.agentCard} style={{borderColor: agent.color}}>
              <div className={styles.agentName} style={{color: agent.color}}>{agent.name}</div>
              <div className={styles.agentRole}>{agent.role}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="AI-Powered Security Operations Center - Intelligent Threat Detection & Response">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <AgentSection />
      </main>
    </Layout>
  );
}
