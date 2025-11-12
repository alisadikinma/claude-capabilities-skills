# Prisma Complete Setup - Modern ORM

**For:** Node.js, TypeScript (PostgreSQL, MySQL, SQLite, MongoDB)  
**Coverage:** Schema, migrations, queries, relations, optimization  
**Tools:** Prisma 5+, Prisma Studio, Prisma Client

---

## 📦 Installation

```bash
# Prisma CLI + Client
npm install -D prisma
npm install @prisma/client

# Initialize Prisma
npx prisma init

# Optional: Prisma Studio (GUI)
# Included in Prisma CLI
```

---

## 📂 Project Structure

```
backend/
├── prisma/
│   ├── schema.prisma           # Schema definition
│   ├── migrations/             # Migration files
│   │   └── 20240101_init/
│   │       └── migration.sql
│   └── seed.ts                 # Seed data
├── src/
│   ├── lib/
│   │   └── prisma.ts           # Prisma client instance
│   ├── repositories/
│   │   └── user.repository.ts
│   └── services/
│       └── user.service.ts
├── .env
└── package.json
```

---

## ⚙️ Schema Configuration

### prisma/schema.prisma

```prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["fullTextSearch", "fullTextIndex"]
  binaryTargets   = ["native", "linux-musl"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// User model
model User {
  id            String    @id @default(uuid())
  email         String    @unique
  username      String    @unique
  password      String
  firstName     String?
  lastName      String?
  avatar        String?
  role          Role      @default(USER)
  isActive      Boolean   @default(true)
  emailVerified Boolean   @default(false)
  lastLogin     DateTime?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  // Relations
  posts         Post[]
  orders        Order[]
  profile       Profile?
  sessions      Session[]

  @@index([email])
  @@index([username])
  @@index([role, isActive])
  @@map("users")
}

model Profile {
  id        String   @id @default(uuid())
  bio       String?  @db.Text
  website   String?
  location  String?
  birthDate DateTime?
  phone     String?
  userId    String   @unique
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("profiles")
}

model Post {
  id          String     @id @default(uuid())
  title       String
  slug        String     @unique
  content     String     @db.Text
  excerpt     String?
  published   Boolean    @default(false)
  publishedAt DateTime?
  viewCount   Int        @default(0)
  authorId    String
  author      User       @relation(fields: [authorId], references: [id], onDelete: Cascade)
  categoryId  String?
  category    Category?  @relation(fields: [categoryId], references: [id])
  tags        Tag[]
  comments    Comment[]
  createdAt   DateTime   @default(now())
  updatedAt   DateTime   @updatedAt

  @@index([slug])
  @@index([authorId])
  @@index([published, publishedAt])
  @@fulltext([title, content])
  @@map("posts")
}

model Category {
  id          String   @id @default(uuid())
  name        String   @unique
  slug        String   @unique
  description String?
  posts       Post[]
  products    Product[]
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@map("categories")
}

model Tag {
  id        String   @id @default(uuid())
  name      String   @unique
  slug      String   @unique
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("tags")
}

model Comment {
  id        String   @id @default(uuid())
  content   String   @db.Text
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  authorId  String
  parentId  String?
  parent    Comment? @relation("CommentReplies", fields: [parentId], references: [id])
  replies   Comment[] @relation("CommentReplies")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([postId])
  @@index([authorId])
  @@map("comments")
}

// E-commerce models
model Product {
  id            String      @id @default(uuid())
  name          String
  slug          String      @unique
  description   String      @db.Text
  price         Decimal     @db.Decimal(10, 2)
  compareAtPrice Decimal?   @db.Decimal(10, 2)
  stock         Int         @default(0)
  sku           String      @unique
  images        String[]
  isActive      Boolean     @default(true)
  categoryId    String?
  category      Category?   @relation(fields: [categoryId], references: [id])
  orderItems    OrderItem[]
  metadata      Json?
  createdAt     DateTime    @default(now())
  updatedAt     DateTime    @updatedAt

  @@index([slug])
  @@index([categoryId])
  @@index([isActive])
  @@fulltext([name, description])
  @@map("products")
}

model Order {
  id            String      @id @default(uuid())
  orderNumber   String      @unique
  userId        String
  user          User        @relation(fields: [userId], references: [id])
  items         OrderItem[]
  totalAmount   Decimal     @db.Decimal(10, 2)
  status        OrderStatus @default(PENDING)
  paymentStatus PaymentStatus @default(PENDING)
  paymentMethod String
  shippingAddress Json
  notes         String?     @db.Text
  createdAt     DateTime    @default(now())
  updatedAt     DateTime    @updatedAt

  @@index([orderNumber])
  @@index([userId, createdAt])
  @@index([status])
  @@map("orders")
}

model OrderItem {
  id        String   @id @default(uuid())
  orderId   String
  order     Order    @relation(fields: [orderId], references: [id], onDelete: Cascade)
  productId String
  product   Product  @relation(fields: [productId], references: [id])
  name      String
  price     Decimal  @db.Decimal(10, 2)
  quantity  Int
  subtotal  Decimal  @db.Decimal(10, 2)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([orderId])
  @@index([productId])
  @@map("order_items")
}

model Session {
  id        String   @id @default(uuid())
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  token     String   @unique
  expiresAt DateTime
  createdAt DateTime @default(now())

  @@index([userId])
  @@index([token])
  @@index([expiresAt])
  @@map("sessions")
}

// Enums
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

enum PaymentStatus {
  PENDING
  PAID
  FAILED
  REFUNDED
}
```

