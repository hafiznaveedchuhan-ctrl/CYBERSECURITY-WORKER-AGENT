'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';
import { Menu, X, Shield, MessageSquare, BookOpen, LogOut, User } from 'lucide-react';

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-gradient-to-r from-cyan-500/20 via-purple-500/10 to-cyan-500/20 bg-gradient-to-r from-slate-900/90 via-slate-800/80 to-slate-900/90 backdrop-blur-xl shadow-xl shadow-cyan-500/10">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative">
              <div className="absolute inset-0 bg-cyan-500 blur-lg opacity-50 group-hover:opacity-100 transition-opacity duration-300" />
              <div className="relative h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg group-hover:shadow-2xl group-hover:shadow-cyan-500/50 transition-all duration-300">
                <Shield className="h-6 w-6 text-white group-hover:scale-110 transition-transform duration-300" />
              </div>
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg gradient-text group-hover:opacity-80 transition-opacity">AI-SOC Employ</span>
              <span className="text-[10px] text-cyan-400/70 -mt-1">Next-Gen Security</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-1 bg-gradient-to-r from-slate-900/50 to-slate-800/30 rounded-2xl p-1.5 border border-cyan-500/20 backdrop-blur-md hover:border-cyan-500/40 transition-all duration-300">
            <NavLink href="/chat" icon={<MessageSquare className="h-4 w-4" />}>
              AI Chat
            </NavLink>
            <NavLink href="/dashboard" icon={<Shield className="h-4 w-4" />}>
              Dashboard
            </NavLink>
            <NavLink
              href={process.env.NEXT_PUBLIC_DOCS_URL || 'https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/'}
              icon={<BookOpen className="h-4 w-4" />}
              external
            >
              Docs
            </NavLink>
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <>
                <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 hover:border-cyan-400/50 transition-all duration-300">
                  <User className="h-4 w-4 text-cyan-400" />
                  <span className="text-sm text-slate-300">{user?.email}</span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => logout()}
                  className="text-slate-400 hover:text-white hover:bg-slate-800/80 rounded-lg transition-all duration-300"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button variant="ghost" size="sm" asChild className="text-slate-300 hover:text-cyan-400 hover:bg-slate-800/50 rounded-lg transition-all duration-300">
                  <Link href="/login">Login</Link>
                </Button>
                <Button size="sm" asChild className="cyber-btn text-white border-0 rounded-lg">
                  <Link href="/signup">Sign Up Free</Link>
                </Button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-slate-800 transition-colors"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? (
              <X className="h-6 w-6 text-slate-300" />
            ) : (
              <Menu className="h-6 w-6 text-slate-300" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-slate-800 animate-slide-up">
            <div className="flex flex-col gap-2">
              <MobileNavLink href="/chat" onClick={() => setIsMenuOpen(false)}>
                <MessageSquare className="h-5 w-5" /> AI Chat
              </MobileNavLink>
              <MobileNavLink href="/dashboard" onClick={() => setIsMenuOpen(false)}>
                <Shield className="h-5 w-5" /> Dashboard
              </MobileNavLink>
              <MobileNavLink
                href={process.env.NEXT_PUBLIC_DOCS_URL || 'https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/'}
                onClick={() => setIsMenuOpen(false)}
              >
                <BookOpen className="h-5 w-5" /> Documentation
              </MobileNavLink>

              <div className="border-t border-slate-800 my-2 pt-2">
                {isAuthenticated ? (
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-slate-300"
                    onClick={() => { logout(); setIsMenuOpen(false); }}
                  >
                    <LogOut className="h-5 w-5 mr-3" /> Logout
                  </Button>
                ) : (
                  <div className="flex flex-col gap-2">
                    <Link
                      href="/login"
                      className="px-4 py-2 text-slate-300 hover:text-white transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Login
                    </Link>
                    <Link
                      href="/signup"
                      className="cyber-btn text-white text-center"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Sign Up Free
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

function NavLink({
  href,
  children,
  icon,
  external = false
}: {
  href: string;
  children: React.ReactNode;
  icon?: React.ReactNode;
  external?: boolean;
}) {
  const Component = external ? 'a' : Link;
  const extraProps = external ? { target: '_blank', rel: 'noopener noreferrer' } : {};

  return (
    <Component
      href={href}
      className="flex items-center gap-2 px-4 py-2 rounded-lg text-slate-400 hover:text-cyan-400 hover:bg-slate-800/50 transition-all duration-200"
      {...extraProps}
    >
      {icon}
      <span className="font-medium">{children}</span>
    </Component>
  );
}

function MobileNavLink({
  href,
  children,
  onClick
}: {
  href: string;
  children: React.ReactNode;
  onClick?: () => void;
}) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 px-4 py-3 rounded-lg text-slate-300 hover:text-cyan-400 hover:bg-slate-800/50 transition-all"
      onClick={onClick}
    >
      {children}
    </Link>
  );
}
