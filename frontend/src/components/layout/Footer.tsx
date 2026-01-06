import Link from 'next/link';
import { Shield, Github, Linkedin, Mail, ExternalLink, Heart, Code2, Brain } from 'lucide-react';

export function Footer() {
  return (
    <footer className="relative border-t border-cyan-500/10 bg-gradient-to-b from-slate-900 to-slate-950">
      {/* Glow Effect */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 left-1/4 w-80 h-80 bg-cyan-500/5 rounded-full blur-3xl" />
        <div className="absolute -top-40 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
      </div>

      <div className="container mx-auto px-4 py-12 relative z-10">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <Link href="/" className="flex items-center gap-3 mb-4 group">
              <div className="relative">
                <div className="absolute inset-0 bg-cyan-500 blur-lg opacity-30 group-hover:opacity-50 transition-opacity" />
                <div className="relative h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
                  <Shield className="h-7 w-7 text-white" />
                </div>
              </div>
              <div>
                <span className="font-bold text-xl gradient-text">AI-SOC Platform</span>
                <p className="text-xs text-slate-500">Next-Gen Security Operations</p>
              </div>
            </Link>
            <p className="text-slate-400 text-sm leading-relaxed mb-4">
              AI-powered Security Operations Center Platform. Transform your cybersecurity
              workflow with intelligent threat detection, automated triage, and expert AI agents.
            </p>
            <div className="flex gap-3">
              <SocialLink href="https://github.com/hafiznaveedchuhan-ctrl" icon={<Github className="h-5 w-5" />} label="GitHub" />
              <SocialLink href="https://linkedin.com" icon={<Linkedin className="h-5 w-5" />} label="LinkedIn" />
              <SocialLink href="mailto:contact@aisoc.dev" icon={<Mail className="h-5 w-5" />} label="Email" />
            </div>
          </div>

          {/* Platform Links */}
          <div>
            <h4 className="font-semibold text-white mb-4 flex items-center gap-2">
              <span className="h-1 w-4 bg-cyan-500 rounded-full" />
              Platform
            </h4>
            <ul className="space-y-3">
              <FooterLink href="/chat">AI Chat Assistant</FooterLink>
              <FooterLink href="/dashboard">Security Dashboard</FooterLink>
              <FooterLink href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/" external>
                Documentation
              </FooterLink>
              <FooterLink href="/tools">Security Tools</FooterLink>
            </ul>
          </div>

          {/* Learning Resources */}
          <div>
            <h4 className="font-semibold text-white mb-4 flex items-center gap-2">
              <span className="h-1 w-4 bg-purple-500 rounded-full" />
              Learn
            </h4>
            <ul className="space-y-3">
              <FooterLink href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/docs/module-1-soc-foundations" external>
                SOC Foundations
              </FooterLink>
              <FooterLink href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/docs/module-2-agentic-ai" external>
                AI Agents
              </FooterLink>
              <FooterLink href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/docs/module-3-ai-soc-workflows" external>
                AI Workflows
              </FooterLink>
              <FooterLink href="https://attack.mitre.org/" external>
                MITRE ATT&CK
              </FooterLink>
            </ul>
          </div>

          {/* AI Agents */}
          <div>
            <h4 className="font-semibold text-white mb-4 flex items-center gap-2">
              <span className="h-1 w-4 bg-green-500 rounded-full" />
              AI Agents
            </h4>
            <div className="grid grid-cols-2 gap-2">
              <AgentBadge name="Supervisor" color="cyan" />
              <AgentBadge name="Triage" color="red" />
              <AgentBadge name="Enrichment" color="blue" />
              <AgentBadge name="ThreatIntel" color="orange" />
              <AgentBadge name="Detection" color="green" />
              <AgentBadge name="Incident" color="purple" />
              <AgentBadge name="Report" color="teal" />
            </div>
          </div>
        </div>

        {/* Divider with gradient */}
        <div className="h-px bg-gradient-to-r from-transparent via-cyan-500/30 to-transparent mb-8" />

        {/* Bottom Section - Owner Info */}
        <div className="flex flex-col items-center text-center space-y-6">
          {/* Owner Credit - Prominent Display */}
          <div className="cyber-card p-6 max-w-md mx-auto">
            <div className="flex items-center justify-center gap-3 mb-3">
              <div className="h-12 w-12 rounded-full bg-gradient-to-br from-cyan-400 via-blue-500 to-purple-600 flex items-center justify-center pulse-glow">
                <Code2 className="h-6 w-6 text-white" />
              </div>
            </div>
            <p className="text-slate-400 text-sm mb-2">Proprietor & Creator</p>
            <h3 className="text-2xl font-bold gradient-text-gold mb-1">
              Hafiz Naveed Uddin
            </h3>
            <div className="flex items-center justify-center gap-2 text-cyan-400">
              <Brain className="h-4 w-4" />
              <span className="text-sm font-semibold">Agentic AI Developer / Architect</span>
            </div>
          </div>

          {/* Copyright & Tech Stack */}
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 text-sm text-slate-500">
            <p className="flex items-center gap-1">
              &copy; {new Date().getFullYear()} AI-SOC Platform. Built with
              <Heart className="h-4 w-4 text-red-500 mx-1 animate-pulse" />
              by Hafiz Naveed Uddin
            </p>
            <span className="hidden md:inline text-slate-700">|</span>
            <p className="flex items-center gap-2">
              <span className="text-cyan-500">Next.js</span>
              <span className="text-slate-700">+</span>
              <span className="text-green-500">FastAPI</span>
              <span className="text-slate-700">+</span>
              <span className="text-purple-500">LangChain</span>
            </p>
          </div>

          {/* Tagline */}
          <p className="text-xs text-slate-600 max-w-lg">
            Empowering security professionals with AI-driven threat detection, automated incident response,
            and intelligent security operations.
          </p>
        </div>
      </div>
    </footer>
  );
}

function FooterLink({
  href,
  children,
  external = false
}: {
  href: string;
  children: React.ReactNode;
  external?: boolean;
}) {
  if (external) {
    return (
      <li>
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-slate-400 hover:text-cyan-400 transition-colors flex items-center gap-1 group"
        >
          {children}
          <ExternalLink className="h-3 w-3 opacity-0 group-hover:opacity-100 transition-opacity" />
        </a>
      </li>
    );
  }

  return (
    <li>
      <Link
        href={href}
        className="text-slate-400 hover:text-cyan-400 transition-colors"
      >
        {children}
      </Link>
    </li>
  );
}

function SocialLink({
  href,
  icon,
  label
}: {
  href: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={label}
      className="h-10 w-10 rounded-lg bg-slate-800/50 border border-slate-700/50 flex items-center justify-center text-slate-400 hover:text-cyan-400 hover:border-cyan-500/50 hover:bg-slate-800 transition-all duration-200"
    >
      {icon}
    </a>
  );
}

function AgentBadge({ name, color }: { name: string; color: string }) {
  const colorClasses: Record<string, string> = {
    cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    orange: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
    green: 'bg-green-500/10 text-green-400 border-green-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    teal: 'bg-teal-500/10 text-teal-400 border-teal-500/20',
  };

  return (
    <span className={`text-xs px-2 py-1 rounded-md border ${colorClasses[color]}`}>
      {name}
    </span>
  );
}
