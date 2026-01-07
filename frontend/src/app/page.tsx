'use client';

import { useState, useRef, useEffect } from 'react';
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
  Activity,
  Send,
  MessageSquare,
  X,
  User,
  Loader2,
  Minimize2,
  Maximize2
} from 'lucide-react';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  agent?: string;
}

export default function Home() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isChatExpanded, setIsChatExpanded] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => typeof window !== 'undefined' ? crypto.randomUUID() : '');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/v1/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage.content, session_id: sessionId }),
      });

      if (!response.ok) throw new Error('Failed to send message');
      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: data.message || data.response || 'No response', agent: data.agent_type || data.agent },
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

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
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-br from-cyan-500/5 via-purple-500/5 to-blue-500/5 rounded-full blur-3xl" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-5xl mx-auto text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border border-cyan-500/30 mb-8 animate-fade-in backdrop-blur-sm">
              <Sparkles className="h-4 w-4 text-cyan-400" />
              <span className="text-sm text-cyan-400 font-medium">AI-Powered Security Operations</span>
              <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl font-bold mb-6 animate-slide-up">
              <span className="text-white">Transform Your</span>
              <br />
              <span className="gradient-text">Security Operations</span>
              <br />
              <span className="text-white">with </span>
              <span className="gradient-text-gold">AI Employ</span>
            </h1>

            {/* Subtitle */}
            <p className="text-xl md:text-2xl text-slate-400 mb-10 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.1s' }}>
              Intelligent threat detection, automated incident response, and expert AI Employs
              working together to protect your organization 24/7.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <Link href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/" className="cyber-btn text-white text-lg px-8 py-4" target="_blank">
                <Zap className="h-5 w-5" />
                Get Started Free
                <ArrowRight className="h-5 w-5" />
              </Link>
              <button
                onClick={() => setIsChatOpen(true)}
                className="cyber-btn-outline text-lg px-8 py-4"
              >
                <Bot className="h-5 w-5" />
                Try AI Employ Now
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto animate-slide-up" style={{ animationDelay: '0.3s' }}>
              <StatCard number="7" label="AI Employs" icon={<Bot className="h-5 w-5" />} />
              <StatCard number="24/7" label="Monitoring" icon={<Activity className="h-5 w-5" />} />
              <StatCard number="95%" label="Accuracy" icon={<Target className="h-5 w-5" />} />
              <StatCard number="10x" label="Faster Response" icon={<Zap className="h-5 w-5" />} />
            </div>
          </div>
        </div>
      </section>

      {/* AI Employs Section */}
      <section className="py-24 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="text-white">Meet Your </span>
              <span className="gradient-text-gold">AI Employ Team</span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Seven specialized AI Employs working together to handle every aspect of security operations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <AgentCard
              name="SUPERVISOR"
              description="Routes requests to the right specialist AI Employ"
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
              description="Our specialized AI Employs analyze the alert, enrich IOCs, map to MITRE ATT&CK techniques, and assess severity."
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
              Join security teams using AI Employs to reduce alert fatigue, accelerate response times,
              and improve detection coverage.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/" className="cyber-btn text-white text-lg px-10 py-4" target="_blank">
                <Zap className="h-5 w-5" />
                Get Started Free
              </Link>
              <Link href="/signup" className="cyber-btn-outline text-lg px-10 py-4">
                Create Account
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

      {/* Floating Chat Widget */}
      {!isChatOpen && (
        <button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-6 right-6 z-50 h-16 w-16 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-2xl hover:scale-110 transition-transform duration-300 group"
        >
          <div className="absolute inset-0 bg-cyan-500 rounded-2xl blur-lg opacity-50 group-hover:opacity-75 transition-opacity" />
          <MessageSquare className="h-7 w-7 text-white relative z-10" />
          <span className="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-green-500 border-2 border-slate-950 animate-pulse" />
        </button>
      )}

      {/* Chat Modal */}
      {isChatOpen && (
        <div
          className={`fixed z-50 transition-all duration-300 ${
            isChatExpanded
              ? 'inset-4 md:inset-8'
              : 'bottom-6 right-6 w-[380px] h-[600px]'
          }`}
        >
          <div className="h-full w-full flex flex-col rounded-2xl overflow-hidden border border-cyan-500/30 bg-slate-900/95 backdrop-blur-xl shadow-2xl">
            {/* Chat Header */}
            <div className="flex items-center justify-between p-4 border-b border-cyan-500/20 bg-gradient-to-r from-slate-900 to-slate-800">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="absolute inset-0 bg-cyan-500 blur-lg opacity-30" />
                  <div className="relative h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
                    <Bot className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold text-white">AI Employ Assistant</h3>
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-xs text-slate-400">Online</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsChatExpanded(!isChatExpanded)}
                  className="h-8 w-8 rounded-lg hover:bg-slate-800 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                  {isChatExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
                </button>
                <button
                  onClick={() => setIsChatOpen(false)}
                  className="h-8 w-8 rounded-lg hover:bg-slate-800 flex items-center justify-center text-slate-400 hover:text-white transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-center py-8">
                  <div className="h-20 w-20 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 flex items-center justify-center mb-6 border border-cyan-500/30 pulse-glow">
                    <Sparkles className="h-10 w-10 text-cyan-400" />
                  </div>
                  <h4 className="text-xl font-semibold gradient-text mb-2">AI Employ Ready</h4>
                  <p className="text-sm text-slate-400 max-w-xs mb-6">
                    Ask me about threat analysis, IOC enrichment, MITRE mapping, or security incidents.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2">
                    {['Analyze phishing email', 'Check IP reputation', 'Generate YARA rule'].map((suggestion) => (
                      <button
                        key={suggestion}
                        onClick={() => setInput(suggestion)}
                        className="text-xs px-3 py-1.5 rounded-full bg-slate-800 border border-slate-700 text-slate-400 hover:text-cyan-400 hover:border-cyan-500/50 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div
                    className={`flex-shrink-0 h-8 w-8 rounded-lg flex items-center justify-center ${
                      message.role === 'user'
                        ? 'bg-purple-500/20 border border-purple-500/30'
                        : 'bg-cyan-500/20 border border-cyan-500/30'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <User className="h-4 w-4 text-purple-400" />
                    ) : (
                      <Bot className="h-4 w-4 text-cyan-400" />
                    )}
                  </div>
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-purple-500/20 to-purple-600/10 border border-purple-500/30'
                        : 'bg-slate-800/80 border border-slate-700'
                    }`}
                  >
                    {message.agent && (
                      <span className="text-xs text-cyan-400 font-medium block mb-1">
                        [{message.agent}]
                      </span>
                    )}
                    <p className="text-sm text-slate-200 whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex gap-3">
                  <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center">
                    <Bot className="h-4 w-4 text-cyan-400" />
                  </div>
                  <div className="bg-slate-800/80 border border-slate-700 rounded-2xl px-4 py-3">
                    <div className="flex items-center gap-2">
                      <Loader2 className="h-4 w-4 text-cyan-400 animate-spin" />
                      <span className="text-sm text-slate-400">AI Employ analyzing...</span>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-cyan-500/20 bg-slate-900/95">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
                  placeholder="Describe your security concern..."
                  className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder:text-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/50 transition-all"
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !input.trim()}
                  className="h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Send className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}

function StatCard({ number, label, icon }: { number: string; label: string; icon: React.ReactNode }) {
  return (
    <div className="cyber-card text-center p-4 hover:scale-105 transition-transform duration-300">
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
    <div className={`relative p-6 rounded-2xl bg-gradient-to-br ${colorClasses[color]} border backdrop-blur-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-xl group`}>
      <div className={`mb-4 ${iconColorClasses[color]} group-hover:scale-110 transition-transform`}>{icon}</div>
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
    <div className="cyber-card p-8 text-center relative hover:scale-105 transition-transform duration-300">
      {/* Step Number */}
      <div className="absolute -top-4 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-white font-bold text-sm shadow-lg">
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
    <div className="cyber-card p-6 group hover:scale-105 transition-transform duration-300">
      <div className="text-cyan-400 mb-4 group-hover:scale-110 transition-transform">{icon}</div>
      <h3 className="text-lg font-bold text-white mb-2">{title}</h3>
      <p className="text-sm text-slate-400">{description}</p>
    </div>
  );
}