---

## 🔧 Prisma Client Setup

### src/lib/prisma.ts

```typescript
import { PrismaClient } from '@prisma/client';

// PrismaClient singleton
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' 
      ? ['query', 'error', 'warn'] 
      : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

// Graceful shutdown
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});

// Connection test
export async function testConnection(): Promise<boolean> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    return true;
  } catch (error) {
    console.error('Database connection failed:', error);
    return false;
  }
}
```

---

## 📝 CRUD Operations

### Basic Queries

```typescript
import { prisma } from './lib/prisma';

// CREATE
const user = await prisma.user.create({
  data: {
    email: 'john@example.com',
    username: 'johndoe',
    password: 'hashed_password',
    firstName: 'John',
    lastName: 'Doe',
    profile: {
      create: {
        bio: 'Software developer',
        website: 'https://johndoe.com'
      }
    }
  },
  include: {
    profile: true
  }
});

// READ
const user = await prisma.user.findUnique({
  where: { email: 'john@example.com' },
  include: {
    profile: true,
    posts: {
      where: { published: true },
      orderBy: { publishedAt: 'desc' },
      take: 10
    }
  }
});

// READ MANY
const users = await prisma.user.findMany({
  where: {
    role: 'USER',
    isActive: true
  },
  select: {
    id: true,
    email: true,
    username: true,
    profile: {
      select: {
        bio: true
      }
    }
  },
  orderBy: {
    createdAt: 'desc'
  },
  take: 20,
  skip: 0
});

// UPDATE
const user = await prisma.user.update({
  where: { id: userId },
  data: {
    firstName: 'Jane',
    profile: {
      update: {
        bio: 'Updated bio'
      }
    }
  }
});

// UPSERT
const user = await prisma.user.upsert({
  where: { email: 'john@example.com' },
  update: {
    lastLogin: new Date()
  },
  create: {
    email: 'john@example.com',
    username: 'johndoe',
    password: 'hashed_password'
  }
});

// DELETE
await prisma.user.delete({
  where: { id: userId }
});

// DELETE MANY
await prisma.user.deleteMany({
  where: {
    emailVerified: false,
    createdAt: {
      lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) // 30 days ago
    }
  }
});

// COUNT
const count = await prisma.user.count({
  where: {
    role: 'USER',
    isActive: true
  }
});
```

### Advanced Queries

```typescript
// Full-text search
const posts = await prisma.post.findMany({
  where: {
    OR: [
      { title: { search: 'prisma tutorial' } },
      { content: { search: 'prisma tutorial' } }
    ]
  }
});

// Complex filtering
const products = await prisma.product.findMany({
  where: {
    AND: [
      { isActive: true },
      { stock: { gt: 0 } },
      {
        OR: [
          { price: { lte: 100 } },
          { compareAtPrice: { lte: 150 } }
        ]
      }
    ]
  }
});

// Aggregations
const stats = await prisma.order.aggregate({
  where: {
    status: 'DELIVERED'
  },
  _sum: {
    totalAmount: true
  },
  _avg: {
    totalAmount: true
  },
  _count: {
    id: true
  },
  _max: {
    totalAmount: true
  }
});

// Group by
const ordersByStatus = await prisma.order.groupBy({
  by: ['status'],
  _count: {
    id: true
  },
  _sum: {
    totalAmount: true
  },
  orderBy: {
    _count: {
      id: 'desc'
    }
  }
});

// Raw queries
const result = await prisma.$queryRaw`
  SELECT u.*, COUNT(p.id) as post_count
  FROM users u
  LEFT JOIN posts p ON p.author_id = u.id
  GROUP BY u.id
  HAVING COUNT(p.id) > 5
