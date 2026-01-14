# Responsive Design Patterns & Mobile-First

## Breakpoint Strategy

### Tailwind Breakpoints
```
Default (mobile):  All base styles for 320px+
sm:  640px   (landscape phone)
md:  768px   (tablet)
lg:  1024px  (laptop)
xl:  1280px  (desktop)
2xl: 1536px  (large desktop)
```

### Mobile-First Approach
```html
<!-- Start with mobile, enhance for larger screens -->
<div class="text-base md:text-lg lg:text-2xl">
  Text starts at 16px, becomes 18px on tablets, 24px on desktop
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  Single column on mobile → 2 columns on tablet → 3 columns on desktop
</div>
```

## Common Responsive Patterns

### Navigation Bar
```typescript
'use client';

import { useState } from 'react';

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <a href="/" className="text-2xl font-bold text-blue-600">
            Logo
          </a>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-8">
            <a href="/" className="text-gray-600 hover:text-gray-900">Home</a>
            <a href="/about" className="text-gray-600 hover:text-gray-900">About</a>
            <a href="/contact" className="text-gray-600 hover:text-gray-900">Contact</a>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Sign in
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 hover:bg-gray-100 rounded-lg"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isOpen && (
          <div className="md:hidden mt-4 space-y-2 border-t border-gray-200 pt-4">
            <a href="/" className="block text-gray-600 hover:text-gray-900 py-2">Home</a>
            <a href="/about" className="block text-gray-600 hover:text-gray-900 py-2">About</a>
            <a href="/contact" className="block text-gray-600 hover:text-gray-900 py-2">Contact</a>
            <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              Sign in
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
```

### Hero Section
```html
<!-- Mobile-first hero with responsive image -->
<section className="relative w-full h-screen min-h-96 md:min-h-screen flex items-center">
  <!-- Background image responsive -->
  <img
    src="hero-mobile.jpg"
    alt="Hero background"
    className="absolute inset-0 w-full h-full object-cover hidden md:block"
  />
  <img
    src="hero.jpg"
    alt="Hero background"
    className="absolute inset-0 w-full h-full object-cover md:hidden"
  />

  <!-- Content overlay -->
  <div className="relative z-10 max-w-7xl mx-auto px-4 w-full">
    <div className="max-w-xl">
      <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-white mb-4 leading-tight">
        Responsive Hero Section
      </h1>
      <p className="text-lg md:text-xl text-gray-100 mb-6">
        This text scales beautifully across all devices
      </p>
      <button className="bg-blue-600 text-white px-6 md:px-8 py-2 md:py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors">
        Get Started
      </button>
    </div>
  </div>
</section>
```

### Grid Layout (Auto-filling)
```html
<!-- Automatically adapts to available space -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6">
  <div class="bg-white p-6 rounded-lg shadow-sm">Card 1</div>
  <div class="bg-white p-6 rounded-lg shadow-sm">Card 2</div>
  <div class="bg-white p-6 rounded-lg shadow-sm">Card 3</div>
  <div class="bg-white p-6 rounded-lg shadow-sm">Card 4</div>
</div>

<!-- On small screens: 1 column (320px)
     On tablets: 2 columns (>600px)
     On desktop: 3+ columns (>900px) -->
```

### Container Queries (Modern Approach)
```css
/* Enable container queries in tailwind.config.js */
theme: {
  extend: {
    containers: {
      'sm': '500px',
      'md': '768px',
      'lg': '1024px',
    }
  }
}
```

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row gap-4">
    <!-- Single column on mobile, row on container > 500px -->
  </div>
</div>
```

## Touch-Friendly Design (Mobile)

```html
<!-- Minimum touch target: 48px × 48px -->
<button class="min-h-12 min-w-12 px-4 py-3 bg-blue-600 text-white rounded-lg">
  Tap me
</button>

<!-- Spacing between touch targets: 8-16px -->
<div class="flex gap-4">
  <button class="px-4 py-3">Button 1</button>
  <button class="px-4 py-3">Button 2</button>
</div>

<!-- Remove hover-only interactions -->
<!-- Bad: Only visible on hover -->
<div class="group">
  <div class="hidden group-hover:block">Hidden content</div>
