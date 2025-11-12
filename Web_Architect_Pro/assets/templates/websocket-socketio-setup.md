# WebSocket & Socket.io Setup - Real-time Communication

**For:** Node.js with Socket.io, WebSocket, Express  
**Coverage:** Real-time messaging, notifications, live updates  
**Tools:** Socket.io 4+, ws, Socket.io Client

---

## 📦 Installation

```bash
# Socket.io (recommended for most cases)
npm install socket.io

# Client (for Node.js clients)
npm install socket.io-client

# Native WebSocket (lightweight alternative)
npm install ws

# TypeScript types
npm install -D @types/socket.io @types/ws
```

---

## 📂 Project Structure

```
backend/
├── src/
│   ├── socket/
│   │   ├── index.ts           # Socket.io server setup
│   │   ├── handlers/
│   │   │   ├── chat.handler.ts
│   │   │   ├── notification.handler.ts
│   │   │   └── game.handler.ts
│   │   ├── middleware/
│   │   │   ├── auth.middleware.ts
│   │   │   └── validate.middleware.ts
│   │   └── events/
│   │       └── events.ts      # Event constants
│   └── server.ts
└── package.json

frontend/
└── src/
    └── services/
        └── socket.service.ts   # Client setup
```

---

## 🔧 Socket.io Server Setup

### socket/index.ts

```typescript
import { Server as HttpServer } from 'http';
import { Server, Socket } from 'socket.io';
import { authenticateSocket } from './middleware/auth.middleware';
import { chatHandler } from './handlers/chat.handler';
import { notificationHandler } from './handlers/notification.handler';

export function setupSocketServer(httpServer: HttpServer) {
  const io = new Server(httpServer, {
    cors: {
      origin: process.env.CLIENT_URL || 'http://localhost:3000',
      credentials: true,
    },
    pingTimeout: 60000,
    pingInterval: 25000,
  });

  // Global middleware
  io.use(authenticateSocket);

  // Connection handler
  io.on('connection', (socket: Socket) => {
    console.log(`✅ User connected: ${socket.id}`);
    console.log(`👤 User ID: ${socket.data.userId}`);

    // Join user's personal room
    socket.join(`user:${socket.data.userId}`);

    // Register handlers
    chatHandler(io, socket);
    notificationHandler(io, socket);

    // Handle disconnection
    socket.on('disconnect', (reason) => {
      console.log(`❌ User disconnected: ${socket.id} - ${reason}`);
    });

    // Error handling
    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });
  });

  return io;
}
```

### server.ts Integration

```typescript
import express from 'express';
import { createServer } from 'http';
import { setupSocketServer } from './socket';

const app = express();
const httpServer = createServer(app);

// Setup Socket.io
const io = setupSocketServer(httpServer);

// Make io accessible in Express routes
app.set('io', io);

// REST routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Send notification via REST endpoint
app.post('/api/notify/:userId', (req, res) => {
  const io = req.app.get('io');
  io.to(`user:${req.params.userId}`).emit('notification', {
    message: 'You have a new notification!',
  });
  res.json({ sent: true });
});

httpServer.listen(4000, () => {
  console.log('🚀 Server running on http://localhost:4000');
});
```

---

## 🔐 Authentication Middleware

### middleware/auth.middleware.ts

```typescript
import { Socket } from 'socket.io';
import jwt from 'jsonwebtoken';

export async function authenticateSocket(socket: Socket, next: Function) {
  try {
    // Get token from handshake
    const token = socket.handshake.auth.token || 
                  socket.handshake.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return next(new Error('Authentication required'));
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;

    // Attach user data to socket
    socket.data.userId = decoded.userId;
    socket.data.username = decoded.username;
    socket.data.role = decoded.role;

    next();
  } catch (error) {
    next(new Error('Invalid token'));
  }
}

// Optional: Check permissions
export function requireRole(role: string) {
  return async (socket: Socket, next: Function) => {
    if (socket.data.role !== role) {
      return next(new Error('Insufficient permissions'));
    }
    next();
  };
}
```

---

## 💬 Chat Handler Example

### handlers/chat.handler.ts

