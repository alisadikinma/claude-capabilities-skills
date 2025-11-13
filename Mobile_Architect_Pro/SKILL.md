---
name: mobile-architect-pro
description: |
  Flutter React Native Xamarin Ionic Kotlin mobile app development cross-platform. iOS Android mobile architecture BLoC Redux MVVM Jetpack Compose patterns.
  Use when: building mobile apps, creating Flutter app, React Native project, mobile architecture, BLoC pattern, Provider Riverpod, Redux Toolkit, state management, navigation setup, native modules, platform channels, offline-first, Firebase integration, push notifications, mobile UI, responsive design, performance optimization, app deployment, Play Store, App Store, mobile testing, cross-platform strategy, framework selection, mobile best practices.
---

# Mobile Architect Pro

Expert guidance for production-grade cross-platform mobile development covering Flutter, React Native, Xamarin, Ionic, and native Kotlin Android development.

## Quick Navigation

- **Framework Selection** → Use decision matrix below
- **Flutter Development** → Read `references/flutter.md`
- **React Native** → Read `references/react-native.md`
- **Xamarin/MAUI** → Read `references/xamarin.md`
- **Ionic/Capacitor** → Read `references/ionic.md`
- **Native Kotlin** → Read `references/kotlin.md`
- **Templates** → Browse `assets/templates/[Framework]/`
- **Scripts** → Use `scripts/analyze_deps.py` for compatibility checks

---

## Framework Selection Matrix

### Decision Criteria

| Criterion | Flutter | React Native | Xamarin | Ionic | Kotlin |
|-----------|---------|--------------|---------|-------|--------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **UI Consistency** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Development Speed** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Native Access** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Web Reuse** | ❌ | ✅ Limited | ❌ | ✅ Full | ❌ |
| **Learning Curve** | Medium | Easy | Medium | Easy | Medium |
| **Team Skills** | Dart | JS/TS | C# | Web | Kotlin |

### Use Case Recommendations

**Choose Flutter when:**
- Need pixel-perfect UI consistency across platforms
- Building content-rich apps (e.g., social, e-commerce)
- Team can learn Dart
- Performance is critical
- Example: Instagram clone, fintech apps

**Choose React Native when:**
- Team has web dev experience (React)
- Need extensive third-party packages
- Iterative development speed priority
- Web version planned (React Native Web)
- Example: Marketplace apps, social platforms

**Choose Xamarin/MAUI when:**
- Existing .NET/C# codebase
- Enterprise environments with Microsoft stack
- Strong type safety required
- Legacy Windows support needed
- Example: Enterprise LOB apps, healthcare

**Choose Ionic when:**
- Existing web app to mobilize
- Small team with web skills only
- PWA + native app requirement
- Budget constraints
- Example: Content apps, simple utilities

**Choose Kotlin (Native) when:**
- Android-only or Android-first strategy
- Maximum performance required
- Deep platform integration needed
- Complex animations/graphics
- Example: Games, AR apps, camera-heavy

---

## Architecture Patterns

### 1. Flutter Architecture (BLoC Pattern)

```
lib/
├── main.dart
├── core/
│   ├── constants/
│   ├── theme/
│   ├── utils/
│   └── network/
├── data/
│   ├── models/
│   ├── repositories/
│   └── datasources/
│       ├── local/
│       └── remote/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── presentation/
│   ├── blocs/
│   ├── pages/
│   └── widgets/
└── injection_container.dart
```

**State Management Options:**
- **BLoC** (Business Logic Component) - Best for large apps
- **Provider** - Simple, Flutter-native
- **Riverpod** - Modern, type-safe
- **GetX** - All-in-one (state + routing + DI)

**Template:** `assets/templates/Flutter/bloc_clean_architecture/`

### 2. React Native Architecture (Clean + Redux)

```
src/
├── index.js
├── core/
│   ├── config/
│   ├── constants/
│   └── utils/
├── data/
│   ├── models/
│   ├── repositories/
│   └── sources/
│       ├── local/
│       └── remote/
├── domain/
│   ├── entities/
│   └── usecases/
├── presentation/
│   ├── components/
│   ├── screens/
│   ├── navigation/
│   └── redux/
│       ├── actions/
│       ├── reducers/
│       └── store.js
└── native/
    ├── android/
    └── ios/
```

**State Management Options:**
- **Redux Toolkit** - Industry standard
- **Context API + Hooks** - Native solution
- **MobX** - Reactive programming
- **Zustand** - Minimal boilerplate

