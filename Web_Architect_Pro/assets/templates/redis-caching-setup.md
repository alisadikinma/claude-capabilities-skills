# Redis Caching Setup - Performance Optimization

**For:** Node.js backends (Express, NestJS, Fastify)  
**Coverage:** Caching strategies, session storage, pub/sub  
**Tools:** Redis 7+, ioredis, redis-om

---

## 📦 Installation

```bash
# Redis client (ioredis - recommended)
npm install ioredis

# Alternative: node-redis
npm install redis

# Redis OM (Object Mapping)
npm install redis-om

# Types
npm install -D @types/ioredis
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── config/
│   │   └── redis.ts           # Redis connection
│   ├── cache/
│   │   ├── cache.service.ts   # Cache abstraction
│   │   ├── strategies/
│   │   │   ├── user.cache.ts
│   │   │   └── post.cache.ts
│   │   └── decorators/
│   │       └── cached.decorator.ts
│   ├── middleware/
│   │   └── cache.middleware.ts
│   └── pubsub/
│       └── redis.pubsub.ts    # Pub/Sub handler
└── .env
```

---

## ⚙️ Redis Connection

### config/redis.ts

```typescript
import Redis from 'ioredis';

// Single instance
export const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0'),
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: false,
});

// Connection events
redis.on('connect', () => {
  console.log('✅ Redis connected');
});

redis.on('error', (error) => {
  console.error('❌ Redis error:', error);
});

redis.on('reconnecting', () => {
  console.log('🔄 Redis reconnecting...');
});

// Cluster configuration (production)
export const redisCluster = new Redis.Cluster(
  [
    { host: 'localhost', port: 6379 },
    { host: 'localhost', port: 6380 },
  ],
  {
    redisOptions: {
      password: process.env.REDIS_PASSWORD,
    },
  }
);

// Sentinel configuration (high availability)
export const redisSentinel = new Redis({
  sentinels: [
    { host: 'sentinel1', port: 26379 },
    { host: 'sentinel2', port: 26379 },
  ],
  name: 'mymaster',
  password: process.env.REDIS_PASSWORD,
});

// Health check
export async function checkRedisHealth(): Promise<boolean> {
  try {
    await redis.ping();
    return true;
  } catch (error) {
    return false;
  }
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  await redis.quit();
  console.log('Redis connection closed');
});
```

### .env

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Cache TTL (seconds)
CACHE_TTL_SHORT=60        # 1 minute
CACHE_TTL_MEDIUM=300      # 5 minutes
CACHE_TTL_LONG=3600       # 1 hour
CACHE_TTL_DAY=86400       # 24 hours
```

---

## 🔧 Cache Service

### cache/cache.service.ts

```typescript
import { redis } from '../config/redis';

export class CacheService {
  /**
   * Get cached value
   */
  async get<T>(key: string): Promise<T | null> {
    try {
      const data = await redis.get(key);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error(`Cache get error for key ${key}:`, error);
      return null;
    }
  }

  /**
   * Set cache with TTL
   */
  async set(key: string, value: any, ttl?: number): Promise<void> {
    try {
      const serialized = JSON.stringify(value);
      
      if (ttl) {
        await redis.setex(key, ttl, serialized);
      } else {
        await redis.set(key, serialized);
      }
    } catch (error) {
      console.error(`Cache set error for key ${key}:`, error);
    }
  }

  /**
   * Delete cache key
   */
  async del(key: string | string[]): Promise<void> {
    try {
      if (Array.isArray(key)) {
        await redis.del(...key);
      } else {
        await redis.del(key);
      }
    } catch (error) {
      console.error(`Cache delete error:`, error);
    }
  }

  /**
   * Check if key exists
   */
  async exists(key: string): Promise<boolean> {
    try {
      const result = await redis.exists(key);
      return result === 1;
    } catch (error) {
      console.error(`Cache exists error for key ${key}:`, error);
      return false;
    }
  }

  /**
   * Increment counter
   */
  async increment(key: string, by: number = 1): Promise<number> {
    try {
      return await redis.incrby(key, by);
    } catch (error) {
      console.error(`Cache increment error for key ${key}:`, error);
      return 0;
    }
  }

  /**
   * Set expiry on existing key
   */
  async expire(key: string, ttl: number): Promise<void> {
    try {
      await redis.expire(key, ttl);
    } catch (error) {
      console.error(`Cache expire error for key ${key}:`, error);
    }
  }

