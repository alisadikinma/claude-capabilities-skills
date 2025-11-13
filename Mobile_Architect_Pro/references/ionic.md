# Ionic & Capacitor Development Guide

Comprehensive reference for production Ionic applications with Angular, React, or Vue, using Capacitor for native functionality.

---

## Table of Contents

1. [Framework Overview](#framework-overview)
2. [Project Setup](#project-setup)
3. [Capacitor Integration](#capacitor-integration)
4. [Angular Implementation](#angular-implementation)
5. [React Implementation](#react-implementation)
6. [Vue Implementation](#vue-implementation)
7. [Native Plugins](#native-plugins)
8. [PWA Features](#pwa-features)
9. [Performance](#performance)
10. [Build & Deployment](#build--deployment)

---

## Framework Overview

### Ionic Variants

| Variant | Framework | Best For |
|---------|-----------|----------|
| **Ionic Angular** | Angular | Enterprise apps, complex logic |
| **Ionic React** | React | Fast development, React ecosystem |
| **Ionic Vue** | Vue 3 | Vue developers, lightweight |

### Capacitor vs Cordova

| Feature | Capacitor | Cordova |
|---------|-----------|---------|
| **Maintenance** | Active | Legacy |
| **Native IDE** | Required | Optional |
| **Web API** | Modern | Legacy |
| **Plugin Ecosystem** | Growing | Mature |
| **PWA Support** | Built-in | Plugin-based |

**Recommendation:** Use Capacitor for new projects.

---

## Project Setup

### Ionic Angular

```bash
# Install CLI
npm install -g @ionic/cli

# Create project
ionic start myApp tabs --type=angular --capacitor

# Add platforms
ionic cap add android
ionic cap add ios

# Run
ionic serve                 # Web
ionic cap run android       # Android
ionic cap open ios          # iOS (Xcode)
```

### Ionic React

```bash
ionic start myApp tabs --type=react --capacitor
cd myApp
ionic serve
```

### Ionic Vue

```bash
ionic start myApp tabs --type=vue --capacitor
cd myApp
ionic serve
```

### Essential Packages

```json
{
  "dependencies": {
    "@ionic/angular": "^7.6.0",
    "@ionic/react": "^7.6.0",
    "@ionic/vue": "^7.6.0",
    
    "@capacitor/core": "^5.6.0",
    "@capacitor/android": "^5.6.0",
    "@capacitor/ios": "^5.6.0",
    
    // Plugins
    "@capacitor/camera": "^5.0.9",
    "@capacitor/geolocation": "^5.0.7",
    "@capacitor/storage": "^1.2.5",
    "@capacitor/network": "^5.0.7",
    "@capacitor/app": "^5.0.7",
    
    // HTTP
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.14.2",
    
    // State (React)
    "zustand": "^4.4.7",
    
    // State (Angular)
    "@ngrx/store": "^17.0.1",
    "@ngrx/effects": "^17.0.1",
    
    // State (Vue)
    "pinia": "^2.1.7"
  }
}
```

---

## Capacitor Integration

### Configuration (capacitor.config.ts)

```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.mycompany.myapp',
  appName: 'MyApp',
  webDir: 'dist',
  bundledWebRuntime: false,
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: "#ffffff",
      showSpinner: false
    },
    Camera: {
      saveToGallery: true
    }
  }
};

export default config;
```

### Sync Native Projects

```bash
# Build web assets
ionic build

# Copy web assets to native projects
ionic cap sync

# Update native dependencies
ionic cap sync android
ionic cap sync ios

# Open in native IDE
ionic cap open android
ionic cap open ios
```

---

## Angular Implementation

### Project Structure

```
src/
├── app/
│   ├── core/
│   │   ├── services/
│   │   ├── guards/
│   │   └── interceptors/
│   ├── shared/
│   │   ├── components/
│   │   ├── directives/
│   │   └── pipes/
│   ├── pages/
│   │   ├── home/
│   │   ├── products/
│   │   └── profile/
│   ├── app-routing.module.ts
│   └── app.component.ts
├── assets/
└── theme/
```

### Service Example

```typescript
// services/product.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Product {
  id: string;
  name: string;
  price: number;
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'https://api.example.com/products';
  
  constructor(private http: HttpClient) {}
  
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }
  
  getProduct(id: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/${id}`);
  }
  
  createProduct(product: Product): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, product);
  }
}
```

### Component Example

```typescript
// pages/products/products.page.ts
import { Component, OnInit } from '@angular/core';
import { ProductService, Product } from '../../services/product.service';

@Component({
  selector: 'app-products',
  templateUrl: './products.page.html',
  styleUrls: ['./products.page.scss']
})
export class ProductsPage implements OnInit {
  products: Product[] = [];
  loading = false;
  
  constructor(private productService: ProductService) {}
  
  ngOnInit() {
    this.loadProducts();
  }
  
  loadProducts() {
    this.loading = true;
    this.productService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.loading = false;
      },
      error: (error) => {
        console.error(error);
        this.loading = false;
      }
    });
  }
  
  doRefresh(event: any) {
    this.productService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        event.target.complete();
      },
      error: () => event.target.complete()
    });
  }
}
```

### Template Example

```html
<!-- products.page.html -->
<ion-header>
  <ion-toolbar>
    <ion-title>Products</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content>
  <ion-refresher slot="fixed" (ionRefresh)="doRefresh($event)">
    <ion-refresher-content></ion-refresher-content>
  </ion-refresher>
  
  <ion-list *ngIf="!loading">
    <ion-item *ngFor="let product of products" [routerLink]="['/products', product.id]">
      <ion-label>
        <h2>{{ product.name }}</h2>
        <p>${{ product.price }}</p>
      </ion-label>
    </ion-item>
  </ion-list>
  
  <div *ngIf="loading" class="loading-container">
    <ion-spinner></ion-spinner>
  </div>
