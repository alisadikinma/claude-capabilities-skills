# GraphQL Setup - Complete Guide

**For:** Node.js with Apollo Server, Express, NestJS  
**Coverage:** Schema, resolvers, queries, mutations, subscriptions  
**Tools:** Apollo Server 4, GraphQL, DataLoader, TypeGraphQL

---

## 📦 Installation

```bash
# Apollo Server (standalone)
npm install @apollo/server graphql

# With Express
npm install @apollo/server express graphql express-graphql

# TypeScript types
npm install -D @types/graphql

# Additional tools
npm install graphql-tag      # Query parsing
npm install dataloader       # Batching & caching
npm install graphql-depth-limit  # Query complexity
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── graphql/
│   │   ├── schema/
│   │   │   ├── index.ts         # Combined schema
│   │   │   ├── user.schema.ts   # User types
│   │   │   └── post.schema.ts   # Post types
│   │   ├── resolvers/
│   │   │   ├── index.ts         # Combined resolvers
│   │   │   ├── user.resolver.ts
│   │   │   └── post.resolver.ts
│   │   ├── dataloaders/
│   │   │   └── user.loader.ts   # DataLoader for batching
│   │   └── directives/
│   │       └── auth.directive.ts # Custom directives
│   ├── server.ts                # Apollo Server setup
│   └── context.ts               # Context builder
└── schema.graphql               # SDL schema file
```

---

## 🔧 Basic Setup

### server.ts (Apollo Server 4)

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { typeDefs } from './graphql/schema';
import { resolvers } from './graphql/resolvers';
import { createContext } from './context';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (error) => {
    // Custom error formatting
    console.error('GraphQL Error:', error);
    return {
      message: error.message,
      code: error.extensions?.code,
      path: error.path,
    };
  },
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    // Add plugins here
  ],
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: createContext,
});

console.log(`🚀 GraphQL server ready at ${url}`);
```

### With Express Integration

```typescript
import express from 'express';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import cors from 'cors';
import { json } from 'body-parser';
import { typeDefs } from './graphql/schema';
import { resolvers } from './graphql/resolvers';
import { createContext } from './context';

const app = express();
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

await server.start();

app.use(
  '/graphql',
  cors(),
  json(),
  expressMiddleware(server, {
    context: createContext,
  })
);

app.listen(4000, () => {
  console.log('🚀 Server ready at http://localhost:4000/graphql');
});
```

---

## 📝 Schema Definition

### schema/user.schema.ts

```typescript
import { gql } from 'graphql-tag';

export const userTypeDefs = gql`
  type User {
    id: ID!
    email: String!
    username: String!
    name: String
    avatar: String
    bio: String
    role: Role!
    isActive: Boolean!
    posts: [Post!]!
    followers: [User!]!
    following: [User!]!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  enum Role {
    USER
    ADMIN
    MODERATOR
  }

  type AuthPayload {
    user: User!
    token: String!
    refreshToken: String!
  }

  input RegisterInput {
    email: String!
    username: String!
    password: String!
    name: String
  }

  input LoginInput {
    email: String!
    password: String!
  }

  input UpdateUserInput {
    name: String
    bio: String
    avatar: String
  }

  extend type Query {
    me: User
    user(id: ID!): User
    users(
      limit: Int = 20
      offset: Int = 0
      search: String
      role: Role
    ): UserConnection!
  }

  extend type Mutation {
    register(input: RegisterInput!): AuthPayload!
    login(input: LoginInput!): AuthPayload!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): Boolean!
    followUser(userId: ID!): User!
    unfollowUser(userId: ID!): User!
  }

  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type UserEdge {
    cursor: String!
    node: User!
  }
`;
```

### schema/post.schema.ts

```typescript
export const postTypeDefs = gql`
  type Post {
    id: ID!
    title: String!
    content: String!
    excerpt: String
    slug: String!
    published: Boolean!
    author: User!
    category: Category
    tags: [Tag!]!
    comments: [Comment!]!
    likeCount: Int!
    viewCount: Int!
    createdAt: DateTime!
    updatedAt: DateTime!
  }

  type Category {
    id: ID!
    name: String!
    slug: String!
    posts: [Post!]!
  }

  type Tag {
    id: ID!
    name: String!
    slug: String!
    posts: [Post!]!
  }

  type Comment {
    id: ID!
    content: String!
    post: Post!
    author: User!
    parent: Comment
    replies: [Comment!]!
    createdAt: DateTime!
  }

  input CreatePostInput {
    title: String!
    content: String!
    excerpt: String
    categoryId: ID
    tagIds: [ID!]
    published: Boolean
  }

  input UpdatePostInput {
    title: String
    content: String
    excerpt: String
    categoryId: ID
    tagIds: [ID!]
    published: Boolean
  }

  extend type Query {
    post(id: ID!): Post
    posts(
      limit: Int = 20
      offset: Int = 0
      published: Boolean
      authorId: ID
      categoryId: ID
      search: String
    ): PostConnection!
  }

  extend type Mutation {
    createPost(input: CreatePostInput!): Post!
    updatePost(id: ID!, input: UpdatePostInput!): Post!
    deletePost(id: ID!): Boolean!
    likePost(postId: ID!): Post!
    addComment(postId: ID!, content: String!): Comment!
  }

  extend type Subscription {
    postCreated: Post!
    postUpdated(postId: ID!): Post!
    commentAdded(postId: ID!): Comment!
  }

  type PostConnection {
    edges: [PostEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type PostEdge {
    cursor: String!
    node: Post!
  }
`;
```

### schema/index.ts (Combined Schema)

```typescript
import { gql } from 'graphql-tag';
import { userTypeDefs } from './user.schema';
import { postTypeDefs } from './post.schema';

