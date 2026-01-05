export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="mb-4 text-4xl font-bold text-primary">AI SOC Platform</h1>
        <p className="mb-8 text-lg text-muted-foreground">
          AI-powered Security Operations Center Platform
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/chat"
            className="rounded-lg bg-primary px-6 py-3 text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            Start Chatting
          </a>
          <a
            href={process.env.NEXT_PUBLIC_DOCS_URL || '/docs'}
            className="rounded-lg border border-border px-6 py-3 hover:bg-accent transition-colors"
          >
            View Textbook
          </a>
        </div>
      </div>
    </main>
  );
}
