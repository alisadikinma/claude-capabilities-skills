# Vitest + Testing Library - Complete Setup

**Framework:** Vitest 1.x + Testing Library  
**Use Case:** Unit & integration testing for Vite-based projects (Vue/React)  
**Coverage:** Component testing, composables/hooks, fast HMR testing  
**Best For:** Vue 3+, React with Vite, TypeScript projects

---

## 📁 Project Structure

```
project-root/
├── src/
│   ├── components/
│   │   ├── Button.vue
│   │   └── __tests__/
│   │       └── Button.spec.ts
│   │
│   ├── composables/
│   │   ├── useCounter.ts
│   │   └── __tests__/
│   │       └── useCounter.spec.ts
│   │
│   └── utils/
│       ├── format.ts
│       └── __tests__/
│           └── format.spec.ts
│
├── tests/
│   ├── setup.ts               # Test setup
│   └── utils/
│       └── test-utils.ts      # Custom utilities
│
├── vitest.config.ts
└── package.json
```

---

## 🔧 Installation

### Vue 3 Projects

```bash
# Core dependencies
npm install -D vitest @vitest/ui
npm install -D @vue/test-utils
npm install -D @testing-library/vue @testing-library/user-event
npm install -D jsdom
npm install -D happy-dom  # Alternative to jsdom (faster)

# Coverage
npm install -D @vitest/coverage-v8
```

### React with Vite

```bash
# Core dependencies
npm install -D vitest @vitest/ui
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @testing-library/user-event
npm install -D jsdom

# Coverage
npm install -D @vitest/coverage-v8
```

---

## ⚙️ Configuration Files

### vitest.config.ts (Vue 3)

```typescript
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'node:url';

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom', // or 'happy-dom'
    setupFiles: ['./tests/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        'src/main.ts',
      ],
      thresholds: {
        branches: 70,
        functions: 70,
        lines: 70,
        statements: 70,
      },
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
```

### vitest.config.ts (React with Vite)

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.*',
        'src/main.tsx',
      ],
      thresholds: {
        branches: 70,
        functions: 70,
        lines: 70,
        statements: 70,
      },
    },
    css: true, // Enable CSS processing
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### tests/setup.ts (Vue 3)

```typescript
import { config } from '@vue/test-utils';
import { vi } from 'vitest';

// Mock global properties
config.global.mocks = {
  $t: (key: string) => key, // i18n mock
};

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
  takeRecords() {
    return [];
  }
} as any;
```

### tests/setup.ts (React)

```typescript
import '@testing-library/jest-dom/vitest';
import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

// Auto cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock fetch
global.fetch = vi.fn();
```

---

## 🧪 Test Utilities

### tests/utils/test-utils.ts (Vue 3)

```typescript
import { mount, VueWrapper } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { createRouter, createMemoryHistory } from 'vue-router';

// Create test router
const createTestRouter = () => {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div>Home</div>' } },
    ],
  });
};

// Custom mount with providers
export const mountWithProviders = (
  component: any,
  options: any = {}
) => {
  const pinia = createPinia();
  const router = createTestRouter();

  return mount(component, {
    global: {
      plugins: [pinia, router],
      ...options.global,
    },
    ...options,
  });
};
```

### tests/utils/test-utils.tsx (React)

```typescript
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };
```

---

## 📝 Example Tests

### Vue Component Test

**src/components/__tests__/Button.spec.ts**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from '../Button.vue';

describe('Button Component', () => {
  it('renders button with text', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click me',
      },
    });

    expect(wrapper.text()).toContain('Click me');
  });

  it('emits click event', async () => {
    const wrapper = mount(Button);
    
    await wrapper.trigger('click');
    
    expect(wrapper.emitted('click')).toBeTruthy();
    expect(wrapper.emitted('click')?.length).toBe(1);
  });

  it('disables button when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true },
    });

    expect(wrapper.attributes('disabled')).toBeDefined();
  });

  it('applies custom class', () => {
    const wrapper = mount(Button, {
      props: { class: 'custom-class' },
    });

    expect(wrapper.classes()).toContain('custom-class');
  });

  it('shows loading state', () => {
    const wrapper = mount(Button, {
      props: { loading: true },
    });

    expect(wrapper.find('.spinner').exists()).toBe(true);
    expect(wrapper.attributes('disabled')).toBeDefined();
  });
});
```

### Vue Composable Test

**src/composables/__tests__/useCounter.spec.ts**

```typescript
import { describe, it, expect } from 'vitest';
import { useCounter } from '../useCounter';

describe('useCounter Composable', () => {
  it('initializes with default value', () => {
    const { count } = useCounter();
    expect(count.value).toBe(0);
  });

  it('initializes with custom value', () => {
    const { count } = useCounter(10);
    expect(count.value).toBe(10);
  });

  it('increments count', () => {
    const { count, increment } = useCounter();
    
    increment();
    expect(count.value).toBe(1);
    
    increment();
    expect(count.value).toBe(2);
  });

  it('decrements count', () => {
    const { count, decrement } = useCounter(5);
    
    decrement();
    expect(count.value).toBe(4);
  });

  it('resets count to initial value', () => {
    const { count, increment, reset } = useCounter(10);
    
    increment();
    increment();
    expect(count.value).toBe(12);
    
    reset();
    expect(count.value).toBe(10);
  });
});
```

### React Component Test

**src/components/__tests__/Button.test.tsx**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when disabled', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Async Test (Vue)

**src/components/__tests__/UserList.spec.ts**

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { flushPromises, mount } from '@vue/test-utils';
import UserList from '../UserList.vue';

// Mock API
vi.mock('@/api/users', () => ({
  fetchUsers: vi.fn(() => Promise.resolve([
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
  ])),
}));

describe('UserList Component', () => {
  it('displays loading state initially', () => {
    const wrapper = mount(UserList);
    expect(wrapper.text()).toContain('Loading');
  });

  it('displays users after loading', async () => {
    const wrapper = mount(UserList);
    
    await flushPromises();
    
    expect(wrapper.text()).toContain('John');
    expect(wrapper.text()).toContain('Jane');
  });

  it('displays error on API failure', async () => {
    const { fetchUsers } = await import('@/api/users');
    vi.mocked(fetchUsers).mockRejectedValueOnce(new Error('Failed'));

    const wrapper = mount(UserList);
    await flushPromises();

    expect(wrapper.text()).toContain('Error');
  });
});
```