</div>

<!-- Good: Always visible, enhancement on desktop -->
<div class="group">
  <div className="text-sm text-gray-600">Visible on all devices</div>
</div>
```

## Typography Scaling

```html
<!-- Responsive typography with clamp() -->
<h1 style="fontSize: 'clamp(1.5rem, 5vw, 3.5rem)'">
  Responsive heading
</h1>

<!-- With Tailwind custom sizing -->
<h1 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold">
  Scales at each breakpoint
</h1>
```

## Viewport-Relative Units

```html
<!-- Full viewport width (including scroll bar) -->
<div class="w-screen">100vw</div>

<!-- Full viewport height -->
<div class="h-screen">100vh</div>

<!-- Responsive sizing with vw (10% of viewport width) -->
<div class="w-1/2 md:w-vw-25">
  Width is 50% on mobile, 25vw on desktop
</div>

<!-- Safe area for notched devices -->
<header class="pt-[env(safe-area-inset-top)]">
  Accounts for iPhone notch
</header>
```

## Image Responsive Patterns

```typescript
import Image from 'next/image';

// Responsive image with srcset
<Image
  src="/image.jpg"
  alt="Responsive image"
  width={1200}
  height={600}
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  className="w-full h-auto"
  priority={true} // For LCP images
/>

// Picture element for art direction
<picture>
  <source media="(min-width: 1024px)" srcSet="/desktop.jpg" />
  <source media="(min-width: 768px)" srcSet="/tablet.jpg" />
  <img src="/mobile.jpg" alt="Art-directed image" className="w-full" />
</picture>
```

## Responsive Video Embedding

```html
<!-- Aspect ratio container maintains ratio on resize -->
<div class="aspect-video bg-black rounded-lg overflow-hidden">
  <iframe
    width="100%"
    height="100%"
    src="https://www.youtube.com/embed/dQw4w9WgXcQ"
    allowFullScreen
  ></iframe>
</div>

<!-- Or with custom aspect ratio -->
<div class="relative w-full" style={{ paddingBottom: '56.25%' }}>
  <iframe
    src="..."
    className="absolute inset-0 w-full h-full"
  ></iframe>
</div>
```

## Testing Responsive Design

### Browser DevTools
```
Chrome DevTools:
1. Press Ctrl+Shift+M for Device Toolbar
2. Test on:
   - iPhone SE (375px)
   - iPad (768px)
   - Desktop (1920px)
3. Check:
   - Text readability
   - Touch target sizes
   - Layout reflow
   - Image scaling
   - No horizontal scrolling
```

### Common Breakpoint Testing
```
Mobile:
- iPhone SE: 375px
- iPhone 13: 390px
- Pixel 5: 393px

Tablet:
- iPad: 768px
- iPad Air: 820px
- Samsung Tab: 800px

Desktop:
- MacBook Air: 1440px
- Full HD: 1920px
- 4K: 2560px
```

## Performance Considerations

```typescript
// Lazy load images outside viewport
<Image
  src="/image.jpg"
  alt="Lazy loaded"
  loading="lazy"
  decoding="async"
/>

// Resize images for device pixel ratio
<Image
  src="/image.jpg"
  alt="Hi-DPI image"
  width={600}
  height={400}
  quality={85}
/>

// Preload critical resources
<link rel="preload" as="image" href="/hero.jpg" />
```

## Responsive Grid Recipes

```html
<!-- 2-column grid that wraps on mobile -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
  ...
</div>

<!-- 3-column grid with auto-wrap -->
<div class="grid grid-cols-[repeat(auto-fit,minmax(200px,1fr))] gap-6">
  ...
</div>

<!-- Asymmetric grid -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
  <div class="md:col-span-2">Wide content</div>
  <div>Sidebar</div>
</div>

<!-- Holy Grail layout -->
<div class="flex flex-col min-h-screen">
  <header class="bg-gray-100">Header</header>
  <div class="flex flex-1">
    <aside class="w-64">Sidebar</aside>
    <main class="flex-1">Main content</main>
  </div>
  <footer class="bg-gray-100">Footer</footer>
</div>
```
