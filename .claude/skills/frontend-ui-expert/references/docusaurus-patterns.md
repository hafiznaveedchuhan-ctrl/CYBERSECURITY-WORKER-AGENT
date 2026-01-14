# Docusaurus Patterns & Custom Components

## Project Setup

```bash
# Create Docusaurus site
npx create-docusaurus@latest my-docs classic

# Install Tailwind (optional)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Add shadcn/ui (optional)
npx shadcn-ui@latest init
```

## Configuration

```javascript
// docusaurus.config.js
module.exports = {
  title: 'My Documentation',
  tagline: 'Build amazing docs',
  url: 'https://docs.example.com',
  baseUrl: '/',

  themeConfig: {
    navbar: {
      title: 'My Docs',
      logo: {
        alt: 'My Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: 'docs/intro',
          label: 'Docs',
          position: 'left',
        },
        {
          href: 'https://github.com',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Tutorial', to: '/docs/intro' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Company`,
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
    },
  },

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/myorg/my-docs/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};
```

## Custom MDX Components

### Info Box Component

```javascript
// src/components/InfoBox.jsx
import React from 'react';

export default function InfoBox({ type = 'info', children, title }) {
  const typeStyles = {
    info: 'bg-blue-50 border-blue-200 text-blue-900',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-900',
    danger: 'bg-red-50 border-red-200 text-red-900',
    success: 'bg-green-50 border-green-200 text-green-900',
  };

  const titleColor = {
    info: 'text-blue-900',
    warning: 'text-yellow-900',
    danger: 'text-red-900',
    success: 'text-green-900',
  };

  return (
    <div className={`border-l-4 p-4 rounded ${typeStyles[type]}`}>
      {title && <h4 className={`font-bold mb-2 ${titleColor[type]}`}>{title}</h4>}
      <div className="text-sm">{children}</div>
    </div>
  );
}
```

### Code Comparison Component

```javascript
// src/components/CodeComparison.jsx
import React from 'react';

export default function CodeComparison({ good, bad }) {
  return (
    <div className="grid md:grid-cols-2 gap-4 my-6">
      <div>
        <h3 className="text-red-600 font-bold mb-2">❌ Bad</h3>
        <pre className="bg-red-50 p-4 rounded-lg overflow-auto">
          <code>{bad}</code>
        </pre>
      </div>
      <div>
        <h3 className="text-green-600 font-bold mb-2">✅ Good</h3>
        <pre className="bg-green-50 p-4 rounded-lg overflow-auto">
          <code>{good}</code>
        </pre>
      </div>
    </div>
  );
}
```

### Usage in MDX

```mdx
---
title: Best Practices
---

import InfoBox from '@site/src/components/InfoBox';
import CodeComparison from '@site/src/components/CodeComparison';

# Best Practices

<InfoBox type="warning" title="Important">
  Always validate user input before processing it.
</InfoBox>

<CodeComparison
  bad={`const count = 5; // Global variable`}
  good={`const useCounter = () => {
  const [count, setCount] = useState(0);
  return { count, setCount };
};`}
/>
```

## Sidebar Configuration

```javascript
// sidebars.js
module.exports = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/configuration',
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/basics',
        'guides/advanced',
        {
          type: 'category',
          label: 'Components',
          items: [
            'guides/components/button',
            'guides/components/form',
          ],
        },
      ],
    },
    {
      type: 'link',
      label: 'API Reference',
      href: '/api',
    },
  ],
};
```

## Custom CSS with Tailwind

```css
/* src/css/custom.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Docusaurus-specific customizations */
:root {
  --docusaurus-primary-color: #3b82f6;
  --docusaurus-secondary-color: #8b5cf6;
}

/* Code blocks */
.docusaurus-highlight-code-line {
  @apply bg-blue-100 block px-3;
}

/* Headings */
h1 {
  @apply text-4xl font-bold mb-4 mt-8;
}

h2 {
  @apply text-2xl font-semibold mb-3 mt-6;
}

/* Links */
a {
  @apply text-blue-600 hover:underline;
}

/* Custom components */
.info-box {
  @apply border-l-4 border-blue-500 bg-blue-50 p-4 rounded;
}
```

## Theme Customization

```javascript
// swizzle components to customize
// docusaurus swizzle @docusaurus/preset-classic NavbarItem

// src/theme/Layout/index.js
import React from 'react';
import Layout from '@theme-original/Layout';

export default function LayoutWrapper(props) {
  return (
    <>
      {/* Your custom wrapper */}
      <Layout {...props} />
    </>
  );
}
```

## Blog Setup

```markdown
---
slug: my-first-blog-post
title: My First Blog Post
authors: [alice]
tags: [hello, docusaurus]
---

Your blog post content here
```

```javascript
// docusaurus.config.js
module.exports = {
  // ...
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/myorg/docs/edit/main/',
          blogSidebarTitle: 'All posts',
          blogSidebarCount: 'ALL',
        },
      },
    ],
  ],
};
```

## Search Integration

```javascript
// docusaurus.config.js with Algolia
module.exports = {
  // ...
  themeConfig: {
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'your_index_name',
      contextualSearch: true,
    },
  },
};
```

## Versioning

```bash
# Create a version
npm run docusaurus docs:version 1.0.0

# File structure
docs/
versioned_docs/
  ├── version-1.0.0/
  └── version-0.9.0/
```

## Static Deployment

```javascript
// docusaurus.config.js
module.exports = {
  // ...
  staticDirectories: ['static'],
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
        },
      },
    ],
  ],
};

// Build
npm run build

// Deploy to GitHub Pages, Vercel, etc.
```

## Custom Landing Page

```javascript
// src/pages/index.js
import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout title="Home" description="Welcome to our docs">
      <main>
        {/* Hero section */}
        <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
          <div className="max-w-4xl mx-auto px-4 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              Welcome to Our Docs
            </h1>
            <p className="text-lg mb-8">
              Everything you need to get started
            </p>
            <Link
              className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-100"
              to="/docs/intro"
            >
              Get Started
            </Link>
          </div>
        </section>

        {/* Features */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-4xl mx-auto px-4">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-bold mb-2">Easy to Use</h3>
                <p className="text-gray-600">Get started in minutes</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-bold mb-2">Comprehensive</h3>
                <p className="text-gray-600">Complete API reference</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm">
                <h3 className="text-xl font-bold mb-2">Community</h3>
                <p className="text-gray-600">Active support and guides</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
```

## Tips & Best Practices

1. **Organize well**: Use clear directory structure with categories
2. **Write examples**: Always include code examples
3. **Keep up-to-date**: Use version control for docs
4. **Search optimization**: Use Algolia for full-text search
5. **Mobile-friendly**: Test on mobile devices
6. **Accessible**: Follow WCAG guidelines
7. **Performance**: Optimize images, use compression
8. **Analytics**: Track what users read
