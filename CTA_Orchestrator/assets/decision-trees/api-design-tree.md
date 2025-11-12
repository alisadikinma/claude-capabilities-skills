# API Design Decision Tree

## Primary Decision Flow

```
START: What API style should I use?
  │
  ├─ Who are the consumers?
  │   ├─ Mobile/Web apps ────────────────────────> REST or GraphQL
  │   ├─ Server-to-server ───────────────────────> gRPC or REST
  │   ├─ Real-time updates ──────────────────────> WebSocket or SSE
  │   └─ Third-party developers ─────────────────> REST (widely supported)
  │
  ├─ Data complexity?
  │   ├─ Simple CRUD ────────────────────────────> REST
  │   ├─ Complex nested data ────────────────────> GraphQL
  │   ├─ High-performance RPC ───────────────────> gRPC
  │   └─ Real-time streaming ────────────────────> WebSocket / gRPC Streams
  │
  ├─ Performance requirements?
  │   ├─ Standard web app (< 100ms) ─────────────> REST
  │   ├─ Low latency (< 10ms) ───────────────────> gRPC
  │   ├─ Bidirectional streaming ────────────────> gRPC / WebSocket
  │   └─ Minimal bandwidth ──────────────────────> gRPC (binary)
  │
  └─ Team expertise?
      ├─ Junior devs / No experience ───────────> REST
      ├─ Experienced team ──────────────────────> Any
      └─ Frontend-heavy team ───────────────────> GraphQL
```

## API Style Comparison

| Feature | REST | GraphQL | gRPC | WebSocket |
|---------|------|---------|------|-----------|
| **Data Format** | JSON/XML | JSON | Protobuf (binary) | Text/Binary |
| **Request Type** | HTTP methods | Queries/Mutations | RPC calls | Bidirectional |
| **Learning Curve** | Easy | Medium | Hard | Medium |
| **Tooling** | Excellent | Good | Good | Good |
| **Caching** | Native (HTTP) | Complex | Custom | N/A |
| **Versioning** | URL/Header | Schema evolution | Protobuf | Custom |
| **Real-time** | Polling/SSE | Subscriptions | Streams | Native |
| **Performance** | Good | Good | Excellent | Excellent |
| **Browser Support** | Native | Native | Limited | Native |
| **Mobile-Friendly** | Excellent | Excellent | Good | Good |
| **Documentation** | OpenAPI | Schema | Protobuf | Custom |

## 1. REST API

### When to Use REST

**Perfect For:**
- ✅ Public APIs (widely understood)
- ✅ Simple CRUD operations
- ✅ HTTP caching is important
- ✅ Stateless interactions
- ✅ Standard web/mobile apps
- ✅ Third-party integrations

**Avoid When:**
- ❌ Need real-time updates (use WebSocket)
- ❌ Complex nested data fetching (use GraphQL)
- ❌ Ultra-low latency required (use gRPC)
- ❌ Microservices internal communication (consider gRPC)

### REST Best Practices

**1. Resource Naming:**
```
✅ Good:
GET    /api/users                 # List users
GET    /api/users/123             # Get user
POST   /api/users                 # Create user
PUT    /api/users/123             # Update user
DELETE /api/users/123             # Delete user

❌ Bad:
GET    /api/getUsers              # Verb in URL
POST   /api/user/create           # Redundant verb
GET    /api/users/delete/123      # Wrong method
```

**2. HTTP Status Codes:**
```
200 OK                  # Success
201 Created             # Resource created
204 No Content          # Success, no response body
400 Bad Request         # Invalid input
401 Unauthorized        # Not authenticated
403 Forbidden           # Authenticated but no permission
404 Not Found           # Resource doesn't exist
409 Conflict            # Duplicate resource
422 Unprocessable       # Validation errors
429 Too Many Requests   # Rate limit exceeded
500 Internal Error      # Server error
503 Service Unavailable # Maintenance/overload
```

**3. Pagination:**
```json
// Cursor-based (recommended for large datasets)
GET /api/users?cursor=eyJ1c2VyX2lkIjoxMjN9&limit=20

{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJ1c2VyX2lkIjoxNDN9",
    "has_more": true
  }
}

// Offset-based (simpler, but less efficient at scale)
GET /api/users?page=2&per_page=20

{
  "data": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total": 1000,
    "total_pages": 50
  }
}
```

