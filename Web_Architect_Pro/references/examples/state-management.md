# State Management Examples

Comprehensive examples untuk state management di React/Next.js applications.

---

## 1. Zustand (Recommended - Lightweight)

### Basic Store

```typescript
// stores/todoStore.ts
import { create } from 'zustand'

interface Todo {
  id: string
  title: string
  completed: boolean
}

interface TodoState {
  todos: Todo[]
  addTodo: (title: string) => void
  toggleTodo: (id: string) => void
  deleteTodo: (id: string) => void
}

export const useTodoStore = create<TodoState>((set) => ({
  todos: [],
  
  addTodo: (title) => set((state) => ({
    todos: [...state.todos, {
      id: crypto.randomUUID(),
      title,
      completed: false
    }]
  })),
  
  toggleTodo: (id) => set((state) => ({
    todos: state.todos.map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    )
  })),
  
  deleteTodo: (id) => set((state) => ({
    todos: state.todos.filter((todo) => todo.id !== id)
  }))
}))

// Usage in component
function TodoList() {
  const { todos, addTodo, toggleTodo, deleteTodo } = useTodoStore()
  
  return (
    <div>
      {todos.map((todo) => (
        <div key={todo.id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(todo.id)}
          />
          <span>{todo.title}</span>
          <button onClick={() => deleteTodo(todo.id)}>Delete</button>
        </div>
      ))}
    </div>
  )
}
```

### Persistent Store (LocalStorage)

```typescript
// stores/authStore.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'

interface User {
  id: number
  email: string
  name: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      
      login: (user, token) => set({
        user,
        token,
        isAuthenticated: true
      }),
      
      logout: () => set({
        user: null,
        token: null,
        isAuthenticated: false
      })
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ 
        token: state.token,
        user: state.user 
      })
    }
  )
)
```

### Slices Pattern (Large Stores)

```typescript
// stores/appStore.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'

// User slice
interface UserSlice {
  user: User | null
  setUser: (user: User) => void
  clearUser: () => void
}

const createUserSlice = (set): UserSlice => ({
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null })
})

// Settings slice
interface SettingsSlice {
  theme: 'light' | 'dark'
  language: string
  setTheme: (theme: 'light' | 'dark') => void
  setLanguage: (language: string) => void
}

const createSettingsSlice = (set): SettingsSlice => ({
  theme: 'light',
  language: 'en',
  setTheme: (theme) => set({ theme }),
  setLanguage: (language) => set({ language })
})

// Combined store
type AppState = UserSlice & SettingsSlice

export const useAppStore = create<AppState>()(
  devtools(
    (set) => ({
      ...createUserSlice(set),
      ...createSettingsSlice(set)
    })
  )
)

// Selective usage (prevents unnecessary re-renders)
function ThemeSwitcher() {
  // Only re-renders when theme changes
  const theme = useAppStore((state) => state.theme)
  const setTheme = useAppStore((state) => state.setTheme)
  
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle Theme
    </button>
  )
}
```

---

## 2. React Query (Server State)

### Basic Usage

```typescript
// lib/queries/users.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'

interface User {
  id: number
  name: string
  email: string
}

// Fetch users
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get<User[]>('/users')
      return data
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

// Fetch single user
export function useUser(id: number) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: async () => {
      const { data } = await api.get<User>(`/users/${id}`)
      return data
    },
    enabled: !!id, // Only fetch if id exists
  })
}

// Create user mutation
export function useCreateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (userData: Omit<User, 'id'>) => {
      const { data } = await api.post<User>('/users', userData)
      return data
    },
    onSuccess: (newUser) => {
      // Optimistically update cache
      queryClient.setQueryData<User[]>(['users'], (old) => 
        old ? [...old, newUser] : [newUser]
      )
      
      // Or invalidate to refetch
      // queryClient.invalidateQueries({ queryKey: ['users'] })
    },
    onError: (error) => {
      console.error('Failed to create user:', error)
    }
  })
}

// Update user mutation
export function useUpdateUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async ({ id, ...userData }: User) => {
      const { data } = await api.put<User>(`/users/${id}`, userData)
      return data
    },
    onSuccess: (updatedUser) => {
      // Update specific user in cache
      queryClient.setQueryData(['users', updatedUser.id], updatedUser)
      
      // Update user in users list
      queryClient.setQueryData<User[]>(['users'], (old) =>
        old?.map((user) => user.id === updatedUser.id ? updatedUser : user)
      )
    }
  })
}

// Delete user mutation
export function useDeleteUser() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (id: number) => {
      await api.delete(`/users/${id}`)
      return id
    },
    onSuccess: (deletedId) => {
      queryClient.setQueryData<User[]>(['users'], (old) =>
        old?.filter((user) => user.id !== deletedId)
      )
    }
  })
}

// Usage in component
function UsersList() {
  const { data: users, isLoading, error } = useUsers()
  const createUser = useCreateUser()
  const updateUser = useUpdateUser()
  const deleteUser = useDeleteUser()
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  const handleCreate = () => {
    createUser.mutate({
      name: 'New User',
      email: 'newuser@example.com'
    })
  }
  
  return (
    <div>
      <button onClick={handleCreate} disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
      
      {users?.map((user) => (
        <div key={user.id}>
          <span>{user.name}</span>
          <button onClick={() => updateUser.mutate(user)}>Edit</button>
          <button onClick={() => deleteUser.mutate(user.id)}>Delete</button>
        </div>
      ))}
    </div>
  )
}
```

