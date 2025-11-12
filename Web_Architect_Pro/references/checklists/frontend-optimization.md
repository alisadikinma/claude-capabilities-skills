# Frontend Optimization Checklist

**Target:** Achieve Web Vitals thresholds (LCP < 2.5s, FID < 100ms, CLS < 0.1)  
**Last Updated:** 2025-01-11

---

## 🎯 Performance Budget

Set and enforce limits:
- [ ] Bundle size < 200KB (gzipped)
- [ ] First Contentful Paint (FCP) < 1.8s
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] Time to Interactive (TTI) < 3.5s
- [ ] Total Blocking Time (TBT) < 300ms
- [ ] Cumulative Layout Shift (CLS) < 0.1

---

## 📦 Code Splitting & Lazy Loading

### Dynamic Imports
- [ ] Route-based code splitting implemented
- [ ] Heavy components loaded dynamically
- [ ] Third-party libraries loaded on-demand
- [ ] Modal/dialog content lazy loaded

**Example (Next.js):**
```typescript
const HeavyChart = dynamic(() => import('@/components/HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});
```

### React.lazy
- [ ] Non-critical components use React.lazy
- [ ] Suspense boundaries for loading states
- [ ] Error boundaries for lazy load failures

---

## 🖼️ Image Optimization

### Image Loading
- [ ] Use next/image or modern <img> with loading="lazy"
- [ ] Priority images marked with priority prop
- [ ] Appropriate sizes attribute for responsive images
- [ ] WebP/AVIF formats with fallbacks

**Checklist:**
```typescript
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority        // ✅ Above fold
  quality={85}    // ✅ Balance quality/size
  placeholder="blur"
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### Image CDN
- [ ] Images served from CDN
- [ ] Automatic format conversion (WebP/AVIF)
- [ ] On-the-fly resizing enabled
- [ ] Cache headers configured (1 year+)

---

## 🎨 CSS Optimization

### Critical CSS
- [ ] Inline critical CSS in <head>
- [ ] Non-critical CSS loaded asynchronously
- [ ] Unused CSS removed (PurgeCSS/Tailwind)
- [ ] CSS minified in production

### Tailwind Optimization
- [ ] JIT mode enabled
- [ ] Unused classes purged
- [ ] Custom utilities extracted
- [ ] @apply used sparingly

**tailwind.config.ts:**
```typescript
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
  // ✅ Production optimizations
  mode: 'jit',
  purge: {
    enabled: process.env.NODE_ENV === 'production',
  },
};
```

---

## 🚀 JavaScript Optimization

### Bundle Analysis
- [ ] Bundle analyzed (webpack-bundle-analyzer)
- [ ] Tree shaking verified
- [ ] Dead code eliminated
- [ ] Duplicate dependencies removed

### Code Optimization
- [ ] Debounce/throttle event handlers
- [ ] Memoize expensive computations
- [ ] Virtualize long lists (react-window)
- [ ] Web Workers for heavy tasks

**Example - Memoization:**
```typescript
const expensiveCalculation = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price, 0);
}, [items]);
```

**Example - Virtualization:**
```typescript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  )}
</FixedSizeList>
```

---

## 🔄 Data Fetching Optimization

### Caching Strategy
- [ ] Implement stale-while-revalidate (SWR)
- [ ] Cache static data (React Query)
- [ ] Deduplicate requests
- [ ] Prefetch on hover/link visible

**React Query Example:**
```typescript
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  staleTime: 5 * 60 * 1000,     // 5 min
  cacheTime: 10 * 60 * 1000,    // 10 min
  refetchOnWindowFocus: false,
});
```

### API Optimization
- [ ] GraphQL queries optimized (no over-fetching)
- [ ] REST pagination implemented
- [ ] Request batching for multiple calls
- [ ] Compression enabled (Brotli/Gzip)

---

## 🌐 Network Optimization

### Resource Hints
- [ ] dns-prefetch for external domains
- [ ] preconnect for critical origins
- [ ] prefetch for next-page resources
- [ ] preload for critical assets

```html
<head>
  <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://api.example.com" />
  <link rel="preload" as="font" href="/fonts/inter.woff2" crossorigin />