**4. Filtering & Sorting:**
```
GET /api/users?status=active&role=admin&sort=-created_at
GET /api/products?price[gte]=100&price[lte]=500
GET /api/posts?search=title:react
```

**5. Response Format:**
```json
// Success Response
{
  "success": true,
  "data": {
    "id": 123,
    "name": "John Doe"
  },
  "meta": {
    "timestamp": "2025-01-11T10:00:00Z"
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Email is required"
      }
    ]
  }
}
```

**6. Versioning:**
```
Option 1: URL versioning (most common)
GET /api/v1/users
GET /api/v2/users

Option 2: Header versioning (cleaner URLs)
GET /api/users
Header: Accept: application/vnd.api+json; version=2

Option 3: Query parameter (not recommended)
GET /api/users?version=2
```

### REST Performance Tips

1. **Use ETags for caching**
2. **Implement compression (gzip/brotli)**
3. **Partial responses:** `GET /api/users?fields=id,name,email`
4. **Batch endpoints:** `POST /api/batch { "requests": [...] }`
5. **Rate limiting:** `X-RateLimit-Remaining: 95`

---

## 2. GraphQL

### When to Use GraphQL

**Perfect For:**
- ✅ Complex data requirements
- ✅ Multiple client types (web, mobile, desktop)
- ✅ Avoid over-fetching/under-fetching
- ✅ Rapid frontend iteration
- ✅ Real-time subscriptions
- ✅ Strong typing requirements

**Avoid When:**
- ❌ Simple CRUD (REST is simpler)
- ❌ File uploads (complex in GraphQL)
- ❌ HTTP caching is critical
- ❌ Team unfamiliar with GraphQL
- ❌ Need rate limiting (harder in GraphQL)

### GraphQL Schema Example

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  publishedAt: DateTime
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(authorId: ID, published: Boolean): [Post!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  
  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post!
}

type Subscription {
  postAdded: Post!
  commentAdded(postId: ID!): Comment!
}

input CreateUserInput {
  name: String!
  email: String!
  password: String!
}
```

### GraphQL Query Examples

```graphql
# Fetch exactly what you need
query GetUserProfile {
  user(id: "123") {
    id
    name
    email
    posts {
      id
      title
      publishedAt
    }
  }
}

# Nested queries with arguments
query GetUserPosts {
  user(id: "123") {
    name
    posts(published: true, limit: 5) {
      title
      comments(limit: 3) {
        content
        author { name }
      }
    }
  }
}

# Mutations
mutation CreatePost {
  createPost(input: {
    title: "New Post"
    content: "Content here"
  }) {
    id
    title
    createdAt
  }
}

# Subscriptions (real-time)
subscription OnPostAdded {
  postAdded {
    id
    title
    author { name }
  }
}
```

### GraphQL Best Practices

1. **Use DataLoader** for batching and caching
2. **Implement query depth limiting** (prevent nested attacks)
3. **Add query complexity analysis** (cost-based limiting)
4. **Use fragments** for reusable query parts
5. **Implement field-level authorization**
6. **Add pagination** (Relay cursor-based)

### GraphQL Performance Concerns

**N+1 Problem:**
```javascript
// ❌ Bad: N+1 queries
const resolvers = {
  User: {
    posts: (user) => db.posts.find({ authorId: user.id })
  }
}

// ✅ Good: Use DataLoader
const postLoader = new DataLoader(async (userIds) => {
  const posts = await db.posts.find({ authorId: { $in: userIds } })
  return userIds.map(id => posts.filter(p => p.authorId === id))
})

const resolvers = {
  User: {
    posts: (user) => postLoader.load(user.id)
  }
}
```

---

## 3. gRPC

### When to Use gRPC

**Perfect For:**
- ✅ Microservices internal communication
- ✅ High-performance requirements (< 10ms)
- ✅ Bidirectional streaming
- ✅ Polyglot services (Python ↔ Go ↔ Java)
- ✅ Server-to-server communication
- ✅ IoT / embedded systems (low bandwidth)

**Avoid When:**
- ❌ Browser-based clients (limited support)
- ❌ Public APIs (REST more accessible)
- ❌ Simple CRUD apps (overkill)
- ❌ Team unfamiliar with Protobuf
- ❌ Need human-readable messages

### Protocol Buffer Definition

```protobuf
syntax = "proto3";

package user.v1;

