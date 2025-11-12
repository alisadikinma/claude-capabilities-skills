# Fastify - High-Performance API Structure

**Framework:** Fastify 4.x + TypeScript  
**Architecture:** Plugin-based + Domain-Driven  
**Database:** PostgreSQL + Prisma ORM  
**Auth:** @fastify/jwt + bcrypt  
**Validation:** JSON Schema (built-in)  
**Use Case:** High-throughput APIs, real-time systems, microservices

---

## 📁 Project Structure

```
fastify-api/
├── src/
│   ├── plugins/                 # Fastify plugins
│   │   ├── prisma.ts            # Database plugin
│   │   ├── jwt.ts               # JWT authentication
│   │   ├── cors.ts              # CORS configuration
│   │   ├── helmet.ts            # Security headers
│   │   └── sensible.ts          # Utilities plugin
│   │
│   ├── modules/                 # Feature modules
│   │   ├── auth/
│   │   │   ├── auth.routes.ts
│   │   │   ├── auth.service.ts
│   │   │   ├── auth.handler.ts
│   │   │   └── auth.schema.ts
│   │   │
│   │   └── users/
│   │       ├── users.routes.ts
│   │       ├── users.service.ts
│   │       ├── users.handler.ts
│   │       ├── users.repository.ts
│   │       └── users.schema.ts
│   │
│   ├── config/                  # Configuration
│   │   ├── env.ts               # Environment validation
│   │   └── server.ts            # Server configuration
│   │
│   ├── utils/                   # Utilities
│   │   ├── password.ts          # Password hashing
│   │   ├── errors.ts            # Custom errors
│   │   └── logger.ts            # Pino logger config
│   │
│   ├── hooks/                   # Lifecycle hooks
│   │   ├── onRequest.ts         # Request hooks
│   │   └── preHandler.ts        # Pre-handler hooks
│   │
│   ├── decorators/              # Custom decorators
│   │   └── authenticate.ts      # Auth decorator
│   │
│   ├── types/                   # TypeScript types
│   │   ├── fastify.d.ts         # Fastify augmentation
│   │   └── index.ts             # Shared types
│   │
│   ├── app.ts                   # Fastify app factory
│   └── server.ts                # Server entry point
│
├── prisma/
│   ├── schema.prisma            # Database schema
│   └── migrations/              # Migrations
│
├── test/
│   ├── helper.ts                # Test utilities
│   ├── routes/
│   │   ├── auth.test.ts
│   │   └── users.test.ts
│   └── plugins/
│       └── prisma.test.ts
│
├── .env.example
├── .eslintrc.js
├── .prettierrc
├── docker-compose.yml
├── Dockerfile
├── package.json
├── tsconfig.json
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Initialize Project

```bash
mkdir fastify-api && cd fastify-api
npm init -y

# Install Fastify core
npm install fastify
npm install @fastify/cors @fastify/helmet @fastify/jwt
npm install @fastify/sensible @fastify/rate-limit
npm install @fastify/env @fastify/formbody

# Install database & validation
npm install @prisma/client
npm install fluent-json-schema

# Install utilities
npm install bcryptjs
npm install pino pino-pretty

# Install dev dependencies
npm install -D typescript @types/node
npm install -D @types/bcryptjs
npm install -D prisma tsx nodemon
npm install -D @fastify/cli
npm install -D tap @types/tap
```

### 2. TypeScript Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@plugins/*": ["src/plugins/*"],
      "@modules/*": ["src/modules/*"],
      "@config/*": ["src/config/*"],
      "@utils/*": ["src/utils/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "test"]
}
```

### 3. Environment Variables

**.env.example:**
```env
# Server
NODE_ENV=development
HOST=0.0.0.0
PORT=3000
LOG_LEVEL=info

# Database
DATABASE_URL="postgresql://postgres:password@localhost:5432/fastify_db"

# JWT
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
JWT_EXPIRES_IN=900

# CORS
CORS_ORIGIN=http://localhost:5173

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_TIMEWINDOW=60000
```

---

## 📝 Core Files Implementation

### src/server.ts

