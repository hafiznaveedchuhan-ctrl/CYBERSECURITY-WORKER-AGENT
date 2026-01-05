'use client';

import Link from 'next/link';

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gray-900 py-20 sm:py-32">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-0 -translate-x-1/2 blur-3xl opacity-20">
          <div
            className="aspect-[1155/678] w-[72.1875rem] bg-gradient-to-tr from-blue-500 to-purple-500"
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
          />
        </div>
      </div>

      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">
            AI-Powered{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              Security Operations
            </span>
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-300">
            Transform your SOC with intelligent AI agents. Automate alert triage, accelerate
            incident response, and learn security operations with our interactive textbook.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link
              href="/signup"
              className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 transition-colors"
            >
              Get Started
            </Link>
            <Link
              href="/docs"
              className="text-sm font-semibold leading-6 text-white hover:text-blue-400 transition-colors"
            >
              Explore Textbook <span aria-hidden="true">→</span>
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mx-auto mt-16 max-w-5xl">
          <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <FeatureCard
              icon="🤖"
              title="AI Agents"
              description="Specialized agents for triage, enrichment, threat intel, and incident response."
            />
            <FeatureCard
              icon="📚"
              title="Interactive Textbook"
              description="Learn security operations with AI-assisted explanations and real-world examples."
            />
            <FeatureCard
              icon="⚡"
              title="Rapid Triage"
              description="Classify and prioritize alerts in seconds with AI-powered analysis."
            />
            <FeatureCard
              icon="📝"
              title="Auto Reports"
              description="Generate comprehensive incident reports with one click."
            />
            <FeatureCard
              icon="🛡️"
              title="MITRE ATT&CK"
              description="Automatic mapping to MITRE techniques for every alert."
            />
            <FeatureCard
              icon="🔒"
              title="Human-in-Loop"
              description="Critical actions require human approval for safety."
            />
          </div>
        </div>

        {/* Stats */}
        <div className="mx-auto mt-16 max-w-4xl">
          <div className="grid grid-cols-2 gap-8 sm:grid-cols-4">
            <StatItem value="<30s" label="Avg Triage Time" />
            <StatItem value="95%" label="Alert Coverage" />
            <StatItem value="7" label="AI Agents" />
            <StatItem value="24/7" label="Availability" />
          </div>
        </div>
      </div>
    </section>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="rounded-xl bg-gray-800/50 p-6 border border-gray-700 hover:border-blue-500/50 transition-colors">
      <span className="text-3xl">{icon}</span>
      <h3 className="mt-4 text-lg font-semibold text-white">{title}</h3>
      <p className="mt-2 text-sm text-gray-400">{description}</p>
    </div>
  );
}

function StatItem({ value, label }: { value: string; label: string }) {
  return (
    <div className="text-center">
      <div className="text-3xl font-bold text-blue-400">{value}</div>
      <div className="mt-1 text-sm text-gray-400">{label}</div>
    </div>
  );
}
