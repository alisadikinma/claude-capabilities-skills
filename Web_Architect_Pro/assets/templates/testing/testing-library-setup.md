# Testing Library - Component Testing Guide

**Framework:** Testing Library (React/Vue/Svelte/Angular)  
**Philosophy:** Test components like users interact with them  
**Use Case:** User-centric component testing, accessibility testing  
**Best For:** Unit & integration tests focused on user behavior

---

## 🎯 Core Principles

1. **Test behavior, not implementation**
2. **Query by accessibility attributes**
3. **Avoid testing internal state**
4. **Focus on user interactions**
5. **Write maintainable tests**

---

## 📦 Installation by Framework

### React Testing Library

```bash
npm install -D @testing-library/react
npm install -D @testing-library/jest-dom
npm install -D @testing-library/user-event
```

### Vue Testing Library

```bash
npm install -D @testing-library/vue
npm install -D @testing-library/jest-dom
npm install -D @testing-library/user-event
```

### Svelte Testing Library

```bash
npm install -D @testing-library/svelte
npm install -D @testing-library/jest-dom
npm install -D @testing-library/user-event
```

---

## 🔍 Query Priority Guide

**Use in this order:**

1. **Queries Accessible to Everyone**
   - `getByRole` - ARIA roles, semantic HTML
   - `getByLabelText` - Form labels
   - `getByPlaceholderText` - Input placeholders
   - `getByText` - Text content
   - `getByDisplayValue` - Current input values

2. **Semantic Queries**
   - `getByAltText` - Image alt text
   - `getByTitle` - Element title attribute

3. **Test IDs (Last Resort)**
   - `getByTestId` - data-testid attribute

---

## 📝 Query Variants

### getBy* - Throws if not found
```typescript
// Expects element to exist
const button = screen.getByRole('button', { name: /submit/i });
```

### queryBy* - Returns null if not found
```typescript
// Check element doesn't exist
const error = screen.queryByText(/error/i);
expect(error).not.toBeInTheDocument();
```

### findBy* - Async, waits for element
```typescript
// Wait for element to appear
const message = await screen.findByText(/success/i);
```

### getAllBy*, queryAllBy*, findAllBy*
```typescript
// Multiple elements
const items = screen.getAllByRole('listitem');
expect(items).toHaveLength(3);
```

---

## 🧪 React Testing Examples

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('handles click', async () => {
    const handleClick = jest.fn();
    const user = userEvent.setup();
    
    render(<Button onClick={handleClick}>Click me</Button>);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('can be disabled', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Form Testing

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits form with credentials', async () => {
    const handleSubmit = jest.fn();
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={handleSubmit} />);
    
    // Use labels to find inputs (accessible)
    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'user@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={jest.fn()} />);
    
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });

  it('clears error on input', async () => {
    const user = userEvent.setup();
    
    render(<LoginForm onSubmit={jest.fn()} />);
    
    await user.click(screen.getByRole('button', { name: /login/i }));
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    
    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    
    expect(screen.queryByText(/email is required/i)).not.toBeInTheDocument();
  });
});
```

### Async Component

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('loads and displays user data', async () => {
    render(<UserProfile userId="1" />);
    
    // Loading state
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    
    // Wait for data
    expect(await screen.findByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    
    // Loading should be gone
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('displays error on failure', async () => {
    // Mock API to return error
    global.fetch = jest.fn(() =>
      Promise.reject(new Error('Failed to fetch'))
    );

    render(<UserProfile userId="1" />);
    
    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });
});
```

### List Rendering

```typescript
import { render, screen } from '@testing-library/react';
import { TodoList } from './TodoList';

describe('TodoList', () => {
  const todos = [
    { id: 1, text: 'Buy milk', completed: false },
    { id: 2, text: 'Walk dog', completed: true },
  ];

  it('renders all todos', () => {
    render(<TodoList todos={todos} />);
    
    const items = screen.getAllByRole('listitem');
    expect(items).toHaveLength(2);
  });

  it('shows completed status', () => {
    render(<TodoList todos={todos} />);
    
    const buyMilk = screen.getByText('Buy milk');
    const walkDog = screen.getByText('Walk dog');
    
    expect(buyMilk).not.toHaveClass('completed');
    expect(walkDog).toHaveClass('completed');
  });

  it('filters completed todos', () => {
    render(<TodoList todos={todos} showCompleted={false} />);
    
    expect(screen.getByText('Buy milk')).toBeInTheDocument();
    expect(screen.queryByText('Walk dog')).not.toBeInTheDocument();
  });
});
```

---

## 🧪 Vue Testing Examples

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/vue';
import userEvent from '@testing-library/user-event';
import Button from './Button.vue';