service UserService {
  rpc GetUser(GetUserRequest) returns (User) {}
  rpc ListUsers(ListUsersRequest) returns (stream User) {}
  rpc CreateUser(CreateUserRequest) returns (User) {}
  rpc UpdateUser(UpdateUserRequest) returns (User) {}
  rpc DeleteUser(DeleteUserRequest) returns (google.protobuf.Empty) {}
  
  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage) {}
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  int64 created_at = 4;
}

message GetUserRequest {
  string id = 1;
}

message ListUsersRequest {
  int32 limit = 1;
  string page_token = 2;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  string password = 3;
}

message ChatMessage {
  string user_id = 1;
  string content = 2;
  int64 timestamp = 3;
}
```

### gRPC Performance Benefits

- **50-70% smaller payloads** (binary vs JSON)
- **2-10x faster serialization** (Protobuf vs JSON)
- **HTTP/2 multiplexing** (multiple requests per connection)
- **Built-in streaming** (server, client, bidirectional)

### gRPC Use Cases

| Scenario | Benefit |
|----------|---------|
| **Microservices mesh** | Low latency, type-safe |
| **Mobile apps** | Bandwidth efficiency |
| **Real-time chat** | Bidirectional streaming |
| **IoT data ingestion** | Efficient binary protocol |
| **ML model serving** | Fast inference requests |

---

## 4. WebSocket

### When to Use WebSocket

**Perfect For:**
- ✅ Real-time collaboration (docs, whiteboards)
- ✅ Live chat applications
- ✅ Gaming / multiplayer apps
- ✅ Live dashboards / monitoring
- ✅ Stock tickers / trading apps
- ✅ Push notifications

**Avoid When:**
- ❌ One-way server → client (use SSE)
- ❌ Occasional updates (REST polling is simpler)
- ❌ Need HTTP caching
- ❌ Stateless architecture required

### WebSocket vs Server-Sent Events (SSE)

| Feature | WebSocket | SSE |
|---------|-----------|-----|
| **Direction** | Bidirectional | Server → Client only |
| **Protocol** | Custom | HTTP |
| **Reconnection** | Manual | Automatic |
| **Binary Data** | Yes | No (text only) |
| **Browser Support** | Excellent | Good (no IE) |
| **Complexity** | Higher | Lower |
| **Use Case** | Chat, gaming | Live updates, notifications |

**Choose SSE when:**
- Only need server → client push
- Want automatic reconnection
- Simpler implementation preferred

**Choose WebSocket when:**
- Need bidirectional communication
- Need binary data transfer
- Building real-time collaborative app

---

## Decision Summary Table

| Requirement | Recommended API | Alternative |
|-------------|----------------|-------------|
| **Public API** | REST | GraphQL (if complex) |
| **Simple CRUD** | REST | - |
| **Complex queries** | GraphQL | REST with includes |
| **Real-time bidirectional** | WebSocket | gRPC streams |
| **Real-time server→client** | SSE | WebSocket |
| **Microservices internal** | gRPC | REST |
| **Mobile app** | REST / GraphQL | gRPC (if perf critical) |
| **IoT / embedded** | gRPC | MQTT |
| **File uploads** | REST | - |
| **High performance** | gRPC | REST with HTTP/2 |
| **Third-party integrations** | REST | - |
| **Batch operations** | GraphQL | REST with batch endpoint |

## Hybrid Approach (Recommended)

```
Frontend (Web/Mobile)
    │
    ├─── REST ─────────> Simple CRUD operations
    ├─── GraphQL ──────> Complex data fetching
    └─── WebSocket ────> Real-time features

Backend Microservices
    │
    └─── gRPC ─────────> Internal service communication

Third-Party Integrations
    │
    └─── REST ─────────> Public API
```

**Example Architecture:**
- **User-facing API:** GraphQL (flexible queries)
- **Admin panel API:** REST (simple, cacheable)
- **Real-time notifications:** WebSocket
- **Service-to-service:** gRPC (fast, type-safe)
- **Webhook callbacks:** REST (standard)

---

**Key Principle:** Start with REST, add GraphQL if complexity justifies it, use gRPC for internal services, WebSocket for real-time features.

**Review Trigger Points:**
- Clients complain about over-fetching (consider GraphQL)
- Internal service latency high (consider gRPC)
- Need real-time features (add WebSocket)
- Performance critical microservices (migrate to gRPC)
