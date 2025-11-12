# Jest Node Setup - Node.js Backend Testing

**For:** Express, NestJS, Fastify backends  
**Coverage:** Unit, Integration, API testing  
**Tools:** Jest, Supertest, ts-jest

---

## 📦 Installation

```bash
# Core testing
npm install -D jest @types/jest ts-jest

# API testing
npm install -D supertest @types/supertest

# Coverage
npm install -D @jest/globals

# Additional tools
npm install -D jest-mock-extended  # Advanced mocking
npm install -D nock  # HTTP mocking
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   └── utils/
├── tests/
│   ├── unit/
│   │   ├── services/
│   │   │   ├── user.service.test.ts
│   │   │   └── payment.service.test.ts
│   │   ├── utils/
│   │   │   └── validation.test.ts
│   │   └── models/
│   │       └── user.model.test.ts
│   ├── integration/
│   │   ├── database/
│   │   │   └── user.repository.test.ts
│   │   └── external/
│   │       └── payment.gateway.test.ts
│   ├── e2e/
│   │   ├── auth.test.ts
│   │   ├── users.test.ts
│   │   └── products.test.ts
│   ├── fixtures/
│   │   ├── users.json
│   │   └── products.json
│   └── setup.ts
├── jest.config.js
└── jest.setup.js
```

---

## ⚙️ Configuration Files

### jest.config.js

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/index.ts',
    '!src/config/**',
    '!src/**/types/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  coverageDirectory: 'coverage',
  verbose: true,
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  testTimeout: 10000,
  clearMocks: true,
  resetMocks: true,
  restoreMocks: true,
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1'
  }
};
```

### jest.setup.js

```javascript
// Global test setup
beforeAll(async () => {
  // Setup test database connection
  // await setupTestDatabase();
});

afterAll(async () => {
  // Cleanup
  // await closeTestDatabase();
});

// Extend Jest matchers
expect.extend({
  toBeValidEmail(received) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received);
    
    return {
      pass,
      message: () => 
        pass
          ? `Expected ${received} not to be a valid email`
          : `Expected ${received} to be a valid email`
    };
  }
});
```

### tests/setup.ts

```typescript
import { config } from 'dotenv';

// Load test environment variables
config({ path: '.env.test' });

// Mock environment variables
process.env.NODE_ENV = 'test';
process.env.JWT_SECRET = 'test-secret-key';
process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test_db';

// Global test utilities
export const mockRequest = (body = {}, params = {}, query = {}) => ({
  body,
  params,
  query,
  headers: {},
  user: null
});

export const mockResponse = () => {
  const res: any = {};
  res.status = jest.fn().mockReturnValue(res);
  res.json = jest.fn().mockReturnValue(res);
  res.send = jest.fn().mockReturnValue(res);
  return res;
};
```

---

## 📝 Test Examples

### 1. Unit Test - Services

```typescript
// tests/unit/services/user.service.test.ts
import { UserService } from '@/services/user.service';
import { UserRepository } from '@/repositories/user.repository';
import { hashPassword, comparePassword } from '@/utils/crypto';

// Mock dependencies
jest.mock('@/repositories/user.repository');
jest.mock('@/utils/crypto');

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepository = new UserRepository() as jest.Mocked<UserRepository>;
    userService = new UserService(mockUserRepository);
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    it('should create user with hashed password', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User'
      };
      
      const hashedPassword = 'hashed_password';
      (hashPassword as jest.Mock).mockResolvedValue(hashedPassword);
      
      mockUserRepository.create.mockResolvedValue({
        id: '1',
        ...userData,
        password: hashedPassword
      });

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(hashPassword).toHaveBeenCalledWith('password123');
      expect(mockUserRepository.create).toHaveBeenCalledWith({
        ...userData,
        password: hashedPassword
      });
      expect(result.password).toBe(hashedPassword);
    });

    it('should throw error if email exists', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue({
        id: '1',
        email: 'test@example.com'
      } as any);

      // Act & Assert
      await expect(
        userService.createUser({
          email: 'test@example.com',
          password: 'pass',
          name: 'Test'
        })
      ).rejects.toThrow('Email already exists');
    });
  });

  describe('authenticateUser', () => {
    it('should return user and token on valid credentials', async () => {
      // Arrange
      const user = {
        id: '1',
        email: 'test@example.com',
        password: 'hashed_password'
      };
      
      mockUserRepository.findByEmail.mockResolvedValue(user as any);
      (comparePassword as jest.Mock).mockResolvedValue(true);

      // Act
      const result = await userService.authenticateUser(
        'test@example.com',
        'password123'
      );

      // Assert
      expect(result).toHaveProperty('user');
      expect(result).toHaveProperty('token');
      expect(result.user.email).toBe('test@example.com');
    });

    it('should throw error on invalid credentials', async () => {
      // Arrange
      mockUserRepository.findByEmail.mockResolvedValue(null);

      // Act & Assert
      await expect(
        userService.authenticateUser('test@example.com', 'wrong')
      ).rejects.toThrow('Invalid credentials');
    });
  });
});
```

### 2. Unit Test - Utils

```typescript
// tests/unit/utils/validation.test.ts
import {
  isValidEmail,
  isStrongPassword,
  sanitizeInput
} from '@/utils/validation';