```typescript
import { Server, Socket } from 'socket.io';

interface JoinRoomData {
  roomId: string;
}

interface MessageData {
  roomId: string;
  content: string;
  replyTo?: string;
}

interface TypingData {
  roomId: string;
  isTyping: boolean;
}

export function chatHandler(io: Server, socket: Socket) {
  // Join chat room
  socket.on('chat:join', async (data: JoinRoomData) => {
    const { roomId } = data;

    // Verify user has access to room
    const hasAccess = await verifyRoomAccess(socket.data.userId, roomId);
    if (!hasAccess) {
      socket.emit('chat:error', { message: 'Access denied' });
      return;
    }

    // Join room
    socket.join(`room:${roomId}`);

    // Notify others
    socket.to(`room:${roomId}`).emit('chat:user-joined', {
      userId: socket.data.userId,
      username: socket.data.username,
    });

    // Send room info
    const messages = await getRecentMessages(roomId, 50);
    socket.emit('chat:room-joined', {
      roomId,
      messages,
    });

    console.log(`👤 ${socket.data.username} joined room ${roomId}`);
  });

  // Leave chat room
  socket.on('chat:leave', (data: JoinRoomData) => {
    const { roomId } = data;
    socket.leave(`room:${roomId}`);

    socket.to(`room:${roomId}`).emit('chat:user-left', {
      userId: socket.data.userId,
      username: socket.data.username,
    });
  });

  // Send message
  socket.on('chat:message', async (data: MessageData) => {
    const { roomId, content, replyTo } = data;

    // Validate message
    if (!content || content.trim().length === 0) {
      socket.emit('chat:error', { message: 'Message cannot be empty' });
      return;
    }

    // Save message to database
    const message = await saveMessage({
      roomId,
      userId: socket.data.userId,
      content: content.trim(),
      replyTo,
    });

    // Broadcast to room (including sender)
    io.to(`room:${roomId}`).emit('chat:message', {
      id: message.id,
      roomId,
      userId: socket.data.userId,
      username: socket.data.username,
      content: message.content,
      replyTo: message.replyTo,
      createdAt: message.createdAt,
    });

    console.log(`💬 Message in room ${roomId}: ${content}`);
  });

  // Typing indicator
  socket.on('chat:typing', (data: TypingData) => {
    const { roomId, isTyping } = data;

    socket.to(`room:${roomId}`).emit('chat:typing', {
      userId: socket.data.userId,
      username: socket.data.username,
      isTyping,
    });
  });

  // Mark messages as read
  socket.on('chat:read', async (data: { roomId: string; messageId: string }) => {
    await markMessageAsRead(data.messageId, socket.data.userId);

    socket.to(`room:${data.roomId}`).emit('chat:read', {
      messageId: data.messageId,
      userId: socket.data.userId,
    });
  });

  // Delete message
  socket.on('chat:delete', async (data: { roomId: string; messageId: string }) => {
    const { roomId, messageId } = data;

    // Verify ownership
    const message = await getMessage(messageId);
    if (message.userId !== socket.data.userId && socket.data.role !== 'admin') {
      socket.emit('chat:error', { message: 'Cannot delete this message' });
      return;
    }

    await deleteMessage(messageId);

    io.to(`room:${roomId}`).emit('chat:deleted', { messageId });
  });
}

// Helper functions (implement based on your DB)
async function verifyRoomAccess(userId: string, roomId: string): Promise<boolean> {
  // Check if user is member of room
  return true;
}

async function getRecentMessages(roomId: string, limit: number) {
  // Fetch recent messages from DB
  return [];
}

async function saveMessage(data: any) {
  // Save to database
  return { id: '123', ...data, createdAt: new Date() };
}

async function getMessage(messageId: string) {
  return { id: messageId, userId: 'user1' };
}

async function deleteMessage(messageId: string) {
  // Delete from database
}

async function markMessageAsRead(messageId: string, userId: string) {
  // Update read status
}
```

---

## 🔔 Notification Handler

### handlers/notification.handler.ts