**Template:** `assets/templates/ReactNative/redux_toolkit/`

### 3. Xamarin/MAUI Architecture (MVVM)

```
YourApp/
├── YourApp/
│   ├── Models/
│   ├── ViewModels/
│   ├── Views/
│   ├── Services/
│   │   ├── IDataService.cs
│   │   └── DataService.cs
│   ├── Helpers/
│   ├── Converters/
│   └── App.xaml
├── YourApp.Android/
└── YourApp.iOS/
```

**MVVM Components:**
- **Model** - Data entities
- **View** - XAML UI
- **ViewModel** - Presentation logic
- **Commands** - ICommand implementations
- **Data Binding** - Two-way sync

**Template:** `assets/templates/Xamarin/mvvm_prism/`

### 4. Ionic Architecture (Component-Based)

```
src/
├── app/
│   ├── core/
│   │   ├── services/
│   │   ├── guards/
│   │   └── interceptors/
│   ├── shared/
│   │   ├── components/
│   │   └── pipes/
│   ├── pages/
│   │   └── home/
│   │       ├── home.page.html
│   │       ├── home.page.ts
│   │       └── home.page.scss
│   ├── app-routing.module.ts
│   └── app.component.ts
├── assets/
└── capacitor.config.ts
```

**Framework Variants:**
- **Ionic Angular** - Full framework
- **Ionic React** - React integration
- **Ionic Vue** - Vue.js integration

**Template:** `assets/templates/Ionic/angular_tabs/`

### 5. Kotlin Native Architecture (Clean MVVM)

```
app/src/main/java/com/yourapp/
├── di/
│   ├── AppModule.kt
│   └── NetworkModule.kt
├── data/
│   ├── local/
│   │   ├── dao/
│   │   └── database/
│   ├── remote/
│   │   ├── api/
│   │   └── dto/
│   └── repository/
├── domain/
│   ├── model/
│   ├── repository/
│   └── usecase/
├── presentation/
│   ├── MainActivity.kt
│   ├── features/
│   │   └── home/
│   │       ├── HomeScreen.kt
│   │       └── HomeViewModel.kt
│   └── theme/
└── util/
```

**Modern Stack:**
- **Jetpack Compose** - Declarative UI
- **Coroutines + Flow** - Async operations
- **Room** - Local database
- **Retrofit** - Network calls
- **Hilt** - Dependency injection

**Template:** `assets/templates/Kotlin/compose_clean/`

---

## Core Implementation Workflows

### Workflow 1: New Project Setup

1. **Analyze requirements**
   - Target platforms (iOS, Android, Web)
   - Performance needs
   - Team expertise
   - Timeline constraints

2. **Select framework** using decision matrix above

3. **Initialize project**
   ```bash
   # Flutter
   flutter create --org com.yourcompany app_name
   
   # React Native
   npx react-native init AppName
   
   # Kotlin
   # Use Android Studio > New Project > Empty Compose Activity
   ```

4. **Apply architecture template**
   - Copy from `assets/templates/[Framework]/`
   - Run `scripts/scaffold.py [framework] [project-path]`

5. **Configure tooling**
   - Linting (ESLint, Dart Analyzer, Detekt)
   - Formatting (Prettier, dart format, ktfmt)
   - Pre-commit hooks
   - CI/CD pipeline

### Workflow 2: State Management Implementation

**For Flutter (BLoC):**
```dart
// 1. Define events
abstract class CounterEvent {}
class Increment extends CounterEvent {}

// 2. Define states
class CounterState {
  final int count;
  CounterState(this.count);
}

// 3. Create BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState(0)) {
    on<Increment>((event, emit) => emit(CounterState(state.count + 1)));
  }
}

// 4. Use in widget
BlocBuilder<CounterBloc, CounterState>(
  builder: (context, state) => Text('${state.count}'),
)
```

**For React Native (Redux Toolkit):**
```javascript
// 1. Create slice
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: state => { state.value += 1 }
  }
});

// 2. Use in component
const count = useSelector(state => state.counter.value);
const dispatch = useDispatch();
<Text onPress={() => dispatch(increment())}>{count}</Text>
```

**For Kotlin (ViewModel + Flow):**
```kotlin
// 1. Define ViewModel
class CounterViewModel : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    
    fun increment() {
        _count.value++
    }
}

// 2. Use in Compose
val viewModel: CounterViewModel = viewModel()
val count by viewModel.count.collectAsState()
Text(text = "$count", modifier = Modifier.clickable { viewModel.increment() })
```

