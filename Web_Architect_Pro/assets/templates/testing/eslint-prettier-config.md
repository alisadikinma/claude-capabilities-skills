# ESLint + Prettier Config - Code Quality Setup

**For:** JavaScript, TypeScript projects  
**Coverage:** Linting, formatting, code quality  
**Tools:** ESLint, Prettier, lint-staged, husky

---

## 📦 Installation

```bash
# ESLint + TypeScript
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Prettier
npm install -D prettier eslint-config-prettier eslint-plugin-prettier

# Git hooks
npm install -D husky lint-staged

# Additional plugins (optional)
npm install -D eslint-plugin-import eslint-plugin-react eslint-plugin-react-hooks
npm install -D eslint-plugin-jest eslint-plugin-node
```

---

## 📂 Project Structure

```
project/
├── .eslintrc.js
├── .prettierrc.js
├── .prettierignore
├── .husky/
│   ├── pre-commit
│   └── pre-push
├── lint-staged.config.js
└── package.json
```

---

## ⚙️ Configuration Files

### .eslintrc.js (TypeScript + React)

```javascript
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
    jest: true
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'plugin:jest/recommended',
    'prettier' // Must be last
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json'],
    ecmaFeatures: {
      jsx: true
    }
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'react-hooks',
    'import',
    'jest',
    'prettier'
  ],
  settings: {
    react: {
      version: 'detect'
    },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json'
      }
    }
  },
  rules: {
    // Prettier integration
    'prettier/prettier': 'error',

    // TypeScript
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }
    ],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'warn',
    '@typescript-eslint/consistent-type-imports': [
      'error',
      { prefer: 'type-imports' }
    ],
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',

    // React
    'react/react-in-jsx-scope': 'off', // Next.js 13+
    'react/prop-types': 'off', // Using TypeScript
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // Import
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index'
        ],
        'newlines-between': 'always',
        alphabetize: { order: 'asc', caseInsensitive: true }
      }
    ],
    'import/no-unresolved': 'error',
    'import/no-cycle': 'error',

    // General
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'error',
    'prefer-const': 'error',
    'no-var': 'error',
    'eqeqeq': ['error', 'always'],
    'curly': ['error', 'all']
  },
  overrides: [
    {
      // Test files
      files: ['**/*.test.ts', '**/*.test.tsx', '**/*.spec.ts'],
      env: {
        jest: true
      },
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
        '@typescript-eslint/no-non-null-assertion': 'off'
      }
    }
  ]
};
```

### .eslintrc.js (Node.js Backend)

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    es2021: true,
    jest: true
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:node/recommended',
    'plugin:jest/recommended',
    'prettier'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json']
  },
  plugins: ['@typescript-eslint', 'node', 'jest', 'prettier'],
  rules: {
    'prettier/prettier': 'error',
    
    // TypeScript
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_' }
    ],
    '@typescript-eslint/explicit-function-return-type': [
      'warn',
      { allowExpressions: true }
    ],
    '@typescript-eslint/no-floating-promises': 'error',
    
    // Node.js
    'node/no-unsupported-features/es-syntax': [
      'error',
      { ignores: ['modules'] }
    ],
    'node/no-missing-import': 'off', // Using TypeScript resolver
    
    // Security
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    
    // Error handling
    'no-throw-literal': 'error',
    'prefer-promise-reject-errors': 'error'
  }
};
```

### .prettierrc.js

```javascript
module.exports = {
  // Line width
  printWidth: 80,
  
  // Indentation
  tabWidth: 2,
  useTabs: false,
  
  // Semicolons
  semi: true,
  
  // Quotes
  singleQuote: true,
  quoteProps: 'as-needed',
  jsxSingleQuote: false,
  
  // Trailing commas
  trailingComma: 'es5',
  
  // Brackets
  bracketSpacing: true,
  bracketSameLine: false,
  
  // Arrows
  arrowParens: 'always',
  
  // Line endings
  endOfLine: 'lf',
  
  // Overrides for specific files
  overrides: [
    {
      files: '*.json',
      options: {
        printWidth: 120
      }
    },
    {
      files: '*.md',
      options: {
        proseWrap: 'always'
      }
    }
  ]
};
```

### .prettierignore

```
# Dependencies
node_modules
vendor

# Build output
dist
build
out
.next

# Coverage
coverage
.nyc_output

# Cache
.cache
.parcel-cache
.turbo

# Logs
*.log

# Environment
.env
.env.*