</ion-content>
```

---

## React Implementation

### Project Structure

```
src/
├── components/
│   ├── ProductCard.tsx
│   └── LoadingSpinner.tsx
├── pages/
│   ├── Home.tsx
│   ├── Products.tsx
│   └── ProductDetail.tsx
├── hooks/
│   ├── useProducts.ts
│   └── useAuth.ts
├── services/
│   └── api.ts
├── store/
│   └── useStore.ts
├── App.tsx
└── index.tsx
```

### API Service

```typescript
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 5000,
});

export interface Product {
  id: string;
  name: string;
  price: number;
}

export const productApi = {
  getProducts: () => api.get<Product[]>('/products'),
  getProduct: (id: string) => api.get<Product>(`/products/${id}`),
  createProduct: (product: Partial<Product>) => 
    api.post<Product>('/products', product),
};
```

### Custom Hook with React Query

```typescript
// hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { productApi, Product } from '../services/api';

export const useProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const { data } = await productApi.getProducts();
      return data;
    },
  });
};

export const useProduct = (id: string) => {
  return useQuery({
    queryKey: ['products', id],
    queryFn: async () => {
      const { data } = await productApi.getProduct(id);
      return data;
    },
  });
};

export const useCreateProduct = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (product: Partial<Product>) => 
      productApi.createProduct(product),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
};
```

### Page Component

```typescript
// pages/Products.tsx
import React from 'react';
import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonList,
  IonItem,
  IonLabel,
  IonRefresher,
  IonRefresherContent,
  IonSpinner,
} from '@ionic/react';
import { useProducts } from '../hooks/useProducts';
import { RefresherEventDetail } from '@ionic/core';

const Products: React.FC = () => {
  const { data: products, isLoading, refetch } = useProducts();
  
  const handleRefresh = (event: CustomEvent<RefresherEventDetail>) => {
    refetch().then(() => {
      event.detail.complete();
    });
  };
  
  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Products</IonTitle>
        </IonToolbar>
      </IonHeader>
      
      <IonContent fullscreen>
        <IonRefresher slot="fixed" onIonRefresh={handleRefresh}>
          <IonRefresherContent />
        </IonRefresher>
        
        {isLoading ? (
          <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
            <IonSpinner />
          </div>
        ) : (
          <IonList>
            {products?.map((product) => (
              <IonItem key={product.id} routerLink={`/products/${product.id}`}>
                <IonLabel>
                  <h2>{product.name}</h2>
                  <p>${product.price}</p>
                </IonLabel>
              </IonItem>
            ))}
          </IonList>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Products;
```

---

## Vue Implementation

### Project Structure

```
src/
├── components/
│   ├── ProductCard.vue
│   └── LoadingSpinner.vue
├── views/
│   ├── Home.vue
│   ├── Products.vue
│   └── ProductDetail.vue
├── composables/
│   └── useProducts.ts
├── services/
│   └── api.ts
├── stores/
│   └── products.ts
├── App.vue
└── main.ts
```

### Pinia Store

```typescript
// stores/products.ts
import { defineStore } from 'pinia';
import axios from 'axios';

export interface Product {
  id: string;
  name: string;
  price: number;
}

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [] as Product[],
    loading: false,
    error: null as string | null,
  }),
  
  actions: {
    async fetchProducts() {
      this.loading = true;
      this.error = null;
      try {
        const { data } = await axios.get<Product[]>('https://api.example.com/products');
        this.products = data;
      } catch (error: any) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    },
    
    async createProduct(product: Partial<Product>) {
      const { data } = await axios.post<Product>('https://api.example.com/products', product);
      this.products.push(data);
    },
  },
});
```

### Component

```vue
<!-- views/Products.vue -->
<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Products</ion-title>
      </ion-toolbar>
    </ion-header>
    
    <ion-content>
      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content></ion-refresher-content>
      </ion-refresher>
      
      <div v-if="store.loading" class="loading-container">
        <ion-spinner></ion-spinner>
      </div>
      
      <ion-list v-else>
        <ion-item 
          v-for="product in store.products" 
          :key="product.id"
          :router-link="`/products/${product.id}`">
          <ion-label>
            <h2>{{ product.name }}</h2>
            <p>${{ product.price }}</p>
          </ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonLabel,
  IonRefresher,
  IonRefresherContent,
  IonSpinner,
} from '@ionic/vue';
import { useProductStore } from '@/stores/products';