### Infinite Query (Pagination)

```typescript
// Infinite scroll pagination
export function useInfiniteProducts() {
  return useInfiniteQuery({
    queryKey: ['products'],
    queryFn: async ({ pageParam = 0 }) => {
      const { data } = await api.get(`/products?skip=${pageParam}&limit=20`)
      return data
    },
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.length === 20 ? allPages.length * 20 : undefined
    },
    initialPageParam: 0,
  })
}

// Usage
function ProductList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteProducts()
  
  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ))}
      
      {hasNextPage && (
        <button
          onClick={() => fetchNextPage()}
          disabled={isFetchingNextPage}
        >
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  )
}
```

---

## 3. React Context (Simple Global State)

```typescript
// contexts/ThemeContext.tsx
import { createContext, useContext, useState, ReactNode } from 'react'

type Theme = 'light' | 'dark'

interface ThemeContextType {
  theme: Theme
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  
  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'))
  }
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (context === undefined) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Layout />
    </ThemeProvider>
  )
}

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()
  
  return (
    <button onClick={toggleTheme}>
      Current theme: {theme}
    </button>
  )
}
```

---

## 4. Redux Toolkit (Complex Applications)

```typescript
// store/slices/cartSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface CartItem {
  id: number
  name: string
  price: number
  quantity: number
}

interface CartState {
  items: CartItem[]
  total: number
}

const initialState: CartState = {
  items: [],
  total: 0
}

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<Omit<CartItem, 'quantity'>>) => {
      const existingItem = state.items.find((item) => item.id === action.payload.id)
      
      if (existingItem) {
        existingItem.quantity += 1
      } else {
        state.items.push({ ...action.payload, quantity: 1 })
      }
      
      state.total = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
    },
    
    removeItem: (state, action: PayloadAction<number>) => {
      state.items = state.items.filter((item) => item.id !== action.payload)
      state.total = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
    },
    
    updateQuantity: (state, action: PayloadAction<{ id: number; quantity: number }>) => {
      const item = state.items.find((item) => item.id === action.payload.id)
      if (item) {
        item.quantity = action.payload.quantity
        state.total = state.items.reduce((sum, item) => sum + item.price * item.quantity, 0)
      }
    },
    
    clearCart: (state) => {
      state.items = []
      state.total = 0
    }
  }
})

export const { addItem, removeItem, updateQuantity, clearCart } = cartSlice.actions
export default cartSlice.reducer

// store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import cartReducer from './slices/cartSlice'

export const store = configureStore({
  reducer: {
    cart: cartReducer
  }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

// hooks/useAppDispatch.ts
import { useDispatch, useSelector } from 'react-redux'
import type { RootState, AppDispatch } from '@/store'

export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
export const useAppSelector = useSelector.withTypes<RootState>()

// Usage
function Cart() {
  const dispatch = useAppDispatch()
  const { items, total } = useAppSelector((state) => state.cart)
  
  return (
    <div>
      <h2>Cart Total: ${total.toFixed(2)}</h2>
      {items.map((item) => (
        <div key={item.id}>
          <span>{item.name} x {item.quantity}</span>
          <button onClick={() => dispatch(removeItem(item.id))}>
            Remove
          </button>
        </div>
      ))}
      <button onClick={() => dispatch(clearCart())}>Clear Cart</button>
    </div>
  )
}
```

---

## Decision Guide

**Use Zustand when:**
- Simple global state (auth, theme, preferences)
- Need TypeScript-first solution
- Want minimal boilerplate
- Small to medium apps

**Use React Query when:**
- Handling server state (API data)
- Need caching, refetching, pagination
- Want automatic background updates
- Any app with API calls

**Use Context when:**
- Very simple state (theme, locale)
- State doesn't change frequently
- Few components need the state
- Want no dependencies

**Use Redux Toolkit when:**
- Complex state logic
- Need time-travel debugging
- Large applications
- Team familiar with Redux
- Need middleware (sagas, thunks)

---

## Best Practices

1. **Separate concerns** - Client state (Zustand) + Server state (React Query)
2. **Use selectors** - Prevent unnecessary re-renders
3. **Keep state minimal** - Derive values when possible
4. **Normalize data** - Avoid nested structures
5. **Memoize expensive computations** - Use useMemo
6. **Persist strategically** - Only persist what's needed
7. **Type everything** - Full TypeScript support
8. **Test state logic** - Unit test stores independently
