import Link from 'next/link';
import {
  Shield,
  Bot,
  Zap,
  FileSearch,
  AlertTriangle,
  Target,
  FileText,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Brain,
  Lock,
  Activity
} from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden hero-gradient">
        {/* Animated Background */}
        <div className="absolute inset-0 grid-bg" />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-slate-950" />

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl float" />
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl float" style={{ animationDelay: '2s' }} />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/20 mb-8 animate-fade-in">
              <Sparkles className="h-4 w-4 text-cyan-400" />
              <span className="text-sm text-cyan-400 font-medium">AI-Powered Security Operations</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-slide-up">
              <span className="text-white">Transform Your</span>
              <br />
              <span className="gradient-text">Security Operations</span>
              <br />
              <span className="text-white">with AI</span>
            </h1>

            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-slate-400 mb-10 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Intelligent threat detection, automated incident response, and expert AI agents
              working together to protect your organization 24/7.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Link href="/signup" className="cyber-btn text-white text-lg px-8 py-4">
                <Zap className="h-5 w-5" />
                Get Started Free
                <ArrowRight className="h-5 w-5" />
              </Link>
              <Link href="/chat" className="cyber-btn-outline text-lg px-8 py-4">
                <Bot className="h-5 w-5" />
                Try AI Chat
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <StatCard number="7" label="AI Agents" icon={<Bot className="h-5 w-5" />} />
              <StatCard number="24/7" label="Monitoring" icon={<Activity className="h-5 w-5" />} />
              <StatCard number="95%" label="Accuracy" icon={<Target className="h-5 w-5" />} />
              <StatCard number="10x" label="Faster Response" icon={<Zap className="h-5 w-5" />} />
            </div>
          </div>
        </div>
      </section>

      {/* AI Agents Section */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="text-white">Meet Your </span>
              <span className="gradient-text">AI Security Team</span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Seven specialized AI agents working together to handle every aspect of security operations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <AgentCard
              name="SUPERVISOR"
              description="Routes requests to the right specialist agent"
              icon={<Brain className="h-6 w-6" />}
              color="cyan"
            />
            <AgentCard
              name="TRIAGE"
              description="Alert classification and severity assessment"
              icon={<AlertTriangle className="h-6 w-6" />}
              color="red"
            />
            <AgentCard
              name="ENRICHMENT"
              description="IOC reputation and context gathering"
              icon={<FileSearch className="h-6 w-6" />}
              color="blue"
            />
            <AgentCard
              name="THREATINTEL"
              description="MITRE ATT&CK mapping and threat analysis"
              icon={<Target className="h-6 w-6" />}
              color="orange"
            />
            <AgentCard
              name="DETECTION"
              description="Sigma and YARA rule generation"
              icon={<Shield className="h-6 w-6" />}
              color="green"
            />
            <AgentCard
              name="INCIDENT"
              description="Response coordination and approvals"
              icon={<Zap className="h-6 w-6" />}
              color="purple"
            />
            <AgentCard
              name="REPORT"
              description="Automated incident report generation"
              icon={<FileText className="h-6 w-6" />}
              color="teal"
            />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/5 via-transparent to-purple-500/5" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="text-white">How It </span>
              <span className="gradient-text">Works</span>
            </h2>
            <p className="text-xl text-slate-400">Three simple steps to AI-powered security</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <StepCard
              step={1}
              title="Paste Your Alert"
              description="Simply paste your security alert into the chat interface. Our AI understands various alert formats from any SIEM or security tool."
              icon={<FileText className="h-8 w-8" />}
            />
            <StepCard
              step={2}
              title="AI Analysis"
              description="Our specialized agents analyze the alert, enrich IOCs, map to MITRE ATT&CK techniques, and assess severity."
              icon={<Brain className="h-8 w-8" />}
            />
            <StepCard
              step={3}
              title="Get Insights"
              description="Receive detailed analysis, recommended actions, detection rules, and auto-generated reports in seconds."
              icon={<Sparkles className="h-8 w-8" />}
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 relative">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="text-white">Enterprise-Grade </span>
              <span className="gradient-text">Features</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Lock className="h-6 w-6" />}
              title="Secure by Design"
              description="Enterprise-grade security with encryption, audit logs, and role-based access control."
            />
            <FeatureCard
              icon={<Zap className="h-6 w-6" />}
              title="Real-time Analysis"
              description="Get instant threat analysis and recommendations with sub-second response times."
            />
            <FeatureCard
              icon={<Target className="h-6 w-6" />}
              title="MITRE ATT&CK"
              description="Automatic mapping to MITRE ATT&CK framework for comprehensive threat intelligence."
            />
            <FeatureCard
              icon={<FileSearch className="h-6 w-6" />}
              title="IOC Enrichment"
              description="Automatic enrichment of indicators with reputation data from multiple sources."
            />
            <FeatureCard
              icon={<Shield className="h-6 w-6" />}
              title="Detection Rules"
              description="Auto-generate Sigma and YARA rules from your security incidents."
            />
            <FeatureCard
              icon={<FileText className="h-6 w-6" />}
              title="Auto Reports"
              description="Generate professional incident reports with one click."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 relative overflow-hidden">
        <div className="absolute inset-0 hero-gradient" />
        <div className="absolute inset-0 grid-bg opacity-50" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your SOC?
            </h2>
            <p className="text-xl text-slate-400 mb-10 max-w-2xl mx-auto">
              Join security teams using AI to reduce alert fatigue, accelerate response times,
              and improve detection coverage.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/signup" className="cyber-btn text-white text-lg px-10 py-4">
                <Zap className="h-5 w-5" />
                Start Free Trial
              </Link>
              <Link
                href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/"
                className="cyber-btn-outline text-lg px-10 py-4"
              >
                View Documentation
              </Link>
            </div>

            {/* Trust Badges */}
            <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-slate-500">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>No Credit Card Required</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>Free Forever Plan</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <span>Cancel Anytime</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