  /**
   * Get multiple keys
   */
  async mget<T>(keys: string[]): Promise<(T | null)[]> {
    try {
      const values = await redis.mget(...keys);
      return values.map(val => val ? JSON.parse(val) : null);
    } catch (error) {
      console.error(`Cache mget error:`, error);
      return keys.map(() => null);
    }
  }

  /**
   * Delete keys by pattern
   */
  async deletePattern(pattern: string): Promise<void> {
    try {
      const keys = await redis.keys(pattern);
      if (keys.length > 0) {
        await redis.del(...keys);
      }
    } catch (error) {
      console.error(`Cache deletePattern error for ${pattern}:`, error);
    }
  }

  /**
   * Get or Set (cache-aside pattern)
   */
  async getOrSet<T>(
    key: string,
    factory: () => Promise<T>,
    ttl?: number
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.get<T>(key);
    if (cached !== null) {
      return cached;
    }

    // Get from factory and cache
    const value = await factory();
    await this.set(key, value, ttl);
    return value;
  }

  /**
   * Remember (wrapper around getOrSet)
   */
  async remember<T>(
    key: string,
    ttl: number,
    callback: () => Promise<T>
  ): Promise<T> {
    return this.getOrSet(key, callback, ttl);
  }
}

export const cacheService = new CacheService();
```

---

## 📝 Caching Strategies

### 1. Cache-Aside (Lazy Loading)

```typescript
// User cache example
export class UserCache {
  private static readonly PREFIX = 'user';
  private static readonly TTL = 3600; // 1 hour

  static getKey(userId: string): string {
    return `${this.PREFIX}:${userId}`;
  }

  static async getUser(userId: string): Promise<User | null> {
    return cacheService.remember(
      this.getKey(userId),
      this.TTL,
      async () => {
        // Fetch from database
        return await User.findById(userId);
      }
    );
  }

  static async invalidateUser(userId: string): Promise<void> {
    await cacheService.del(this.getKey(userId));
  }

  static async updateUser(userId: string, user: User): Promise<void> {
    await cacheService.set(this.getKey(userId), user, this.TTL);
  }
}

// Usage
const user = await UserCache.getUser('123');
```

### 2. Write-Through Cache

```typescript
export class PostCache {
  private static readonly PREFIX = 'post';
  private static readonly TTL = 300; // 5 minutes

  static async createPost(postData: CreatePostInput): Promise<Post> {
    // Write to database
    const post = await Post.create(postData);

    // Write to cache
    await cacheService.set(
      `${this.PREFIX}:${post.id}`,
      post,
      this.TTL
    );

    return post;
  }

  static async updatePost(postId: string, updates: UpdatePostInput): Promise<Post> {
    // Update database
    const post = await Post.findByIdAndUpdate(postId, updates, { new: true });

    // Update cache
    await cacheService.set(
      `${this.PREFIX}:${post.id}`,
      post,
      this.TTL
    );

    // Invalidate list caches
    await cacheService.deletePattern(`${this.PREFIX}:list:*`);

    return post;
  }
}
```

### 3. Write-Behind (Write-Back) Cache

```typescript
export class AnalyticsCache {
  private static readonly QUEUE_KEY = 'analytics:queue';
  private static readonly BATCH_SIZE = 100;

  static async trackPageView(data: PageViewData): Promise<void> {
    // Add to queue in Redis
    await redis.rpush(this.QUEUE_KEY, JSON.stringify(data));

    // Process queue if batch size reached
    const queueLength = await redis.llen(this.QUEUE_KEY);
    if (queueLength >= this.BATCH_SIZE) {
      await this.processQueue();
    }
  }

  private static async processQueue(): Promise<void> {
    // Get batch
    const batch = await redis.lpop(this.QUEUE_KEY, this.BATCH_SIZE);

    if (batch.length > 0) {
      // Batch insert to database
      const records = batch.map(item => JSON.parse(item));
      await Analytics.insertMany(records);
    }
  }
}
```

### 4. Distributed Cache with Patterns

```typescript
// List caching with pagination
export class PostListCache {
  private static readonly PREFIX = 'post:list';
  private static readonly TTL = 300;

  static async getPublishedPosts(page: number = 1, limit: number = 20) {
    const key = `${this.PREFIX}:published:${page}:${limit}`;

    return cacheService.remember(key, this.TTL, async () => {
      const skip = (page - 1) * limit;
      return await Post.find({ published: true })
        .skip(skip)
        .limit(limit)
        .sort({ createdAt: -1 });
    });
  }

