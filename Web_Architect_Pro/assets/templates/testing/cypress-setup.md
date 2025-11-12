# Cypress - E2E Testing Complete Setup

**Framework:** Cypress 13.x  
**Use Case:** E2E testing, component testing, API testing  
**Coverage:** Browser automation, time travel debugging, network stubbing  
**Best For:** Interactive debugging, real-time reloads, visual testing

---

## 📁 Project Structure

```
project-root/
├── cypress/
│   ├── e2e/
│   │   ├── auth/
│   │   │   ├── login.cy.ts
│   │   │   └── register.cy.ts
│   │   │
│   │   ├── dashboard/
│   │   │   └── dashboard.cy.ts
│   │   │
│   │   └── api/
│   │       └── users-api.cy.ts
│   │
│   ├── fixtures/
│   │   ├── users.json
│   │   └── auth.json
│   │
│   ├── support/
│   │   ├── commands.ts          # Custom commands
│   │   ├── e2e.ts               # E2E support file
│   │   └── component.ts         # Component testing support
│   │
│   └── downloads/               # Downloaded files
│
├── cypress.config.ts
└── package.json
```

---

## 🔧 Installation

```bash
# Install Cypress
npm install -D cypress

# Open Cypress for first time setup
npx cypress open

# Install TypeScript types
npm install -D @cypress/webpack-preprocessor
npm install -D typescript

# Component testing (React)
npm install -D @cypress/react @cypress/webpack-dev-server

# Component testing (Vue)
npm install -D @cypress/vue @cypress/webpack-dev-server
```

---

## ⚙️ Configuration

### cypress.config.ts

```typescript
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:5173',
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    env: {
      apiUrl: 'http://localhost:3000/api',
    },
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',
  },

  component: {
    devServer: {
      framework: 'react', // or 'vue'
      bundler: 'vite',
    },
    specPattern: 'src/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/component.ts',
  },

  retries: {
    runMode: 2,
    openMode: 0,
  },

  screenshotsFolder: 'cypress/screenshots',
  videosFolder: 'cypress/videos',
  downloadsFolder: 'cypress/downloads',
});
```

---

## 📝 Support Files

### cypress/support/e2e.ts

```typescript
import './commands';

// Hide fetch/XHR requests in command log
const app = window.top;
if (!app.document.head.querySelector('[data-hide-command-log-request]')) {
  const style = app.document.createElement('style');
  style.innerHTML = '.command-name-request, .command-name-xhr { display: none }';
  style.setAttribute('data-hide-command-log-request', '');
  app.document.head.appendChild(style);
}

// Global before hook
beforeEach(() => {
  cy.log('Starting new test');
});

// Global after hook
afterEach(() => {
  cy.log('Test completed');
});
```

### cypress/support/commands.ts

```typescript
/// <reference types="cypress" />

declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      logout(): Chainable<void>;
      getBySel(selector: string): Chainable<JQuery<HTMLElement>>;
      getBySelLike(selector: string): Chainable<JQuery<HTMLElement>>;
      fillForm(data: Record<string, string>): Chainable<void>;
    }
  }
}

// Custom login command
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-test="email"]').type(email);
    cy.get('[data-test="password"]').type(password);
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/dashboard');
  });
});

// Custom logout command
Cypress.Commands.add('logout', () => {
  cy.get('[data-test="user-menu"]').click();
  cy.get('[data-test="logout-button"]').click();
});

// Get by data-test attribute
Cypress.Commands.add('getBySel', (selector: string) => {
  return cy.get(`[data-test="${selector}"]`);
});

// Get by partial data-test match
Cypress.Commands.add('getBySelLike', (selector: string) => {
  return cy.get(`[data-test*="${selector}"]`);
});

// Fill form helper
Cypress.Commands.add('fillForm', (data: Record<string, string>) => {
  Object.entries(data).forEach(([key, value]) => {
    cy.get(`[name="${key}"]`).clear().type(value);
  });
});
```

---

## 📝 Example Tests

