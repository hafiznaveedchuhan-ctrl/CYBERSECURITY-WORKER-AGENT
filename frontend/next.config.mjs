/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  basePath: '/CYBERSECURITY-WORKER-AGENT',
  assetPrefix: '/CYBERSECURITY-WORKER-AGENT/',

  // Environment variables available to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://cybersecurity-worker-agent.onrender.com',
    NEXT_PUBLIC_DOCS_URL: process.env.NEXT_PUBLIC_DOCS_URL || 'https://hafiznaveedchuhan-ctrl.github.io/CYBERSECURITY-WORKER-AGENT/',
  },
};

export default nextConfig;
