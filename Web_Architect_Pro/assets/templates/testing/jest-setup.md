# Jest + React Testing Library - Complete Setup

**Framework:** Jest 29.x + React Testing Library 14.x  
**Use Case:** Unit & integration testing for React/Next.js applications  
**Coverage:** Component testing, hooks testing, API mocking  
**Best For:** React 18+, Next.js 13+, TypeScript projects

---

## 📁 Project Structure

```
project-root/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   └── __tests__/
│   │       └── Button.test.tsx
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   └── __tests__/
│   │       └── useAuth.test.ts
│   │
│   └── utils/
│       ├── format.ts
│       └── __tests__/
│           └── format.test.ts
│
├── __tests__/
│   ├── setup.ts                # Test setup file
│   └── utils/
│       └── test-utils.tsx      # Custom render function
│
├── jest.config.js
├── jest.setup.js
└── package.json
```

---

## 🔧 Installation

### React Projects (CRA, Vite)

```bash
# Core dependencies
npm install -D jest @types/jest
npm install -D @testing-library/react @testing-library/jest-dom
npm install -D @testing-library/user-event
npm install -D jest-environment-jsdom

# For TypeScript
npm install -D ts-jest @types/testing-library__jest-dom

# For Next.js
npm install -D @testing-library/react @testing-library/jest-dom
```

### Next.js Specific Setup

```bash
npm install -D jest jest-environment-jsdom @testing-library/react
npm install -D @testing-library/jest-dom @testing-library/user-event
```

---

## ⚙️ Configuration Files

### jest.config.js (React/Vite)

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/main.tsx',
    '!src/vite-env.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react-jsx',
      },
    }],
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
};
```

### jest.config.js (Next.js 13+)

```javascript
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testMatch: [
    '**/__tests__/**/*.test.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};

module.exports = createJestConfig(customJestConfig);
```

### jest.setup.js

```javascript
import '@testing-library/jest-dom';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
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
};

// Mock fetch
global.fetch = jest.fn();
```

### __mocks__/fileMock.js

```javascript
module.exports = 'test-file-stub';
```

---

## 🧪 Test Utilities

### __tests__/utils/test-utils.tsx

```typescript
import { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Custom render with providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
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

// Re-export everything
export * from '@testing-library/react';
export { customRender as render };
```

---

## 📝 Example Tests

### Component Test

**src/components/__tests__/Button.test.tsx**

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from '../Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles click events', async () => {
    const handleClick = jest.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies custom className', () => {
    render(<Button className="custom-class">Styled</Button>);
    expect(screen.getByRole('button')).toHaveClass('custom-class');
  });

  it('renders loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

### Hook Test

**src/hooks/__tests__/useAuth.test.ts**

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../useAuth';

describe('useAuth Hook', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('initializes with no user', () => {
    const { result } = renderHook(() => useAuth());
    expect(result.current.user).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('logs in user successfully', async () => {
    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      result.current.login({ email: 'test@example.com', password: 'password' });
    });

    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user?.email).toBe('test@example.com');
  });

  it('logs out user', async () => {
    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      result.current.login({ email: 'test@example.com', password: 'password' });
    });

    result.current.logout();

    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBeNull();
  });

  it('persists auth state in localStorage', async () => {
    const { result } = renderHook(() => useAuth());

    await waitFor(() => {
      result.current.login({ email: 'test@example.com', password: 'password' });
    });

    const token = localStorage.getItem('token');
    expect(token).toBeTruthy();
  });
});
```

### API Mock Test

**src/services/__tests__/api.test.ts**

```typescript
import { fetchUsers } from '../api';

describe('API Service', () => {
  beforeEach(() => {
    (global.fetch as jest.Mock).mockClear();
  });

  it('fetches users successfully', async () => {
    const mockUsers = [
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' },
    ];

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });

    const users = await fetchUsers();

    expect(users).toEqual(mockUsers);
    expect(global.fetch).toHaveBeenCalledWith('/api/users');
  });

  it('handles API errors', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    await expect(fetchUsers()).rejects.toThrow('Failed to fetch users');
  });

  it('handles network errors', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error('Network error')
    );

    await expect(fetchUsers()).rejects.toThrow('Network error');
  });
});
```

### Form Validation Test

**src/components/__tests__/LoginForm.test.tsx**

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from '../LoginForm';

describe('LoginForm', () => {
  it('shows validation errors for empty fields', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });

  it('shows error for invalid email', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={jest.fn()} />);

    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.click(screen.getByRole('button', { name: /login/i }));

    expect(await screen.findByText(/invalid email/i)).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    const handleSubmit = jest.fn();
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });
});
```

---

## 🎯 Common Testing Patterns

### Testing Async Components

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { UserProfile } from '../UserProfile';

describe('UserProfile', () => {
  it('displays loading state', () => {
    render(<UserProfile userId="1" />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('displays user data after loading', async () => {
    render(<UserProfile userId="1" />);
    
    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
  });

  it('displays error message on failure', async () => {
    render(<UserProfile userId="invalid" />);
    
    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });
});
```