```typescript
import { build } from './app';
import { env } from './config/env';

const start = async () => {
  const server = await build({
    logger: {
      level: env.LOG_LEVEL,
      transport: env.NODE_ENV === 'development' ? {
        target: 'pino-pretty',
        options: {
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      } : undefined,
    },
  });

  try {
    await server.listen({
      host: env.HOST,
      port: env.PORT,
    });

    console.log(`🚀 Server running on http://${env.HOST}:${env.PORT}`);
  } catch (err) {
    server.log.error(err);
    process.exit(1);
  }

  // Graceful shutdown
  const signals = ['SIGINT', 'SIGTERM'];
  signals.forEach((signal) => {
    process.on(signal, async () => {
      console.log(`${signal} received, closing server...`);
      await server.close();
      process.exit(0);
    });
  });
};

start();
```

### src/app.ts

```typescript
import Fastify, { FastifyInstance, FastifyServerOptions } from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import sensible from '@fastify/sensible';
import rateLimit from '@fastify/rate-limit';
import { prismaPlugin } from './plugins/prisma';
import { jwtPlugin } from './plugins/jwt';
import { authRoutes } from './modules/auth/auth.routes';
import { userRoutes } from './modules/users/users.routes';
import { env } from './config/env';

export const build = async (opts: FastifyServerOptions = {}): Promise<FastifyInstance> => {
  const app = Fastify(opts);

  // Register plugins
  await app.register(helmet, { 
    contentSecurityPolicy: env.NODE_ENV === 'production' 
  });
  
  await app.register(cors, { 
    origin: env.CORS_ORIGIN,
    credentials: true 
  });

  await app.register(sensible);

  await app.register(rateLimit, {
    max: env.RATE_LIMIT_MAX,
    timeWindow: env.RATE_LIMIT_TIMEWINDOW,
  });

  // Custom plugins
  await app.register(prismaPlugin);
  await app.register(jwtPlugin);

  // Health check
  app.get('/health', async (request, reply) => {
    return { 
      status: 'ok', 
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
    };
  });

  // API routes
  await app.register(authRoutes, { prefix: '/api/v1/auth' });
  await app.register(userRoutes, { prefix: '/api/v1/users' });

  // Global error handler
  app.setErrorHandler((error, request, reply) => {
    request.log.error(error);

    const statusCode = error.statusCode || 500;
    const message = env.NODE_ENV === 'production' && statusCode === 500
      ? 'Internal Server Error'
      : error.message;

    reply.status(statusCode).send({
      statusCode,
      error: error.name,
      message,
    });
  });

  // 404 handler
  app.setNotFoundHandler((request, reply) => {
    reply.status(404).send({
      statusCode: 404,
      error: 'Not Found',
      message: 'Route not found',
    });
  });

  return app;
};
```

### src/config/env.ts

```typescript
import { Type, Static } from '@sinclair/typebox';
import Ajv from 'ajv';

const EnvSchema = Type.Object({
  NODE_ENV: Type.Union([
    Type.Literal('development'),
    Type.Literal('production'),
    Type.Literal('test')
  ]),
  HOST: Type.String({ default: '0.0.0.0' }),
  PORT: Type.Number({ default: 3000 }),
  LOG_LEVEL: Type.String({ default: 'info' }),
  DATABASE_URL: Type.String(),
  JWT_SECRET: Type.String({ minLength: 32 }),
  JWT_EXPIRES_IN: Type.Number({ default: 900 }),
  CORS_ORIGIN: Type.String({ default: 'http://localhost:5173' }),
  RATE_LIMIT_MAX: Type.Number({ default: 100 }),
  RATE_LIMIT_TIMEWINDOW: Type.Number({ default: 60000 }),
});

type Env = Static<typeof EnvSchema>;

const ajv = new Ajv({
  removeAdditional: true,
  useDefaults: true,
  coerceTypes: true,
});

const validate = ajv.compile(EnvSchema);
const valid = validate(process.env);

if (!valid) {
  throw new Error(
    'Invalid environment variables:\n' +
    JSON.stringify(validate.errors, null, 2)
  );
}

export const env = process.env as unknown as Env;
```

### src/plugins/prisma.ts

```typescript
import { FastifyInstance } from 'fastify';
import fp from 'fastify-plugin';
import { PrismaClient } from '@prisma/client';