describe('Button', () => {
  it('renders with text', () => {
    render(Button, {
      slots: {
        default: 'Click me',
      },
    });
    
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('emits click event', async () => {
    const user = userEvent.setup();
    const { emitted } = render(Button, {
      slots: { default: 'Click me' },
    });
    
    await user.click(screen.getByRole('button'));
    
    expect(emitted().click).toBeTruthy();
    expect(emitted().click).toHaveLength(1);
  });

  it('applies variant class', () => {
    render(Button, {
      props: { variant: 'primary' },
      slots: { default: 'Button' },
    });
    
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });
});
```

### Form Testing (Vue)

```typescript
import { render, screen } from '@testing-library/vue';
import userEvent from '@testing-library/user-event';
import LoginForm from './LoginForm.vue';

describe('LoginForm', () => {
  it('emits submit with credentials', async () => {
    const user = userEvent.setup();
    const { emitted } = render(LoginForm);
    
    await user.type(screen.getByLabelText(/email/i), 'user@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(emitted().submit).toBeTruthy();
    expect(emitted().submit[0][0]).toEqual({
      email: 'user@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();
    render(LoginForm);
    
    await user.click(screen.getByRole('button', { name: /login/i }));
    
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

### Composition API Testing

```typescript
import { render, screen, waitFor } from '@testing-library/vue';
import Counter from './Counter.vue';

describe('Counter with Composition API', () => {
  it('increments count', async () => {
    const user = userEvent.setup();
    render(Counter);
    
    expect(screen.getByText(/count: 0/i)).toBeInTheDocument();
    
    await user.click(screen.getByRole('button', { name: /increment/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
    });
  });

  it('starts with initial count', () => {
    render(Counter, {
      props: { initialCount: 10 },
    });
    
    expect(screen.getByText(/count: 10/i)).toBeInTheDocument();
  });
});
```

---

## 🎯 Common Patterns

### Testing Accessibility

```typescript
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button Accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('is keyboard accessible', async () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    const button = screen.getByRole('button');
    button.focus();
    
    await userEvent.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalled();
  });
});
```

### Testing with Context/Providers

```typescript
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from './ThemeContext';
import { ThemedButton } from './ThemedButton';

function renderWithTheme(ui: React.ReactElement, theme = 'light') {
  return render(
    <ThemeProvider theme={theme}>
      {ui}
    </ThemeProvider>
  );
}

describe('ThemedButton', () => {
  it('uses light theme', () => {
    renderWithTheme(<ThemedButton />, 'light');
    expect(screen.getByRole('button')).toHaveClass('btn-light');
  });

  it('uses dark theme', () => {
    renderWithTheme(<ThemedButton />, 'dark');
    expect(screen.getByRole('button')).toHaveClass('btn-dark');
  });
});
```

### Testing Router Navigation

```typescript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import { Navigation } from './Navigation';

function renderWithRouter(ui: React.ReactElement) {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
}

describe('Navigation', () => {
  it('navigates to different routes', async () => {
    const user = userEvent.setup();
    renderWithRouter(<Navigation />);
    
    await user.click(screen.getByRole('link', { name: /about/i }));
    
    expect(window.location.pathname).toBe('/about');
  });
});
```

### Testing Custom Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('increments count', () => {
    const { result } = renderHook(() => useCounter());
    
    expect(result.current.count).toBe(0);
    
    result.current.increment();
    
    expect(result.current.count).toBe(1);
  });

  it('accepts initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    
    result.current.increment();
    result.current.increment();
    expect(result.current.count).toBe(7);
    
    result.current.reset();
    expect(result.current.count).toBe(5);
  });
});
```

### Testing with React Query

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserList } from './UserList';

function createWrapper() {
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
}

describe('UserList', () => {
  it('fetches and displays users', async () => {
    render(<UserList />, { wrapper: createWrapper() });
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });
});
```

---

## 🔍 Debugging Tips

### Debug Output

```typescript
import { render, screen } from '@testing-library/react';

it('debug test', () => {
  render(<MyComponent />);
  
  // Print entire DOM
  screen.debug();
  
  // Print specific element
  screen.debug(screen.getByRole('button'));
  
  // Limit output lines
  screen.debug(undefined, 300000);
});
```

### Suggested Queries

```typescript
// When query fails, get suggestions
screen.getByRole('buttons'); // Typo
// Error message shows:
// Here are the accessible roles:
//   button:
//   Name "Submit":
//   <button />
```

### logRoles

```typescript
import { render, logRoles } from '@testing-library/react';

it('log all roles', () => {
  const { container } = render(<MyComponent />);
  logRoles(container);
});
```

---

## ✅ Best Practices

1. **Prefer getByRole:**
   ```typescript
   // ✅ Good - Accessible
   screen.getByRole('button', { name: /submit/i })
   
   // ❌ Bad - Brittle
   screen.getByClassName('submit-btn')
   ```

2. **Use userEvent over fireEvent:**
   ```typescript
   // ✅ Good - Realistic
   const user = userEvent.setup();
   await user.click(button);
   
   // ❌ Bad - Less realistic
   fireEvent.click(button);
   ```

3. **Don't test implementation:**
   ```typescript
   // ❌ Bad - Testing internal state
   expect(component.state.count).toBe(1);
   
   // ✅ Good - Testing behavior
   expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
   ```

4. **Use semantic queries:**
   ```typescript
   // ✅ Good
   screen.getByLabelText(/email/i)
   
   // ❌ Avoid unless necessary
   screen.getByTestId('email-input')
   ```

5. **Wait for async changes:**
   ```typescript
   // ✅ Good
   await screen.findByText(/success/i);
   
   // ❌ Bad
   await wait(1000);
   ```

---

## 🛠️ Custom Matchers

```typescript
// jest-dom provides these matchers:
expect(element).toBeInTheDocument();
expect(element).toBeVisible();
expect(element).toBeEmpty();
expect(element).toBeDisabled();
expect(element).toBeEnabled();
expect(element).toBeInvalid();
expect(element).toBeRequired();
expect(element).toHaveClass('class-name');
expect(element).toHaveStyle({ color: 'red' });
expect(element).toHaveTextContent('text');
expect(element).toHaveValue('value');
expect(element).toHaveAttribute('attr', 'value');
expect(element).toHaveFocus();
expect(element).toBeChecked();
```

---

## ✅ Production Checklist

- [ ] Using correct query priority (getByRole first)
- [ ] Testing user behavior, not implementation
- [ ] Using userEvent for interactions
- [ ] Properly waiting for async changes
- [ ] Accessibility tests included
- [ ] Custom render utilities for providers
- [ ] Mocking external dependencies
- [ ] Descriptive test names
- [ ] Debugging tools configured
- [ ] All user flows covered

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