### Basic E2E Test

**cypress/e2e/auth/login.cy.ts**

```typescript
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('displays login form', () => {
    cy.contains('h1', /login/i).should('be.visible');
    cy.getBySel('email').should('be.visible');
    cy.getBySel('password').should('be.visible');
    cy.getBySel('login-button').should('be.visible');
  });

  it('logs in with valid credentials', () => {
    cy.getBySel('email').type('user@example.com');
    cy.getBySel('password').type('password123');
    cy.getBySel('login-button').click();

    cy.url().should('include', '/dashboard');
    cy.contains('Welcome').should('be.visible');
  });

  it('shows error with invalid credentials', () => {
    cy.getBySel('email').type('wrong@example.com');
    cy.getBySel('password').type('wrongpass');
    cy.getBySel('login-button').click();

    cy.contains(/invalid credentials/i).should('be.visible');
    cy.url().should('include', '/login');
  });

  it('validates required fields', () => {
    cy.getBySel('login-button').click();
    
    cy.contains(/email is required/i).should('be.visible');
    cy.contains(/password is required/i).should('be.visible');
  });

  it('remembers me checkbox works', () => {
    cy.getBySel('remember-me').check();
    cy.getBySel('email').type('user@example.com');
    cy.getBySel('password').type('password123');
    cy.getBySel('login-button').click();

    // Verify localStorage/cookie
    cy.getCookie('remember_token').should('exist');
  });
});
```

### Using Custom Commands

**cypress/e2e/dashboard/dashboard.cy.ts**

```typescript
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password123');
    cy.visit('/dashboard');
  });

  it('displays user information', () => {
    cy.getBySel('user-name').should('contain', 'John Doe');
    cy.getBySel('user-email').should('contain', 'user@example.com');
  });

  it('allows navigation to settings', () => {
    cy.getBySel('settings-link').click();
    cy.url().should('include', '/settings');
  });

  it('logs out successfully', () => {
    cy.logout();
    cy.url().should('include', '/login');
  });
});
```

### API Testing

**cypress/e2e/api/users-api.cy.ts**

```typescript
describe('Users API', () => {
  it('GET /api/users returns user list', () => {
    cy.request('GET', `${Cypress.env('apiUrl')}/users`).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');
      expect(response.body.length).to.be.greaterThan(0);
    });
  });

  it('POST /api/users creates new user', () => {
    cy.request({
      method: 'POST',
      url: `${Cypress.env('apiUrl')}/users`,
      body: {
        name: 'John Doe',
        email: 'john@example.com',
      },
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('id');
      expect(response.body.name).to.eq('John Doe');
    });
  });

  it('handles authentication', () => {
    // Login first
    cy.request({
      method: 'POST',
      url: `${Cypress.env('apiUrl')}/auth/login`,
      body: {
        email: 'user@example.com',
        password: 'password123',
      },
    }).then((loginResponse) => {
      const token = loginResponse.body.token;

      // Use token in subsequent request
      cy.request({
        method: 'GET',
        url: `${Cypress.env('apiUrl')}/profile`,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }).then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body).to.have.property('email');
      });
    });
  });
});
```

### Network Stubbing

**cypress/e2e/mocking/stub-api.cy.ts**

```typescript
describe('API Stubbing', () => {
  it('stubs API response', () => {
    cy.intercept('GET', '/api/users', {
      statusCode: 200,
      body: [
        { id: 1, name: 'Mocked User 1' },
        { id: 2, name: 'Mocked User 2' },
      ],
    }).as('getUsers');

    cy.visit('/users');
    cy.wait('@getUsers');

    cy.contains('Mocked User 1').should('be.visible');
    cy.contains('Mocked User 2').should('be.visible');
  });

  it('modifies API response', () => {
    cy.intercept('GET', '/api/config', (req) => {
      req.reply((res) => {
        res.body.feature_flag = true;
        return res;
      });
    });

    cy.visit('/');
  });

  it('simulates network error', () => {
    cy.intercept('GET', '/api/users', {
      statusCode: 500,
      body: { error: 'Internal Server Error' },
    }).as('getUsersError');

    cy.visit('/users');
    cy.wait('@getUsersError');

    cy.contains(/error loading users/i).should('be.visible');
  });

  it('adds delay to response', () => {
    cy.intercept('GET', '/api/users', (req) => {
      req.reply((res) => {
        res.delay = 2000; // 2 second delay
      });
    });

    cy.visit('/users');
    cy.getBySel('loading-spinner').should('be.visible');
  });
});
```