`;
```

---

## 🔄 Relations & Nested Writes

```typescript
// Create with nested relations
const post = await prisma.post.create({
  data: {
    title: 'Getting Started with Prisma',
    slug: 'getting-started-prisma',
    content: 'Lorem ipsum...',
    author: {
      connect: { id: authorId }
    },
    category: {
      connectOrCreate: {
        where: { slug: 'tutorials' },
        create: {
          name: 'Tutorials',
          slug: 'tutorials'
        }
      }
    },
    tags: {
      connectOrCreate: [
        {
          where: { slug: 'prisma' },
          create: { name: 'Prisma', slug: 'prisma' }
        },
        {
          where: { slug: 'typescript' },
          create: { name: 'TypeScript', slug: 'typescript' }
        }
      ]
    }
  },
  include: {
    author: true,
    category: true,
    tags: true
  }
});

// Update with nested relations
const order = await prisma.order.update({
  where: { id: orderId },
  data: {
    status: 'SHIPPED',
    items: {
      updateMany: {
        where: { productId: productId },
        data: { quantity: { increment: 1 } }
      }
    }
  }
});

// Disconnect relations
await prisma.post.update({
  where: { id: postId },
  data: {
    tags: {
      disconnect: [{ id: tagId }]
    }
  }
});
```

---

## 🚀 Transactions

```typescript
// Sequential operations (all or nothing)
const result = await prisma.$transaction(async (tx) => {
  // Create user
  const user = await tx.user.create({
    data: {
      email: 'new@example.com',
      username: 'newuser',
      password: 'hashed'
    }
  });

  // Create profile
  const profile = await tx.profile.create({
    data: {
      userId: user.id,
      bio: 'Welcome!'
    }
  });

  // Create session
  const session = await tx.session.create({
    data: {
      userId: user.id,
      token: 'token_here',
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
    }
  });

  return { user, profile, session };
});

// Batch operations
const [deletedPosts, updatedUsers] = await prisma.$transaction([
  prisma.post.deleteMany({
    where: { published: false, createdAt: { lt: oldDate } }
  }),
  prisma.user.updateMany({
    where: { lastLogin: { lt: inactiveDate } },
    data: { isActive: false }
  })
]);

// Interactive transactions with isolation level
await prisma.$transaction(
  async (tx) => {
    const user = await tx.user.findUnique({
      where: { id: userId }
    });

    if (!user) throw new Error('User not found');

    await tx.user.update({
      where: { id: userId },
      data: { balance: { decrement: amount } }
    });

    await tx.order.create({
      data: {
        userId: userId,
        totalAmount: amount,
        // ...
      }
    });
  },
  {
    isolationLevel: 'Serializable',
    maxWait: 5000,
    timeout: 10000
  }
);
```

---

## 📊 Migrations

```bash
# Create migration
npx prisma migrate dev --name init

# Apply migrations (production)
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset

# Check migration status
npx prisma migrate status

# Resolve migration conflicts
npx prisma migrate resolve --applied 20240101_migration_name

# Generate Prisma Client
npx prisma generate
```

### Migration Best Practices

```typescript
// Always create migrations for schema changes
// prisma/migrations/20240101_add_user_role/migration.sql

-- AlterTable
ALTER TABLE "users" ADD COLUMN "role" TEXT NOT NULL DEFAULT 'USER';

-- CreateIndex
CREATE INDEX "users_role_idx" ON "users"("role");

-- Custom migration logic
UPDATE "users" 
SET "role" = 'ADMIN' 
WHERE "email" IN ('admin@example.com', 'owner@example.com');
```

---

## 🌱 Database Seeding

### prisma/seed.ts

