# REST API Best Practices - Complete Guide

**For:** Express, NestJS, Fastify, FastAPI, Django, Laravel  
**Coverage:** Design, conventions, versioning, documentation  
**Standards:** RESTful principles, HTTP methods, status codes

---

## 🎯 Core Principles

### RESTful Architecture

```
Resource-Oriented Design:
✅ Use nouns for resources (not verbs)
✅ Use HTTP methods for actions
✅ Predictable URL structure
✅ Stateless communication
✅ Standard status codes
```

---

## 📐 URL Structure & Naming

### Resource Naming Conventions

```
✅ GOOD - Plural nouns, lowercase, kebab-case
GET    /api/v1/users
GET    /api/v1/users/123
GET    /api/v1/users/123/orders
POST   /api/v1/blog-posts
GET    /api/v1/product-categories

❌ BAD - Verbs, mixed case, unclear structure
GET    /api/getUsers
POST   /api/CreateUser
GET    /api/user_list
DELETE /api/removeUser/123
```

### URL Structure Best Practices

```typescript
// Base structure
/{version}/{resource}/{identifier}/{sub-resource}

// Examples
GET    /v1/users                    // List all users
GET    /v1/users/123                // Get specific user
POST   /v1/users                    // Create user
PUT    /v1/users/123                // Update entire user
PATCH  /v1/users/123                // Partial update
DELETE /v1/users/123                // Delete user

// Nested resources
GET    /v1/users/123/orders         // User's orders
GET    /v1/orders/456/items         // Order items
POST   /v1/posts/789/comments       // Add comment to post

// Query parameters for filtering
GET    /v1/products?category=electronics&sort=price&order=desc
GET    /v1/users?status=active&role=admin&page=2&limit=20
GET    /v1/posts?published=true&author=123&search=tutorial

// Avoid deep nesting (max 2 levels)
✅ GET /v1/users/123/orders
❌ GET /v1/users/123/orders/456/items/789/details
```

---

## 🔧 HTTP Methods

### Method Usage

```typescript
// GET - Retrieve resources (safe, idempotent)
GET /v1/users                 // List all users
GET /v1/users/123             // Get single user
GET /v1/users/123/profile     // Get user profile

// POST - Create new resource (not idempotent)
POST /v1/users
{
  "email": "john@example.com",
  "name": "John Doe"
}

// PUT - Replace entire resource (idempotent)
PUT /v1/users/123
{
  "email": "john@example.com",
  "name": "John Doe",
  "bio": "Developer",
  "avatar": "url"
}

// PATCH - Partial update (not idempotent)
PATCH /v1/users/123
{
  "name": "Jane Doe"
}

// DELETE - Remove resource (idempotent)
DELETE /v1/users/123

// HEAD - Get headers only (like GET without body)
HEAD /v1/users/123

// OPTIONS - Get allowed methods
OPTIONS /v1/users
```

### Advanced Method Usage

```typescript
// Bulk operations
POST   /v1/users/bulk-create
DELETE /v1/users/bulk-delete
PATCH  /v1/users/bulk-update

// Actions on resources (when REST isn't enough)
POST   /v1/users/123/activate
POST   /v1/orders/456/cancel
POST   /v1/posts/789/publish
POST   /v1/invoices/101/send

// Search (POST for complex queries)
POST   /v1/users/search
{
  "filters": {
    "age": { "gte": 18, "lte": 65 },
    "location": "New York",
    "interests": ["tech", "sports"]
  }
}
```

---

## 📊 HTTP Status Codes

### Success Codes (2xx)

```typescript
// 200 OK - Standard success
GET    /v1/users/123              → 200 + user data
PUT    /v1/users/123              → 200 + updated user
PATCH  /v1/users/123              → 200 + updated user
DELETE /v1/users/123              → 200 + success message

// 201 Created - Resource created
POST   /v1/users                  → 201 + created user
Location: /v1/users/123

// 202 Accepted - Request accepted, processing async
POST   /v1/reports/generate       → 202 + job info

// 204 No Content - Success, no response body
DELETE /v1/users/123              → 204 (no body)
PATCH  /v1/users/123/archive      → 204
```

### Client Error Codes (4xx)

```typescript
// 400 Bad Request - Invalid input
POST   /v1/users
{
  "email": "invalid-email"        → 400 + validation errors
}

// 401 Unauthorized - Authentication required
GET    /v1/profile                → 401 (no token)

// 403 Forbidden - Authenticated but no permission
DELETE /v1/users/123              → 403 (not admin)

// 404 Not Found - Resource doesn't exist
GET    /v1/users/999              → 404

// 405 Method Not Allowed - HTTP method not supported
POST   /v1/users/123              → 405

// 409 Conflict - Resource state conflict
POST   /v1/users
{
  "email": "existing@example.com"  → 409 (email exists)
}

// 422 Unprocessable Entity - Validation failed
POST   /v1/users
{
  "email": "valid@example.com",
  "age": -5                        → 422 + validation details
}

// 429 Too Many Requests - Rate limit exceeded
GET    /v1/users                  → 429 + retry info
```