### Workflow 3: API Integration

**Standard pattern for all frameworks:**

1. **Define API service interface**
2. **Implement repository pattern**
3. **Create data models/DTOs**
4. **Add error handling**
5. **Implement caching strategy**

**Example (Flutter):**
```dart
// 1. API service
class ApiService {
  final Dio _dio;
  
  Future<List<Product>> fetchProducts() async {
    final response = await _dio.get('/products');
    return (response.data as List)
        .map((json) => Product.fromJson(json))
        .toList();
  }
}

// 2. Repository
class ProductRepository {
  final ApiService _apiService;
  final LocalDatabase _localDb;
  
  Future<List<Product>> getProducts({bool forceRefresh = false}) async {
    if (!forceRefresh) {
      final cached = await _localDb.getProducts();
      if (cached.isNotEmpty) return cached;
    }
    
    final products = await _apiService.fetchProducts();
    await _localDb.saveProducts(products);
    return products;
  }
}
```

### Workflow 4: Navigation Setup

**Flutter (go_router):**
```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) => DetailsScreen(
            id: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
  ],
);
```

**React Native (React Navigation):**
```javascript
const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

**Kotlin (Compose Navigation):**
```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController, startDestination = "home") {
        composable("home") { HomeScreen(navController) }
        composable("details/{id}") { backStackEntry ->
            DetailsScreen(backStackEntry.arguments?.getString("id"))
        }
    }
}
```

---

## Performance Optimization

### General Principles

1. **Lazy loading** - Load data/screens on demand
2. **Image optimization** - Compress, cache, lazy load
3. **List virtualization** - Render only visible items
4. **Minimize rebuilds** - Use memoization/keys
5. **Code splitting** - Bundle optimization
6. **Native modules** - Offload heavy computation

### Flutter-Specific

- Use `const` constructors aggressively
- Implement `ListView.builder` for long lists
- Profile with DevTools (timeline view)
- Use `RepaintBoundary` for expensive widgets
- Cache network images with `cached_network_image`

### React Native-Specific

- Use `FlatList`/`SectionList` (not `ScrollView` for long lists)
- Implement `React.memo` for expensive components
- Use `useMemo`/`useCallback` hooks
- Enable Hermes JavaScript engine
- Profile with Flipper

### Kotlin-Specific

- Use `LazyColumn`/`LazyRow` in Compose
- Implement `remember` for expensive calculations
- Use `derivedStateOf` for computed states
- Profile with Android Profiler
- Use R8/ProGuard for release builds

---

## Offline-First Architecture

### Strategy Selection

| Strategy | Use When | Complexity |
|----------|----------|------------|
| **Cache-First** | Static content, news apps | Low |
| **Network-First** | Real-time data, chat | Low |
| **Cache-Then-Network** | Social feeds, e-commerce | Medium |
| **Sync Queue** | Form submissions, orders | High |

### Implementation Pattern

```
1. Check local cache
2. Return cached data immediately (if exists)
3. Fetch from network in background
4. Update cache with fresh data
5. Notify UI of update
6. Queue failed requests for retry
```

**Flutter Example (with Hive):**
```dart
class OfflineFirstRepository {
  final ApiService _api;
  final HiveBox _cache;
  
  Stream<List<Item>> getItems() async* {
    // Emit cached data first
    final cached = _cache.get('items');
    if (cached != null) yield cached;
    
    // Fetch fresh data
    try {
      final fresh = await _api.fetchItems();
      await _cache.put('items', fresh);
      yield fresh;
    } catch (e) {
      // Network error, stick with cache
      if (cached == null) rethrow;
    }
  }
}
```

---

## Native Module Integration

### When to Use Native Modules

- Hardware access (camera, sensors, Bluetooth)
- Platform-specific APIs (HealthKit, Google Play Services)
- Performance-critical operations
- Third-party SDKs without cross-platform wrappers

### Flutter Platform Channels

```dart
// Dart side
class BatteryService {
  static const platform = MethodChannel('com.app/battery');
  
  Future<int> getBatteryLevel() async {
    return await platform.invokeMethod('getBatteryLevel');
  }
}

// Kotlin (Android) side
class MainActivity: FlutterActivity() {
  override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.app/battery")
      .setMethodCallHandler { call, result ->
        if (call.method == "getBatteryLevel") {
          val batteryLevel = getBatteryLevel()
          result.success(batteryLevel)
        }
      }
  }
}
```

### React Native Native Modules

```javascript
// JavaScript
import { NativeModules } from 'react-native';
const { BatteryModule } = NativeModules;

