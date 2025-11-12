# MongoDB + Mongoose Setup - NoSQL Database

**For:** Node.js, Express, NestJS backends  
**Coverage:** Schema design, CRUD, aggregation, indexing  
**Tools:** MongoDB 6+, Mongoose 7+, MongoDB Compass

---

## 📦 Installation

```bash
# MongoDB driver + Mongoose
npm install mongoose

# Types for TypeScript
npm install -D @types/mongoose

# Development tools
npm install -D mongodb-memory-server  # In-memory DB for testing
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── config/
│   │   └── database.ts          # MongoDB connection
│   ├── models/
│   │   ├── User.model.ts
│   │   ├── Product.model.ts
│   │   └── Order.model.ts
│   ├── schemas/
│   │   └── user.schema.ts       # Schema definitions
│   ├── repositories/
│   │   └── user.repository.ts   # Data access layer
│   ├── services/
│   │   └── user.service.ts
│   └── utils/
│       ├── db.helpers.ts
│       └── validators.ts
├── .env
└── package.json
```

---

## ⚙️ Database Configuration

### config/database.ts

```typescript
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp';

export const connectDatabase = async (): Promise<void> => {
  try {
    await mongoose.connect(MONGODB_URI, {
      // Connection options
      maxPoolSize: 10,
      minPoolSize: 2,
      socketTimeoutMS: 45000,
      serverSelectionTimeoutMS: 5000,
      family: 4, // Use IPv4
    });

    console.log('✅ MongoDB connected successfully');

    // Connection events
    mongoose.connection.on('error', (err) => {
      console.error('❌ MongoDB connection error:', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.warn('⚠️  MongoDB disconnected');
    });

    // Graceful shutdown
    process.on('SIGINT', async () => {
      await mongoose.connection.close();
      console.log('MongoDB connection closed through app termination');
      process.exit(0);
    });
  } catch (error) {
    console.error('Failed to connect to MongoDB:', error);
    process.exit(1);
  }
};

// Health check
export const checkDatabaseHealth = async (): Promise<boolean> => {
  try {
    await mongoose.connection.db.admin().ping();
    return true;
  } catch {
    return false;
  }
};
```

### .env

```env
MONGODB_URI=mongodb://localhost:27017/myapp
MONGODB_URI_TEST=mongodb://localhost:27017/myapp_test

# MongoDB Atlas (production)
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority
```

---

## 📝 Schema Examples

### 1. User Schema (Complete)

```typescript
// models/User.model.ts
import mongoose, { Schema, Document, Model } from 'mongoose';
import bcrypt from 'bcryptjs';

// Interface for User document
export interface IUser extends Document {
  email: string;
  username: string;
  password: string;
  firstName?: string;
  lastName?: string;
  avatar?: string;
  role: 'user' | 'admin' | 'moderator';
  isActive: boolean;
  emailVerified: boolean;
  lastLogin?: Date;
  createdAt: Date;
  updatedAt: Date;
  
  // Virtual
  fullName: string;
  
  // Methods
  comparePassword(candidatePassword: string): Promise<boolean>;
  generateAuthToken(): string;
}

// Interface for User model (static methods)
interface IUserModel extends Model<IUser> {
  findByEmail(email: string): Promise<IUser | null>;
  findActiveUsers(): Promise<IUser[]>;
}

// Schema definition
const userSchema = new Schema<IUser, IUserModel>(
  {
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,
      lowercase: true,
      trim: true,
      validate: {
        validator: (v: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
        message: 'Invalid email format'
      }
    },
    username: {
      type: String,
      required: true,
      unique: true,
      trim: true,
      minlength: [3, 'Username must be at least 3 characters'],
      maxlength: [30, 'Username cannot exceed 30 characters']
    },
    password: {
      type: String,
      required: true,
      minlength: [8, 'Password must be at least 8 characters'],
      select: false // Don't return password by default
    },
    firstName: {
      type: String,
      trim: true
    },
    lastName: {
      type: String,
      trim: true
    },
    avatar: String,
    role: {
      type: String,
      enum: ['user', 'admin', 'moderator'],
      default: 'user'
    },
    isActive: {
      type: Boolean,
      default: true
    },
    emailVerified: {
      type: Boolean,
      default: false
    },
    lastLogin: Date
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

// Indexes
userSchema.index({ email: 1 });
userSchema.index({ username: 1 });
userSchema.index({ role: 1, isActive: 1 });
userSchema.index({ createdAt: -1 });

// Virtual property
userSchema.virtual('fullName').get(function(this: IUser) {
  return `${this.firstName || ''} ${this.lastName || ''}`.trim();
});

// Pre-save middleware - Hash password
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error as Error);
  }
});

// Instance method - Compare password
userSchema.methods.comparePassword = async function(
  candidatePassword: string
): Promise<boolean> {
  return bcrypt.compare(candidatePassword, this.password);
};

// Instance method - Generate auth token
userSchema.methods.generateAuthToken = function(): string {
  // Implement JWT token generation
  return 'jwt_token_here';
};

// Static method - Find by email
userSchema.statics.findByEmail = function(email: string) {
  return this.findOne({ email: email.toLowerCase() });
};

// Static method - Find active users
userSchema.statics.findActiveUsers = function() {
  return this.find({ isActive: true });
};

// Export model
export const User = mongoose.model<IUser, IUserModel>('User', userSchema);
```

