import Link from 'next/link';

export function Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-bold text-lg mb-4">AI SOC Platform</h3>
            <p className="text-sm text-muted-foreground">
              AI-powered Security Operations Center for modern cybersecurity teams.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Platform</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/chat" className="hover:text-foreground transition-colors">
                  AI Chat
                </Link>
              </li>
              <li>
                <Link
                  href={process.env.NEXT_PUBLIC_DOCS_URL || '/docs'}
                  className="hover:text-foreground transition-colors"
                >
                  Textbook
                </Link>
              </li>
              <li>
                <Link href="/tools" className="hover:text-foreground transition-colors">
                  Security Tools
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <Link href="/docs/fundamentals" className="hover:text-foreground transition-colors">
                  SOC Fundamentals
                </Link>
              </li>
              <li>
                <Link href="/docs/detection" className="hover:text-foreground transition-colors">
                  Detection Engineering
                </Link>
              </li>
              <li>
                <Link href="/docs/incident-response" className="hover:text-foreground transition-colors">
                  Incident Response
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Links</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>
                <a
                  href="https://github.com/hafiznaveedchuhan-ctrl/CYBERSECURITY-WORKER-AGENT"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors"
                >
                  GitHub
                </a>
              </li>
              <li>
                <a
                  href="https://attack.mitre.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-foreground transition-colors"
                >
                  MITRE ATT&CK
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t mt-8 pt-8 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} AI SOC Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