### Testing with React Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor } from '@testing-library/react';
import { UserList } from '../UserList';

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

describe('UserList with React Query', () => {
  it('fetches and displays users', async () => {
    render(<UserList />, { wrapper: createWrapper() });

    await waitFor(() => {
      expect(screen.getByText(/john doe/i)).toBeInTheDocument();
    });
  });
});
```

### Testing Context

```typescript
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '../ThemeContext';
import { ThemedButton } from '../ThemedButton';

describe('ThemedButton', () => {
  it('uses theme from context', () => {
    render(
      <ThemeProvider theme="dark">
        <ThemedButton />
      </ThemeProvider>
    );

    const button = screen.getByRole('button');
    expect(button).toHaveClass('dark-theme');
  });
});
```

---

## 📦 Package.json Scripts

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2",
    "test:debug": "node --inspect-brk node_modules/.bin/jest --runInBand"
  }
}
```

---

## 🔍 VSCode Integration

**.vscode/settings.json**

```json
{
  "jest.autoRun": "off",
  "jest.showCoverageOnLoad": true,
  "jest.testExplorer": {
    "enabled": true
  }
}
```

**Install VSCode Extension:** Jest Runner

---

## ✅ Best Practices

1. **Use Testing Library Queries Priority:**
   - `getByRole` > `getByLabelText` > `getByPlaceholderText` > `getByText` > `getByTestId`

2. **Avoid Testing Implementation Details:**
   ```typescript
   // ❌ Bad
   expect(component.state.count).toBe(1);
   
   // ✅ Good
   expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
   ```

3. **Use userEvent Over fireEvent:**
   ```typescript
   // ❌ Less realistic
   fireEvent.click(button);
   
   // ✅ More realistic
   await userEvent.click(button);
   ```

4. **Mock External Dependencies:**
   ```typescript
   jest.mock('../api', () => ({
     fetchUsers: jest.fn(),
   }));
   ```

5. **Clean Up After Each Test:**
   ```typescript
   afterEach(() => {
     jest.clearAllMocks();
     cleanup();
   });
   ```

---

## 🐛 Debugging Tests

### Run Single Test

```bash
# By name pattern
npm test -- --testNamePattern="renders button"

# By file
npm test -- Button.test.tsx

# Watch mode with specific file
npm test -- --watch Button.test.tsx
```

### Debug in VSCode

```json
{
  "type": "node",
  "request": "launch",
  "name": "Jest Debug",
  "program": "${workspaceFolder}/node_modules/.bin/jest",
  "args": ["--runInBand"],
  "console": "integratedTerminal",
  "internalConsoleOptions": "neverOpen"
}
```

---

## 📊 Coverage Reports

```bash
# Generate coverage
npm test -- --coverage

# View in browser
open coverage/lcov-report/index.html
```

---

## ✅ Production Checklist

- [ ] Jest config file created
- [ ] Setup file with @testing-library/jest-dom
- [ ] Custom render utility with providers
- [ ] All components have tests
- [ ] Hooks tested with renderHook
- [ ] API calls mocked properly
- [ ] Coverage threshold ≥70%
- [ ] CI pipeline runs tests
- [ ] Tests pass in watch mode
- [ ] VSCode Jest extension configured

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