declare module 'fastify' {
  interface FastifyInstance {
    prisma: PrismaClient;
  }
}

async function prismaPlugin(fastify: FastifyInstance) {
  const prisma = new PrismaClient({
    log: fastify.log.level === 'debug' 
      ? ['query', 'info', 'warn', 'error']
      : ['error'],
  });

  await prisma.$connect();

  fastify.decorate('prisma', prisma);

  fastify.addHook('onClose', async (instance) => {
    await instance.prisma.$disconnect();
  });

  fastify.log.info('✅ Prisma connected');
}

export const prismaPlugin = fp(prismaPlugin, {
  name: 'prisma',
});
```

### src/plugins/jwt.ts

```typescript
import { FastifyInstance } from 'fastify';
import fp from 'fastify-plugin';
import jwt from '@fastify/jwt';
import { env } from '@config/env';

async function jwtPlugin(fastify: FastifyInstance) {
  await fastify.register(jwt, {
    secret: env.JWT_SECRET,
    sign: {
      expiresIn: env.JWT_EXPIRES_IN,
    },
  });

  // Authentication decorator
  fastify.decorate('authenticate', async (request, reply) => {
    try {
      await request.jwtVerify();
    } catch (err) {
      reply.send(err);
    }
  });
}

export const jwtPlugin = fp(jwtPlugin, {
  name: 'jwt',
});
```

---

## 🔐 Authentication Module

### src/modules/auth/auth.schema.ts

```typescript
import S from 'fluent-json-schema';

export const registerSchema = {
  body: S.object()
    .prop('email', S.string().format(S.FORMATS.EMAIL).required())
    .prop('password', S.string().minLength(8).required())
    .prop('name', S.string().minLength(2).required()),
  response: {
    201: S.object()
      .prop('user', S.object()
        .prop('id', S.number())
        .prop('email', S.string())
        .prop('name', S.string())
      )
      .prop('token', S.string()),
  },
};

export const loginSchema = {
  body: S.object()
    .prop('email', S.string().format(S.FORMATS.EMAIL).required())
    .prop('password', S.string().required()),
  response: {
    200: S.object()
      .prop('user', S.object()
        .prop('id', S.number())
        .prop('email', S.string())
        .prop('name', S.string())
      )
      .prop('token', S.string()),
  },
};
```

### src/modules/auth/auth.handler.ts

```typescript
import { FastifyRequest, FastifyReply } from 'fastify';
import { AuthService } from './auth.service';

interface RegisterBody {
  email: string;
  password: string;
  name: string;
}

interface LoginBody {
  email: string;
  password: string;
}

export class AuthHandler {
  constructor(private authService: AuthService) {}

  async register(
    request: FastifyRequest<{ Body: RegisterBody }>,
    reply: FastifyReply
  ) {
    const result = await this.authService.register(request.body);
    reply.code(201).send(result);
  }

  async login(
    request: FastifyRequest<{ Body: LoginBody }>,
    reply: FastifyReply
  ) {
    const result = await this.authService.login(request.body);
    reply.send(result);
  }
}
```

### src/modules/auth/auth.routes.ts

```typescript
import { FastifyInstance } from 'fastify';
import { AuthHandler } from './auth.handler';
import { AuthService } from './auth.service';
import { registerSchema, loginSchema } from './auth.schema';

export async function authRoutes(fastify: FastifyInstance) {
  const authService = new AuthService(fastify.prisma, fastify.jwt);
  const authHandler = new AuthHandler(authService);

  fastify.post(
    '/register',
    { schema: registerSchema },
    authHandler.register.bind(authHandler)
  );

  fastify.post(
    '/login',
    { schema: loginSchema },
    authHandler.login.bind(authHandler)
  );

  fastify.post(
    '/me',
    { onRequest: [fastify.authenticate] },
    async (request, reply) => {
      return { user: request.user };
    }
  );
}
```

### src/modules/auth/auth.service.ts

```typescript
import { PrismaClient } from '@prisma/client';
import { JWT } from '@fastify/jwt';
import { hashPassword, comparePassword } from '@utils/password';

interface RegisterInput {
  email: string;
  password: string;
  name: string;
}

interface LoginInput {
  email: string;
  password: string;
}

export class AuthService {
  constructor(
    private prisma: PrismaClient,
    private jwt: JWT
  ) {}