describe('Validation Utils', () => {
  describe('isValidEmail', () => {
    it.each([
      ['test@example.com', true],
      ['user.name@domain.co.uk', true],
      ['invalid.email', false],
      ['@nodomain.com', false],
      ['missing@', false]
    ])('validates %s as %s', (email, expected) => {
      expect(isValidEmail(email)).toBe(expected);
    });
  });

  describe('isStrongPassword', () => {
    it('should accept strong passwords', () => {
      expect(isStrongPassword('Str0ng!Pass')).toBe(true);
    });

    it('should reject weak passwords', () => {
      expect(isStrongPassword('weak')).toBe(false);
      expect(isStrongPassword('12345678')).toBe(false);
      expect(isStrongPassword('NoNumbers!')).toBe(false);
    });
  });

  describe('sanitizeInput', () => {
    it('should remove HTML tags', () => {
      expect(sanitizeInput('<script>alert("xss")</script>'))
        .toBe('alert("xss")');
    });

    it('should trim whitespace', () => {
      expect(sanitizeInput('  test  ')).toBe('test');
    });
  });
});
```

### 3. Integration Test - Database

```typescript
// tests/integration/database/user.repository.test.ts
import { UserRepository } from '@/repositories/user.repository';
import { setupTestDatabase, teardownTestDatabase } from '@tests/fixtures/database';

describe('UserRepository Integration', () => {
  let repository: UserRepository;

  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    repository = new UserRepository();
    // Clear users table
    await repository.deleteAll();
  });

  describe('create', () => {
    it('should create user in database', async () => {
      // Arrange
      const userData = {
        email: 'test@example.com',
        password: 'hashedpass',
        name: 'Test User'
      };

      // Act
      const user = await repository.create(userData);

      // Assert
      expect(user).toHaveProperty('id');
      expect(user.email).toBe(userData.email);
      
      // Verify in DB
      const found = await repository.findById(user.id);
      expect(found).not.toBeNull();
      expect(found!.email).toBe(userData.email);
    });
  });

  describe('findByEmail', () => {
    it('should find existing user', async () => {
      // Arrange
      const created = await repository.create({
        email: 'test@example.com',
        password: 'pass',
        name: 'Test'
      });

      // Act
      const found = await repository.findByEmail('test@example.com');

      // Assert
      expect(found).not.toBeNull();
      expect(found!.id).toBe(created.id);
    });

    it('should return null for non-existent user', async () => {
      const found = await repository.findByEmail('nonexistent@example.com');
      expect(found).toBeNull();
    });
  });

  describe('update', () => {
    it('should update user fields', async () => {
      // Arrange
      const user = await repository.create({
        email: 'test@example.com',
        password: 'pass',
        name: 'Original Name'
      });

      // Act
      const updated = await repository.update(user.id, {
        name: 'Updated Name'
      });

      // Assert
      expect(updated.name).toBe('Updated Name');
      expect(updated.email).toBe('test@example.com'); // Unchanged
    });
  });
});
```

### 4. E2E Test - API Endpoints

```typescript
// tests/e2e/auth.test.ts
import request from 'supertest';
import { app } from '@/app';
import { setupTestDatabase, teardownTestDatabase } from '@tests/fixtures/database';