```typescript
import { Server, Socket } from 'socket.io';

export function notificationHandler(io: Server, socket: Socket) {
  // Subscribe to notifications
  socket.on('notifications:subscribe', () => {
    console.log(`🔔 ${socket.data.username} subscribed to notifications`);
  });

  // Mark notification as read
  socket.on('notifications:read', async (data: { notificationId: string }) => {
    await markNotificationAsRead(data.notificationId, socket.data.userId);

    socket.emit('notifications:read-success', {
      notificationId: data.notificationId,
    });
  });

  // Get unread count
  socket.on('notifications:count', async () => {
    const count = await getUnreadNotificationCount(socket.data.userId);

    socket.emit('notifications:count', { count });
  });
}

// Send notification to user (called from other parts of app)
export function sendNotification(io: Server, userId: string, notification: any) {
  io.to(`user:${userId}`).emit('notification', notification);
}

async function markNotificationAsRead(notificationId: string, userId: string) {
  // Update database
}

async function getUnreadNotificationCount(userId: string): Promise<number> {
  // Query database
  return 0;
}
```

---

## 🎮 Advanced: Game/Presence Example

### handlers/game.handler.ts

```typescript
import { Server, Socket } from 'socket.io';

interface GameMove {
  gameId: string;
  move: any;
}

export function gameHandler(io: Server, socket: Socket) {
  // Join game
  socket.on('game:join', async (data: { gameId: string }) => {
    const { gameId } = data;

    socket.join(`game:${gameId}`);

    const game = await getGame(gameId);

    socket.emit('game:state', { game });

    io.to(`game:${gameId}`).emit('game:player-joined', {
      playerId: socket.data.userId,
      username: socket.data.username,
    });
  });

  // Make move
  socket.on('game:move', async (data: GameMove) => {
    const { gameId, move } = data;

    // Validate and process move
    const updatedGame = await processGameMove(gameId, socket.data.userId, move);

    // Broadcast to all players
    io.to(`game:${gameId}`).emit('game:move-made', {
      playerId: socket.data.userId,
      move,
      game: updatedGame,
    });

    // Check for game end
    if (updatedGame.isFinished) {
      io.to(`game:${gameId}`).emit('game:finished', {
        winner: updatedGame.winner,
      });
    }
  });

  // Leave game
  socket.on('game:leave', (data: { gameId: string }) => {
    socket.leave(`game:${data.gameId}`);

    io.to(`game:${data.gameId}`).emit('game:player-left', {
      playerId: socket.data.userId,
    });
  });
}

async function getGame(gameId: string) {
  return { id: gameId, state: {} };
}

async function processGameMove(gameId: string, playerId: string, move: any) {
  // Process move and update game state
  return { id: gameId, isFinished: false };
}
```

---

## 👨‍💻 Client Setup (React/Vue)

### socket.service.ts

```typescript
import { io, Socket } from 'socket.io-client';

class SocketService {
  private socket: Socket | null = null;
  private token: string | null = null;

  connect(token: string) {
    this.token = token;

    this.socket = io(process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:4000', {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    // Connection events
    this.socket.on('connect', () => {
      console.log('✅ Connected to WebSocket');
    });

    this.socket.on('disconnect', (reason) => {
      console.log('❌ Disconnected:', reason);
    });

    this.socket.on('connect_error', (error) => {
      console.error('Connection error:', error.message);
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  // Chat methods
  joinRoom(roomId: string) {
    this.socket?.emit('chat:join', { roomId });
  }

  leaveRoom(roomId: string) {
    this.socket?.emit('chat:leave', { roomId });
  }

  sendMessage(roomId: string, content: string) {
    this.socket?.emit('chat:message', { roomId, content });
  }

  onMessage(callback: (message: any) => void) {
    this.socket?.on('chat:message', callback);
  }

  onTyping(callback: (data: any) => void) {
    this.socket?.on('chat:typing', callback);
  }

  setTyping(roomId: string, isTyping: boolean) {
    this.socket?.emit('chat:typing', { roomId, isTyping });
  }

  // Notification methods
  onNotification(callback: (notification: any) => void) {
    this.socket?.on('notification', callback);
  }

  // Cleanup
  removeAllListeners() {
    this.socket?.removeAllListeners();
  }
}

export const socketService = new SocketService();
```

### React Hook Example