### 2. Product Schema with Relations

```typescript
// models/Product.model.ts
import mongoose, { Schema, Document, Types } from 'mongoose';

export interface IProduct extends Document {
  name: string;
  slug: string;
  description: string;
  price: number;
  compareAtPrice?: number;
  category: Types.ObjectId;
  tags: string[];
  images: string[];
  stock: number;
  sku: string;
  isActive: boolean;
  metadata: Record<string, any>;
  createdBy: Types.ObjectId;
  createdAt: Date;
  updatedAt: Date;
}

const productSchema = new Schema<IProduct>(
  {
    name: {
      type: String,
      required: true,
      trim: true,
      maxlength: 200
    },
    slug: {
      type: String,
      required: true,
      unique: true,
      lowercase: true
    },
    description: {
      type: String,
      required: true,
      maxlength: 5000
    },
    price: {
      type: Number,
      required: true,
      min: 0
    },
    compareAtPrice: {
      type: Number,
      min: 0
    },
    category: {
      type: Schema.Types.ObjectId,
      ref: 'Category',
      required: true
    },
    tags: [String],
    images: [String],
    stock: {
      type: Number,
      required: true,
      min: 0,
      default: 0
    },
    sku: {
      type: String,
      required: true,
      unique: true
    },
    isActive: {
      type: Boolean,
      default: true
    },
    metadata: {
      type: Schema.Types.Mixed,
      default: {}
    },
    createdBy: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true
    }
  },
  {
    timestamps: true
  }
);

// Indexes
productSchema.index({ name: 'text', description: 'text' });
productSchema.index({ slug: 1 });
productSchema.index({ category: 1, isActive: 1 });
productSchema.index({ price: 1 });
productSchema.index({ tags: 1 });

// Pre-save - Generate slug
productSchema.pre('save', function(next) {
  if (this.isModified('name')) {
    this.slug = this.name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  }
  next();
});

export const Product = mongoose.model<IProduct>('Product', productSchema);
```

### 3. Order Schema with Subdocuments

