# API Integration Patterns

**Last Updated:** 2025-01-11  
**Category:** Examples

---

## 🔌 REST API Integration (Next.js + FastAPI)

### Backend (FastAPI)

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    
    class Config:
        from_attributes = True

@app.get("/api/v1/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 20):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user
```

### Frontend API Client

```typescript
// lib/api/client.ts
import axios, { AxiosInstance } from 'axios';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL,
      headers: { 'Content-Type': 'application/json' },
    });

    this.client.interceptors.request.use((config) => {
      const token = authService.getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.client.get<T>(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.post<T>(url, data);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

### API Service Layer

```typescript
// lib/api/users.ts
export interface User {
  id: number;
  email: string;
  name: string;
}

export const userApi = {
  getAll: (params?: { skip?: number; limit?: number }) =>
    apiClient.get<User[]>('/api/v1/users', params),

  getById: (id: number) =>
    apiClient.get<User>(`/api/v1/users/${id}`),

  create: (data: CreateUserData) =>
    apiClient.post<User>('/api/v1/users', data),
};
```

### React Hook with React Query

```typescript
// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '@/lib/api/users';

export function useUsers(params?: { skip?: number; limit?: number }) {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => userApi.getAll(params),
    staleTime: 5 * 60 * 1000,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserData) => userApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created');
    },
  });
}
```

### Component Usage

```typescript
// components/UsersList.tsx
'use client';

import { useUsers, useCreateUser } from '@/hooks/useUsers';

export function UsersList() {
  const { data: users, isLoading } = useUsers({ limit: 20 });
  const createUser = useCreateUser();

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {users?.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

---

## 📡 GraphQL Integration (Apollo Client)

### Backend (Strawberry)

```python
import strawberry
from typing import List

@strawberry.type
class User:
    id: int
    email: str
    name: str

@strawberry.type
class Query:
    @strawberry.field
    async def users(self, limit: int = 20) -> List[User]:
        return await get_users(limit)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, email: str, name: str) -> User:
        return await create_user_service(email, name)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

### Frontend (Apollo Client)

```typescript
// lib/apollo/client.ts
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: process.env.NEXT_PUBLIC_GRAPHQL_URL,
});

const authLink = setContext((_, { headers }) => {
  const token = authService.getAccessToken();
  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : '',
    },
  };
});

export const apolloClient = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});
```

### GraphQL Queries

```typescript
// lib/apollo/queries.ts
import { gql } from '@apollo/client';

export const GET_USERS = gql`
  query GetUsers($limit: Int) {
    users(limit: $limit) {
      id
      email
      name
    }
  }
`;

export const CREATE_USER = gql`
  mutation CreateUser($email: String!, $name: String!) {
    createUser(email: $email, name: $name) {
      id
      email
      name
    }
  }
`;
```

### React Hooks

```typescript
import { useQuery, useMutation } from '@apollo/client';
import { GET_USERS, CREATE_USER } from '@/lib/apollo/queries';

export function useUsersQuery(limit?: number) {
  return useQuery(GET_USERS, { variables: { limit } });
}

export function useCreateUserMutation() {
  return useMutation(CREATE_USER, {
    refetchQueries: [GET_USERS],
  });
}
```

---

## 🔌 WebSocket Integration

### Backend (FastAPI)

```python
from fastapi import WebSocket
from typing import List, Dict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    async def broadcast(self, message: dict, room: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str):
    await manager.connect(websocket, room)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(json.loads(data), room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
```

### Frontend (React)

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';

export function useWebSocket(room: string) {
  const [messages, setMessages] = useState<any[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    ws.current = new WebSocket(`ws://localhost:8000/ws/${room}`);

    ws.current.onopen = () => setIsConnected(true);
    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, JSON.parse(event.data)]);
    };
    ws.current.onclose = () => setIsConnected(false);

    return () => ws.current?.close();
  }, [room]);

  const sendMessage = (data: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    }
  };

  return { messages, isConnected, sendMessage };
}
```

---

**Last Updated:** 2025-01-11  
**Maintained by:** Ali Sadikin MA
