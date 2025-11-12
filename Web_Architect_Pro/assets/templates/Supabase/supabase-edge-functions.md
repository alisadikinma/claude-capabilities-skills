# Supabase Edge Functions

Serverless functions running on Deno runtime at the edge for low-latency execution.

## Quick Setup

### 1. Install Supabase CLI

```bash
npm install -g supabase
```

### 2. Initialize Project

```bash
supabase init
supabase login
```

### 3. Create Function

```bash
supabase functions new my-function
```

## Basic Edge Function

### Hello World

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

serve(async (req) => {
  return new Response(
    JSON.stringify({ message: 'Hello from Edge Functions!' }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

### Deploy Function

```bash
supabase functions deploy hello-world
```

### Invoke Function

```typescript
// From client
const { data, error } = await supabase.functions.invoke('hello-world');
console.log(data); // { message: 'Hello from Edge Functions!' }
```

## Authentication in Edge Functions

### Get Authenticated User

```typescript
// supabase/functions/protected/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  // Get JWT from Authorization header
  const authHeader = req.headers.get('Authorization');
  if (!authHeader) {
    return new Response('Unauthorized', { status: 401 });
  }

  // Create Supabase client
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    {
      global: {
        headers: { Authorization: authHeader }
      }
    }
  );

  // Get user
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error || !user) {
    return new Response('Unauthorized', { status: 401 });
  }

  return new Response(
    JSON.stringify({ message: `Hello ${user.email}!` }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

## Database Operations

### Query Database

```typescript
// supabase/functions/get-posts/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  );

  const { data, error } = await supabase
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(10);

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(JSON.stringify({ posts: data }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
```

### Insert Data

```typescript
// supabase/functions/create-post/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const { title, content } = await req.json();

  const authHeader = req.headers.get('Authorization');
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    { global: { headers: { Authorization: authHeader ?? '' } } }
  );

  // Get user
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return new Response('Unauthorized', { status: 401 });
  }

  // Insert post
  const { data, error } = await supabase
    .from('posts')
    .insert({ title, content, user_id: user.id })
    .select()
    .single();

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(JSON.stringify({ post: data }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
```

## Third-Party API Integration

### OpenAI Integration

```typescript
// supabase/functions/ai-completion/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

serve(async (req) => {
  const { prompt } = await req.json();

  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'gpt-4-turbo-preview',
      messages: [{ role: 'user', content: prompt }]
    })
  });

  const data = await response.json();
  const answer = data.choices[0].message.content;

  return new Response(JSON.stringify({ answer }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
```

### Stripe Payment

```typescript
// supabase/functions/create-payment/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import Stripe from 'https://esm.sh/stripe@14.5.0';

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') ?? '', {
  apiVersion: '2023-10-16'
});

serve(async (req) => {
  const { amount, currency = 'usd' } = await req.json();

  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount,
      currency,
      automatic_payment_methods: { enabled: true }
    });

    return new Response(
      JSON.stringify({ clientSecret: paymentIntent.client_secret }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});
```

## CORS Handling

```typescript
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    // Your function logic here
    const data = { message: 'Success' };

    return new Response(JSON.stringify(data), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }
});
```

## Scheduled Functions (Cron)

### Setup Cron Job

```typescript
// supabase/functions/daily-cleanup/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  // Verify cron secret
  const cronSecret = req.headers.get('x-cron-secret');
  if (cronSecret !== Deno.env.get('CRON_SECRET')) {
    return new Response('Unauthorized', { status: 401 });
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  );

  // Delete old records (older than 30 days)
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

  const { data, error } = await supabase
    .from('logs')
    .delete()
    .lt('created_at', thirtyDaysAgo.toISOString());

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response(
    JSON.stringify({ message: 'Cleanup completed', deleted: data?.length }),
    { headers: { 'Content-Type': 'application/json' } }
  );
});
```

### Schedule with Platform Cron

```yaml
# In Supabase Dashboard > Edge Functions > Settings
# Add cron schedule:
# 0 0 * * * (daily at midnight)
```

## Client-Side Invocation

### Basic Invoke

```typescript
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { name: 'John' }
});
```

### With Headers

```typescript
const { data, error } = await supabase.functions.invoke('my-function', {
  headers: {
    'custom-header': 'value'
  },
  body: { data: 'value' }
});
```

### Handle Response

```typescript
const { data, error } = await supabase.functions.invoke('my-function');

if (error) {
  console.error('Function error:', error);
  return;
}

console.log('Function response:', data);
```

## Local Development

### Run Locally

```bash
# Start local Supabase
supabase start

# Serve function locally
supabase functions serve my-function

# Or serve all functions
supabase functions serve
```

### Test Locally

```bash
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/my-function' \
  --header 'Authorization: Bearer YOUR_ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"name":"John"}'
```

## Environment Variables

### Set Secrets

```bash
# Set secret
supabase secrets set MY_SECRET=value

# Set multiple
supabase secrets set API_KEY=key STRIPE_KEY=sk_test_...

# List secrets
supabase secrets list
```

### Access in Function

```typescript
const apiKey = Deno.env.get('API_KEY');
const stripeKey = Deno.env.get('STRIPE_KEY');
```

## Best Practices

### Performance
- ✅ Keep functions focused (single responsibility)
- ✅ Use streaming for large responses
- ✅ Cache external API calls when possible
- ✅ Minimize cold start time (avoid heavy imports)

### Security
- ✅ Always validate user authentication
- ✅ Use service role key only when necessary
- ✅ Validate input data
- ✅ Handle errors gracefully
- ✅ Use secrets for API keys

### Development
- ✅ Test locally before deploying
- ✅ Use TypeScript for better DX
- ✅ Implement proper CORS handling
- ✅ Log errors for debugging
- ✅ Version your functions

### Monitoring
- ✅ Check function logs in Dashboard
- ✅ Monitor execution time
- ✅ Track error rates
- ✅ Set up alerts for failures

---

**Version:** 1.0.0  
**Last Updated:** 2025-01-12