```typescript
// models/Order.model.ts
import mongoose, { Schema, Document, Types } from 'mongoose';

interface IOrderItem {
  product: Types.ObjectId;
  name: string;
  price: number;
  quantity: number;
  subtotal: number;
}

export interface IOrder extends Document {
  orderNumber: string;
  user: Types.ObjectId;
  items: IOrderItem[];
  totalAmount: number;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  shippingAddress: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  paymentMethod: string;
  paymentStatus: 'pending' | 'paid' | 'failed' | 'refunded';
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
}

const orderItemSchema = new Schema<IOrderItem>({
  product: {
    type: Schema.Types.ObjectId,
    ref: 'Product',
    required: true
  },
  name: { type: String, required: true },
  price: { type: Number, required: true, min: 0 },
  quantity: { type: Number, required: true, min: 1 },
  subtotal: { type: Number, required: true, min: 0 }
});

const orderSchema = new Schema<IOrder>(
  {
    orderNumber: {
      type: String,
      required: true,
      unique: true
    },
    user: {
      type: Schema.Types.ObjectId,
      ref: 'User',
      required: true
    },
    items: [orderItemSchema],
    totalAmount: {
      type: Number,
      required: true,
      min: 0
    },
    status: {
      type: String,
      enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
      default: 'pending'
    },
    shippingAddress: {
      street: { type: String, required: true },
      city: { type: String, required: true },
      state: { type: String, required: true },
      zipCode: { type: String, required: true },
      country: { type: String, required: true }
    },
    paymentMethod: {
      type: String,
      required: true
    },
    paymentStatus: {
      type: String,
      enum: ['pending', 'paid', 'failed', 'refunded'],
      default: 'pending'
    },
    notes: String
  },
  {
    timestamps: true
  }
);

// Indexes
orderSchema.index({ orderNumber: 1 });
orderSchema.index({ user: 1, createdAt: -1 });
orderSchema.index({ status: 1 });
orderSchema.index({ createdAt: -1 });

// Pre-save - Generate order number
orderSchema.pre('save', async function(next) {
  if (this.isNew) {
    const count = await mongoose.model('Order').countDocuments();
    this.orderNumber = `ORD-${Date.now()}-${count + 1}`;
  }
  next();
});

export const Order = mongoose.model<IOrder>('Order', orderSchema);
```

---

## 🔧 Repository Pattern

### repositories/user.repository.ts

```typescript
import { User, IUser } from '../models/User.model';
import { FilterQuery, UpdateQuery } from 'mongoose';

export class UserRepository {
  async create(userData: Partial<IUser>): Promise<IUser> {
    const user = new User(userData);
    return user.save();
  }

  async findById(id: string): Promise<IUser | null> {
    return User.findById(id).select('+password');
  }

  async findByEmail(email: string): Promise<IUser | null> {
    return User.findOne({ email: email.toLowerCase() }).select('+password');
  }

  async findAll(
    filter: FilterQuery<IUser> = {},
    options: { skip?: number; limit?: number; sort?: any } = {}
  ): Promise<IUser[]> {
    const { skip = 0, limit = 10, sort = { createdAt: -1 } } = options;
    
    return User.find(filter)
      .sort(sort)
      .skip(skip)
      .limit(limit)
      .exec();
  }

  async update(
    id: string,
    updateData: UpdateQuery<IUser>
  ): Promise<IUser | null> {
    return User.findByIdAndUpdate(
      id,
      updateData,
      { new: true, runValidators: true }
    );
  }

  async delete(id: string): Promise<boolean> {
    const result = await User.findByIdAndDelete(id);
    return result !== null;
  }

  async count(filter: FilterQuery<IUser> = {}): Promise<number> {
    return User.countDocuments(filter);
  }

  async exists(filter: FilterQuery<IUser>): Promise<boolean> {
    return User.exists(filter).then(result => result !== null);
  }
}
```

---

## 🚀 Advanced Queries

### Aggregation Pipeline

```typescript
// Get user statistics
async getUserStats() {
  return User.aggregate([
    {
      $match: { isActive: true }
    },
    {
      $group: {
        _id: '$role',
        count: { $sum: 1 },
        avgLoginDays: {
          $avg: {
            $divide: [
              { $subtract: [new Date(), '$lastLogin'] },
              1000 * 60 * 60 * 24
            ]
          }
        }
      }
    },
    {
      $sort: { count: -1 }
    }
  ]);
}

// Product sales aggregation
async getProductSales(startDate: Date, endDate: Date) {
  return Order.aggregate([
    {
      $match: {
        createdAt: { $gte: startDate, $lte: endDate },
        status: 'delivered'
      }
    },
    {
      $unwind: '$items'
    },
    {
      $group: {
        _id: '$items.product',
        totalSold: { $sum: '$items.quantity' },
        totalRevenue: { $sum: '$items.subtotal' },
        orderCount: { $sum: 1 }
      }
    },
    {
      $lookup: {
        from: 'products',
        localField: '_id',
        foreignField: '_id',
        as: 'productDetails'
      }
    },
    {
      $unwind: '$productDetails'
    },
    {
      $project: {
        _id: 1,
        productName: '$productDetails.name',
        totalSold: 1,
        totalRevenue: 1,
        orderCount: 1
      }
    },
    {
      $sort: { totalRevenue: -1 }
    },
    {
      $limit: 10
    }
  ]);
}
```