// Base types
const baseTypeDefs = gql`
  scalar DateTime
  scalar JSON

  type Query {
    _empty: String
  }

  type Mutation {
    _empty: String
  }

  type Subscription {
    _empty: String
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }

  directive @auth(requires: Role = USER) on FIELD_DEFINITION
  directive @rateLimit(limit: Int!, duration: Int!) on FIELD_DEFINITION
`;

export const typeDefs = [baseTypeDefs, userTypeDefs, postTypeDefs];
```

---

## 🔧 Resolvers

### resolvers/user.resolver.ts

```typescript
import { GraphQLError } from 'graphql';
import { User } from '../models/User';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

export const userResolvers = {
  Query: {
    me: async (parent, args, context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }
      return context.user;
    },

    user: async (parent, { id }, context) => {
      const user = await User.findById(id);
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND' }
        });
      }
      return user;
    },

    users: async (parent, { limit, offset, search, role }, context) => {
      const filter: any = {};
      if (search) {
        filter.$or = [
          { username: { $regex: search, $options: 'i' } },
          { email: { $regex: search, $options: 'i' } },
        ];
      }
      if (role) filter.role = role;

      const [users, totalCount] = await Promise.all([
        User.find(filter).skip(offset).limit(limit),
        User.countDocuments(filter),
      ]);

      return {
        edges: users.map((user, index) => ({
          cursor: Buffer.from(`${offset + index}`).toString('base64'),
          node: user,
        })),
        pageInfo: {
          hasNextPage: offset + limit < totalCount,
          hasPreviousPage: offset > 0,
        },
        totalCount,
      };
    },
  },

  Mutation: {
    register: async (parent, { input }, context) => {
      // Check if user exists
      const existingUser = await User.findOne({ email: input.email });
      if (existingUser) {
        throw new GraphQLError('Email already in use', {
          extensions: { code: 'BAD_USER_INPUT' }
        });
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(input.password, 10);

      // Create user
      const user = await User.create({
        ...input,
        password: hashedPassword,
      });

      // Generate token
      const token = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET!,
        { expiresIn: '7d' }
      );

      return { user, token };
    },

    login: async (parent, { input }, context) => {
      const user = await User.findOne({ email: input.email }).select('+password');
      
      if (!user || !(await bcrypt.compare(input.password, user.password))) {
        throw new GraphQLError('Invalid credentials', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      const token = jwt.sign(
        { userId: user.id, role: user.role },
        process.env.JWT_SECRET!,
        { expiresIn: '7d' }
      );

      return { user, token };
    },

    updateUser: async (parent, { id, input }, context) => {
      if (!context.user || (context.user.id !== id && context.user.role !== 'ADMIN')) {
        throw new GraphQLError('Not authorized', {
          extensions: { code: 'FORBIDDEN' }
        });
      }

      const user = await User.findByIdAndUpdate(id, input, { new: true });
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND' }
        });
      }

      return user;
    },

    followUser: async (parent, { userId }, context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      const userToFollow = await User.findById(userId);
      if (!userToFollow) {
        throw new GraphQLError('User not found', {
          extensions: { code: 'NOT_FOUND' }
        });
      }

      // Add to following/followers lists
      await User.findByIdAndUpdate(context.user.id, {
        $addToSet: { following: userId }
      });
      await User.findByIdAndUpdate(userId, {
        $addToSet: { followers: context.user.id }
      });

      return userToFollow;
    },
  },

  User: {
    posts: async (parent, args, context) => {
      // Use DataLoader to avoid N+1 queries
      return context.loaders.postsByAuthor.load(parent.id);
    },

    followers: async (parent, args, context) => {
      return context.loaders.usersByIds.loadMany(parent.followers || []);
    },

    following: async (parent, args, context) => {
      return context.loaders.usersByIds.loadMany(parent.following || []);
    },
  },
};
```

### resolvers/post.resolver.ts

```typescript
export const postResolvers = {
  Query: {
    post: async (parent, { id }, context) => {
      const post = await Post.findById(id);
      if (!post) {
        throw new GraphQLError('Post not found', {
          extensions: { code: 'NOT_FOUND' }
        });
      }

      // Increment view count
      await Post.findByIdAndUpdate(id, { $inc: { viewCount: 1 } });

      return post;
    },

    posts: async (parent, args, context) => {
      const { limit, offset, published, authorId, categoryId, search } = args;

      const filter: any = {};
      if (published !== undefined) filter.published = published;
      if (authorId) filter.authorId = authorId;
      if (categoryId) filter.categoryId = categoryId;
      if (search) {
        filter.$text = { $search: search };
      }

      const [posts, totalCount] = await Promise.all([
        Post.find(filter).skip(offset).limit(limit).sort({ createdAt: -1 }),
        Post.countDocuments(filter),
      ]);

      return {
        edges: posts.map((post, index) => ({
          cursor: Buffer.from(`${offset + index}`).toString('base64'),
          node: post,
        })),
        pageInfo: {
          hasNextPage: offset + limit < totalCount,
          hasPreviousPage: offset > 0,
        },
        totalCount,
      };
    },
  },

  Mutation: {
    createPost: async (parent, { input }, context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      const post = await Post.create({
        ...input,
        authorId: context.user.id,
      });

      // Publish subscription
      context.pubsub.publish('POST_CREATED', { postCreated: post });

      return post;
    },

    updatePost: async (parent, { id, input }, context) => {
      const post = await Post.findById(id);
      
      if (!post) {
        throw new GraphQLError('Post not found', {
          extensions: { code: 'NOT_FOUND' }
        });
      }

      if (post.authorId !== context.user?.id && context.user?.role !== 'ADMIN') {
        throw new GraphQLError('Not authorized', {
          extensions: { code: 'FORBIDDEN' }
        });
      }

      const updatedPost = await Post.findByIdAndUpdate(id, input, { new: true });

      // Publish subscription
      context.pubsub.publish('POST_UPDATED', { 
        postUpdated: updatedPost,
        postId: id 
      });

      return updatedPost;
    },

    likePost: async (parent, { postId }, context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      const post = await Post.findByIdAndUpdate(
        postId,
        { $inc: { likeCount: 1 } },
        { new: true }
      );

      return post;
    },

    addComment: async (parent, { postId, content }, context) => {
      if (!context.user) {
        throw new GraphQLError('Not authenticated', {
          extensions: { code: 'UNAUTHENTICATED' }
        });
      }

      const comment = await Comment.create({
        postId,
        authorId: context.user.id,
        content,
      });

      // Publish subscription
      context.pubsub.publish('COMMENT_ADDED', {
        commentAdded: comment,
        postId,
      });

      return comment;
    },
  },

  Subscription: {
    postCreated: {
      subscribe: (parent, args, context) => {
        return context.pubsub.asyncIterator(['POST_CREATED']);
      },
    },

    postUpdated: {
      subscribe: (parent, { postId }, context) => {
        return context.pubsub.asyncIterator([`POST_UPDATED_${postId}`]);
      },
    },

    commentAdded: {
      subscribe: (parent, { postId }, context) => {
        return context.pubsub.asyncIterator([`COMMENT_ADDED_${postId}`]);
      },
    },
  },

  Post: {
    author: async (parent, args, context) => {
      return context.loaders.userById.load(parent.authorId);
    },

    category: async (parent, args, context) => {
      if (!parent.categoryId) return null;
      return context.loaders.categoryById.load(parent.categoryId);
    },

    tags: async (parent, args, context) => {
      return context.loaders.tagsByIds.loadMany(parent.tagIds || []);
    },

    comments: async (parent, args, context) => {
      return Comment.find({ postId: parent.id }).sort({ createdAt: -1 });
    },
  },
};
```

### resolvers/index.ts

```typescript
import { userResolvers } from './user.resolver';
import { postResolvers } from './post.resolver';
import { GraphQLDateTime, GraphQLJSON } from 'graphql-scalars';