const level = await BatteryModule.getBatteryLevel();
```

```kotlin
// Kotlin (Android)
class BatteryModule(reactContext: ReactApplicationContext) : 
    ReactContextBaseJavaModule(reactContext) {
    
    override fun getName() = "BatteryModule"
    
    @ReactMethod
    fun getBatteryLevel(promise: Promise) {
        val level = // get battery level
        promise.resolve(level)
    }
}
```

---

## Testing Strategy

### Test Pyramid

```
        E2E (10%)
       /        \
    Integration (20%)
   /              \
  Unit Tests (70%)
```

### Flutter Testing

```dart
// Unit test
test('Counter increments', () {
  final counter = Counter();
  counter.increment();
  expect(counter.value, 1);
});

// Widget test
testWidgets('Button tap increments counter', (tester) async {
  await tester.pumpWidget(MyApp());
  expect(find.text('0'), findsOneWidget);
  await tester.tap(find.byIcon(Icons.add));
  await tester.pump();
  expect(find.text('1'), findsOneWidget);
});

// Integration test
testWidgets('Full user flow', (tester) async {
  await tester.pumpWidget(MyApp());
  await tester.tap(find.text('Login'));
  await tester.enterText(find.byType(TextField), 'user@example.com');
  await tester.tap(find.text('Submit'));
  await tester.pumpAndSettle();
  expect(find.text('Welcome'), findsOneWidget);
});
```

### React Native Testing

```javascript
// Unit test (Jest)
test('increments counter', () => {
  const counter = new Counter();
  counter.increment();
  expect(counter.value).toBe(1);
});

// Component test (React Testing Library)
test('button tap increments', () => {
  const { getByText } = render(<Counter />);
  expect(getByText('0')).toBeTruthy();
  fireEvent.press(getByText('Increment'));
  expect(getByText('1')).toBeTruthy();
});

// E2E test (Detox)
describe('Login flow', () => {
  it('should login successfully', async () => {
    await element(by.id('email')).typeText('user@example.com');
    await element(by.id('password')).typeText('password');
    await element(by.text('Login')).tap();
    await expect(element(by.text('Welcome'))).toBeVisible();
  });
});
```

---

## Deployment & Distribution

### App Store Submission Checklist

**iOS (App Store):**
1. [ ] Apple Developer account ($99/year)
2. [ ] App icons (all sizes)
3. [ ] Launch screens
4. [ ] Privacy policy URL
5. [ ] App Store screenshots
6. [ ] Build with release configuration
7. [ ] Archive and upload via Xcode/Transporter
8. [ ] Fill App Store Connect metadata
9. [ ] Submit for review

**Android (Play Store):**
1. [ ] Google Play Developer account ($25 one-time)
2. [ ] App icon (512x512 PNG)
3. [ ] Feature graphic (1024x500)
4. [ ] Screenshots (multiple sizes)
5. [ ] Privacy policy URL
6. [ ] Generate signed APK/AAB
7. [ ] Upload to Play Console
8. [ ] Complete store listing
9. [ ] Submit for review

### CI/CD Pipeline (Example: GitHub Actions)

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v3
        with:
          name: apk
          path: build/app/outputs/flutter-apk/app-release.apk
```

---

## Troubleshooting Common Issues

### Build Failures

**Flutter:**
- Clear cache: `flutter clean && flutter pub get`
- Update Flutter: `flutter upgrade`
- Check Dart SDK version compatibility

**React Native:**
- Clear cache: `rm -rf node_modules && npm install`
- Reset Metro: `npx react-native start --reset-cache`
- Clean Gradle (Android): `cd android && ./gradlew clean`

**Kotlin:**
- Invalidate caches: Android Studio > File > Invalidate Caches
- Clean build: `./gradlew clean`
- Update Gradle: Check `gradle-wrapper.properties`

### Performance Issues

1. Profile with platform tools first
2. Check for memory leaks
3. Optimize images/assets
4. Reduce overdraw
5. Implement pagination
6. Use production builds for testing

---

## Further Resources

- **Flutter Details:** `references/flutter.md`
- **React Native Details:** `references/react-native.md`
- **Xamarin Details:** `references/xamarin.md`
- **Ionic Details:** `references/ionic.md`
- **Kotlin Details:** `references/kotlin.md`
- **Dependency Analysis:** `scripts/analyze_deps.py`
- **Project Scaffolding:** `scripts/scaffold.py`

---

**Last Updated:** January 2025