### Server Error Codes (5xx)

```typescript
// 500 Internal Server Error - Generic server error
GET    /v1/users                  → 500 (unexpected error)

// 502 Bad Gateway - Upstream server error
GET    /v1/users                  → 502 (database down)

// 503 Service Unavailable - Temporary unavailable
GET    /v1/users                  → 503 (maintenance mode)

// 504 Gateway Timeout - Upstream timeout
GET    /v1/reports/large          → 504 (query timeout)
```

---

## 📝 Request/Response Format

### Standard Request Format

```typescript
// Headers
POST /v1/users
Content-Type: application/json
Authorization: Bearer eyJhbGc...
Accept: application/json
X-Request-ID: uuid-here

// Body (JSON)
{
  "email": "john@example.com",
  "name": "John Doe",
  "role": "user"
}
```

### Standard Response Format

```typescript
// Success Response
{
  "success": true,
  "data": {
    "id": "123",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "user",
    "createdAt": "2024-01-12T10:30:00Z"
  },
  "meta": {
    "timestamp": "2024-01-12T10:30:00Z",
    "version": "1.0"
  }
}

// Error Response
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      },
      {
        "field": "age",
        "message": "Must be at least 18"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-01-12T10:30:00Z",
    "requestId": "uuid-here"
  }
}

// List Response with Pagination
{
  "success": true,
  "data": [
    { "id": "1", "name": "User 1" },
    { "id": "2", "name": "User 2" }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false
  },
  "meta": {
    "timestamp": "2024-01-12T10:30:00Z"
  }
}
```

---

## 🔄 Pagination Strategies

### Offset-Based Pagination

```typescript
// Request
GET /v1/users?page=2&limit=20

// Response
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}

// Implementation (Express)
app.get('/v1/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 20;
  const skip = (page - 1) * limit;

  const [users, total] = await Promise.all([
    User.find().skip(skip).limit(limit),
    User.countDocuments()
  ]);

  res.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
});
```

### Cursor-Based Pagination (Better for large datasets)

```typescript
// Request
GET /v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

// Response
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "prevCursor": "eyJpZCI6MTAzfQ",
    "hasNext": true,
    "hasPrev": true
  }
}

// Implementation
app.get('/v1/users', async (req, res) => {
  const limit = parseInt(req.query.limit) || 20;
  const cursor = req.query.cursor 
    ? JSON.parse(Buffer.from(req.query.cursor, 'base64').toString())
    : null;

  const query = cursor ? { _id: { $gt: cursor.id } } : {};
  const users = await User.find(query).limit(limit + 1);

  const hasNext = users.length > limit;
  const results = hasNext ? users.slice(0, -1) : users;

  const nextCursor = hasNext
    ? Buffer.from(JSON.stringify({ id: results[results.length - 1]._id })).toString('base64')
    : null;

  res.json({
    data: results,
    pagination: { nextCursor, hasNext }
  });
});
```

---

## 🔍 Filtering, Sorting, Searching

### Query Parameters

```typescript
// Filtering
GET /v1/products?category=electronics&price[gte]=100&price[lte]=500
GET /v1/users?status=active&role=admin&verified=true

// Sorting
GET /v1/products?sort=price         // Ascending
GET /v1/products?sort=-price        // Descending
GET /v1/products?sort=price,-createdAt  // Multiple

// Field selection (sparse fieldsets)
GET /v1/users?fields=id,name,email
GET /v1/products?fields=-password,-secret  // Exclude fields

// Search
GET /v1/products?search=laptop
GET /v1/users?q=john

// Combined
GET /v1/products?category=electronics&sort=-price&fields=id,name,price&page=1&limit=20
```

### Implementation Example

```typescript
// Express + MongoDB
app.get('/v1/products', async (req, res) => {
  const {
    category,
    price,
    sort = '-createdAt',
    fields,
    page = 1,
    limit = 20,
    search
  } = req.query;

  // Build filter
  const filter: any = {};
  if (category) filter.category = category;
  if (price) {
    filter.price = {};
    if (price.gte) filter.price.$gte = price.gte;
    if (price.lte) filter.price.$lte = price.lte;
  }
  if (search) {
    filter.$text = { $search: search };
  }

  // Build sort
  const sortObj = sort.split(',').reduce((acc, field) => {
    if (field.startsWith('-')) {
      acc[field.substring(1)] = -1;
    } else {
      acc[field] = 1;
    }
    return acc;
  }, {});

  // Build field selection
  const selectFields = fields
    ? fields.split(',').join(' ')
    : undefined;

  // Execute query
  const skip = (page - 1) * limit;
  const [products, total] = await Promise.all([
    Product.find(filter)
      .sort(sortObj)
      .select(selectFields)
      .skip(skip)
      .limit(limit),
    Product.countDocuments(filter)
  ]);

  res.json({
    data: products,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit)
    }
  });
});
```