const store = useProductStore();

onMounted(() => {
  store.fetchProducts();
});

const handleRefresh = (event: CustomEvent) => {
  store.fetchProducts().then(() => {
    event.target.complete();
  });
};
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>
```

---

## Native Plugins

### Camera Plugin

```typescript
import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';

const takePicture = async () => {
  try {
    const image = await Camera.getPhoto({
      quality: 90,
      allowEditing: false,
      resultType: CameraResultType.Uri,
      source: CameraSource.Camera,
    });
    
    const imageUrl = image.webPath;
    // Use imageUrl
  } catch (error) {
    console.error('Camera error:', error);
  }
};
```

### Geolocation Plugin

```typescript
import { Geolocation } from '@capacitor/geolocation';

const getCurrentPosition = async () => {
  try {
    const coordinates = await Geolocation.getCurrentPosition();
    const { latitude, longitude } = coordinates.coords;
    console.log('Position:', latitude, longitude);
  } catch (error) {
    console.error('Geolocation error:', error);
  }
};
```

### Storage Plugin (Preferences)

```typescript
import { Preferences } from '@capacitor/preferences';

// Set
await Preferences.set({ key: 'username', value: 'john' });

// Get
const { value } = await Preferences.get({ key: 'username' });

// Remove
await Preferences.remove({ key: 'username' });

// Clear all
await Preferences.clear();
```

### Network Plugin

```typescript
import { Network } from '@capacitor/network';

const checkNetwork = async () => {
  const status = await Network.getStatus();
  console.log('Network status:', status.connected);
};

// Listen to network changes
Network.addListener('networkStatusChange', status => {
  console.log('Network changed:', status.connected);
});
```

---

## PWA Features

### Service Worker

```typescript
// service-worker.js (generated by framework)
// Configure in angular.json, vite.config.ts, or vue.config.js

// Angular: @angular/service-worker
// React: workbox (via Vite PWA plugin)
// Vue: @vueuse/pwa
```

### Manifest Configuration

```json
{
  "name": "My Ionic App",
  "short_name": "MyApp",
  "description": "My awesome Ionic app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3880ff",
  "icons": [
    {
      "src": "assets/icon/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png"
    },
    {
      "src": "assets/icon/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

---

## Performance

### Best Practices

```typescript
// 1. Virtual Scrolling
<ion-content>
  <ion-virtual-scroll [items]="items" approxItemHeight="50px">
    <ion-item *virtualItem="let item">
      {{ item.name }}
    </ion-item>
  </ion-virtual-scroll>
</ion-content>

// 2. Lazy Loading Routes
// Angular
const routes: Routes = [
  {
    path: 'products',
    loadChildren: () => import('./pages/products/products.module')
      .then(m => m.ProductsPageModule)
  }
];

// React
const Products = lazy(() => import('./pages/Products'));

// 3. Image Optimization
<ion-img [src]="imageUrl" loading="lazy"></ion-img>

// 4. Infinite Scroll
<ion-infinite-scroll (ionInfinite)="loadMore($event)">
  <ion-infinite-scroll-content></ion-infinite-scroll-content>
</ion-infinite-scroll>
```

---

## Build & Deployment

### Build Commands

```bash
# Development build
ionic build

# Production build
ionic build --prod

# Sync to native projects
ionic cap sync

# Build native apps
ionic cap build android
ionic cap build ios
```

### Android Release

```bash
# Generate signed APK/AAB
cd android
./gradlew assembleRelease
./gradlew bundleRelease
```

### iOS Release

```bash
# Open in Xcode
ionic cap open ios

# Archive via Xcode
# Product > Archive > Upload to App Store Connect
```

### PWA Deployment

```bash
# Build for web
ionic build --prod

# Deploy dist/ folder to:
# - Netlify
# - Vercel
# - Firebase Hosting
# - Any static host
```

---

## Common Issues

### Capacitor Sync Errors

```bash
# Clean and reinstall
rm -rf node_modules
npm install
ionic cap sync
```

### Plugin Not Working

```typescript
// Check platform
import { Capacitor } from '@capacitor/core';

if (Capacitor.isNativePlatform()) {
  // Use native plugin
} else {
  // Use web fallback
}
```

### Build Failures

```bash
# Clean native builds
cd android && ./gradlew clean && cd ..
cd ios && rm -rf Pods && pod install && cd ..

# Rebuild
ionic build
ionic cap sync
```

---

**See Also:**
- Main SKILL.md for architecture patterns
- `assets/templates/Ionic/` for project templates
- Ionic documentation: https://ionicframework.com/docs
- Capacitor documentation: https://capacitorjs.com/docs

**Last Updated:** January 2025