function StatCard({ number, label, icon }: { number: string; label: string; icon: React.ReactNode }) {
  return (
    <div className="cyber-card text-center p-4">
      <div className="flex items-center justify-center gap-2 mb-2">
        <span className="text-cyan-400">{icon}</span>
        <span className="text-3xl font-bold gradient-text">{number}</span>
      </div>
      <span className="text-sm text-slate-400">{label}</span>
    </div>
  );
}

function AgentCard({
  name,
  description,
  icon,
  color
}: {
  name: string;
  description: string;
  icon: React.ReactNode;
  color: string;
}) {
  const colorClasses: Record<string, string> = {
    cyan: 'from-cyan-500/20 to-cyan-600/5 border-cyan-500/30 hover:border-cyan-400/50',
    red: 'from-red-500/20 to-red-600/5 border-red-500/30 hover:border-red-400/50',
    blue: 'from-blue-500/20 to-blue-600/5 border-blue-500/30 hover:border-blue-400/50',
    orange: 'from-orange-500/20 to-orange-600/5 border-orange-500/30 hover:border-orange-400/50',
    green: 'from-green-500/20 to-green-600/5 border-green-500/30 hover:border-green-400/50',
    purple: 'from-purple-500/20 to-purple-600/5 border-purple-500/30 hover:border-purple-400/50',
    teal: 'from-teal-500/20 to-teal-600/5 border-teal-500/30 hover:border-teal-400/50',
  };

  const iconColorClasses: Record<string, string> = {
    cyan: 'text-cyan-400',
    red: 'text-red-400',
    blue: 'text-blue-400',
    orange: 'text-orange-400',
    green: 'text-green-400',
    purple: 'text-purple-400',
    teal: 'text-teal-400',
  };

  return (
    <div className={`relative p-6 rounded-2xl bg-gradient-to-br ${colorClasses[color]} border backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 group`}>
      <div className={`mb-4 ${iconColorClasses[color]}`}>{icon}</div>
      <h3 className="font-bold text-white mb-2 text-lg">{name}</h3>
      <p className="text-sm text-slate-400">{description}</p>
    </div>
  );
}

function StepCard({
  step,
  title,
  description,
  icon
}: {
  step: number;
  title: string;
  description: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="cyber-card p-8 text-center relative">
      {/* Step Number */}
      <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-white font-bold text-sm">
        {step}
      </div>

      <div className="text-cyan-400 mb-4 flex justify-center">{icon}</div>
      <h3 className="text-xl font-bold text-white mb-3">{title}</h3>
      <p className="text-slate-400">{description}</p>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="cyber-card p-6 group">
      <div className="text-cyan-400 mb-4 group-hover:scale-110 transition-transform">{icon}</div>
      <h3 className="text-lg font-bold text-white mb-2">{title}</h3>
      <p className="text-sm text-slate-400">{description}</p>
    </div>
  );
}
