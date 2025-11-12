# TypeScript Strict Config - Type Safety Setup

**For:** TypeScript projects (React, Node.js, Full-stack)  
**Coverage:** Strict type checking, best practices  
**Tools:** TypeScript 5.0+, ts-node, type definitions

---

## 📦 Installation

```bash
# TypeScript
npm install -D typescript @types/node

# React types
npm install -D @types/react @types/react-dom

# Node.js development
npm install -D ts-node nodemon

# Additional type definitions
npm install -D @types/jest @types/express
```

---

## 📂 Project Structure

```
project/
├── tsconfig.json              # Base config
├── tsconfig.build.json        # Production build
├── tsconfig.test.json         # Test environment
├── src/
│   ├── types/
│   │   ├── global.d.ts        # Global types
│   │   ├── api.types.ts       # API types
│   │   └── index.ts           # Exported types
│   └── utils/
│       └── typeGuards.ts      # Type guards
└── package.json
```

---

## ⚙️ Configuration Files

### tsconfig.json (Base - Strict)

```json
{
  "compilerOptions": {
    /* Language and Environment */
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,

    /* Modules */
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,

    /* Emit */
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": true,
    "noEmit": false,
    "importHelpers": true,
    "downlevelIteration": true,

    /* Interop Constraints */
    "isolatedModules": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    /* Type Checking - STRICT MODE */
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "useUnknownInCatchVariables": true,
    "alwaysStrict": true,

    /* Additional Checks */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,

    /* Path Mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"],
      "@hooks/*": ["src/hooks/*"],
      "@api/*": ["src/api/*"]
    },

    /* Advanced */
    "skipLibCheck": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false
  },
  "include": ["src/**/*", "tests/**/*"],
  "exclude": ["node_modules", "dist", "build", "coverage"]
}
```

### tsconfig.json (Node.js Backend)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "moduleResolution": "node",
    "outDir": "./dist",
    "rootDir": "./src",

    /* Strict Type Checking */
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,

    /* Additional Checks */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,

    /* Emit */
    "declaration": true,
    "sourceMap": true,
    "removeComments": true,

    /* Interop */
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,

    /* Node.js Specific */
    "resolveJsonModule": true,
    "skipLibCheck": true,

    /* Path Mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### tsconfig.build.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": false,
    "declaration": true,
    "declarationMap": false,
    "sourceMap": false,
    "removeComments": true
  },
  "exclude": [
    "node_modules",
    "**/*.test.ts",
    "**/*.test.tsx",
    "**/*.spec.ts",
    "tests/**/*"
  ]
}
```

### tsconfig.test.json

```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "noEmit": true,
    "types": ["jest", "@testing-library/jest-dom"]
  },
  "include": ["src/**/*", "tests/**/*"]
}
```

---

## 📝 Type Examples & Patterns

### 1. Strict Null Checks

```typescript
// ❌ Bad - Implicit undefined
function getUser(id: string) {
  const user = users.find(u => u.id === id);
  return user.name; // Error: Object is possibly 'undefined'
}

// ✅ Good - Explicit handling
function getUser(id: string): string | null {
  const user = users.find(u => u.id === id);
  return user ? user.name : null;
}

// ✅ Better - Optional chaining
function getUserName(id: string): string | undefined {
  return users.find(u => u.id === id)?.name;
}

// ✅ Best - Type guard
function getUser(id: string): User {
  const user = users.find(u => u.id === id);
  if (!user) {
    throw new Error(`User ${id} not found`);
  }
  return user;
}
```

### 2. No Implicit Any

```typescript
// ❌ Bad - Implicit any
function processData(data) {
  return data.value;
}

// ✅ Good - Explicit types
function processData(data: { value: number }): number {
  return data.value;
}

// ✅ Better - Generic
function processData<T>(data: T): T {
  return data;
}

// ✅ Best - Type parameter constraint
function processData<T extends { value: number }>(data: T): number {
  return data.value;
}
```

### 3. Strict Function Types

```typescript
// Type definitions
type Handler = (event: MouseEvent) => void;
type GenericHandler = (event: Event) => void;

// ❌ Bad - Type mismatch
const handler: Handler = (event: Event) => {
  // Error: Type 'Event' is not assignable to 'MouseEvent'
};

// ✅ Good - Correct types
const handler: Handler = (event: MouseEvent) => {
  console.log(event.clientX);
};

// ✅ Generic approach
function addListener<T extends Event>(
  element: HTMLElement,
  type: string,
  handler: (event: T) => void
): void {
  element.addEventListener(type, handler as EventListener);
}
```

### 4. Index Signature Safety

```typescript
// With noUncheckedIndexedAccess: true

interface Data {
  [key: string]: number;
}

const data: Data = { a: 1, b: 2 };

// ❌ Bad - Unchecked access
const value: number = data['c']; // Error: Type 'number | undefined'

// ✅ Good - Checked access
const value = data['c'];
if (value !== undefined) {
  const squared: number = value * value;
}

// ✅ Better - Type guard
function isValidKey(key: string, obj: Data): key is keyof Data {
  return key in obj;
}

if (isValidKey('c', data)) {
  const value: number = data['c'];
}
```

### 5. Type Guards

```typescript
// Type predicates
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

// Usage
function processValue(value: unknown) {
  if (isString(value)) {
    // value is string here
    return value.toUpperCase();
  }
  
  if (isUser(value)) {
    // value is User here
    return value.name;
  }
  
  throw new Error('Invalid value type');
}
```

### 6. Discriminated Unions

```typescript
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string }
  | { status: 'loading' };