# Lock files
package-lock.json
yarn.lock
pnpm-lock.yaml
```

### lint-staged.config.js

```javascript
module.exports = {
  // TypeScript/JavaScript
  '*.{ts,tsx,js,jsx}': [
    'eslint --fix',
    'prettier --write',
    () => 'tsc --noEmit' // Type check
  ],
  
  // JSON, YAML, Markdown
  '*.{json,yaml,yml,md}': ['prettier --write'],
  
  // CSS, SCSS
  '*.{css,scss}': ['prettier --write'],
  
  // Run tests for changed files
  '*.test.{ts,tsx}': ['jest --bail --findRelatedTests']
};
```

---

## 🪝 Git Hooks with Husky

### Setup Husky

```bash
# Initialize
npx husky install

# Add to package.json
npm pkg set scripts.prepare="husky install"

# Create hooks
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/pre-push "npm test"
```

### .husky/pre-commit

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🔍 Running lint-staged..."
npx lint-staged

echo "✅ Pre-commit checks passed!"
```

### .husky/pre-push

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

echo "🧪 Running tests..."
npm test -- --watchAll=false --passWithNoTests

echo "✅ Pre-push checks passed!"
```

---

## 📋 Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx,.js,.jsx",
    "lint:fix": "eslint . --ext .ts,.tsx,.js,.jsx --fix",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\"",
    "type-check": "tsc --noEmit",
    "check-all": "npm run type-check && npm run lint && npm run format:check",
    "prepare": "husky install"
  }
}
```

---

## 🚀 Usage Examples

### Lint All Files

```bash
# Check for issues
npm run lint

# Auto-fix issues
npm run lint:fix

# Lint specific directory
npx eslint src/
```

### Format Code

```bash
# Format all files
npm run format

# Check formatting
npm run format:check

# Format specific file
npx prettier --write src/components/Button.tsx
```

### Pre-commit Flow

```bash
# Automatic on git commit
git add .
git commit -m "feat: add new feature"
# → lint-staged runs
# → ESLint fixes issues
# → Prettier formats code
# → TypeScript type checks
# → Commit proceeds if all pass
```

---

## 🔧 IDE Integration

### VS Code (.vscode/settings.json)

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### VS Code Extensions

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "editorconfig.editorconfig"
  ]
}
```

---

## 🎯 Common Rules Explained

### Import Organization

```typescript
// ✅ Good - Grouped and alphabetized
import { useState, useEffect } from 'react';
import axios from 'axios';

import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';

import { formatDate } from './utils';

// ❌ Bad - Random order
import { formatDate } from './utils';
import { useState } from 'react';
import { Button } from '@/components/Button';
```

### Type Imports

```typescript
// ✅ Good - Explicit type import
import type { User } from '@/types';
import { fetchUser } from '@/api';

// ❌ Bad - Mixed import
import { User, fetchUser } from '@/api';
```

### Unused Variables

```typescript
// ✅ Good - Prefix with underscore
const handleClick = (_event, data) => {
  console.log(data);
};

// ❌ Bad - Unused variable
const handleClick = (event, data) => {
  console.log(data);
};
```

### Console Usage

```typescript
// ✅ Allowed
console.error('Critical error:', error);
console.warn('Warning:', warning);

// ❌ Not allowed (in production)
console.log('Debug info:', data);
```

---

## 🔍 Advanced Configuration

### Custom Rules

```javascript
// .eslintrc.js
rules: {
  'custom-rule/no-hardcoded-strings': 'error',
  'max-lines': ['error', { max: 300 }],
  'max-params': ['error', 4],
  'complexity': ['error', 10]
}
```

### Project-specific Overrides

```javascript
overrides: [
  {
    files: ['*.config.js', 'scripts/**'],
    rules: {
      'no-console': 'off',
      '@typescript-eslint/no-var-requires': 'off'
    }
  },
  {
    files: ['src/legacy/**'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off'
    }
  }
]
```

---

## 📊 CI/CD Integration

### GitHub Actions

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm run type-check
```

---

## ✅ Best Practices

1. **Consistent Config:** Share ESLint/Prettier across team
2. **Pre-commit Hooks:** Catch issues before commit
3. **IDE Integration:** Format on save
4. **Incremental Adoption:** Fix critical issues first
5. **Custom Rules:** Add project-specific rules
6. **Documentation:** Explain disabled rules
7. **Regular Updates:** Keep dependencies current
8. **Team Alignment:** Discuss rule changes
9. **Performance:** Use caching for large projects
10. **Monorepo Support:** Override configs per package

---

## 🐛 Common Issues

**Issue:** `Parsing error: Cannot read file 'tsconfig.json'`  
**Fix:** Ensure `parserOptions.project` path is correct

**Issue:** ESLint conflicts with Prettier  
**Fix:** Add `prettier` last in `extends` array

**Issue:** `Import 'X' not found`  
**Fix:** Configure `import/resolver` in settings

**Issue:** Slow linting in large projects  
**Fix:** Use `.eslintignore`, enable caching

---

**Ready for:** TypeScript, React, Node.js projects  
**Next:** Run `npm run check-all` to validate