### File Upload

**cypress/e2e/upload/file-upload.cy.ts**

```typescript
describe('File Upload', () => {
  it('uploads a file', () => {
    cy.visit('/upload');

    const fileName = 'test-file.pdf';
    cy.fixture(fileName, 'binary')
      .then(Cypress.Blob.binaryStringToBlob)
      .then((fileContent) => {
        cy.getBySel('file-input').attachFile({
          fileContent,
          fileName,
          mimeType: 'application/pdf',
        });
      });

    cy.getBySel('upload-button').click();
    cy.contains(/upload successful/i).should('be.visible');
  });

  it('uploads multiple files', () => {
    cy.visit('/upload-multiple');

    cy.fixture('file1.jpg', 'binary')
      .then(Cypress.Blob.binaryStringToBlob)
      .then((file1) => {
        cy.fixture('file2.jpg', 'binary')
          .then(Cypress.Blob.binaryStringToBlob)
          .then((file2) => {
            const files = [
              { fileContent: file1, fileName: 'file1.jpg', mimeType: 'image/jpeg' },
              { fileContent: file2, fileName: 'file2.jpg', mimeType: 'image/jpeg' },
            ];
            cy.getBySel('file-input').attachFile(files);
          });
      });

    cy.getBySel('upload-button').click();
  });
});
```

### Using Fixtures

**cypress/fixtures/users.json**

```json
{
  "validUser": {
    "email": "user@example.com",
    "password": "password123"
  },
  "adminUser": {
    "email": "admin@example.com",
    "password": "admin123"
  }
}
```

**Usage:**

```typescript
describe('Login with Fixtures', () => {
  it('logs in with valid user', () => {
    cy.fixture('users').then((users) => {
      cy.visit('/login');
      cy.getBySel('email').type(users.validUser.email);
      cy.getBySel('password').type(users.validUser.password);
      cy.getBySel('login-button').click();
    });
  });
});
```

---

## 🎯 Advanced Patterns

### Session Management

```typescript
// Reuse authentication across tests
describe('Authenticated Tests', () => {
  beforeEach(() => {
    cy.session('user-session', () => {
      cy.visit('/login');
      cy.getBySel('email').type('user@example.com');
      cy.getBySel('password').type('password123');
      cy.getBySel('login-button').click();
    });
  });

  it('test 1', () => { /* authenticated */ });
  it('test 2', () => { /* authenticated */ });
});
```

### Viewport Testing

```typescript
describe('Responsive Design', () => {
  const viewports = [
    { name: 'mobile', width: 375, height: 667 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'desktop', width: 1920, height: 1080 },
  ];

  viewports.forEach(({ name, width, height }) => {
    it(`displays correctly on ${name}`, () => {
      cy.viewport(width, height);
      cy.visit('/');
      cy.getBySel('header').should('be.visible');
    });
  });
});
```

### Wait for Conditions

```typescript
describe('Dynamic Content', () => {
  it('waits for element', () => {
    cy.visit('/');
    cy.getBySel('loader').should('not.exist');
    cy.getBySel('content').should('be.visible');
  });

  it('waits for API call', () => {
    cy.intercept('GET', '/api/data').as('getData');
    cy.visit('/');
    cy.wait('@getData').its('response.statusCode').should('eq', 200);
  });

  it('waits with custom condition', () => {
    cy.visit('/');
    cy.window().its('app.isReady').should('equal', true);
  });
});
```

### Database Seeding

