# Playwright - E2E Testing Complete Setup

**Framework:** Playwright 1.40+  
**Use Case:** End-to-end testing, cross-browser testing, visual regression  
**Coverage:** Multi-browser (Chromium, Firefox, WebKit), mobile emulation  
**Best For:** Production-grade E2E testing, CI/CD integration

---

## 📁 Project Structure

```
project-root/
├── tests/
│   ├── e2e/
│   │   ├── auth/
│   │   │   ├── login.spec.ts
│   │   │   └── register.spec.ts
│   │   │
│   │   ├── dashboard/
│   │   │   └── dashboard.spec.ts
│   │   │
│   │   └── api/
│   │       └── users-api.spec.ts
│   │
│   ├── fixtures/
│   │   ├── test-data.ts
│   │   └── auth.fixture.ts
│   │
│   └── utils/
│       └── helpers.ts
│
├── playwright.config.ts
├── playwright-report/         # Generated reports
├── test-results/              # Test artifacts
└── package.json
```

---

## 🔧 Installation

```bash
# Install Playwright
npm init playwright@latest

# Or manual install
npm install -D @playwright/test
npx playwright install

# Install specific browsers only
npx playwright install chromium
npx playwright install firefox
npx playwright install webkit

# With dependencies (Linux)
npx playwright install --with-deps
```

---

## ⚙️ Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

---

## 📝 Example Tests

### Basic Test

**tests/e2e/auth/login.spec.ts**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('displays login form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /login/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /login/i })).toBeVisible();
  });

  test('logs in with valid credentials', async ({ page }) => {
    await page.getByLabel(/email/i).fill('user@example.com');
    await page.getByLabel(/password/i).fill('password123');
    await page.getByRole('button', { name: /login/i }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText(/welcome/i)).toBeVisible();
  });

  test('shows error with invalid credentials', async ({ page }) => {
    await page.getByLabel(/email/i).fill('wrong@example.com');
    await page.getByLabel(/password/i).fill('wrongpass');
    await page.getByRole('button', { name: /login/i }).click();

    await expect(page.getByText(/invalid credentials/i)).toBeVisible();
    await expect(page).toHaveURL('/login');
  });

  test('validates email format', async ({ page }) => {
    await page.getByLabel(/email/i).fill('invalid-email');
    await page.getByLabel(/password/i).fill('password123');
    await page.getByRole('button', { name: /login/i }).click();

    await expect(page.getByText(/invalid email/i)).toBeVisible();
  });
});
```

### Page Object Model

**tests/fixtures/pages/LoginPage.ts**

```typescript
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel(/email/i);
    this.passwordInput = page.getByLabel(/password/i);
    this.loginButton = page.getByRole('button', { name: /login/i });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectError(message: string) {
    await this.errorMessage.waitFor({ state: 'visible' });
    await this.errorMessage.getByText(message).waitFor();
  }
}
```

**Usage:**

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../fixtures/pages/LoginPage';

test('login with POM', async ({ page }) => {
  const loginPage = new LoginPage(page);
  
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password123');
  
  await expect(page).toHaveURL('/dashboard');
});
```

### Custom Fixtures

**tests/fixtures/auth.fixture.ts**

```typescript
import { test as base, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

type AuthFixtures = {
  authenticatedPage: any;
  loginPage: LoginPage;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page }, use) => {
    // Auto-login before test
    await page.goto('/login');
    await page.getByLabel(/email/i).fill('user@example.com');
    await page.getByLabel(/password/i).fill('password123');
    await page.getByRole('button', { name: /login/i }).click();
    await page.waitForURL('/dashboard');
    
    await use(page);
  },
});

export { expect };
```

**Usage:**

```typescript
import { test, expect } from '../fixtures/auth.fixture';

test('access dashboard', async ({ authenticatedPage }) => {
  // Already logged in!
  await expect(authenticatedPage.getByText(/dashboard/i)).toBeVisible();
});
```

### API Testing

**tests/e2e/api/users-api.spec.ts**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Users API', () => {
  test('GET /api/users returns user list', async ({ request }) => {
    const response = await request.get('/api/users');
    
    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);
    
    const users = await response.json();
    expect(users).toBeInstanceOf(Array);
    expect(users.length).toBeGreaterThan(0);
  });

  test('POST /api/users creates new user', async ({ request }) => {
    const response = await request.post('/api/users', {
      data: {
        name: 'John Doe',
        email: 'john@example.com',
      },
    });

    expect(response.status()).toBe(201);
    
    const user = await response.json();
    expect(user.name).toBe('John Doe');
    expect(user.email).toBe('john@example.com');
  });

  test('handles authentication', async ({ request }) => {
    // Login first
    const loginResponse = await request.post('/api/auth/login', {
      data: {
        email: 'user@example.com',
        password: 'password123',
      },
    });

    const { token } = await loginResponse.json();

    // Use token in subsequent requests
    const response = await request.get('/api/profile', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    expect(response.ok()).toBeTruthy();
  });
});
```

### Visual Regression Testing

**tests/e2e/visual/homepage.spec.ts**

```typescript
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test('responsive layout snapshots', async ({ page }) => {
    await page.goto('/');

    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('desktop.png');

    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('tablet.png');

    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page).toHaveScreenshot('mobile.png');
  });

  test('element snapshot', async ({ page }) => {
    await page.goto('/');
    const header = page.locator('header');
    
    await expect(header).toHaveScreenshot('header.png');
  });
});
```

### File Upload Test

```typescript
import { test, expect } from '@playwright/test';
import path from 'path';