```typescript
import { PrismaClient, Role } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding database...');

  // Clear existing data
  await prisma.session.deleteMany();
  await prisma.orderItem.deleteMany();
  await prisma.order.deleteMany();
  await prisma.product.deleteMany();
  await prisma.comment.deleteMany();
  await prisma.post.deleteMany();
  await prisma.tag.deleteMany();
  await prisma.category.deleteMany();
  await prisma.profile.deleteMany();
  await prisma.user.deleteMany();

  // Create users
  const hashedPassword = await bcrypt.hash('password123', 10);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@example.com',
      username: 'admin',
      password: hashedPassword,
      firstName: 'Admin',
      lastName: 'User',
      role: Role.ADMIN,
      emailVerified: true,
      profile: {
        create: {
          bio: 'System administrator',
          website: 'https://example.com'
        }
      }
    }
  });

  const users = await Promise.all(
    Array.from({ length: 10 }, async (_, i) => {
      return prisma.user.create({
        data: {
          email: `user${i}@example.com`,
          username: `user${i}`,
          password: hashedPassword,
          firstName: `User`,
          lastName: `${i}`,
          emailVerified: true,
          profile: {
            create: {
              bio: `I am user number ${i}`
            }
          }
        }
      });
    })
  );

  // Create categories
  const categories = await Promise.all([
    prisma.category.create({
      data: { name: 'Technology', slug: 'technology' }
    }),
    prisma.category.create({
      data: { name: 'Lifestyle', slug: 'lifestyle' }
    })
  ]);

  // Create tags
  const tags = await Promise.all([
    prisma.tag.create({ data: { name: 'Tutorial', slug: 'tutorial' } }),
    prisma.tag.create({ data: { name: 'Guide', slug: 'guide' } })
  ]);

  // Create posts
  await Promise.all(
    users.slice(0, 5).map((user, i) =>
      prisma.post.create({
        data: {
          title: `Post ${i + 1}`,
          slug: `post-${i + 1}`,
          content: 'Lorem ipsum dolor sit amet...',
          excerpt: 'Short excerpt...',
          published: true,
          publishedAt: new Date(),
          authorId: user.id,
          categoryId: categories[i % 2].id,
          tags: {
            connect: tags.map(tag => ({ id: tag.id }))
          }
        }
      })
    )
  );

  console.log('✅ Database seeded successfully!');
}

main()
  .catch((e) => {
    console.error('❌ Seeding failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

### package.json

```json
{
  "prisma": {
    "seed": "ts-node prisma/seed.ts"
  }
}
```

```bash
# Run seed
npx prisma db seed
```

---

## 🎯 Repository Pattern

### repositories/user.repository.ts

```typescript
import { prisma } from '../lib/prisma';
import { User, Prisma } from '@prisma/client';

export class UserRepository {
  async create(data: Prisma.UserCreateInput): Promise<User> {
    return prisma.user.create({ data });
  }

  async findById(id: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { id },
      include: { profile: true }
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return prisma.user.findUnique({
      where: { email: email.toLowerCase() }
    });
  }

  async findMany(params: {
    skip?: number;
    take?: number;
    where?: Prisma.UserWhereInput;
    orderBy?: Prisma.UserOrderByWithRelationInput;
  }): Promise<User[]> {
    const { skip, take, where, orderBy } = params;
    return prisma.user.findMany({
      skip,
      take,
      where,
      orderBy
    });
  }

  async update(id: string, data: Prisma.UserUpdateInput): Promise<User> {
    return prisma.user.update({
      where: { id },
      data
    });
  }

  async delete(id: string): Promise<User> {
    return prisma.user.delete({
      where: { id }
    });
  }

  async count(where?: Prisma.UserWhereInput): Promise<number> {
    return prisma.user.count({ where });
  }
}
```

---

## ✅ Best Practices

1. **Use Transactions:** For multi-table operations
2. **Indexes:** Add for frequently queried fields
3. **Select Fields:** Only fetch needed data
4. **Batch Operations:** Use `createMany`, `updateMany`
5. **Connection Pooling:** Configure for production
6. **Type Safety:** Leverage Prisma types
7. **Migrations:** Always use migrations, never manual SQL
8. **Soft Deletes:** Implement via `deletedAt` field
9. **Pagination:** Use cursor-based for large datasets
10. **Logging:** Enable query logs in dev

---

## 🐛 Common Issues

**Issue:** `prisma generate` fails  
**Fix:** Delete `node_modules/.prisma` and regenerate

**Issue:** Migration conflicts  
**Fix:** Use `prisma migrate resolve`

**Issue:** Slow queries  
**Fix:** Add indexes, use `explain` in raw queries

**Issue:** Connection pool exhausted  
**Fix:** Increase pool size, close connections properly

---

## 🚀 Prisma Studio

```bash
# Open Prisma Studio GUI
npx prisma studio
```

---

**Ready for:** PostgreSQL, MySQL, SQLite, MongoDB  
**Next:** Run `npx prisma migrate dev` to start
