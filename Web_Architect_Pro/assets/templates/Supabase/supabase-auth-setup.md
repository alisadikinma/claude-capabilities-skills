# Supabase Authentication + Row Level Security

Complete authentication setup with email/password, social logins, and Row Level Security (RLS) policies.

## Quick Setup

### 1. Install Supabase Client

```bash
npm install @supabase/supabase-js
# OR
pip install supabase
```

### 2. Initialize Client

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

## Authentication Methods

### Email/Password Signup

```typescript
// TypeScript
async function signUp(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: 'https://yourapp.com/auth/callback',
      data: {
        full_name: 'John Doe',
        avatar_url: 'https://...'
      }
    }
  });
  
  if (error) throw error;
  return data;
}
```

```python
# Python
def sign_up(email: str, password: str):
    response = supabase.auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "full_name": "John Doe"
            }
        }
    })
    return response
```

### Email/Password Login

```typescript
async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });
  
  if (error) throw error;
  return data;
}
```

### Social Login (OAuth)

```typescript
// Google
async function signInWithGoogle() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: 'https://yourapp.com/auth/callback',
      scopes: 'email profile',
      queryParams: {
        access_type: 'offline',
        prompt: 'consent'
      }
    }
  });
  
  if (error) throw error;
  return data;
}

// GitHub
async function signInWithGitHub() {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: 'https://yourapp.com/auth/callback'
    }
  });
}

// Available providers: google, github, gitlab, azure, bitbucket, 
// discord, facebook, twitter, slack, spotify, twitch, linkedin
```

### Magic Link (Passwordless)

```typescript
async function signInWithMagicLink(email: string) {
  const { data, error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: 'https://yourapp.com/auth/callback'
    }
  });
  
  if (error) throw error;
  return data;
}
```

### Phone Authentication

```typescript
async function signInWithPhone(phone: string) {
  // Send OTP
  const { data, error } = await supabase.auth.signInWithOtp({
    phone: '+1234567890'
  });
  
  if (error) throw error;
  return data;
}

async function verifyOTP(phone: string, token: string) {
  const { data, error } = await supabase.auth.verifyOtp({
    phone,
    token,
    type: 'sms'
  });
  
  if (error) throw error;
  return data;
}
```

## Session Management

### Get Current User

```typescript
async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error) throw error;
  return user;
}

// Get session
async function getSession() {
  const { data: { session }, error } = await supabase.auth.getSession();
  return session;
}
```

### Logout

```typescript
async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}
```

### Password Reset

```typescript
async function resetPassword(email: string) {
  const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: 'https://yourapp.com/update-password'
  });
  
  if (error) throw error;
  return data;
}

async function updatePassword(newPassword: string) {
  const { data, error } = await supabase.auth.updateUser({
    password: newPassword
  });
  
  if (error) throw error;
  return data;
}
```

## React Integration

### Auth Context Provider

```typescript
// contexts/AuthContext.tsx
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const signIn = async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password
    });
    if (error) throw error;
  };

  const signUp = async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  };

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
```

### Protected Route Component

```typescript
// components/ProtectedRoute.tsx
'use client';

import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  return <>{children}</>;
}
```

## Row Level Security (RLS)

### Enable RLS

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own posts
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = user_id);

-- Users can only insert their own posts
CREATE POLICY "Users can insert own posts"
ON posts FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users can update own posts"
ON posts FOR UPDATE
USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "Users can delete own posts"
ON posts FOR DELETE
USING (auth.uid() = user_id);
```

### Public Read, Authenticated Write

```sql
-- Anyone can read
CREATE POLICY "Public posts are viewable by everyone"
ON posts FOR SELECT
USING (true);

-- Only authenticated users can insert
CREATE POLICY "Authenticated users can insert posts"
ON posts FOR INSERT
TO authenticated
WITH CHECK (true);
```

### Role-Based Access

```sql
-- Create custom claims in user metadata
-- Update user: UPDATE auth.users SET raw_user_meta_data = 
-- raw_user_meta_data || '{"role": "admin"}' WHERE id = 'user-id';

-- Admin can do everything
CREATE POLICY "Admins have full access"
ON posts FOR ALL
USING (
  auth.jwt() -> 'user_metadata' ->> 'role' = 'admin'
);

-- Moderators can update/delete
CREATE POLICY "Moderators can moderate"
ON posts FOR UPDATE
USING (
  auth.jwt() -> 'user_metadata' ->> 'role' IN ('admin', 'moderator')
);
```

### Team/Organization Access

```sql
-- Create teams table
CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create team members junction table
CREATE TABLE team_members (
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'member', -- 'owner', 'admin', 'member'
  PRIMARY KEY (team_id, user_id)
);

-- Projects belong to teams
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID REFERENCES teams(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Users can only see projects from their teams
CREATE POLICY "Team members can view projects"
ON projects FOR SELECT
USING (
  team_id IN (
    SELECT team_id FROM team_members 
    WHERE user_id = auth.uid()
  )
);

-- Only team admins/owners can create projects
CREATE POLICY "Team admins can create projects"
ON projects FOR INSERT
WITH CHECK (
  team_id IN (
    SELECT team_id FROM team_members 
    WHERE user_id = auth.uid() 
    AND role IN ('owner', 'admin')
  )
);
```

## User Profile Management

### Create Profiles Table

```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  avatar_url TEXT,
  bio TEXT,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Public profiles are viewable by everyone
CREATE POLICY "Profiles are viewable by everyone"
ON profiles FOR SELECT
USING (true);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = id);

-- Automatically create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (
    new.id,
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

### Update Profile

```typescript
async function updateProfile(updates: {
  full_name?: string;
  avatar_url?: string;
  bio?: string;
}) {
  const { data, error } = await supabase
    .from('profiles')
    .update(updates)
    .eq('id', (await supabase.auth.getUser()).data.user?.id)
    .select()
    .single();
  
  if (error) throw error;
  return data;
}
```

## Middleware (Next.js)

```typescript
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  const {
    data: { session },
  } = await supabase.auth.getSession();

  // Protect /dashboard routes
  if (req.nextUrl.pathname.startsWith('/dashboard') && !session) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  // Redirect logged-in users away from auth pages
  if (
    (req.nextUrl.pathname === '/login' || 
     req.nextUrl.pathname === '/signup') && 
    session
  ) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }

  return res;
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup'],
};
```

## Best Practices

### Security
- ✅ Always enable RLS on tables with user data
- ✅ Use service role key only in backend/server-side code
- ✅ Never expose service role key to frontend
- ✅ Validate user input before database operations
- ✅ Use `auth.uid()` in RLS policies for user-specific data

### Performance
- ✅ Cache user sessions client-side
- ✅ Use `onAuthStateChange` listener for reactive updates
- ✅ Implement refresh token rotation
- ✅ Add indexes on foreign keys (user_id)

### UX
- ✅ Show loading states during auth operations
- ✅ Provide clear error messages
- ✅ Implement password strength indicators
- ✅ Add email verification flow
- ✅ Enable password recovery

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-12
