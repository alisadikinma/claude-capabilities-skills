# Vue 3 Project Structure (Vite)

**Stack:** Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS

---

## 📁 Complete Project Structure

```
my-vue-app/
├── public/
│   ├── favicon.ico
│   └── robots.txt
├── src/
│   ├── assets/
│   │   ├── images/
│   │   └── styles/
│   │       └── main.css
│   ├── components/
│   │   ├── ui/
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseInput.vue
│   │   │   ├── BaseCard.vue
│   │   │   └── BaseModal.vue
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.vue
│   │   │   │   ├── RegisterForm.vue
│   │   │   │   └── ProtectedRoute.vue
│   │   │   ├── dashboard/
│   │   │   │   └── StatsCard.vue
│   │   │   └── posts/
│   │   │       ├── PostList.vue
│   │   │       ├── PostCard.vue
│   │   │       └── PostForm.vue
│   │   └── layouts/
│   │       ├── MainLayout.vue
│   │       ├── AuthLayout.vue
│   │       └── DashboardLayout.vue
│   ├── composables/
│   │   ├── useAuth.ts
│   │   ├── useUsers.ts
│   │   ├── usePosts.ts
│   │   └── useDebounce.ts
│   ├── api/
│   │   ├── client.ts
│   │   ├── users.ts
│   │   ├── posts.ts
│   │   └── auth.ts
│   ├── router/
│   │   ├── index.ts
│   │   └── guards.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   └── posts.ts
│   ├── types/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   └── post.ts
│   ├── utils/
│   │   ├── format.ts
│   │   ├── validation.ts
│   │   └── helpers.ts
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DashboardView.vue
│   │   ├── ProfileView.vue
│   │   └── NotFoundView.vue
│   ├── App.vue
│   └── main.ts
├── .env.example
├── .env.local
├── .gitignore
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```

---

## 🚀 Setup Commands

```bash
# Create project
npm create vite@latest my-vue-app -- --template vue-ts

cd my-vue-app

# Install core dependencies
npm install

# Install routing
npm install vue-router@4

# Install state management
npm install pinia

# Install API & data fetching
npm install axios

# Install UI & styling
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install form validation
npm install vee-validate yup

# Install utilities
npm install @vueuse/core  # Vue composition utilities
npm install @tanstack/vue-query  # Data fetching

# Install dev tools
npm install -D @types/node
```

---

## 📄 Key Configuration Files

### `vite.config.ts`
```typescript
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### `tailwind.config.js`
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

### `tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

---

## 🎨 Core Files Setup

### `src/main.ts`
```typescript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { VueQueryPlugin } from '@tanstack/vue-query';
import App from './App.vue';
import router from './router';
import './assets/styles/main.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(VueQueryPlugin);

app.mount('#app');
```

### `src/App.vue`
```vue
<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style scoped>
#app {
  @apply min-h-screen bg-gray-50;
}
</style>
```

### `src/assets/styles/main.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-border;
  }
  
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}

@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }
  
  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700;
  }
  
  .btn-secondary {
    @apply bg-gray-200 text-gray-900 hover:bg-gray-300;
  }
}
```

---

## 🗺️ Router Setup

### `src/router/index.ts`
```typescript
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import HomeView from '@/views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router;
```

---

## 📦 Pinia Store Setup

### `src/stores/auth.ts`
```typescript
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const accessToken = ref<string | null>(null);
  
  const isAuthenticated = computed(() => !!accessToken.value);
  
  function login(userData: User, token: string) {
    user.value = userData;
    accessToken.value = token;
    localStorage.setItem('access_token', token);
  }
  
  function logout() {
    user.value = null;
    accessToken.value = null;
    localStorage.removeItem('access_token');
  }
  
  function initAuth() {
    const token = localStorage.getItem('access_token');
    if (token) {
      accessToken.value = token;
      // Fetch user data
    }
  }
  
  return {
    user,
    accessToken,
    isAuthenticated,
    login,
    logout,
    initAuth,
  };
});
```

---

## 🔌 API Client Setup

### `src/api/client.ts`
```typescript
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### `src/api/users.ts`
```typescript
import { apiClient } from './client';
import type { User } from '@/types/user';

export const userApi = {
  getAll: (params?: { skip?: number; limit?: number }) =>
    apiClient.get<User[]>('/api/v1/users', { params }),
  
  getById: (id: number) =>
    apiClient.get<User>(`/api/v1/users/${id}`),
  
  create: (data: CreateUserData) =>
    apiClient.post<User>('/api/v1/users', data),
  
  update: (id: number, data: UpdateUserData) =>
    apiClient.put<User>(`/api/v1/users/${id}`, data),
  
  delete: (id: number) =>
    apiClient.delete(`/api/v1/users/${id}`),
};
```

---

## 🎯 Composables (Vue Composition API)

### `src/composables/useUsers.ts`
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query';
import { userApi } from '@/api/users';

export function useUsers(params?: { skip?: number; limit?: number }) {
  return useQuery({
    queryKey: ['users', params],
    queryFn: async () => {
      const response = await userApi.getAll(params);
      return response.data;
    },
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (data: CreateUserData) => {
      const response = await userApi.create(data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}
```

---

## 🎨 Component Examples

### `src/components/ui/BaseButton.vue`
```vue
<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  isLoading: false,
  disabled: false,
});
</script>

<template>
  <button
    :class="[
      'btn rounded-md font-medium transition-colors',
      {
        'btn-primary': variant === 'primary',
        'bg-gray-200 hover:bg-gray-300': variant === 'secondary',
        'bg-red-600 text-white hover:bg-red-700': variant === 'danger',
        'px-3 py-1.5 text-sm': size === 'sm',
        'px-4 py-2': size === 'md',
        'px-6 py-3 text-lg': size === 'lg',
        'opacity-50 cursor-not-allowed': disabled || isLoading,
      }
    ]"
    :disabled="disabled || isLoading"
  >
    <span v-if="isLoading">Loading...</span>
    <slot v-else />
  </button>
</template>
```

### `src/views/DashboardView.vue`
```vue
<script setup lang="ts">
import { useUsers } from '@/composables/useUsers';
import { useAuthStore } from '@/stores/auth';
import DashboardLayout from '@/components/layouts/DashboardLayout.vue';

const authStore = useAuthStore();
const { data: users, isLoading } = useUsers({ limit: 10 });
</script>

<template>
  <DashboardLayout>
    <div class="p-6">
      <h1 class="text-3xl font-bold mb-6">
        Welcome, {{ authStore.user?.name }}
      </h1>
      
      <div v-if="isLoading" class="text-center py-8">
        Loading...
      </div>
      
      <div v-else class="grid gap-4">
        <div
          v-for="user in users"
          :key="user.id"
          class="p-4 bg-white rounded-lg shadow"
        >
          <h3 class="font-semibold">{{ user.name }}</h3>
          <p class="text-gray-600">{{ user.email }}</p>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>
```

---

## 📝 Environment Variables

### `.env.example`
```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=My Vue App
```

---

## 🚀 Scripts

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit"
  }
}
```

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