export const resolvers = {
  DateTime: GraphQLDateTime,
  JSON: GraphQLJSON,

  Query: {
    ...userResolvers.Query,
    ...postResolvers.Query,
  },

  Mutation: {
    ...userResolvers.Mutation,
    ...postResolvers.Mutation,
  },

  Subscription: {
    ...postResolvers.Subscription,
  },

  User: userResolvers.User,
  Post: postResolvers.Post,
};
```

---

## 🚀 DataLoader (N+1 Problem Solution)

### dataloaders/user.loader.ts

```typescript
import DataLoader from 'dataloader';
import { User } from '../models/User';

export const createUserLoader = () => {
  return new DataLoader(async (userIds: readonly string[]) => {
    const users = await User.find({ _id: { $in: userIds } });
    
    // Map users to match order of userIds
    const userMap = new Map(users.map(user => [user.id, user]));
    return userIds.map(id => userMap.get(id) || null);
  });
};

export const createPostsByAuthorLoader = () => {
  return new DataLoader(async (authorIds: readonly string[]) => {
    const posts = await Post.find({ authorId: { $in: authorIds } });
    
    // Group posts by authorId
    const postsByAuthor = new Map<string, any[]>();
    posts.forEach(post => {
      const authorPosts = postsByAuthor.get(post.authorId) || [];
      authorPosts.push(post);
      postsByAuthor.set(post.authorId, authorPosts);
    });
    
    return authorIds.map(id => postsByAuthor.get(id) || []);
  });
};
```

---

## 🔐 Context & Authentication

### context.ts

```typescript
import { PubSub } from 'graphql-subscriptions';
import jwt from 'jsonwebtoken';
import { User } from './models/User';
import { createUserLoader, createPostsByAuthorLoader } from './dataloaders';