```typescript
// useSocket.ts
import { useEffect, useState } from 'react';
import { socketService } from '../services/socket.service';

export function useSocket(token: string | null) {
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    if (!token) return;

    const socket = socketService.connect(token);

    socket.on('connect', () => setIsConnected(true));
    socket.on('disconnect', () => setIsConnected(false));

    return () => {
      socketService.disconnect();
    };
  }, [token]);

  return { isConnected, socket: socketService };
}

// useChat.ts
import { useEffect, useState } from 'react';
import { socketService } from '../services/socket.service';

export function useChat(roomId: string) {
  const [messages, setMessages] = useState<any[]>([]);

  useEffect(() => {
    // Join room
    socketService.joinRoom(roomId);

    // Listen for new messages
    socketService.onMessage((message) => {
      setMessages((prev) => [...prev, message]);
    });

    // Cleanup
    return () => {
      socketService.leaveRoom(roomId);
      socketService.removeAllListeners();
    };
  }, [roomId]);

  const sendMessage = (content: string) => {
    socketService.sendMessage(roomId, content);
  };

  return { messages, sendMessage };
}
```

### React Component Example

```typescript
function ChatRoom({ roomId }: { roomId: string }) {
  const { messages, sendMessage } = useChat(roomId);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput('');
  };

  const handleTyping = () => {
    if (!isTyping) {
      setIsTyping(true);
      socketService.setTyping(roomId, true);

      setTimeout(() => {
        setIsTyping(false);
        socketService.setTyping(roomId, false);
      }, 2000);
    }
  };

  return (
    <div>
      <div className="messages">
        {messages.map((msg) => (
          <div key={msg.id}>
            <strong>{msg.username}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => {
          setInput(e.target.value);
          handleTyping();
        }}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

---

## 🎯 Rooms & Namespaces

### Rooms (grouping sockets)

```typescript
// Join multiple rooms
socket.join(['room:123', 'room:456', `user:${userId}`]);

// Emit to specific room
io.to('room:123').emit('message', data);

// Emit to multiple rooms
io.to('room:123').to('room:456').emit('message', data);

// Emit to all except sender
socket.to('room:123').emit('message', data);

// Leave room
socket.leave('room:123');

// Get all sockets in room
const sockets = await io.in('room:123').fetchSockets();
```

### Namespaces (separate channels)

```typescript
// Create namespaces
const chatNamespace = io.of('/chat');
const notificationNamespace = io.of('/notifications');

chatNamespace.on('connection', (socket) => {
  console.log('Chat connection');
});

notificationNamespace.on('connection', (socket) => {
  console.log('Notification connection');
});

// Client connects to namespace
const chatSocket = io('http://localhost:4000/chat');
const notificationSocket = io('http://localhost:4000/notifications');
```

---

## 📊 Broadcasting Patterns

```typescript
// To all connected clients
io.emit('announcement', 'Server maintenance in 5 minutes');

// To all except sender
socket.broadcast.emit('user-connected', { userId });

// To specific room
io.to('room:123').emit('message', data);

// To all in room except sender
socket.to('room:123').emit('message', data);

// To specific socket
io.to(socketId).emit('private-message', data);

// Volatile (skip if client disconnected)
socket.volatile.emit('position-update', { x, y });

// With acknowledgment
socket.emit('question', data, (answer) => {
  console.log('Client answered:', answer);
});
```

---

## ✅ Best Practices

1. **Authentication:** Always authenticate sockets
2. **Rate Limiting:** Prevent spam/abuse
3. **Validation:** Validate all incoming data
4. **Error Handling:** Handle errors gracefully
5. **Cleanup:** Remove listeners on disconnect
6. **Rooms:** Use rooms for efficient broadcasting
7. **Heartbeat:** Configure ping/pong intervals
8. **Scalability:** Use Redis adapter for multiple servers
9. **Logging:** Log connections and errors
10. **Testing:** Test reconnection scenarios

---

## 🔧 Redis Adapter (Multiple Servers)

```typescript
import { createAdapter } from '@socket.io/redis-adapter';
import { createClient } from 'redis';

const pubClient = createClient({ url: 'redis://localhost:6379' });
const subClient = pubClient.duplicate();

await Promise.all([pubClient.connect(), subClient.connect()]);

io.adapter(createAdapter(pubClient, subClient));
```

---

**Ready for:** Real-time web applications  
**Next:** Connect client and test real-time features