---

## 🔐 Authentication & Authorization

### Authentication Headers

```typescript
// Bearer Token (JWT)
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

// API Key
X-API-Key: your-api-key-here

// Basic Auth (avoid in production)
Authorization: Basic base64(username:password)
```

### Authorization Patterns

```typescript
// Resource-level authorization
GET    /v1/users/123              // Only user 123 or admin
PUT    /v1/users/123              // Only user 123 or admin
DELETE /v1/users/123              // Only admin

// Role-based access control (RBAC)
app.delete('/v1/users/:id', 
  authenticate,
  authorize(['admin']),
  async (req, res) => {
    // Delete user
  }
);

// Resource ownership check
app.put('/v1/posts/:id',
  authenticate,
  async (req, res) => {
    const post = await Post.findById(req.params.id);
    
    if (post.authorId !== req.user.id && req.user.role !== 'admin') {
      return res.status(403).json({
        error: 'You can only edit your own posts'
      });
    }
    
    // Update post
  }
);
```

---

## 📚 API Versioning

### URL Versioning (Recommended)

```typescript
// Version in path
GET /v1/users
GET /v2/users

// Express implementation
app.use('/v1', v1Routes);
app.use('/v2', v2Routes);

// Route organization
/routes
  /v1
    /users.ts
    /products.ts
  /v2
    /users.ts
    /products.ts
```

### Header Versioning

```typescript
// Version in header
GET /users
Accept: application/vnd.api.v1+json

// Implementation
app.use((req, res, next) => {
  const version = req.get('Accept')?.match(/v(\d+)/)?.[1] || '1';
  req.apiVersion = version;
  next();
});
```

### Breaking Changes Strategy

```
v1: Original API
v2: Breaking changes, deprecate v1 in 6 months
v3: Remove v1, v2 becomes legacy

Deprecation headers:
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: </v2/users>; rel="successor-version"
```

---

## 📖 API Documentation

### OpenAPI/Swagger Example

```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: User management API

paths:
  /v1/users:
    get:
      summary: List all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
        createdAt:
          type: string
          format: date-time
```

---

## ⚡ Performance Best Practices

### 1. Response Compression

```typescript
// Express
import compression from 'compression';
app.use(compression());

// Only compress responses > 1KB
app.use(compression({ threshold: 1024 }));
```

### 2. Caching Headers

```typescript
// Cache-Control
app.get('/v1/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  
  // Cache for 5 minutes
  res.set('Cache-Control', 'public, max-age=300');
  
  // ETag for conditional requests
  res.set('ETag', user.updatedAt.toISOString());
  
  res.json(user);
});

// Handle If-None-Match
if (req.get('If-None-Match') === etag) {
  return res.status(304).end();
}
```

### 3. Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/v1/', limiter);

// Response headers
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640000000
```

### 4. Response Optimization

```typescript
// Only return necessary fields
app.get('/v1/users', async (req, res) => {
  const users = await User.find()
    .select('id name email')  // Exclude unnecessary fields
    .lean();  // Return plain objects (faster)
  
  res.json(users);
});

// Lazy loading relationships
app.get('/v1/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  
  // Don't auto-populate all relationships
  // Let client request: ?include=posts,comments
  
  res.json(user);
});
```

---

## ✅ REST API Checklist

**URL Design:**
- [ ] Use plural nouns for resources
- [ ] Use kebab-case for multi-word resources
- [ ] Avoid deep nesting (max 2 levels)
- [ ] Use query params for filtering/sorting

**HTTP Methods:**
- [ ] GET for reading
- [ ] POST for creating
- [ ] PUT for full updates
- [ ] PATCH for partial updates
- [ ] DELETE for removing

**Status Codes:**
- [ ] 2xx for success
- [ ] 4xx for client errors
- [ ] 5xx for server errors
- [ ] Specific codes (404, 422, etc.)

**Responses:**
- [ ] Consistent JSON structure
- [ ] Include meta information
- [ ] Pagination for lists
- [ ] Error details with validation

**Security:**
- [ ] Authentication on protected routes
- [ ] Authorization checks
- [ ] Rate limiting
- [ ] Input validation
- [ ] HTTPS only in production

**Performance:**
- [ ] Response compression
- [ ] Caching headers
- [ ] Field selection
- [ ] Pagination
- [ ] Database indexing

**Documentation:**
- [ ] OpenAPI/Swagger spec
- [ ] Example requests/responses
- [ ] Authentication guide
- [ ] Error code reference
- [ ] Changelog for versions

---

**Ready for:** Production REST APIs  
**Next:** Implement using your framework's best practices