const pubsub = new PubSub();

export const createContext = async ({ req }) => {
  // Get token from header
  const token = req.headers.authorization?.replace('Bearer ', '');

  let user = null;
  if (token) {
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!);
      user = await User.findById(decoded.userId);
    } catch (error) {
      console.error('Invalid token:', error);
    }
  }

  // Create DataLoaders
  const loaders = {
    userById: createUserLoader(),
    postsByAuthor: createPostsByAuthorLoader(),
    // Add more loaders as needed
  };

  return {
    user,
    loaders,
    pubsub,
  };
};
```

---

## 📡 Subscriptions Setup

### With WebSocket

```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import express from 'express';

const schema = makeExecutableSchema({ typeDefs, resolvers });

const app = express();
const httpServer = createServer(app);

// WebSocket server
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});

await server.start();

app.use('/graphql', cors(), json(), expressMiddleware(server, { context: createContext }));

httpServer.listen(4000, () => {
  console.log('🚀 Server ready at http://localhost:4000/graphql');
});
```

---

## 🎯 Client Usage Examples

### Queries

```typescript
// Simple query
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      username
      email
      posts {
        id
        title
      }
    }
  }
`;

// Query with variables
const result = await client.query({
  query: GET_USER,
  variables: { id: '123' },
});

// List query with pagination
const GET_POSTS = gql`
  query GetPosts($limit: Int, $offset: Int) {
    posts(limit: $limit, offset: $offset) {
      edges {
        node {
          id
          title
          author {
            username
          }
        }
      }
      pageInfo {
        hasNextPage
      }
      totalCount
    }
  }
`;
```

### Mutations

```typescript
// Create mutation
const CREATE_POST = gql`
  mutation CreatePost($input: CreatePostInput!) {
    createPost(input: $input) {
      id
      title
      content
      author {
        username
      }
    }
  }
`;

const result = await client.mutate({
  mutation: CREATE_POST,
  variables: {
    input: {
      title: 'My Post',
      content: 'Post content',
      published: true,
    },
  },
});
```

### Subscriptions

```typescript
const POST_CREATED = gql`
  subscription OnPostCreated {
    postCreated {
      id
      title
      author {
        username
      }
    }
  }
`;

client.subscribe({
  query: POST_CREATED,
}).subscribe({
  next: (data) => console.log('New post:', data),
  error: (error) => console.error('Subscription error:', error),
});
```

---

## ✅ Best Practices

1. **Use DataLoader:** Prevent N+1 query problems
2. **Type Safety:** Use TypeScript or TypeGraphQL
3. **Authentication:** Implement in context
4. **Authorization:** Use directives or check in resolvers
5. **Error Handling:** Use GraphQLError with extensions
6. **Query Complexity:** Limit depth and complexity
7. **Pagination:** Use cursor-based for scalability
8. **Caching:** Implement response caching
9. **Monitoring:** Track query performance
10. **Documentation:** Auto-generated from schema

---

**Ready for:** Production GraphQL APIs  
**Next:** Access GraphQL Playground at http://localhost:4000/graphql
