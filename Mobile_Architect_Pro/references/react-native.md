# React Native Development Guide

Comprehensive reference for production React Native applications with JavaScript/TypeScript, state management, and native modules.

---

## Table of Contents

1. [Setup & Configuration](#setup--configuration)
2. [TypeScript Integration](#typescript-integration)
3. [Component Architecture](#component-architecture)
4. [State Management](#state-management)
5. [Navigation](#navigation)
6. [Styling](#styling)
7. [Native Modules](#native-modules)
8. [Performance Optimization](#performance-optimization)
9. [Testing](#testing)
10. [Build & Deployment](#build--deployment)

---

## Setup & Configuration

### Project Initialization

```bash
# React Native CLI
npx react-native init MyApp

# With TypeScript
npx react-native init MyApp --template react-native-template-typescript

# Expo (managed workflow)
npx create-expo-app MyApp
```

### Essential Packages

```json
{
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.73.0",
    
    // State Management
    "@reduxjs/toolkit": "^2.0.1",
    "react-redux": "^9.0.4",
    "zustand": "^4.4.7",
    
    // Navigation
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/native-stack": "^6.9.17",
    "@react-navigation/bottom-tabs": "^6.5.11",
    
    // HTTP
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.14.2",
    
    // Storage
    "@react-native-async-storage/async-storage": "^1.21.0",
    "react-native-mmkv": "^2.11.0",
    
    // UI Libraries
    "react-native-paper": "^5.11.3",
    "react-native-elements": "^3.4.3",
    
    // Utilities
    "date-fns": "^3.0.6",
    "react-hook-form": "^7.49.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.45",
    "@types/react-native": "^0.72.8",
    "@testing-library/react-native": "^12.4.2",
    "jest": "^29.7.0",
    "detox": "^20.14.8"
  }
}
```

---

## TypeScript Integration

### Configuration (tsconfig.json)

```json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "commonjs",
    "lib": ["es2017"],
    "jsx": "react-native",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@components/*": ["components/*"],
      "@screens/*": ["screens/*"],
      "@utils/*": ["utils/*"]
    }
  },
  "exclude": ["node_modules"]
}
```

### Type Definitions

```typescript
// src/types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

export interface Product {
  id: string;
  name: string;
  price: number;
  description: string;
}

// Navigation types
export type RootStackParamList = {
  Home: undefined;
  Details: { id: string };
  Profile: { userId: string };
};

// API Response types
export interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
}
```

---

## Component Architecture

### Functional Components with Hooks

```typescript
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

interface ProductListProps {
  category: string;
  onProductPress: (id: string) => void;
}

export const ProductList: React.FC<ProductListProps> = ({ 
  category, 
  onProductPress 
}) => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  
  // Fetch products
  useEffect(() => {
    fetchProducts();
  }, [category]);
  
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const response = await api.getProducts(category);
      setProducts(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };
  
  // Memoized callback
  const handlePress = useCallback((id: string) => {
    onProductPress(id);
  }, [onProductPress]);
  
  // Memoized expensive computation
  const totalPrice = useMemo(() => {
    return products.reduce((sum, p) => sum + p.price, 0);
  }, [products]);
  
  const renderItem = useCallback(({ item }: { item: Product }) => (
    <ProductItem 
      product={item} 
      onPress={handlePress}
    />
  ), [handlePress]);
  
  if (loading) {
    return <ActivityIndicator size="large" />;
  }
  
  return (
    <View style={styles.container}>
      <Text style={styles.total}>Total: ${totalPrice}</Text>
      <FlatList
        data={products}
        renderItem={renderItem}
        keyExtractor={item => item.id}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  total: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
  },
});
```

### Optimization with React.memo

```typescript
interface ProductItemProps {
  product: Product;
  onPress: (id: string) => void;
}

export const ProductItem = React.memo<ProductItemProps>(({ product, onPress }) => {
  return (
    <TouchableOpacity 
      onPress={() => onPress(product.id)}
      style={styles.item}
    >
      <Text style={styles.name}>{product.name}</Text>
      <Text style={styles.price}>${product.price}</Text>
    </TouchableOpacity>
  );
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.product.id === nextProps.product.id &&
         prevProps.product.price === nextProps.product.price;
});
```

---

## State Management

### Redux Toolkit (Recommended)

```typescript
// store/slices/authSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  loading: false,
  error: null,
};

export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { email: string; password: string }) => {
    const response = await api.login(credentials);
    return response.data;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Login failed';
      });
  },
});

export const { logout, setUser } = authSlice.actions;
export default authSlice.reducer;

// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    // other reducers
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Usage in component
import { useSelector, useDispatch } from 'react-redux';
import { login } from './store/slices/authSlice';

const LoginScreen = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user, loading } = useSelector((state: RootState) => state.auth);
  
  const handleLogin = () => {
    dispatch(login({ email: 'user@example.com', password: 'password' }));
  };
  
  return (
    <View>
      <Button title="Login" onPress={handleLogin} />
      {loading && <ActivityIndicator />}
    </View>
  );
};
```

### Zustand (Lightweight Alternative)

```typescript
import create from 'zustand';

interface AuthStore {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  
  login: async (email, password) => {
    const response = await api.login({ email, password });
    set({ user: response.data.user, token: response.data.token });
  },
  
  logout: () => set({ user: null, token: null }),
}));

// Usage
const LoginScreen = () => {
  const { login, user } = useAuthStore();
  
  const handleLogin = async () => {
    await login('user@example.com', 'password');
  };
  
  return <Button title="Login" onPress={handleLogin} />;
};
```

---

## Navigation

### React Navigation (Stack + Tabs)

```typescript
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();

const HomeTabs = () => (
  <Tab.Navigator>
    <Tab.Screen name="Feed" component={FeedScreen} />
    <Tab.Screen name="Search" component={SearchScreen} />
    <Tab.Screen name="Profile" component={ProfileScreen} />
  </Tab.Navigator>
);

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen 
          name="Home" 
          component={HomeTabs}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Details" 
          component={DetailsScreen}
          options={{ title: 'Product Details' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

// Navigation in components
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';

type DetailsScreenNavigationProp = NativeStackNavigationProp<
  RootStackParamList,
  'Details'
>;

const HomeScreen = () => {
  const navigation = useNavigation<DetailsScreenNavigationProp>();
  
  return (
    <Button 
      title="Go to Details"
      onPress={() => navigation.navigate('Details', { id: '123' })}
    />
  );
};
```

---

## Styling

### StyleSheet API

```typescript
import { StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    paddingHorizontal: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333333',
    marginBottom: 12,
  },
  card: {
    backgroundColor: '#f5f5f5',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    // Shadow for iOS
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    // Elevation for Android
    elevation: 3,
  },
  responsiveWidth: {
    width: width * 0.9, // 90% of screen width
  },
});
```

### Styled Components

```typescript
import styled from 'styled-components/native';

export const Container = styled.View`
  flex: 1;
  background-color: #ffffff;
  padding: 16px;
`;

export const Title = styled.Text`
  font-size: 24px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 12px;
`;

export const Card = styled.View`
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
`;

// Usage
const HomeScreen = () => (
  <Container>
    <Title>Welcome</Title>
    <Card>
      <Text>Card content</Text>
    </Card>
  </Container>
);
```

---

## Native Modules

### Creating Native Module (Kotlin/Java)

```kotlin
// android/app/src/main/java/com/myapp/BatteryModule.kt
package com.myapp

import android.content.Context
import android.os.BatteryManager
import com.facebook.react.bridge.*

class BatteryModule(reactContext: ReactApplicationContext) : 
    ReactContextBaseJavaModule(reactContext) {
    
    override fun getName() = "BatteryModule"
    
    @ReactMethod
    fun getBatteryLevel(promise: Promise) {
        try {
            val batteryManager = reactApplicationContext
                .getSystemService(Context.BATTERY_SERVICE) as BatteryManager
            val level = batteryManager
                .getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
            promise.resolve(level)
        } catch (e: Exception) {
            promise.reject("ERROR", e.message)
        }
    }
    
    @ReactMethod
    fun showToast(message: String) {
        Toast.makeText(reactApplicationContext, message, Toast.LENGTH_SHORT).show()
    }
}

// Register module
class BatteryPackage : ReactPackage {
    override fun createNativeModules(reactContext: ReactApplicationContext): 
        List<NativeModule> {
        return listOf(BatteryModule(reactContext))
    }
    
    override fun createViewManagers(reactContext: ReactApplicationContext): 
        List<ViewManager<*, *>> {
        return emptyList()
    }
}
```

### Using Native Module (JavaScript/TypeScript)

```typescript
// src/modules/BatteryModule.ts
import { NativeModules } from 'react-native';

interface BatteryModuleInterface {
  getBatteryLevel(): Promise<number>;
  showToast(message: string): void;
}

const { BatteryModule } = NativeModules as { 
  BatteryModule: BatteryModuleInterface 
};

export default BatteryModule;

// Usage in component
import BatteryModule from './modules/BatteryModule';

const BatteryScreen = () => {
  const [level, setLevel] = useState<number>(0);
  
  useEffect(() => {
    BatteryModule.getBatteryLevel()
      .then(setLevel)
      .catch(console.error);
  }, []);
  
  return (
    <View>
      <Text>Battery: {level}%</Text>
      <Button 
        title="Show Toast"
        onPress={() => BatteryModule.showToast('Hello from native!')}
      />
    </View>
  );
};
```

---

## Performance Optimization

### FlatList Optimization

```typescript
const OptimizedList = () => {
  const [data, setData] = useState<Product[]>([]);
  
  const renderItem = useCallback(({ item }: { item: Product }) => (
    <ProductItem product={item} />
  ), []);
  
  const keyExtractor = useCallback((item: Product) => item.id, []);
  
  const getItemLayout = useCallback((data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  }), []);
  
  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      getItemLayout={getItemLayout} // For fixed-height items
      maxToRenderPerBatch={10}
      windowSize={5}
      removeClippedSubviews={true}
      initialNumToRender={10}
    />
  );
};
```

### Image Optimization

```typescript
import FastImage from 'react-native-fast-image';

const OptimizedImage = ({ uri }: { uri: string }) => (
  <FastImage
    source={{
      uri,
      priority: FastImage.priority.normal,
      cache: FastImage.cacheControl.immutable,
    }}
    resizeMode={FastImage.resizeMode.cover}
    style={{ width: 200, height: 200 }}
  />
);
```

### Hermes Engine

```javascript
// android/app/build.gradle
project.ext.react = [
    enableHermes: true  // Enable Hermes
]

// Verify Hermes is running
const isHermes = () => !!global.HermesInternal;
console.log('Hermes:', isHermes());
```

---

## Testing

### Unit Tests (Jest)

```typescript
// __tests__/utils.test.ts
import { formatPrice } from '../src/utils/format';

describe('formatPrice', () => {
  it('formats number as currency', () => {
    expect(formatPrice(1000)).toBe('$1,000.00');
  });
  
  it('handles decimal values', () => {
    expect(formatPrice(99.99)).toBe('$99.99');
  });
});
```

### Component Tests (React Native Testing Library)

```typescript
// __tests__/LoginScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import LoginScreen from '../src/screens/LoginScreen';

describe('LoginScreen', () => {
  it('renders login form', () => {
    const { getByPlaceholderText, getByText } = render(<LoginScreen />);
    
    expect(getByPlaceholderText('Email')).toBeTruthy();
    expect(getByPlaceholderText('Password')).toBeTruthy();
    expect(getByText('Login')).toBeTruthy();
  });
  
  it('handles login submission', async () => {
    const { getByPlaceholderText, getByText } = render(<LoginScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Email'), 'user@example.com');
    fireEvent.changeText(getByPlaceholderText('Password'), 'password');
    fireEvent.press(getByText('Login'));
    
    await waitFor(() => {
      expect(getByText('Welcome')).toBeTruthy();
    });
  });
});
```

### E2E Tests (Detox)

```typescript
// e2e/login.e2e.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });
  
  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('user@example.com');
    await element(by.id('password-input')).typeText('password');
    await element(by.id('login-button')).tap();
    
    await waitFor(element(by.text('Welcome')))
      .toBeVisible()
      .withTimeout(5000);
  });
});
```

---

## Build & Deployment

### Android Release

```bash
# Generate release keystore
keytool -genkeypair -v -storetype PKCS12 -keystore my-release-key.keystore \
  -alias my-key-alias -keyalg RSA -keysize 2048 -validity 10000

# Build release APK
cd android
./gradlew assembleRelease

# Build AAB (App Bundle)
./gradlew bundleRelease
```

**android/gradle.properties:**
```properties
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=*****
MYAPP_RELEASE_KEY_PASSWORD=*****
```

**android/app/build.gradle:**
```gradle
android {
    signingConfigs {
        release {
            storeFile file(MYAPP_RELEASE_STORE_FILE)
            storePassword MYAPP_RELEASE_STORE_PASSWORD
            keyAlias MYAPP_RELEASE_KEY_ALIAS
            keyPassword MYAPP_RELEASE_KEY_PASSWORD
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### iOS Release

```bash
# Install dependencies
cd ios
pod install
cd ..

# Build release
npx react-native run-ios --configuration Release

# Archive via Xcode
# Open ios/MyApp.xcworkspace in Xcode
# Product > Archive
# Upload to App Store Connect
```

---

## Common Issues

### Metro Bundler

```bash
# Clear cache
npx react-native start --reset-cache

# Clean build
cd android && ./gradlew clean && cd ..
cd ios && rm -rf Pods && pod install && cd ..
```

### Build Errors

```bash
# Android
cd android
./gradlew clean
cd ..

# iOS
cd ios
rm -rf Pods Podfile.lock
pod deintegrate
pod install
cd ..
```

### Performance Issues

1. Enable Hermes
2. Use FlatList (not ScrollView)
3. Implement React.memo
4. Use Flipper for profiling
5. Optimize images (use FastImage)

---

**See Also:**
- Main SKILL.md for architecture patterns
- `assets/templates/ReactNative/` for project templates
- `scripts/analyze_deps.py` for dependency analysis

**Last Updated:** January 2025