  async register(input: RegisterInput) {
    const existingUser = await this.prisma.user.findUnique({
      where: { email: input.email },
    });

    if (existingUser) {
      throw new Error('Email already registered');
    }

    const hashedPassword = await hashPassword(input.password);

    const user = await this.prisma.user.create({
      data: {
        email: input.email,
        password: hashedPassword,
        name: input.name,
      },
      select: {
        id: true,
        email: true,
        name: true,
      },
    });

    const token = this.jwt.sign({ 
      sub: user.id, 
      email: user.email 
    });

    return { user, token };
  }

  async login(input: LoginInput) {
    const user = await this.prisma.user.findUnique({
      where: { email: input.email },
    });

    if (!user || !(await comparePassword(input.password, user.password))) {
      throw new Error('Invalid credentials');
    }

    const token = this.jwt.sign({ 
      sub: user.id, 
      email: user.email 
    });

    return {
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
      token,
    };
  }
}
```

---

## 👤 Users Module Example

### src/modules/users/users.schema.ts

```typescript
import S from 'fluent-json-schema';

export const getUserSchema = {
  params: S.object()
    .prop('id', S.number().required()),
  response: {
    200: S.object()
      .prop('id', S.number())
      .prop('email', S.string())
      .prop('name', S.string())
      .prop('createdAt', S.string().format(S.FORMATS.DATE_TIME)),
  },
};

export const updateUserSchema = {
  params: S.object()
    .prop('id', S.number().required()),
  body: S.object()
    .prop('name', S.string().minLength(2)),
  response: {
    200: S.object()
      .prop('id', S.number())
      .prop('email', S.string())
      .prop('name', S.string()),
  },
};
```

---

## 📦 Package.json Scripts

```json
{
  "scripts": {
    "dev": "nodemon --exec tsx src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js",
    "test": "tap test/**/*.test.ts",
    "test:coverage": "tap test/**/*.test.ts --coverage-report=lcov",
    "prisma:generate": "prisma generate",
    "prisma:migrate": "prisma migrate dev",
    "prisma:studio": "prisma studio",
    "lint": "eslint src --ext .ts",
    "format": "prettier --write \"src/**/*.ts\""
  }
}
```

---

## 🐳 Docker Setup

**Dockerfile:**
```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
RUN npx prisma generate

FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma
COPY package*.json ./

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/fastify_db
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastify_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

---

## ⚡ Performance Tips

**1. JSON Schema Compilation**
```typescript
// Pre-compile schemas for better performance
const compiledSchema = app.getSchema('schemaId');
```

**2. Connection Pooling**
```typescript
// In prisma.schema
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  connection_limit = 10
  pool_timeout = 10
}
```

**3. Serialization**
```typescript
// Use fast-json-stringify for responses
fastify.get('/fast', {
  schema: {
    response: {
      200: { /* your schema */ }
    }
  }
}, async () => {
  return { data: 'serialized fast' };
});
```

---

## ✅ Production Checklist

- [ ] Environment variables validated with TypeBox
- [ ] Prisma connection pooling configured
- [ ] JWT secret min 32 characters
- [ ] Rate limiting enabled globally
- [ ] CORS origin whitelist configured
- [ ] Helmet security headers active
- [ ] Request validation with JSON Schema
- [ ] Error logging with Pino
- [ ] Health check endpoint working
- [ ] Graceful shutdown implemented
- [ ] Database migrations tested
- [ ] Load testing completed (autocannon)
- [ ] API documentation (Swagger via @fastify/swagger)
- [ ] Unit tests passing (tap)
- [ ] Docker image optimized
- [ ] CI/CD pipeline configured

---

## 📊 Performance Benchmarks

Fastify is one of the fastest Node.js frameworks:

```bash
# Install autocannon for benchmarking
npm install -g autocannon

# Run benchmark
autocannon -c 100 -d 10 http://localhost:3000/health

# Expected results (on modern hardware):
# Requests/sec:  30,000+
# Latency avg:   3ms
# Throughput:    5+ MB/sec
```

---

**Template Version:** 1.0  
**Last Updated:** 2025-01-12  
**Maintainer:** Web_Architect_Pro Skill
