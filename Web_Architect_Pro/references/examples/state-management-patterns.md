# State Management Patterns

**Quick Reference Guide**  
**Last Updated:** 2025-01-11

---

## Zustand (React - Simple & Fast)

```typescript
import { create } from 'zustand';

interface UserState {
  user: User | null;
  token: string | null;
  setUser: (user: User, token: string) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  token: null,
  
  setUser: (user, token) => set({ user, token }),
  logout: () => set({ user: null, token: null }),
}));

// Usage
function Header() {
  const { user, logout } = useUserStore();
  return <button onClick={logout}>{user?.name}</button>;
}
```

---

## Redux Toolkit (React - Enterprise)

```typescript
// store/slices/authSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const loginUser = createAsyncThunk(
  'auth/login',
  async ({ email, password }) => {
    const res = await api.post('/auth/login', { email, password });
    return res.data;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState: { user: null, loading: false },
  reducers: {
    logout: (state) => { state.user = null; },
  },
  extraReducers: (builder) => {
    builder.addCase(loginUser.fulfilled, (state, action) => {
      state.user = action.payload.user;
    });
  },
});

export default authSlice.reducer;

// Usage
function Component() {
  const dispatch = useAppDispatch();
  const user = useAppSelector(state => state.auth.user);
  
  return <button onClick={() => dispatch(loginUser({ email, password }))}>
    Login
  </button>;
}
```

---

## Pinia (Vue 3)

```typescript
// stores/user.ts
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  
  actions: {
    async login(email: string, password: string) {
      const res = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      this.user = data.user;
      this.token = data.token;
    },
    
    logout() {
      this.user = null;
      this.token = null;
    },
  },
});

// Usage in component
const userStore = useUserStore();
await userStore.login(email, password);
```

---

## Context API (React - Small Apps)

```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState } from 'react';

interface AuthContextType {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }) {
  const [user, setUser] = useState<User | null>(null);
  
  const login = (user: User) => setUser(user);
  const logout = () => setUser(null);
  
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be within AuthProvider');
  return context;
};

// Usage
function Component() {
  const { user, logout } = useAuth();
  return <button onClick={logout}>{user?.name}</button>;
}
```

---

## When to Use What?

| State Type | Solution | Example |
|-----------|----------|---------|
| Local component | useState | Form inputs, toggles |
| Shared UI state | Context/Zustand | Theme, modals |
| User auth | Zustand/Pinia | Login, profile |
| Complex business logic | Redux Toolkit | E-commerce cart |
| Server state | React Query | API data, caching |

---

**Last Updated:** 2025-01-11
