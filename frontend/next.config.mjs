/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',

  // Environment variables available to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.CHATBOT_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_DOCS_URL: process.env.DOCS_URL || 'http://localhost:3001',
  },

  // Redirect /docs to the Docusaurus site
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.CHATBOT_API_URL || 'http://localhost:8000'}/:path*`,
      },
    ];
  },
};

export default nextConfig;
