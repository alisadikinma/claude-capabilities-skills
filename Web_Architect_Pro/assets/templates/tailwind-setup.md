# Tailwind CSS Complete Setup Guide

**Universal guide for Next.js, React (Vite), and Vue 3**

---

## 🎨 Installation & Configuration

### Next.js 14 (App Router)

```bash
# Tailwind is included by default with create-next-app
npx create-next-app@latest my-app --typescript --tailwind --app

# Or install manually in existing project
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Configuration:**

`tailwind.config.ts`:
```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
        mono: ['var(--font-roboto-mono)', 'monospace'],
      },
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
}

export default config
```

`app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }

  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800;
  }
  
  .container-custom {
    @apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
  }
}
```

---

### React (Vite)

```bash
# Install Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Configuration:**

`tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
```

`src/index.css` or `src/assets/styles/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
  
  h1 {
    @apply text-4xl font-bold;
  }
  
  h2 {
    @apply text-3xl font-semibold;
  }
  
  h3 {
    @apply text-2xl font-semibold;
  }
}

@layer components {
  .card {
    @apply bg-white rounded-lg shadow-md p-6;
  }
  
  .input-field {
    @apply w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500;
  }
}
```

---

### Vue 3 (Vite)

```bash
# Install Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

**Configuration:**

`tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
}
```

`src/assets/styles/main.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700;
  }
}
```

---

## 🎨 Essential Tailwind Patterns

### Responsive Design

```html
<!-- Mobile-first approach -->
<div class="text-sm md:text-base lg:text-lg xl:text-xl">
  Responsive text
</div>

<!-- Grid layout -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</div>

<!-- Flexbox utilities -->
<div class="flex flex-col md:flex-row items-center justify-between gap-4">
  <div>Left</div>
  <div>Right</div>
</div>
```

### Dark Mode

`tailwind.config.js`:
```javascript
export default {
  darkMode: 'class', // or 'media'
  // ... rest of config
}
```

Usage:
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Content that adapts to dark mode
</div>
```

### Custom Components (Using @layer)

```css
@layer components {
  /* Button variants */
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-all duration-200;
  }
  
  .btn-primary {
    @apply btn bg-primary-600 text-white hover:bg-primary-700 active:scale-95;
  }
  
  .btn-secondary {
    @apply btn bg-gray-200 text-gray-900 hover:bg-gray-300;
  }
  
  .btn-outline {
    @apply btn border-2 border-primary-600 text-primary-600 hover:bg-primary-50;
  }
  
  /* Card component */
  .card {
    @apply bg-white rounded-lg shadow-md p-6 transition-shadow hover:shadow-lg;
  }
  
  /* Input styles */
  .input {
    @apply w-full px-4 py-2 border border-gray-300 rounded-md 
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
           disabled:bg-gray-100 disabled:cursor-not-allowed;
  }
  
  /* Badge */
  .badge {
    @apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium;
  }
  
  .badge-success {
    @apply badge bg-green-100 text-green-800;
  }
  
  .badge-warning {
    @apply badge bg-yellow-100 text-yellow-800;
  }
  
  .badge-error {
    @apply badge bg-red-100 text-red-800;
  }
}
```

---

## 🔧 Useful Plugins

### Official Tailwind Plugins

```bash
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
```

`tailwind.config.js`:
```javascript
export default {
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
```

### Plugin: Forms
Better default styles for form elements:
```html
<input type="text" class="form-input rounded-md" />
<select class="form-select rounded-md">...</select>
<textarea class="form-textarea rounded-md"></textarea>
```

### Plugin: Typography
For rich text content:
```html
<article class="prose lg:prose-xl">
  <h1>Heading</h1>
  <p>Paragraph with automatic styling</p>
</article>
```

### Plugin: Aspect Ratio
Maintain aspect ratios:
```html
<div class="aspect-w-16 aspect-h-9">
  <iframe src="..."></iframe>
</div>
```

---

## 🎯 Common UI Components

### Button Component (React/TSX)

```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', size = 'md', children }: ButtonProps) {
  const baseStyles = 'btn inline-flex items-center justify-center transition-colors';
  
  const variants = {
    primary: 'bg-primary-600 text-white hover:bg-primary-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50',
  };
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2',
    lg: 'px-6 py-3 text-lg',
  };
  
  return (
    <button className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}>
      {children}
    </button>
  );
}
```

### Card Component (Vue)

```vue
<script setup lang="ts">
interface Props {
  title?: string;
  hover?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  hover: false,
});
</script>

<template>
  <div 
    :class="[
      'bg-white rounded-lg shadow-md p-6',
      hover && 'transition-shadow hover:shadow-lg'
    ]"
  >
    <h3 v-if="title" class="text-xl font-semibold mb-4">
      {{ title }}
    </h3>
    <slot />
  </div>
</template>
```

### Modal Component (React)

```tsx
export function Modal({ isOpen, onClose, children }: ModalProps) {
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
        >
          ✕
        </button>
        {children}
      </div>
    </div>
  );
}
```

---

## 📱 Responsive Breakpoints

```javascript
// tailwind.config.js
theme: {
  screens: {
    'sm': '640px',   // Mobile landscape
    'md': '768px',   // Tablet
    'lg': '1024px',  // Desktop
    'xl': '1280px',  // Large desktop
    '2xl': '1536px', // Extra large
  }
}
```

Usage:
```html
<div class="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
  Responsive width
</div>
```

---

## 🎨 Color Palette Example

```javascript
// tailwind.config.js
theme: {
  extend: {
    colors: {
      brand: {
        50: '#f0f9ff',
        100: '#e0f2fe',
        200: '#bae6fd',
        300: '#7dd3fc',
        400: '#38bdf8',
        500: '#0ea5e9', // Primary brand color
        600: '#0284c7',
        700: '#0369a1',
        800: '#075985',
        900: '#0c4a6e',
        950: '#082f49',
      },
    },
  },
}
```

---

## 🚀 Performance Tips

1. **Purge unused styles** (automatic in production):
```javascript
// tailwind.config.js
export default {
  content: ['./src/**/*.{js,jsx,ts,tsx,vue}'], // Specify all template files
}
```

2. **Use JIT mode** (enabled by default in Tailwind 3+)

3. **Optimize for production**:
```bash
npm run build
# Tailwind automatically purges unused styles
```

4. **Bundle size comparison**:
- Development: ~3.5MB
- Production (purged): ~10KB (typical)

---

## 📚 Useful Resources

- **Official Docs:** https://tailwindcss.com
- **Tailwind UI:** https://tailwindui.com (Premium components)
- **Headless UI:** https://headlessui.com (Unstyled components)
- **Heroicons:** https://heroicons.com (SVG icons)
- **Tailwind Play:** https://play.tailwindcss.com (Online playground)

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