**cypress/support/commands.ts**

```typescript
Cypress.Commands.add('seedDatabase', () => {
  cy.request('POST', `${Cypress.env('apiUrl')}/test/seed`);
});

Cypress.Commands.add('resetDatabase', () => {
  cy.request('POST', `${Cypress.env('apiUrl')}/test/reset`);
});
```

**Usage:**

```typescript
describe('With Seeded Data', () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.seedDatabase();
  });

  it('displays seeded users', () => {
    cy.visit('/users');
    cy.getBySel('user-list').children().should('have.length', 10);
  });
});
```

---

## 📦 Package.json Scripts

```json
{
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:run:chrome": "cypress run --browser chrome",
    "cy:run:firefox": "cypress run --browser firefox",
    "cy:run:edge": "cypress run --browser edge",
    "cy:run:headed": "cypress run --headed",
    "cy:run:spec": "cypress run --spec 'cypress/e2e/auth/login.cy.ts'",
    "cy:component": "cypress open --component",
    "cy:component:run": "cypress run --component"
  }
}
```

---

## 🚀 Cypress Features

### Time Travel

```typescript
// Click through test steps in GUI
cy.getBySel('button').click(); // Step 1
cy.getBySel('input').type('text'); // Step 2
// Can click on any step in GUI to see DOM state
```

### Real-time Reloads

Tests automatically re-run when files change in GUI mode.

### Network Traffic Control

```typescript
cy.intercept('GET', '/api/*', (req) => {
  req.continue((res) => {
    // Log all API calls
    cy.log(`${req.method} ${req.url} - ${res.statusCode}`);
  });
});
```

### Screenshots

```typescript
cy.screenshot('my-screenshot');
cy.getBySel('element').screenshot('element-screenshot');
```

### Video Recording

Automatically records videos in headless mode.

---

## 🔍 Debugging

### Debug Command

```typescript
cy.getBySel('button').click();
cy.debug(); // Pause execution
cy.getBySel('result').should('be.visible');
```

### Pause Command

```typescript
cy.getBySel('button').click();
cy.pause(); // Pause and allow manual interaction
```

### Console Logs

```typescript
cy.getBySel('data').then(($el) => {
  console.log('Element:', $el);
  debugger; // Use browser DevTools
});
```

---

## 📊 CI/CD Integration

### GitHub Actions

**.github/workflows/cypress.yml**

```yaml
name: Cypress Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  cypress-run:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:5173'
          browser: chrome
          record: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
      
      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots
      
      - name: Upload videos
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: cypress-videos
          path: cypress/videos
```

### Cypress Dashboard

```bash
# Record tests to Cypress Dashboard
npx cypress run --record --key <record-key>
```

---

## ✅ Best Practices

1. **Use data-test attributes:**
   ```html
   <button data-test="submit-button">Submit</button>
   ```

2. **Avoid brittle selectors:**
   ```typescript
   // ❌ Bad
   cy.get('.btn-primary.submit')
   
   // ✅ Good
   cy.getBySel('submit-button')
   ```

3. **Don't use cy.wait(time):**
   ```typescript
   // ❌ Bad
   cy.wait(3000)
   
   // ✅ Good
   cy.wait('@apiCall')
   cy.getBySel('element').should('be.visible')
   ```

4. **Chain commands:**
   ```typescript
   cy.getBySel('input')
     .clear()
     .type('text')
     .should('have.value', 'text');
   ```

5. **Use aliases:**
   ```typescript
   cy.getBySel('button').as('submitButton');
   cy.get('@submitButton').click();
   ```

---

## ✅ Production Checklist

- [ ] Cypress config optimized
- [ ] Custom commands created
- [ ] Tests organized by feature
- [ ] Network stubbing configured
- [ ] Session management implemented
- [ ] Fixtures created for test data
- [ ] CI pipeline configured
- [ ] Video recording enabled
- [ ] Screenshot on failure enabled
- [ ] Cypress Dashboard integrated (optional)

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
