# Next.js 14+ Project Structure Template

**Framework:** Next.js 14 with App Router  
**Language:** TypeScript  
**Styling:** Tailwind CSS  
**State Management:** Zustand  
**Data Fetching:** TanStack Query (React Query)

---

## Complete Project Structure

```
my-nextjs-app/
├── .env.local                          # Environment variables
├── .env.production                     # Production env vars
├── .gitignore
├── next.config.js                      # Next.js configuration
├── tailwind.config.ts                  # Tailwind configuration
├── tsconfig.json                       # TypeScript configuration
├── package.json
├── README.md
│
├── public/                             # Static assets
│   ├── images/
│   ├── fonts/
│   └── icons/
│
├── src/
│   ├── app/                            # App Router (Next.js 14+)
│   │   ├── layout.tsx                  # Root layout
│   │   ├── page.tsx                    # Home page
│   │   ├── loading.tsx                 # Loading UI
│   │   ├── error.tsx                   # Error UI
│   │   ├── not-found.tsx               # 404 page
│   │   │
│   │   ├── (auth)/                     # Route group (auth)
│   │   │   ├── layout.tsx              # Auth layout
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   ├── register/
│   │   │   │   └── page.tsx
│   │   │   └── forgot-password/
│   │   │       └── page.tsx
│   │   │
│   │   ├── (dashboard)/                # Route group (dashboard)
│   │   │   ├── layout.tsx              # Dashboard layout
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── profile/
│   │   │   │   └── page.tsx
│   │   │   ├── settings/
│   │   │   │   └── page.tsx
│   │   │   └── users/
│   │   │       ├── page.tsx            # Users list
│   │   │       └── [id]/
│   │   │           └── page.tsx        # User detail
│   │   │
│   │   └── api/                        # API routes
│   │       ├── auth/
│   │       │   ├── login/
│   │       │   │   └── route.ts
│   │       │   └── logout/
│   │       │       └── route.ts
│   │       └── users/
│   │           ├── route.ts            # GET /api/users, POST /api/users
│   │           └── [id]/
│   │               └── route.ts        # GET, PUT, DELETE /api/users/:id
│   │
│   ├── components/                     # Reusable components
│   │   ├── ui/                         # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── layouts/                    # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── DashboardLayout.tsx
│   │   │
│   │   └── features/                   # Feature-specific components
│   │       ├── auth/
│   │       │   ├── LoginForm.tsx
│   │       │   └── RegisterForm.tsx
│   │       ├── users/
│   │       │   ├── UserCard.tsx
│   │       │   ├── UserList.tsx
│   │       │   └── UserForm.tsx
│   │       └── dashboard/
│   │           ├── StatsCard.tsx
│   │           └── RecentActivity.tsx
│   │
│   ├── lib/                            # Utility libraries
│   │   ├── api/                        # API client
│   │   │   ├── client.ts               # Axios instance
│   │   │   ├── endpoints.ts            # API endpoints
│   │   │   └── types.ts                # API types
│   │   │
│   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useUser.ts
│   │   │   ├── useDebounce.ts
│   │   │   └── useLocalStorage.ts
│   │   │
│   │   ├── utils/                      # Utility functions
│   │   │   ├── format.ts               # Date, number formatting
│   │   │   ├── validation.ts           # Input validation
│   │   │   ├── cn.ts                   # Class name merger
│   │   │   └── errors.ts               # Error handling
│   │   │
│   │   └── db/                         # Database (if using Prisma)
│   │       ├── prisma.ts               # Prisma client
│   │       └── schema.prisma           # Database schema
│   │
│   ├── store/                          # State management (Zustand)
│   │   ├── authStore.ts                # Auth state
│   │   ├── userStore.ts                # User state
│   │   └── uiStore.ts                  # UI state (modals, sidebars)
│   │
│   ├── types/                          # TypeScript types
│   │   ├── api.ts                      # API response types
│   │   ├── models.ts                   # Data models
│   │   └── global.d.ts                 # Global type declarations
│   │
│   ├── config/                         # Configuration files
│   │   ├── site.ts                     # Site metadata
│   │   ├── routes.ts                   # Route constants
│   │   └── constants.ts                # App constants
│   │
│   └── middleware.ts                   # Next.js middleware (auth, etc.)
│
└── tests/                              # Test files
    ├── unit/
    ├── integration/
    └── e2e/
```

---

## Key Files Configuration

