# Figma to Code Workflow

## Step 1: Extract Design Specifications

### Colors
```
From Figma design inspection:
- Primary: #3B82F6 (Blue 500)
- Secondary: #8B5CF6 (Purple 500)
- Text: #111827 (Gray 900)
- Text Muted: #6B7280 (Gray 500)
- Background: #FFFFFF
- Border: #E5E7EB (Gray 200)

Tailwind Mapping:
text-blue-600, bg-blue-50, border-blue-200
```

### Typography
```
From Figma:
- Heading 1: Poppins Bold, 32px, line-height 40px
- Heading 2: Poppins Semi-Bold, 24px, line-height 32px
- Body: Inter Regular, 16px, line-height 24px
- Caption: Inter Regular, 14px, line-height 20px

Tailwind Mapping:
h1: text-4xl font-bold leading-tight
h2: text-2xl font-semibold leading-tight
p: text-base font-normal leading-relaxed
caption: text-sm font-normal text-gray-600
```

### Spacing & Sizing
```
From Figma grid (8px base):
- 4px = 0.5  (xs)
- 8px = 1    (sm)
- 16px = 2   (md)
- 24px = 3   (lg)
- 32px = 4   (xl)
- 48px = 6   (2xl)

Tailwind Scale:
p-1 to p-6 = 0.25rem to 1.5rem
gap-4 = 1rem (16px)
```

### Shadows
```
From Figma:
- Subtle: blur 4px, spread 0, Y-offset 1px, alpha 10%
- Default: blur 8px, spread -2px, Y-offset 4px, alpha 10%
- Elevated: blur 20px, spread -2px, Y-offset 8px, alpha 15%

Tailwind Mapping:
shadow-sm (subtle)
shadow (default)
shadow-lg (elevated)
```

## Step 2: Identify Component Structure

From Figma artboards:

```
Button Component states:
├── Default
├── Hover
├── Active
├── Disabled
└── Loading

Card Component:
├── Header
├── Content
├── Footer
└── (Hoverable variant)

Form Field:
├── Label
├── Input
├── Helper text
└── Error state
```

## Step 3: Breakpoint Mapping

### Common Figma Artboards
```
Mobile:    375px (iPhone SE)
Tablet:    768px (iPad)
Desktop:   1440px (Desktop)

Tailwind Breakpoints:
sm:  640px   (Small tablet)
md:  768px   (Tablet)
lg:  1024px  (Desktop)
xl:  1280px  (Wide desktop)
```

### Responsive Example
```
Mobile (375px):
- Single column layout
- Full-width buttons
- Large, readable typography

Tablet (768px):
- Two column grid
- Inline buttons
- Reduced spacing

Desktop (1440px):
- Three column layout
- Multiple inline buttons
- Optimized spacing
```

## Step 4: Design Token System

### Create `tailwind.config.ts`
```typescript
import type { Config } from 'tailwindcss'

export default {
  content: [
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#8B5CF6',
        text: {
          primary: '#111827',
          muted: '#6B7280',
        },
      },
      fontFamily: {
        heading: ['Poppins', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
      fontSize: {
        h1: ['32px', { lineHeight: '40px' }],
        h2: ['24px', { lineHeight: '32px' }],
        body: ['16px', { lineHeight: '24px' }],
      },
      boxShadow: {
        subtle: '0 1px 4px rgba(0,0,0,0.1)',
        default: '0 4px 8px rgba(0,0,0,0.1)',
        elevated: '0 8px 20px rgba(0,0,0,0.15)',
      },
    },
  },
} satisfies Config
```

## Step 5: Build Components

### Step 5a: Button Component

**From Figma**: Extract button variants, sizes, and states

```typescript
// components/ui/Button.tsx
'use client';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  className,
  children,
  ...props
}: ButtonProps) {
  const baseStyles = 'font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed';

  const variants = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500',
    secondary: 'bg-purple-600 text-white hover:bg-purple-700 focus:ring-purple-500',
    outline: 'border-2 border-gray-300 bg-transparent text-gray-900 hover:bg-gray-50 focus:ring-gray-500',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-sm rounded',
    md: 'px-4 py-2 text-base rounded-lg',
    lg: 'px-6 py-3 text-lg rounded-lg',
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={cn(baseStyles, variants[variant], sizes[size], className)}
      {...props}
    >
      {isLoading && <span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />}
      {children}
    </button>
  );
}
```