describe('Authentication API', () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe('POST /api/auth/register', () => {
    it('should register new user', async () => {
      const userData = {
        email: 'newuser@example.com',
        password: 'StrongPass123!',
        name: 'New User'
      };

      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      expect(response.body).toHaveProperty('user');
      expect(response.body).toHaveProperty('token');
      expect(response.body.user.email).toBe(userData.email);
      expect(response.body.user).not.toHaveProperty('password');
    });

    it('should reject invalid email', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'invalid-email',
          password: 'StrongPass123!',
          name: 'Test'
        })
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });

    it('should reject duplicate email', async () => {
      const userData = {
        email: 'duplicate@example.com',
        password: 'Pass123!',
        name: 'Test'
      };

      // First registration
      await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      // Duplicate registration
      const response = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(409);

      expect(response.body.error).toContain('already exists');
    });
  });

  describe('POST /api/auth/login', () => {
    const userCredentials = {
      email: 'login@example.com',
      password: 'LoginPass123!'
    };

    beforeEach(async () => {
      // Register user for login tests
      await request(app)
        .post('/api/auth/register')
        .send({
          ...userCredentials,
          name: 'Login User'
        });
    });

    it('should login with valid credentials', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send(userCredentials)
        .expect(200);

      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user.email).toBe(userCredentials.email);
    });

    it('should reject invalid password', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: userCredentials.email,
          password: 'WrongPassword'
        })
        .expect(401);

      expect(response.body.error).toContain('Invalid credentials');
    });

    it('should reject non-existent user', async () => {
      const response = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'nonexistent@example.com',
          password: 'AnyPassword'
        })
        .expect(401);
    });
  });

  describe('GET /api/auth/me', () => {
    let authToken: string;

    beforeEach(async () => {
      // Register and login to get token
      const response = await request(app)
        .post('/api/auth/register')
        .send({
          email: 'authuser@example.com',
          password: 'AuthPass123!',
          name: 'Auth User'
        });
      
      authToken = response.body.token;
    });

    it('should return current user with valid token', async () => {
      const response = await request(app)
        .get('/api/auth/me')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body).toHaveProperty('id');
      expect(response.body.email).toBe('authuser@example.com');
    });

    it('should reject request without token', async () => {
      await request(app)
        .get('/api/auth/me')
        .expect(401);
    });

    it('should reject invalid token', async () => {
      await request(app)
        .get('/api/auth/me')
        .set('Authorization', 'Bearer invalid-token')
        .expect(401);
    });
  });
});
```

### 5. Mocking External APIs

```typescript
// tests/integration/external/payment.gateway.test.ts
import nock from 'nock';
import { PaymentGateway } from '@/services/payment.gateway';

describe('PaymentGateway External API', () => {
  let gateway: PaymentGateway;

  beforeEach(() => {
    gateway = new PaymentGateway();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should process payment successfully', async () => {
    // Mock Stripe API
    nock('https://api.stripe.com')
      .post('/v1/charges')
      .reply(200, {
        id: 'ch_test123',
        status: 'succeeded',
        amount: 5000
      });

    const result = await gateway.charge({
      amount: 5000,
      currency: 'usd',
      source: 'tok_test'
    });

    expect(result.status).toBe('succeeded');
    expect(result.id).toBe('ch_test123');
  });

  it('should handle payment failure', async () => {
    nock('https://api.stripe.com')
      .post('/v1/charges')
      .reply(402, {
        error: {
          message: 'Insufficient funds'
        }
      });

    await expect(
      gateway.charge({
        amount: 5000,
        currency: 'usd',
        source: 'tok_test'
      })
    ).rejects.toThrow('Insufficient funds');
  });
});
```

---

## 🚀 Running Tests

```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test user.service.test

# Specific test
npm test -- -t "should create user"

# Update snapshots
npm test -- -u

# Verbose output
npm test -- --verbose

# Silent mode
npm test -- --silent

# Run only changed tests
npm test -- --onlyChanged
```

---

## 📊 Coverage Reports

```bash
# Generate HTML report
npm test -- --coverage --coverageDirectory=coverage

# Open report
open coverage/index.html

# Coverage with threshold
npm test -- --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80,"statements":80}}'
```

---

## 🔍 Advanced Patterns

### Test Fixtures

```typescript
// tests/fixtures/users.ts
export const mockUsers = [
  {
    id: '1',
    email: 'user1@example.com',
    name: 'User One'
  },
  {
    id: '2',
    email: 'user2@example.com',
    name: 'User Two'
  }
];

export const createMockUser = (overrides = {}) => ({
  id: '1',
  email: 'default@example.com',
  name: 'Default User',
  ...overrides
});
```

### Custom Matchers

```typescript
// tests/matchers.ts
expect.extend({
  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `Expected ${received} to be within range ${floor} - ${ceiling}`
    };
  }
});

// Usage
expect(response.time).toBeWithinRange(0, 1000);
```

---

## ✅ Best Practices

1. **Isolation:** Each test independent
2. **Clear Names:** Describe behavior, not implementation
3. **AAA Pattern:** Arrange → Act → Assert
4. **Mock External:** Mock APIs, databases for unit tests
5. **Test Behavior:** Not implementation details
6. **Coverage:** 80%+ for critical paths
7. **Fast Tests:** Unit tests < 100ms
8. **Setup/Teardown:** Use beforeEach/afterEach
9. **Async Handling:** Use async/await properly
10. **Snapshots:** Use sparingly for complex structures

---

## 🐛 Common Issues

**Issue:** `Cannot find module '@/services'`  
**Fix:** Check `moduleNameMapper` in jest.config.js

**Issue:** `Timeout - Async callback not invoked`  
**Fix:** Return promise or use async/await

**Issue:** `Cannot use import statement`  
**Fix:** Ensure ts-jest preset configured

**Issue:** Tests run in wrong order  
**Fix:** Don't rely on test execution order

---

**Ready for:** Express, NestJS, Fastify  
**Next:** Run `npm test` to validate setup