function handleResponse<T>(response: ApiResponse<T>) {
  // TypeScript narrows the type based on status
  switch (response.status) {
    case 'success':
      // response.data is available here
      console.log(response.data);
      break;
    
    case 'error':
      // response.error is available here
      console.error(response.error);
      break;
    
    case 'loading':
      // Only status is available here
      console.log('Loading...');
      break;
  }
}
```

### 7. Utility Types

```typescript
// Original type
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

// Partial - All properties optional
type PartialUser = Partial<User>;
// { id?: string; name?: string; ... }

// Required - All properties required
type RequiredUser = Required<User>;

// Pick - Select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;
// { id: string; name: string }

// Omit - Exclude specific properties
type UserWithoutDates = Omit<User, 'createdAt'>;

// Readonly - Immutable
type ReadonlyUser = Readonly<User>;

// Record - Key-value map
type UserMap = Record<string, User>;

// Custom utility
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

### 8. Async/Await Types

```typescript
// ❌ Bad - Missing error handling type
async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// ✅ Good - Explicit return type
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json() as Promise<User>;
}

// ✅ Better - Result type
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      return { success: false, error: new Error('Not found') };
    }
    const user = await response.json();
    return { success: true, value: user };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error : new Error('Unknown error')
    };
  }
}
```

### 9. Generic Constraints

```typescript
// Basic constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Multiple constraints
function merge<T extends object, U extends object>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

// Conditional types
type NonNullable<T> = T extends null | undefined ? never : T;
type Flatten<T> = T extends Array<infer U> ? U : T;

// Usage
type Str = NonNullable<string | null>; // string
type Num = Flatten<number[]>; // number
```

### 10. Advanced Patterns

```typescript
// Builder pattern with strict types
class UserBuilder {
  private user: Partial<User> = {};

  setName(name: string): this {
    this.user.name = name;
    return this;
  }

  setEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  build(): User {
    // TypeScript ensures all required fields are set
    if (!this.user.name || !this.user.email) {
      throw new Error('Missing required fields');
    }
    return this.user as User;
  }
}

// Factory with type inference
function createFactory<T>(constructor: new () => T) {
  return (): T => new constructor();
}

const userFactory = createFactory(User);
const user = userFactory(); // Type: User
```

---

## 🔧 Common Type Errors & Solutions

### Error: Object is possibly 'undefined'

```typescript
// ❌ Error
const user = users.find(u => u.id === id);
console.log(user.name); // Error

// ✅ Solutions
// 1. Optional chaining
console.log(user?.name);

// 2. Nullish coalescing
const name = user?.name ?? 'Unknown';

// 3. Type guard
if (user) {
  console.log(user.name);
}

// 4. Non-null assertion (use sparingly)
console.log(user!.name);
```

### Error: Property 'X' does not exist

```typescript
// ❌ Error
interface Config {
  apiUrl: string;
}
const config: Config = {};
console.log(config.apiUrl); // Error

// ✅ Solutions
// 1. Optional property
interface Config {
  apiUrl?: string;
}

// 2. Default value
interface Config {
  apiUrl: string;
}
const config: Config = { apiUrl: 'default' };

// 3. Type assertion
const config = {} as Config;
```

### Error: Type 'X' is not assignable to type 'Y'

```typescript
// ❌ Error
const num: number = '123'; // Error

// ✅ Solutions
// 1. Convert type
const num: number = parseInt('123', 10);

// 2. Union type
const value: number | string = '123';

// 3. Type assertion (if you're sure)
const num = '123' as unknown as number; // Not recommended
```

---

## 📋 Package.json Scripts

```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "build": "tsc -p tsconfig.build.json",
    "build:watch": "tsc -p tsconfig.build.json --watch",
    "clean": "rm -rf dist"
  }
}
```

---

## ✅ Best Practices

1. **Enable Strict Mode:** Always use `"strict": true`
2. **Avoid Any:** Use `unknown` instead when type is uncertain
3. **Type Guards:** Create reusable type checking functions
4. **Utility Types:** Leverage built-in utility types
5. **Explicit Returns:** Specify function return types
6. **No Implicit Any:** Force explicit type annotations
7. **Null Checks:** Always handle undefined/null cases
8. **Index Signatures:** Use noUncheckedIndexedAccess
9. **Discriminated Unions:** Use for state management
10. **Generic Constraints:** Add constraints to generics

---

## 🐛 Common Issues

**Issue:** `Cannot find module '@/components'`  
**Fix:** Configure `paths` in tsconfig.json

**Issue:** `Module has no default export`  
**Fix:** Use named imports or add `esModuleInterop: true`

**Issue:** `Type instantiation is excessively deep`  
**Fix:** Simplify complex recursive types

**Issue:** Slow type checking  
**Fix:** Use `skipLibCheck: true`, optimize project references

---

## 🚀 Gradual Adoption

```javascript
// Start with basic strict mode
{
  "strict": true
}

// Add incrementally
{
  "strict": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true
}

// Full strict mode
{
  "strict": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noImplicitReturns": true,
  "noFallthroughCasesInSwitch": true,
  "noUncheckedIndexedAccess": true
}
```

---

**Ready for:** TypeScript 5.0+ projects  
**Next:** Run `npm run type-check` to validate