### Step 5b: Card Component

**From Figma**: Identify card sections and nesting

```typescript
// components/ui/Card.tsx
interface CardProps {
  children: React.ReactNode;
  hoverable?: boolean;
  className?: string;
}

export function Card({ children, hoverable = false, className }: CardProps) {
  return (
    <div
      className={cn(
        'bg-white rounded-lg border border-gray-200 shadow-subtle',
        hoverable && 'hover:shadow-elevated hover:border-gray-300 transition-shadow',
        className
      )}
    >
      {children}
    </div>
  );
}

export function CardHeader({ title, subtitle, className }: { title: string; subtitle?: string; className?: string }) {
  return (
    <div className={cn('px-6 py-4 border-b border-gray-200', className)}>
      <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
      {subtitle && <p className="text-sm text-text-muted mt-1">{subtitle}</p>}
    </div>
  );
}

export function CardContent({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn('px-6 py-4', className)}>{children}</div>;
}

export function CardFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn('px-6 py-4 border-t border-gray-200 bg-gray-50', className)}>{children}</div>;
}
```

## Step 6: Responsive Testing

### Test at Key Breakpoints
```
375px (Mobile): Single column, full-width elements
768px (Tablet): Two columns, readable text
1440px (Desktop): Three+ columns, optimized layout
```

### Browser Tools
```
Chrome DevTools:
1. Device Toolbar (Ctrl+Shift+M)
2. Test common devices: iPhone 12, iPad, Desktop
3. Check:
   - Text readability
   - Touch target sizes (≥48px)
   - Layout reflow
   - Image scaling
```

## Step 7: Document Design Tokens

Create `docs/design-tokens.md`:

```markdown
# Design Tokens

## Colors
| Name | Value | Tailwind |
|------|-------|----------|
| Primary | #3B82F6 | bg-blue-600 |
| Secondary | #8B5CF6 | bg-purple-600 |
| Text Primary | #111827 | text-gray-900 |
| Text Muted | #6B7280 | text-gray-500 |

## Typography
| Element | Family | Size | Weight | Line Height |
|---------|--------|------|--------|-------------|
| H1 | Poppins | 32px | Bold | 40px |
| H2 | Poppins | 24px | Semi-Bold | 32px |
| Body | Inter | 16px | Regular | 24px |

## Spacing (8px Grid)
| Scale | Value |
|-------|-------|
| xs | 4px |
| sm | 8px |
| md | 16px |
| lg | 24px |
| xl | 32px |

## Shadows
| Name | Value | Tailwind |
|------|-------|----------|
| Subtle | 0 1px 4px rgba(0,0,0,0.1) | shadow-subtle |
| Default | 0 4px 8px rgba(0,0,0,0.1) | shadow |
| Elevated | 0 8px 20px rgba(0,0,0,0.15) | shadow-elevated |
```

## Common Pitfalls to Avoid

1. **Hardcoding Values**
   - ❌ Bad: `style={{ color: '#3B82F6' }}`
   - ✓ Good: `className="text-blue-600"`

2. **Ignoring Responsive Design**
   - ❌ Bad: Only designing for desktop
   - ✓ Good: Test at 375px, 768px, 1440px

3. **Forgetting Accessibility**
   - ❌ Bad: Colors alone convey meaning
   - ✓ Good: High contrast (4.5:1), ARIA labels

4. **Not Testing Dark Mode**
   - ❌ Bad: Only testing light mode
   - ✓ Good: Use `dark:` classes

5. **Fixed Dimensions**
   - ❌ Bad: `width: 400px` (breaks on mobile)
   - ✓ Good: `w-full md:w-1/2` (responsive)

## Design Sync Tools

- **Figma to React**: Use Figma to code plugins (Design2Code, Locofy)
- **Component Library Sync**: Maintain design system in Figma AND code
- **Token Management**: Use tools like Tokens Studio for Figma
- **Version Control**: Track changes in both Figma and Git