  static async invalidateAll(): Promise<void> {
    await cacheService.deletePattern(`${this.PREFIX}:*`);
  }
}
```

---

## 🎯 Cache Middleware

### middleware/cache.middleware.ts

```typescript
import { Request, Response, NextFunction } from 'express';
import { cacheService } from '../cache/cache.service';

/**
 * HTTP cache middleware
 */
export function cacheMiddleware(ttl: number = 300) {
  return async (req: Request, res: Response, next: NextFunction) => {
    // Only cache GET requests
    if (req.method !== 'GET') {
      return next();
    }

    // Generate cache key from URL + query params
    const key = `http:${req.originalUrl}`;

    // Try to get cached response
    const cached = await cacheService.get(key);
    if (cached) {
      return res.json(cached);
    }

    // Store original json method
    const originalJson = res.json.bind(res);

    // Override json method to cache response
    res.json = function(data: any) {
      // Cache the response
      cacheService.set(key, data, ttl).catch(console.error);

      // Send response
      return originalJson(data);
    };

    next();
  };
}

// Usage
app.get('/api/posts', cacheMiddleware(300), async (req, res) => {
  const posts = await Post.find();
  res.json(posts);
});
```

---

## 🔄 Pub/Sub Pattern

### pubsub/redis.pubsub.ts

```typescript
import Redis from 'ioredis';

class RedisPubSub {
  private publisher: Redis;
  private subscriber: Redis;
  private handlers = new Map<string, Set<Function>>();

  constructor() {
    this.publisher = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6379'),
    });

    this.subscriber = new Redis({
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT || '6379'),
    });

    // Setup message handler
    this.subscriber.on('message', (channel, message) => {
      const handlers = this.handlers.get(channel);
      if (handlers) {
        const data = JSON.parse(message);
        handlers.forEach(handler => handler(data));
      }
    });
  }

  /**
   * Publish message to channel
   */
  async publish(channel: string, data: any): Promise<void> {
    await this.publisher.publish(channel, JSON.stringify(data));
  }

  /**
   * Subscribe to channel
   */
  async subscribe(channel: string, handler: Function): Promise<void> {
    if (!this.handlers.has(channel)) {
      this.handlers.set(channel, new Set());
      await this.subscriber.subscribe(channel);
    }

    this.handlers.get(channel)!.add(handler);
  }

  /**
   * Unsubscribe from channel
   */
  async unsubscribe(channel: string, handler?: Function): Promise<void> {
    if (!handler) {
      // Unsubscribe all handlers
      await this.subscriber.unsubscribe(channel);
      this.handlers.delete(channel);
    } else {
      // Unsubscribe specific handler
      const handlers = this.handlers.get(channel);
      if (handlers) {
        handlers.delete(handler);
        if (handlers.size === 0) {
          await this.subscriber.unsubscribe(channel);
          this.handlers.delete(channel);
        }
      }
    }
  }

  /**
   * Pattern subscribe
   */
  async psubscribe(pattern: string, handler: Function): Promise<void> {
    if (!this.handlers.has(pattern)) {
      this.handlers.set(pattern, new Set());
      await this.subscriber.psubscribe(pattern);
    }

    this.handlers.get(pattern)!.add(handler);
  }
}

export const pubsub = new RedisPubSub();

// Usage example
pubsub.subscribe('user:created', (data) => {
  console.log('New user created:', data);
});

await pubsub.publish('user:created', { userId: '123', email: 'user@example.com' });
```

---

## 🎯 Advanced Patterns

### Rate Limiting with Redis

```typescript
export class RateLimiter {
  static async checkRateLimit(
    userId: string,
    action: string,
    limit: number,
    windowSeconds: number
  ): Promise<{ allowed: boolean; remaining: number }> {
    const key = `ratelimit:${userId}:${action}`;
    
    const current = await redis.incr(key);
    
    if (current === 1) {
      // First request, set expiry
      await redis.expire(key, windowSeconds);
    }

    const remaining = Math.max(0, limit - current);

    return {
      allowed: current <= limit,
      remaining,
    };
  }
}

// Usage
const { allowed, remaining } = await RateLimiter.checkRateLimit(
  userId,
  'api:request',
  100, // limit
  3600 // 1 hour
);

if (!allowed) {
  return res.status(429).json({ error: 'Rate limit exceeded', remaining });
}
```

### Session Storage

```typescript
export class SessionStore {
  private static readonly PREFIX = 'session';
  private static readonly TTL = 86400; // 24 hours

  static async create(sessionId: string, data: any): Promise<void> {
    await cacheService.set(
      `${this.PREFIX}:${sessionId}`,
      data,
      this.TTL
    );
  }