</head>
```

### HTTP/2 & HTTP/3
- [ ] HTTP/2 enabled on server
- [ ] HTTP/3 (QUIC) available if supported
- [ ] Server push for critical resources
- [ ] Multiplexing leveraged

---

## 🗂️ Font Optimization

### Font Loading
- [ ] Use font-display: swap or optional
- [ ] Self-host fonts (avoid external requests)
- [ ] Subset fonts (only needed characters)
- [ ] Preload critical fonts

**Next.js Font Example:**
```typescript
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  preload: true,
});
```

---

## ⚡ Runtime Performance

### React Performance
- [ ] Use React.memo for pure components
- [ ] useCallback for stable function refs
- [ ] useMemo for expensive calculations
- [ ] Avoid inline functions in JSX
- [ ] Key props optimized for lists

**Example:**
```typescript
const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data.name}</div>;
}, (prevProps, nextProps) => {
  return prevProps.data.id === nextProps.data.id;
});
```

### Event Handlers
- [ ] Debounce search inputs
- [ ] Throttle scroll listeners
- [ ] Passive event listeners for scroll/touch
- [ ] Remove event listeners on unmount

---

## 📊 Monitoring & Measurement

### Performance Monitoring
- [ ] Web Vitals tracked (Core Web Vitals)
- [ ] Real User Monitoring (RUM) implemented
- [ ] Error tracking (Sentry/Rollbar)
- [ ] Performance budgets enforced in CI

**Web Vitals Tracking:**
```typescript
import { getCLS, getFID, getLCP } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getLCP(console.log);
```

### Tools Used
- [ ] Lighthouse CI in pipeline
- [ ] Chrome DevTools Performance profiling
- [ ] React DevTools Profiler
- [ ] Bundle analyzer reviewed regularly

---

## 🧹 Build Optimization

### Production Build
- [ ] Minification enabled (Terser/SWC)
- [ ] Source maps disabled in production
- [ ] Environment variables optimized
- [ ] Dead code elimination verified

### Next.js Optimizations
```javascript
// next.config.js
module.exports = {
  reactStrictMode: true,
  swcMinify: true,               // ✅ Use SWC
  compress: true,                // ✅ Gzip compression
  poweredByHeader: false,        // ✅ Remove X-Powered-By
  
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
  },
  
  experimental: {
    optimizeCss: true,           // ✅ Optimize CSS
    optimizePackageImports: ['lucide-react'],
  },
};
```

---

## 🎭 Layout Stability (CLS)

### Prevent Layout Shifts
- [ ] Image dimensions specified (width/height)
- [ ] Font fallbacks configured
- [ ] Skeleton screens for loading states
- [ ] Reserve space for dynamic content
- [ ] Avoid injecting content above existing

**Example:**
```typescript
// ✅ Good - dimensions specified
<img src="/hero.jpg" width={1200} height={600} alt="Hero" />

// ❌ Bad - no dimensions
<img src="/hero.jpg" alt="Hero" />
```

---

## 📱 Mobile Optimization

### Mobile-Specific
- [ ] Touch targets ≥ 48x48px
- [ ] Viewport meta tag configured
- [ ] Tap delay removed (300ms)
- [ ] Horizontal scroll prevented
- [ ] Native input types used

```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```

---

## 🔍 SEO & Accessibility

### SEO Basics
- [ ] Meta tags (title, description) present
- [ ] Open Graph tags for social sharing
- [ ] Structured data (JSON-LD) implemented
- [ ] Sitemap.xml generated
- [ ] robots.txt configured

### Accessibility
- [ ] Semantic HTML used
- [ ] ARIA labels where needed
- [ ] Keyboard navigation working
- [ ] Color contrast ratio ≥ 4.5:1
- [ ] Screen reader tested

---

## ✅ Verification Checklist

Before deployment:
- [ ] Lighthouse score > 90 (all categories)
- [ ] PageSpeed Insights tested (mobile + desktop)
- [ ] WebPageTest analysis complete
- [ ] Bundle size within budget
- [ ] No console errors in production
- [ ] Performance regression tests passing

---

## 📈 Target Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| FID | ≤ 100ms | 100ms - 300ms | > 300ms |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| FCP | ≤ 1.8s | 1.8s - 3.0s | > 3.0s |
| TTI | ≤ 3.5s | 3.5s - 7.3s | > 7.3s |

---

## 🛠️ Quick Wins (High Impact, Low Effort)

1. **Enable Brotli compression** - 20-25% smaller than Gzip
2. **Add loading="lazy" to images** - Defer offscreen images
3. **Implement font-display: swap** - Prevent invisible text
4. **Use React.memo** - Prevent unnecessary re-renders
5. **Enable SWC minifier** - Faster builds, smaller bundles

---

**Last Updated:** 2025-01-11  
**Review Frequency:** Monthly
