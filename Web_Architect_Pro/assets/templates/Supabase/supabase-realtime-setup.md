# Supabase Realtime

Real-time subscriptions for database changes, presence tracking, and broadcast messaging.

## Quick Setup

### 1. Enable Realtime

```sql
-- Enable Realtime for a table
ALTER PUBLICATION supabase_realtime ADD TABLE posts;

-- Enable for specific operations only
ALTER PUBLICATION supabase_realtime ADD TABLE posts 
WITH (PUBLISH='insert,update');
```

## Database Changes (Postgres Changes)

### Subscribe to INSERT

```typescript
import { supabase } from '@/lib/supabase';

// Listen for new posts
const channel = supabase
  .channel('posts-insert')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('New post:', payload.new);
    }
  )
  .subscribe();

// Cleanup
channel.unsubscribe();
```

### Subscribe to UPDATE

```typescript
supabase
  .channel('posts-update')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Updated:', payload.old, '→', payload.new);
    }
  )
  .subscribe();
```

### Subscribe to DELETE

```typescript
supabase
  .channel('posts-delete')
  .on(
    'postgres_changes',
    {
      event: 'DELETE',
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Deleted:', payload.old);
    }
  )
  .subscribe();
```

### Subscribe to All Changes

```typescript
supabase
  .channel('posts-all')
  .on(
    'postgres_changes',
    {
      event: '*', // INSERT, UPDATE, DELETE
      schema: 'public',
      table: 'posts'
    },
    (payload) => {
      console.log('Change:', payload.eventType, payload.new);
    }
  )
  .subscribe();
```

### Filter by Column

```typescript
// Only listen to posts by specific user
supabase
  .channel('user-posts')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'posts',
      filter: 'user_id=eq.123'
    },
    (payload) => {
      console.log('User post changed:', payload);
    }
  )
  .subscribe();
```

## React Integration

### Real-time Posts List

```typescript
'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

interface Post {
  id: string;
  title: string;
  content: string;
  created_at: string;
}

export function RealtimePosts() {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    // Fetch initial posts
    supabase
      .from('posts')
      .select('*')
      .order('created_at', { ascending: false })
      .then(({ data }) => setPosts(data || []));

    // Subscribe to new posts
    const channel = supabase
      .channel('posts-changes')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'posts'
        },
        (payload) => {
          setPosts((current) => [payload.new as Post, ...current]);
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'UPDATE',
          schema: 'public',
          table: 'posts'
        },
        (payload) => {
          setPosts((current) =>
            current.map((post) =>
              post.id === payload.new.id ? (payload.new as Post) : post
            )
          );
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'DELETE',
          schema: 'public',
          table: 'posts'
        },
        (payload) => {
          setPosts((current) =>
            current.filter((post) => post.id !== payload.old.id)
          );
        }
      )
      .subscribe();

    return () => {
      channel.unsubscribe();
    };
  }, []);

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id} className="p-4 border rounded mb-2">
          <h3 className="font-bold">{post.title}</h3>
          <p>{post.content}</p>
        </div>
      ))}
    </div>
  );
}
```

### Custom Hook for Realtime

```typescript
// hooks/useRealtimeTable.ts
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export function useRealtimeTable<T>(
  table: string,
  initialQuery?: any
) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch initial data
    const query = supabase.from(table).select('*');
    
    if (initialQuery) {
      // Apply filters
      Object.entries(initialQuery).forEach(([key, value]) => {
        query.eq(key, value);
      });
    }

    query.then(({ data: initialData }) => {
      setData(initialData as T[] || []);
      setLoading(false);
    });

    // Subscribe to changes
    const channel = supabase
      .channel(`${table}-changes`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setData((current) => [payload.new as T, ...current]);
          } else if (payload.eventType === 'UPDATE') {
            setData((current) =>
              current.map((item: any) =>
                item.id === payload.new.id ? (payload.new as T) : item
              )
            );
          } else if (payload.eventType === 'DELETE') {
            setData((current) =>
              current.filter((item: any) => item.id !== payload.old.id)
            );
          }
        }
      )
      .subscribe();

    return () => {
      channel.unsubscribe();
    };
  }, [table]);

  return { data, loading };
}

// Usage
function MyComponent() {
  const { data: posts, loading } = useRealtimeTable('posts');
  // ...
}
```

## Presence (Track Online Users)

### Track User Presence

```typescript
const channel = supabase.channel('room-1');

// Track current user
await channel.subscribe(async (status) => {
  if (status === 'SUBSCRIBED') {
    const user = await supabase.auth.getUser();
    
    await channel.track({
      user_id: user.data.user?.id,
      username: user.data.user?.email,
      online_at: new Date().toISOString()
    });
  }
});

// Listen to presence changes
channel.on('presence', { event: 'sync' }, () => {
  const state = channel.presenceState();
  console.log('Online users:', state);
});

channel.on('presence', { event: 'join' }, ({ key, newPresences }) => {
  console.log('User joined:', newPresences);
});

channel.on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
  console.log('User left:', leftPresences);
});
```