  static async get(sessionId: string): Promise<any | null> {
    return cacheService.get(`${this.PREFIX}:${sessionId}`);
  }

  static async destroy(sessionId: string): Promise<void> {
    await cacheService.del(`${this.PREFIX}:${sessionId}`);
  }

  static async refresh(sessionId: string): Promise<void> {
    await cacheService.expire(`${this.PREFIX}:${sessionId}`, this.TTL);
  }
}
```

### Distributed Locks

```typescript
export class DistributedLock {
  static async acquire(
    lockKey: string,
    ttl: number = 10000
  ): Promise<string | null> {
    const lockId = Math.random().toString(36);
    const result = await redis.set(
      `lock:${lockKey}`,
      lockId,
      'PX',
      ttl,
      'NX'
    );
    
    return result === 'OK' ? lockId : null;
  }

  static async release(lockKey: string, lockId: string): Promise<boolean> {
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;
    
    const result = await redis.eval(script, 1, `lock:${lockKey}`, lockId);
    return result === 1;
  }

  static async withLock<T>(
    lockKey: string,
    callback: () => Promise<T>,
    ttl: number = 10000
  ): Promise<T> {
    const lockId = await this.acquire(lockKey, ttl);
    
    if (!lockId) {
      throw new Error('Failed to acquire lock');
    }

    try {
      return await callback();
    } finally {
      await this.release(lockKey, lockId);
    }
  }
}

// Usage
await DistributedLock.withLock('process:job:123', async () => {
  // Critical section - only one instance can execute this
  await processJob('123');
});
```

### Sorted Sets for Leaderboards

```typescript
export class Leaderboard {
  private static readonly KEY = 'leaderboard:global';

  static async addScore(userId: string, score: number): Promise<void> {
    await redis.zadd(this.KEY, score, userId);
  }

  static async getTopPlayers(limit: number = 10): Promise<Array<{ userId: string; score: number }>> {
    const results = await redis.zrevrange(this.KEY, 0, limit - 1, 'WITHSCORES');
    
    const players = [];
    for (let i = 0; i < results.length; i += 2) {
      players.push({
        userId: results[i],
        score: parseInt(results[i + 1]),
      });
    }
    
    return players;
  }

  static async getUserRank(userId: string): Promise<number | null> {
    const rank = await redis.zrevrank(this.KEY, userId);
    return rank !== null ? rank + 1 : null;
  }

  static async getUserScore(userId: string): Promise<number | null> {
    const score = await redis.zscore(this.KEY, userId);
    return score !== null ? parseInt(score) : null;
  }
}
```

---

## 🧪 Testing

```typescript
import { redis } from '../config/redis';
import { cacheService } from '../cache/cache.service';

describe('Cache Service', () => {
  beforeEach(async () => {
    await redis.flushdb();
  });

  it('should set and get value', async () => {
    await cacheService.set('test:key', { name: 'John' });
    const value = await cacheService.get('test:key');
    expect(value).toEqual({ name: 'John' });
  });

  it('should expire after TTL', async () => {
    await cacheService.set('test:ttl', 'value', 1);
    await new Promise(resolve => setTimeout(resolve, 1100));
    const value = await cacheService.get('test:ttl');
    expect(value).toBeNull();
  });
});
```

---

## ✅ Best Practices

1. **Key Naming:** Use consistent prefixes (e.g., `user:123`, `post:list:1`)
2. **TTL Always:** Set expiration to prevent memory issues
3. **Serialization:** JSON.stringify for complex objects
4. **Error Handling:** Cache failures shouldn't break app
5. **Invalidation:** Clear cache on data updates
6. **Monitoring:** Track hit/miss ratio
7. **Memory Management:** Use eviction policies (LRU)
8. **Cluster Mode:** Use for production scaling
9. **Pub/Sub:** For real-time updates across servers
10. **Testing:** Test cache invalidation logic

---

## 🐛 Common Issues

**Issue:** Memory usage growing indefinitely  
**Fix:** Set TTL on all keys, use `maxmemory-policy`

**Issue:** Cache stampede (thundering herd)  
**Fix:** Use distributed locks or stale-while-revalidate

**Issue:** Stale data in cache  
**Fix:** Implement proper cache invalidation strategy

**Issue:** Slow queries despite caching  
**Fix:** Profile cache hit ratio, optimize key patterns

---

**Ready for:** Production caching with Redis  
**Next:** Monitor cache metrics and optimize TTL values
