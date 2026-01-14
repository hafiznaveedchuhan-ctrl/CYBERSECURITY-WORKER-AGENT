# Accessibility Checklist (WCAG AA)

## Color & Contrast

### WCAG AA Standards
- **Normal text**: 4.5:1 contrast ratio
- **Large text** (18px+ or 14px+ bold): 3:1 contrast ratio
- **UI components**: 3:1 contrast ratio (borders, outlines, focus states)

### Testing
```html
<!-- Bad: Gray text on white (2.4:1 ratio - fails) -->
<p style="color: #999999; background: white">Hard to read</p>

<!-- Good: Gray text on white (7:1 ratio - passes) -->
<p class="text-gray-700 bg-white">Easy to read</p>
```

**Tools**: WebAIM Contrast Checker, WAVE, Axe DevTools

## Semantic HTML

```html
<!-- Bad: Non-semantic -->
<div onclick="navigate('/')">Home</div>
<div class="heading">Page Title</div>

<!-- Good: Semantic -->
<button onclick="navigate('/')">Home</button>
<h1>Page Title</h1>
```

### Semantic Elements
```html
<header>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<aside>
  <h2>Related</h2>
  <ul>
    <li><a href="#">Link</a></li>
  </ul>
</aside>

<footer>
  <p>&copy; 2024</p>
</footer>
```

## Keyboard Navigation

### Focus Management
```html
<!-- Visible focus indicator (don't remove!) -->
<button class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
  Click me
</button>

<!-- Skip to main content -->
<a href="#main" class="sr-only focus:not-sr-only">
  Skip to main content
</a>

<main id="main">
  Content here
</main>
```

### Tab Order
```typescript
// Control tab order with tabIndex
<div>
  <button tabIndex={1}>First</button>
  <button tabIndex={2}>Second</button>
  <button tabIndex={0}>Last (0 = natural DOM order)</button>
</div>

// Or better: manage in DOM order
<div>
  <button>First</button>
  <button>Second</button>
  <button>Third</button>
</div>
```

### Keyboard Event Handling
```typescript
'use client';

function Dropdown() {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        toggleDropdown();
        break;
      case 'Escape':
        closeDropdown();
        break;
    }
  };

  return (
    <button
      onKeyDown={handleKeyDown}
      role="button"
      aria-expanded={isOpen}
      aria-haspopup="true"
    >
      Menu
    </button>
  );
}
```

## ARIA Labels & Roles

### Form Accessibility
```html
<!-- Good: Explicit label -->
<label htmlFor="email">Email address</label>
<input id="email" type="email" aria-describedby="email-hint" />
<small id="email-hint">We'll never share your email</small>

<!-- Good: Error messaging -->
<input
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : 'email-hint'}
/>
{error && <span id="email-error">{error}</span>}
```

### Button Accessibility
```html
<!-- Good: Descriptive button text -->
<button>Delete account</button>

<!-- Bad: Non-descriptive text -->
<button>Click here</button>

<!-- Screen reader only text for icons -->
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Close menu</span>
</button>
```

### Landmark Regions
```html
<header role="banner">Header</header>
<nav role="navigation">Navigation</nav>
<main role="main">Main content</main>
<aside role="complementary">Sidebar</aside>
<footer role="contentinfo">Footer</footer>
```

### ARIA Live Regions
```html
<!-- Announce changes to screen readers -->
<div aria-live="polite" aria-atomic="true" id="status">
  {status}
</div>

<!-- For alerts (higher priority) -->
<div aria-live="assertive" role="alert">
  Critical message
</div>
```

## Images

### Alternative Text
```html
<!-- Good: Descriptive -->
<img src="office.jpg" alt="Team meeting in conference room" />

<!-- Good: Decorative (empty alt) -->
<img src="divider.jpg" alt="" aria-hidden="true" />

<!-- Good: Icon with text -->
<svg aria-hidden="true" width="24" height="24">...</svg>
<span>Settings</span>
```

