# Tailwind CSS Patterns & Techniques

## Responsive Design Pattern

```html
<!-- Mobile-first: single column becomes multi-column at larger screens -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div class="bg-white p-4 rounded-lg">Item 1</div>
  <div class="bg-white p-4 rounded-lg">Item 2</div>
  <div class="bg-white p-4 rounded-lg">Item 3</div>
</div>

<!-- Responsive typography -->
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">
  Responsive Heading
</h1>

<!-- Responsive spacing -->
<div class="p-4 md:p-6 lg:p-8">
  Content with responsive padding
</div>

<!-- Hide/show elements at different breakpoints -->
<div class="hidden lg:block">
  Only visible on large screens
</div>

<div class="lg:hidden">
  Hidden on large screens
</div>
```

## Dark Mode Implementation

```javascript
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  theme: {
    colors: {
      primary: 'rgb(var(--color-primary) / <alpha-value>)',
      // ...
    },
  },
};
```

```html
<!-- Dark mode variants -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <h1 class="text-2xl font-bold">Dark Mode Compatible</h1>
  <p class="text-gray-600 dark:text-gray-400">Subtitle</p>
</div>

<!-- Dark mode toggle -->
<button
  onClick={() => document.documentElement.classList.toggle('dark')}
  class="p-2 rounded-lg bg-gray-100 dark:bg-gray-800"
>
  Toggle Dark Mode
</button>
```

## Gradient & Colors

```html
<!-- Linear gradient -->
<div class="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500">
  Colorful gradient background
</div>

<!-- Diagonal gradient -->
<div class="bg-gradient-to-br from-blue-600 to-blue-900">
  Content
</div>

<!-- Gradient text -->
<h1 class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
  Gradient Text Heading
</h1>

<!-- Color opacity -->
<div class="bg-blue-600/50">
  50% opacity blue background
</div>
```

## Utility-First Button Styles

```html
<!-- Compound button classes -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
  Click me
</button>

<!-- Using @apply in CSS for reusable combinations -->
```

```css
/* styles/components.css */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500;
  }

  .btn-secondary {
    @apply px-4 py-2 bg-gray-200 text-gray-900 rounded-lg font-medium hover:bg-gray-300 transition-colors;
  }
}
```

```html
<button class="btn-primary">Primary Button</button>
<button class="btn-secondary">Secondary Button</button>
```

## Flexbox & Grid Layouts

```html
<!-- Flex layouts -->
<div class="flex items-center justify-between gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Auto-wrapping grid -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-6">
  <div>Card 1</div>
  <div>Card 2</div>
  <div>Card 3</div>
</div>

<!-- Aspect ratio for responsive media -->
<div class="aspect-video bg-gray-200 rounded-lg overflow-hidden">
  <img src="image.jpg" alt="Full width, maintains 16:9 ratio" />
</div>

<!-- Centered content -->
<div class="flex items-center justify-center min-h-screen">
  <h1>Centered Content</h1>
</div>
```

## Shadow & Elevation

```html
<!-- Progressive shadow elevation -->
<div class="shadow-sm">Subtle shadow</div>
<div class="shadow">Default shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-2xl">Extra large shadow</div>

<!-- Custom shadow on hover -->
<div class="shadow hover:shadow-lg transition-shadow">
  Hover for elevated effect
</div>

<!-- Inner shadow effect -->
<div class="shadow-inner bg-gray-100 p-4">
  Inner shadow effect
</div>
```

## Border & Ring Patterns

```html
<!-- Borders with different widths -->
<div class="border border-gray-200">Default border</div>
<div class="border-2 border-blue-500">Thicker blue border</div>
<div class="border-l-4 border-green-500">Left border accent</div>

<!-- Rounded borders -->
<div class="rounded-lg">Standard rounded</div>
<div class="rounded-full">Fully rounded (circle)</div>
<div class="rounded-t-lg">Rounded top only</div>

<!-- Focus ring (accessibility) -->
<button class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
  Accessible focus state
</button>

<!-- Divider -->
<div class="border-t border-gray-300 my-4"></div>
```

## Spacing & Sizing

```html
<!-- Margin and padding scale -->
<div class="m-4">Margin 1rem</div>
<div class="p-8">Padding 2rem</div>
<div class="mx-auto">Horizontal auto center</div>
<div class="gap-6">Gap 1.5rem</div>

<!-- Responsive sizing -->
<div class="w-full md:w-1/2 lg:w-1/3">
  Full width on mobile, half on tablet, third on desktop
</div>

<!-- Min/max constraints -->
<div class="min-h-screen">Full viewport height minimum</div>
<div class="max-w-4xl">Maximum width 56rem</div>
<div class="h-12">Fixed height</div>
```

## Animation & Transitions

```html
<!-- Preset animations -->
<div class="animate-bounce">Bouncing element</div>
<div class="animate-spin">Spinning loader</div>
<div class="animate-pulse">Pulsing skeleton</div>

<!-- Transitions -->
<button class="bg-blue-600 hover:bg-blue-700 transition-colors duration-200">
  Smooth color transition
</button>

<div class="opacity-0 hover:opacity-100 transition-opacity">
  Fade in on hover
</div>

<!-- Transform animations -->
<div class="transform hover:scale-105 transition-transform">
  Scale up on hover
</div>

<div class="transform hover:rotate-12 transition-transform">
  Rotate on hover
</div>
```

## Custom Theme Extension

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
      },
      fontSize: {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'base': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
      },
      spacing: {
        '2xs': '0.25rem',
        'xs': '0.5rem',
        'sm': '0.75rem',
        'md': '1rem',
        'lg': '1.5rem',
        'xl': '2rem',
      },
      borderRadius: {
        'xs': '0.25rem',
        'sm': '0.375rem',
        'base': '0.5rem',
        'md': '0.75rem',
        'lg': '1rem',
      },
    },
  },
};
```

## Screen Reader Only Content

```html
<!-- Content visible only to screen readers -->
<span class="sr-only">
  This text is only for screen readers
</span>

<!-- In Tailwind config -->
```

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {},
  },
  plugins: [],
};

// Add to globals.css
@layer components {
  .sr-only {
    @apply absolute w-px h-px p-0 -m-px overflow-hidden bg-white border-0 rounded-0 whitespace-nowrap;
  }
}
```

## Performance Optimization

```javascript
// tailwind.config.js - Content purging
module.exports = {
  content: [
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
    './src/pages/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
};
```

```html
<!-- Minimize unused CSS by scanning all files -->
<!-- Only classes found in these files will be included in final bundle -->
```

## Utility Function: classnames Helper

```typescript
// lib/cn.ts
export function cn(...classes: (string | undefined | null | boolean)[]): string {
  return classes
    .filter((cls) => typeof cls === 'string')
    .join(' ')
    .split(/\s+/)
    .filter(Boolean)
    .join(' ');
}

// Or use clsx package (simpler)
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

## Advanced: CSS Variables with Tailwind

```css
/* globals.css */
@layer base {
  :root {
    --color-primary: 59 130 246;     /* blue-500 RGB */
    --color-secondary: 139 92 246;   /* purple-500 RGB */
  }

  .dark {
    --color-primary: 37 99 235;      /* blue-600 RGB */
    --color-secondary: 124 58 202;   /* purple-600 RGB */
  }
}
```

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    colors: {
      primary: 'rgb(var(--color-primary) / <alpha-value>)',
      secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
    },
  },
};
```

```html
<div class="bg-primary/50 text-secondary">
  Content using CSS variables
</div>
```