### Online Users Component

```typescript
'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

interface OnlineUser {
  user_id: string;
  username: string;
  online_at: string;
}

export function OnlineUsers({ roomId }: { roomId: string }) {
  const [users, setUsers] = useState<OnlineUser[]>([]);

  useEffect(() => {
    const channel = supabase.channel(roomId);

    channel.subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        const user = await supabase.auth.getUser();
        
        await channel.track({
          user_id: user.data.user?.id,
          username: user.data.user?.email,
          online_at: new Date().toISOString()
        });
      }
    });

    channel.on('presence', { event: 'sync' }, () => {
      const state = channel.presenceState<OnlineUser>();
      const onlineUsers = Object.values(state).flat();
      setUsers(onlineUsers);
    });

    return () => {
      channel.unsubscribe();
    };
  }, [roomId]);

  return (
    <div>
      <h3>Online Users ({users.length})</h3>
      <ul>
        {users.map((user) => (
          <li key={user.user_id}>{user.username}</li>
        ))}
      </ul>
    </div>
  );
}
```

## Broadcast (Send Messages)

### Send & Receive Messages

```typescript
const channel = supabase.channel('chat-room');

// Listen to messages
channel
  .on('broadcast', { event: 'message' }, (payload) => {
    console.log('Received:', payload);
  })
  .subscribe();

// Send message
await channel.send({
  type: 'broadcast',
  event: 'message',
  payload: { text: 'Hello everyone!' }
});
```

### Chat Component

```typescript
'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

interface Message {
  id: string;
  user_id: string;
  username: string;
  text: string;
  created_at: string;
}

export function Chat({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [channel, setChannel] = useState<any>(null);

  useEffect(() => {
    const newChannel = supabase.channel(roomId);

    newChannel
      .on('broadcast', { event: 'message' }, (payload) => {
        setMessages((current) => [...current, payload.payload as Message]);
      })
      .subscribe();

    setChannel(newChannel);

    return () => {
      newChannel.unsubscribe();
    };
  }, [roomId]);

  async function sendMessage() {
    if (!input.trim() || !channel) return;

    const user = await supabase.auth.getUser();
    
    const message: Message = {
      id: crypto.randomUUID(),
      user_id: user.data.user?.id || '',
      username: user.data.user?.email || 'Anonymous',
      text: input,
      created_at: new Date().toISOString()
    };

    await channel.send({
      type: 'broadcast',
      event: 'message',
      payload: message
    });

    setInput('');
  }

  return (
    <div className="flex flex-col h-96 border rounded-lg">
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg) => (
          <div key={msg.id} className="bg-gray-100 p-2 rounded">
            <div className="font-bold text-sm">{msg.username}</div>
            <div>{msg.text}</div>
          </div>
        ))}
      </div>
      <div className="flex gap-2 p-4 border-t">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          className="flex-1 px-3 py-2 border rounded"
        />
        <button
          onClick={sendMessage}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Send
        </button>
      </div>
    </div>
  );
}
```

## Typing Indicators

```typescript
'use client';

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

export function TypingIndicator({ roomId }: { roomId: string }) {
  const [typing, setTyping] = useState<string[]>([]);
  const [channel, setChannel] = useState<any>(null);

  useEffect(() => {
    const newChannel = supabase.channel(roomId);

    newChannel
      .on('broadcast', { event: 'typing' }, (payload) => {
        const { username, isTyping } = payload.payload;
        
        setTyping((current) =>
          isTyping
            ? [...current, username]
            : current.filter((u) => u !== username)
        );
      })
      .subscribe();

    setChannel(newChannel);

    return () => {
      newChannel.unsubscribe();
    };
  }, [roomId]);

  async function handleTyping(isTyping: boolean) {
    if (!channel) return;

    const user = await supabase.auth.getUser();
    
    await channel.send({
      type: 'broadcast',
      event: 'typing',
      payload: {
        username: user.data.user?.email,
        isTyping
      }
    });
  }

  return (
    <div>
      {typing.length > 0 && (
        <div className="text-sm text-gray-500">
          {typing.join(', ')} {typing.length === 1 ? 'is' : 'are'} typing...
        </div>
      )}
    </div>
  );
}
```

## Best Practices

### Performance
- ✅ Unsubscribe from channels when component unmounts
- ✅ Use specific event filters to reduce message volume
- ✅ Batch state updates when handling multiple changes
- ✅ Use presence for user tracking instead of database queries

### Security
- ✅ Enable RLS on tables with Realtime enabled
- ✅ Filter broadcasts based on user permissions
- ✅ Validate payload data before processing
- ✅ Use authenticated channels for sensitive data

### Architecture
- ✅ Use Postgres Changes for database sync
- ✅ Use Broadcast for ephemeral messaging
- ✅ Use Presence for online status tracking
- ✅ Consider message persistence in database for chat history

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-12
