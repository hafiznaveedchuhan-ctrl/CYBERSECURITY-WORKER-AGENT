import { Hero } from '@/components/Hero';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900">
      <Hero />

      {/* How It Works Section */}
      <section className="py-20 bg-gray-800/50">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-white mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <StepCard
              step={1}
              title="Paste Your Alert"
              description="Simply paste your security alert into the chat interface. Our AI understands various alert formats."
            />
            <StepCard
              step={2}
              title="AI Analysis"
              description="Our specialized agents analyze the alert, enrich IOCs, and map to MITRE ATT&CK techniques."
            />
            <StepCard
              step={3}
              title="Get Actionable Insights"
              description="Receive severity assessment, recommended actions, and auto-generated reports."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your SOC?
          </h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Join security teams using AI to reduce alert fatigue, accelerate response times,
            and improve detection coverage.
          </p>
          <a
            href="/signup"
            className="inline-block rounded-lg bg-blue-600 px-8 py-4 text-lg font-semibold text-white hover:bg-blue-500 transition-colors"
          >
            Start Free Trial
          </a>
        </div>
      </section>
    </main>
  );
}

function StepCard({
  step,
  title,
  description,
}: {
  step: number;
  title: string;
  description: string;
}) {
  return (
    <div className="text-center">
      <div className="mx-auto w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-xl mb-4">
        {step}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  );
}