---

## 🎯 Common Testing Patterns

### Testing Pinia Store (Vue)

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { setActivePinia, createPinia } from 'pinia';
import { useUserStore } from '@/stores/user';

describe('User Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('initializes with empty user', () => {
    const store = useUserStore();
    expect(store.user).toBeNull();
  });

  it('sets user on login', async () => {
    const store = useUserStore();
    
    await store.login({ email: 'test@example.com', password: 'pass' });
    
    expect(store.user).toBeTruthy();
    expect(store.user?.email).toBe('test@example.com');
  });

  it('clears user on logout', async () => {
    const store = useUserStore();
    
    await store.login({ email: 'test@example.com', password: 'pass' });
    store.logout();
    
    expect(store.user).toBeNull();
  });
});
```

### Testing Vue Router

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import { createRouter, createMemoryHistory } from 'vue-router';
import App from '../App.vue';

describe('App with Router', () => {
  it('navigates to home page', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/about', component: { template: '<div>About</div>' } },
      ],
    });

    const wrapper = mount(App, {
      global: {
        plugins: [router],
      },
    });

    await router.push('/');
    await router.isReady();

    expect(wrapper.text()).toContain('Home');
  });
});
```

### Snapshot Testing

```typescript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Card from '../Card.vue';

describe('Card Component Snapshot', () => {
  it('matches snapshot', () => {
    const wrapper = mount(Card, {
      props: {
        title: 'Test Card',
        content: 'This is test content',
      },
    });

    expect(wrapper.html()).toMatchSnapshot();
  });
});
```

---

## 📦 Package.json Scripts

```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest watch"
  }
}
```

---

## 🚀 Vitest UI

Vitest comes with a beautiful UI for running tests:

```bash
npm run test:ui
```

Visit `http://localhost:51204/__vitest__/` to see:
- Real-time test results
- Code coverage visualization
- Test execution timeline
- Console logs per test
- Module graph visualization

---

## ⚡ Performance Features

### In-Source Testing

```typescript
// src/utils/format.ts
export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
}

if (import.meta.vitest) {
  const { describe, it, expect } = import.meta.vitest;

  describe('formatCurrency', () => {
    it('formats amount as USD', () => {
      expect(formatCurrency(100)).toBe('$100.00');
    });
  });
}
```

### Test Sharding (CI)

```bash
# Run tests in parallel across multiple machines
vitest run --shard=1/3  # Machine 1
vitest run --shard=2/3  # Machine 2
vitest run --shard=3/3  # Machine 3
```

---

## 🔍 VSCode Integration

**.vscode/settings.json**

```json
{
  "vitest.enable": true,
  "vitest.commandLine": "npm run test"
}
```

**Install VSCode Extension:** Vitest

---

## ✅ Best Practices

1. **Use `describe` and `it` without imports:**
   ```typescript
   // Enabled by globals: true in config
   describe('MyComponent', () => {
     it('works', () => {
       expect(true).toBe(true);
     });
   });
   ```

2. **Mock modules at top level:**
   ```typescript
   vi.mock('@/api/users', () => ({
     fetchUsers: vi.fn(),
   }));
   ```

3. **Use `flushPromises` for async Vue:**
   ```typescript
   await flushPromises(); // Wait for all promises
   ```

4. **Prefer `happy-dom` for speed:**
   ```typescript
   // vitest.config.ts
   test: {
     environment: 'happy-dom', // Faster than jsdom
   }
   ```

5. **Use concurrent tests carefully:**
   ```typescript
   it.concurrent('test 1', async () => { /* ... */ });
   it.concurrent('test 2', async () => { /* ... */ });
   ```

---

## 🐛 Debugging

### Debug in VSCode

```json
{
  "type": "node",
  "request": "launch",
  "name": "Debug Vitest Tests",
  "runtimeExecutable": "npm",
  "runtimeArgs": ["run", "test"],
  "console": "integratedTerminal"
}
```

### Run specific test

```bash
# By file
npm test -- Button.spec.ts

# By pattern
npm test -- --grep="renders button"

# Single test with UI
npm run test:ui -- Button.spec.ts
```

---

## 📊 Coverage Reports

```bash
# Generate coverage
npm run test:coverage

# View HTML report
open coverage/index.html
```

---

## ✅ Production Checklist

- [ ] Vitest config with coverage thresholds
- [ ] Setup file with test utilities
- [ ] Custom render/mount function with providers
- [ ] All components tested
- [ ] Composables/hooks tested
- [ ] Store/state management tested
- [ ] Coverage ≥70%
- [ ] CI pipeline runs tests
- [ ] Vitest UI accessible in dev
- [ ] VSCode extension configured

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