### 1. `next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  images: {
    domains: ['api.example.com', 'cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
  },
  
  env: {
    API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  
  // Enable experimental features
  experimental: {
    serverActions: true,
  },
  
  // Webpack configuration
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
      };
    }
    return config;
  },
};

module.exports = nextConfig;
```

### 2. `tailwind.config.ts`

```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... rest of shades
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};

export default config;
```

### 3. `src/app/layout.tsx` (Root Layout)

```typescript
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/Providers';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'My App',
  description: 'Modern web application',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans antialiased">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
```

### 4. `src/components/Providers.tsx`

```typescript
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        cacheTime: 5 * 60 * 1000, // 5 minutes
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### 5. `src/lib/api/client.ts`

```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 (refresh token)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const { data } = await axios.post('/api/auth/refresh', {
          refresh_token: refreshToken,
        });
        
        localStorage.setItem('access_token', data.access_token);
        apiClient.defaults.headers.common['Authorization'] = 
          `Bearer ${data.access_token}`;
        
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Redirect to login
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

### 6. `src/store/authStore.ts` (Zustand)

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      login: (user, token) => set({
        user,
        accessToken: token,
        isAuthenticated: true,
      }),

      logout: () => set({
        user: null,
        accessToken: null,
        isAuthenticated: false,
      }),

      updateUser: (userData) => set((state) => ({
        user: state.user ? { ...state.user, ...userData } : null,
      })),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

### 7. `src/lib/hooks/useAuth.ts`

```typescript
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import apiClient from '@/lib/api/client';

export function useAuth() {
  const { user, isAuthenticated, login, logout } = useAuthStore();
  const router = useRouter();

  const loginUser = async (email: string, password: string) => {
    try {
      const { data } = await apiClient.post('/api/auth/login', {
        email,
        password,
      });

      login(data.user, data.access_token);
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      
      router.push('/dashboard');
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  const logoutUser = () => {
    logout();
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  };

  return {
    user,
    isAuthenticated,
    loginUser,
    logoutUser,
  };
}
```

### 8. `src/middleware.ts` (Auth Middleware)

```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

const publicRoutes = ['/login', '/register', '/forgot-password'];
const protectedRoutes = ['/dashboard', '/profile', '/settings'];

export function middleware(request: NextRequest) {
  const token = request.cookies.get('access_token')?.value;
  const { pathname } = request.nextUrl;

  // Redirect authenticated users away from auth pages
  if (token && publicRoutes.includes(pathname)) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Redirect unauthenticated users to login
  if (!token && protectedRoutes.some(route => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

---

## Environment Variables

### `.env.local`

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Database (if using Prisma)
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

# Authentication
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000

# External Services
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

---

## Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,json}\"",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:e2e": "playwright test"
  }
}
```

---

## Essential Dependencies

```bash
# Core
npm install next@latest react@latest react-dom@latest typescript

# Styling
npm install tailwindcss postcss autoprefixer
npm install @tailwindcss/forms @tailwindcss/typography

# State Management
npm install zustand

# Data Fetching
npm install @tanstack/react-query axios

# Forms & Validation
npm install react-hook-form zod @hookform/resolvers

# UI Components (optional)
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu

# Dev Dependencies
npm install -D @types/node @types/react @types/react-dom
npm install -D prettier eslint-config-prettier
npm install -D jest @testing-library/react @testing-library/jest-dom
```

---

## Usage Example

**Creating a New Feature:**

```bash
# 1. Create feature directory
mkdir -p src/app/(dashboard)/products
mkdir -p src/components/features/products

# 2. Create page
# src/app/(dashboard)/products/page.tsx

# 3. Create components
# src/components/features/products/ProductList.tsx
# src/components/features/products/ProductCard.tsx

# 4. Create API client
# src/lib/api/products.ts

# 5. Create hooks
# src/lib/hooks/useProducts.ts

# 6. Create types
# src/types/product.ts
```

---

## Best Practices

1. **Use App Router (Not Pages Router)**
2. **Server Components by Default** - Add `'use client'` only when needed
3. **Colocate Files** - Keep related files together in route groups
4. **TypeScript Strict Mode** - Catch errors early
5. **Environment Variables** - Use `NEXT_PUBLIC_` prefix for client-side vars
6. **Image Optimization** - Always use `next/image`
7. **Dynamic Imports** - Code split heavy components
8. **API Routes** - Use for BFF (Backend for Frontend) pattern

---

**Last Updated:** 2025-01-11  
**Compatibility:** Next.js 14+, React 18+, TypeScript 5+