### SVG Accessibility
```html
<!-- Good: SVG with title and desc -->
<svg viewBox="0 0 100 100" role="img">
  <title>Chart title</title>
  <desc>Chart showing sales by region</desc>
  <path d="..." />
</svg>

<!-- Good: SVG as decoration -->
<svg aria-hidden="true">
  <path d="..." />
</svg>
```

## Form Accessibility

### Required Fields
```html
<label htmlFor="name">
  Name
  <span aria-label="required">*</span>
</label>
<input id="name" required aria-required="true" />
```

### Error Handling
```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
}

export function Form({ onSubmit }: FormProps) {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div role="alert" aria-live="polite">
        {Object.values(errors).length > 0 && (
          <div className="bg-red-50 p-4 rounded-lg mb-4">
            <h2 className="font-bold text-red-900">Please fix the following:</h2>
            <ul className="list-disc pl-5 mt-2">
              {Object.entries(errors).map(([field, error]) => (
                <li key={field} className="text-red-800">{error}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      <Input
        label="Email"
        error={errors.email}
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? 'email-error' : undefined}
      />
      {errors.email && <span id="email-error">{errors.email}</span>}
    </form>
  );
}
```

## Headings & Structure

```html
<!-- Good: Proper hierarchy -->
<h1>Page Title</h1>
<h2>Section 1</h2>
<h3>Subsection 1.1</h3>
<h3>Subsection 1.2</h3>
<h2>Section 2</h2>

<!-- Bad: Skipped levels -->
<h1>Title</h1>
<h3>Skipped h2!</h3>
```

## Links

```html
<!-- Good: Descriptive link text -->
<a href="/about">Learn about our company</a>

<!-- Bad: Generic link text -->
<a href="/about">Click here</a>

<!-- Good: External link indicator -->
<a href="/about">Learn about (opens in new tab)</a>
<a href="/about">
  Learn about
  <span aria-label="opens in new tab">
    <svg>...</svg>
  </span>
</a>
```

## Screen Reader Only Content

```css
/* styles/globals.css */
@layer components {
  .sr-only {
    @apply absolute w-px h-px p-0 -m-px overflow-hidden bg-white border-0 rounded-0 whitespace-nowrap clip-path-inset-50%;
  }
}
```

```html
<button>
  <svg aria-hidden="true" className="w-6 h-6">...</svg>
  <span className="sr-only">Close modal</span>
</button>
```

## Testing Tools

- **Automated**: axe DevTools, Wave, WAVE, Lighthouse
- **Manual**: Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- **Screen Reader**: NVDA (Windows), JAWS, VoiceOver (Mac)

## Quick Checklist

- [ ] Color contrast ≥4.5:1 for normal text
- [ ] All images have alt text
- [ ] Keyboard navigation works (Tab through entire page)
- [ ] Focus indicators visible
- [ ] Semantic HTML used (button, a, form, etc.)
- [ ] Form labels associated with inputs
- [ ] Error messages linked to inputs (aria-describedby)
- [ ] Modal dialog has focus trap
- [ ] Dropdown/menu has keyboard support
- [ ] No content hidden from screen readers (unless decorative)
- [ ] Page has skip to main content link
- [ ] Heading hierarchy is correct (no skipped levels)
- [ ] ARIA attributes used correctly
- [ ] Dynamic content updates announced (aria-live)

## Common Accessibility Wins

1. **Add alt text** to all images
2. **Use semantic HTML** instead of divs
3. **Ensure color contrast** (use contrast checker)
4. **Keyboard navigation** (Tab, Enter, Escape)
5. **Focus indicators** (never remove outline)
6. **Label form fields** (label element or aria-label)
7. **ARIA for dynamic content** (aria-live for notifications)
8. **Heading hierarchy** (h1, h2, h3 in order)
9. **Skip links** (skip to main content)
10. **Test with screen reader** (VoiceOver, NVDA, JAWS)