test('upload file', async ({ page }) => {
  await page.goto('/upload');

  const fileInput = page.locator('input[type="file"]');
  const filePath = path.join(__dirname, '../fixtures/test-file.pdf');
  
  await fileInput.setInputFiles(filePath);
  await page.getByRole('button', { name: /upload/i }).click();

  await expect(page.getByText(/upload successful/i)).toBeVisible();
});
```

### Mocking Network Requests

```typescript
import { test, expect } from '@playwright/test';

test('mock API responses', async ({ page }) => {
  // Intercept and mock
  await page.route('/api/users', (route) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'Mock User 1' },
        { id: 2, name: 'Mock User 2' },
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('Mock User 1')).toBeVisible();
});

test('modify API response', async ({ page }) => {
  await page.route('/api/config', async (route) => {
    const response = await route.fetch();
    const json = await response.json();
    
    // Modify response
    json.feature_flag = true;
    
    await route.fulfill({ response, json });
  });

  await page.goto('/');
});
```

---

## 🎯 Advanced Patterns

### Parallel Test Execution

```typescript
import { test } from '@playwright/test';

test.describe.configure({ mode: 'parallel' });

test.describe('Parallel Tests', () => {
  test('test 1', async ({ page }) => { /* ... */ });
  test('test 2', async ({ page }) => { /* ... */ });
  test('test 3', async ({ page }) => { /* ... */ });
});
```

### Test Annotations

```typescript
import { test, expect } from '@playwright/test';

test('flaky test', async ({ page }) => {
  test.slow(); // Triple timeout
  // ...
});

test('skip in CI', async ({ page }) => {
  test.skip(!!process.env.CI, 'Not ready for CI');
  // ...
});

test('fixme: broken test', async ({ page }) => {
  test.fixme(); // Mark as known issue
  // ...
});

test.only('run only this test', async ({ page }) => {
  // Only this test will run
});
```

### Multiple Tabs/Windows

```typescript
import { test, expect } from '@playwright/test';

test('handle multiple tabs', async ({ context }) => {
  const page1 = await context.newPage();
  await page1.goto('/');

  const [page2] = await Promise.all([
    context.waitForEvent('page'),
    page1.getByText('Open in new tab').click(),
  ]);

  await page2.waitForLoadState();
  await expect(page2).toHaveURL('/new-page');
});
```

### Geolocation & Permissions

```typescript
import { test, expect } from '@playwright/test';

test('use geolocation', async ({ context, page }) => {
  await context.grantPermissions(['geolocation']);
  await context.setGeolocation({ latitude: 37.7749, longitude: -122.4194 });

  await page.goto('/map');
  await expect(page.getByText(/San Francisco/i)).toBeVisible();
});
```

---

## 📦 Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:chromium": "playwright test --project=chromium",
    "test:e2e:report": "playwright show-report",
    "test:e2e:codegen": "playwright codegen http://localhost:5173"
  }
}
```

---

## 🚀 Playwright Features

### Trace Viewer

When test fails with trace enabled:

```bash
npx playwright show-trace test-results/trace.zip
```

Features:
- Timeline of actions
- Network requests
- Console logs
- Screenshots at each step
- DOM snapshots

### Code Generator

```bash
# Generate test code by recording
npx playwright codegen http://localhost:5173

# With authentication
npx playwright codegen --save-storage=auth.json http://localhost:5173
npx playwright codegen --load-storage=auth.json http://localhost:5173/dashboard
```

### UI Mode (Interactive)

```bash
npm run test:e2e:ui
```

Features:
- Run/debug tests interactively
- Time travel through test steps
- View DOM snapshots
- Network panel
- Console logs

---

## 🔍 Debugging

### Debug Mode

```bash
# Debug all tests
npx playwright test --debug

# Debug specific test
npx playwright test login.spec.ts --debug

# Debug from specific line
npx playwright test login.spec.ts:10 --debug
```

### Console Logs

```typescript
test('with console logs', async ({ page }) => {
  page.on('console', msg => console.log('BROWSER:', msg.text()));
  await page.goto('/');
});
```

### Slow Motion

```typescript
import { chromium } from '@playwright/test';

const browser = await chromium.launch({ slowMo: 1000 }); // 1 second delay
```

---

## 📊 CI/CD Integration

### GitHub Actions

**.github/workflows/playwright.yml**

```yaml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright Browsers
        run: npx playwright install --with-deps
      
      - name: Run Playwright tests
        run: npm run test:e2e
      
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

### Docker

**Dockerfile.playwright**

```dockerfile
FROM mcr.microsoft.com/playwright:v1.40.0-jammy

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

CMD ["npm", "run", "test:e2e"]
```

---

## ✅ Best Practices

1. **Use Locators Wisely:**
   ```typescript
   // ✅ Good - Accessible
   page.getByRole('button', { name: /submit/i })
   page.getByLabel(/email/i)
   
   // ❌ Bad - Brittle
   page.locator('.submit-btn')
   ```

2. **Wait for State, Not Timeout:**
   ```typescript
   // ✅ Good
   await page.waitForLoadState('networkidle');
   
   // ❌ Bad
   await page.waitForTimeout(3000);
   ```

3. **Use Auto-waiting:**
   ```typescript
   // No need for manual waits
   await page.getByText('Button').click(); // Auto-waits
   ```

4. **Isolate Tests:**
   ```typescript
   test.beforeEach(async ({ page }) => {
     // Fresh state for each test
   });
   ```

5. **Use Fixtures for Setup:**
   ```typescript
   // Reusable auth state
   export const test = base.extend({ /* ... */ });
   ```

---

## ✅ Production Checklist

- [ ] Playwright config with all browsers
- [ ] Tests organized by feature
- [ ] Page Object Model implemented
- [ ] Custom fixtures created
- [ ] API tests included
- [ ] Visual regression tests setup
- [ ] CI pipeline configured
- [ ] Test reports generated
- [ ] Trace on failure enabled
- [ ] Parallel execution configured

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