### Population (Relations)

```typescript
// Populate single reference
const product = await Product.findById(id)
  .populate('category')
  .populate('createdBy', 'name email');

// Populate nested
const order = await Order.findById(id)
  .populate({
    path: 'user',
    select: 'name email'
  })
  .populate({
    path: 'items.product',
    select: 'name price images'
  });

// Multiple levels
const order = await Order.findById(id)
  .populate({
    path: 'items.product',
    populate: {
      path: 'category',
      select: 'name'
    }
  });
```

### Text Search

```typescript
// Full-text search
const products = await Product.find({
  $text: { $search: 'laptop gaming' }
})
  .sort({ score: { $meta: 'textScore' } })
  .limit(10);

// Regex search
const users = await User.find({
  username: { $regex: 'john', $options: 'i' }
});
```

---

## 📊 Performance Optimization

### Indexing Strategy

```typescript
// Compound index
userSchema.index({ role: 1, isActive: 1, createdAt: -1 });

// Text index
productSchema.index({ name: 'text', description: 'text' });

// Geospatial index
locationSchema.index({ coordinates: '2dsphere' });

// TTL index (auto-delete after expiry)
sessionSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 });

// Unique compound index
orderSchema.index({ userId: 1, orderNumber: 1 }, { unique: true });
```

### Query Optimization

```typescript
// Use lean() for read-only queries (faster)
const users = await User.find().lean();

// Select specific fields
const users = await User.find().select('name email');

// Limit and skip for pagination
const users = await User.find()
  .skip((page - 1) * limit)
  .limit(limit);

// Use cursor for large datasets
const cursor = User.find().cursor();
for (let user = await cursor.next(); user != null; user = await cursor.next()) {
  // Process user
}
```

---

## 🧪 Testing with In-Memory MongoDB

```typescript
// tests/setup.ts
import { MongoMemoryServer } from 'mongodb-memory-server';
import mongoose from 'mongoose';

let mongoServer: MongoMemoryServer;

export const setupTestDatabase = async () => {
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();
  await mongoose.connect(uri);
};

export const teardownTestDatabase = async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
};

export const clearDatabase = async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
};

// Test example
import { User } from '../models/User.model';

beforeAll(async () => {
  await setupTestDatabase();
});

afterAll(async () => {
  await teardownTestDatabase();
});

beforeEach(async () => {
  await clearDatabase();
});

test('should create user', async () => {
  const user = await User.create({
    email: 'test@example.com',
    username: 'testuser',
    password: 'password123'
  });

  expect(user.email).toBe('test@example.com');
  expect(user.password).not.toBe('password123'); // Hashed
});
```

---

## ✅ Best Practices

1. **Schema Design:** Embed vs Reference appropriately
2. **Indexes:** Add indexes for frequent queries
3. **Validation:** Use built-in validators
4. **Middleware:** Hash passwords, sanitize data
5. **Lean Queries:** Use `.lean()` for read-only
6. **Population:** Avoid over-populating
7. **Pagination:** Always limit query results
8. **Transactions:** Use for multi-document operations
9. **Error Handling:** Catch validation errors
10. **Connection Pool:** Configure properly for production

---

## 🐛 Common Issues

**Issue:** Duplicate key error  
**Fix:** Check unique indexes, use `upsert` carefully

**Issue:** Slow queries  
**Fix:** Add indexes, use `.explain()` to analyze

**Issue:** Connection timeout  
**Fix:** Check network, increase timeout settings

**Issue:** Memory leak  
**Fix:** Close cursors, avoid keeping large results in memory

---

**Ready for:** Node.js backends with MongoDB  
**Next:** Run connection test with `npm start`
