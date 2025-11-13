# Flutter Development Guide

Comprehensive reference for production Flutter applications with Dart, state management, and best practices.

---

## Table of Contents

1. [Dart Fundamentals](#dart-fundamentals)
2. [Widget Architecture](#widget-architecture)
3. [State Management](#state-management)
4. [Navigation & Routing](#navigation--routing)
5. [Data Persistence](#data-persistence)
6. [Network & APIs](#network--apis)
7. [Performance Optimization](#performance-optimization)
8. [Testing](#testing)
9. [Platform Integration](#platform-integration)
10. [Build & Deployment](#build--deployment)

---

## Dart Fundamentals

### Key Language Features

```dart
// Null safety
String? nullableString;
String nonNullableString = 'Hello';

// Late initialization
late String lateString;
void init() {
  lateString = 'Initialized';
}

// Async/Await
Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 1));
  return 'Data';
}

// Streams
Stream<int> countStream() async* {
  for (int i = 0; i < 5; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;
  }
}

// Extension methods
extension StringExtension on String {
  String capitalize() => 
    '${this[0].toUpperCase()}${substring(1)}';
}
```

### Recommended Packages

```yaml
dependencies:
  # State Management
  flutter_bloc: ^8.1.3
  provider: ^6.0.5
  riverpod: ^2.4.0
  get: ^4.6.6
  
  # Network
  dio: ^5.3.3
  http: ^1.1.0
  
  # Local Storage
  hive: ^2.2.3
  sqflite: ^2.3.0
  shared_preferences: ^2.2.2
  
  # Navigation
  go_router: ^12.0.0
  
  # Dependency Injection
  get_it: ^7.6.4
  injectable: ^2.3.2
  
  # Utilities
  freezed: ^2.4.5
  json_serializable: ^6.7.1
```

---

## Widget Architecture

### Stateless vs Stateful

```dart
// Stateless - immutable
class MyStatelessWidget extends StatelessWidget {
  final String title;
  
  const MyStatelessWidget({Key? key, required this.title}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Text(title);
  }
}

// Stateful - mutable state
class MyStatefulWidget extends StatefulWidget {
  @override
  State<MyStatefulWidget> createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  int _counter = 0;
  
  void _increment() {
    setState(() {
      _counter++;
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$_counter'),
        ElevatedButton(
          onPressed: _increment,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

### Widget Lifecycle

```dart
class LifecycleWidget extends StatefulWidget {
  @override
  State<LifecycleWidget> createState() => _LifecycleWidgetState();
}

class _LifecycleWidgetState extends State<LifecycleWidget> 
    with WidgetsBindingObserver {
  
  @override
  void initState() {
    super.initState();
    // Called once when widget is inserted into the tree
    WidgetsBinding.instance.addObserver(this);
  }
  
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Called when dependencies change
  }
  
  @override
  void didUpdateWidget(LifecycleWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Called when widget configuration changes
  }
  
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    // Called when app lifecycle changes
    switch (state) {
      case AppLifecycleState.resumed:
        // App is visible and responding
        break;
      case AppLifecycleState.inactive:
        // App is inactive
        break;
      case AppLifecycleState.paused:
        // App is not visible
        break;
      case AppLifecycleState.detached:
        // App is still running but detached
        break;
    }
  }
  
  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
    // Cleanup
  }
  
  @override
  Widget build(BuildContext context) => Container();
}
```

---

## State Management

### BLoC Pattern (Recommended for Large Apps)

```dart
// 1. Events
abstract class CounterEvent {}
class Increment extends CounterEvent {}
class Decrement extends CounterEvent {}

// 2. States
class CounterState {
  final int count;
  final bool isLoading;
  
  const CounterState({required this.count, this.isLoading = false});
  
  CounterState copyWith({int? count, bool? isLoading}) {
    return CounterState(
      count: count ?? this.count,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

// 3. BLoC
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(CounterState(count: 0)) {
    on<Increment>((event, emit) async {
      emit(state.copyWith(isLoading: true));
      await Future.delayed(Duration(seconds: 1));
      emit(state.copyWith(count: state.count + 1, isLoading: false));
    });
    
    on<Decrement>((event, emit) {
      emit(state.copyWith(count: state.count - 1));
    });
  }
}

// 4. Usage in Widget
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => CounterBloc(),
      child: CounterView(),
    );
  }
}

class CounterView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, CounterState>(
      builder: (context, state) {
        if (state.isLoading) {
          return CircularProgressIndicator();
        }
        
        return Column(
          children: [
            Text('${state.count}'),
            ElevatedButton(
              onPressed: () => context.read<CounterBloc>().add(Increment()),
              child: Text('Increment'),
            ),
          ],
        );
      },
    );
  }
}
```

### Provider (Simple Apps)

```dart
// 1. ChangeNotifier Model
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners();
  }
}

// 2. Provide
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => CounterProvider(),
      child: MyApp(),
    ),
  );
}

// 3. Consume
class CounterWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final counter = context.watch<CounterProvider>();
    
    return Column(
      children: [
        Text('${counter.count}'),
        ElevatedButton(
          onPressed: () => context.read<CounterProvider>().increment(),
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

### Riverpod (Modern Approach)

```dart
// 1. Define provider
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  
  void increment() => state++;
  void decrement() => state--;
}

// 2. Consume
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    
    return Column(
      children: [
        Text('$count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).increment(),
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

---

## Navigation & Routing

### GoRouter (Recommended)

```dart
final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsScreen(id: id);
          },
        ),
      ],
    ),
    GoRoute(
      path: '/profile',
      builder: (context, state) => ProfileScreen(),
    ),
  ],
  redirect: (context, state) {
    final isLoggedIn = // check auth
    if (!isLoggedIn && state.location != '/login') {
      return '/login';
    }
    return null;
  },
);

// Usage
void main() {
  runApp(MaterialApp.router(
    routerConfig: router,
  ));
}

// Navigate
context.go('/details/123');
context.push('/profile');
context.pop();
```

---

## Data Persistence

### Hive (NoSQL, Fast)

```dart
// 1. Define model
@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  late String name;
  
  @HiveField(1)
  late int age;
}

// 2. Initialize
await Hive.initFlutter();
Hive.registerAdapter(UserAdapter());
await Hive.openBox<User>('users');

// 3. CRUD operations
final box = Hive.box<User>('users');

// Create
final user = User()..name = 'John'..age = 30;
await box.add(user);

// Read
final users = box.values.toList();
final user = box.getAt(0);

// Update
user.age = 31;
await user.save();

// Delete
await box.deleteAt(0);
```

### SQLite (Relational)

```dart
// 1. Database helper
class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;
  
  DatabaseHelper._init();
  
  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('app.db');
    return _database!;
  }
  
  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);
    
    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }
  
  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
      )
    ''');
  }
  
  Future<int> insert(Map<String, dynamic> row) async {
    final db = await database;
    return await db.insert('users', row);
  }
  
  Future<List<Map<String, dynamic>>> queryAll() async {
    final db = await database;
    return await db.query('users');
  }
}
```

---

## Network & APIs

### Dio (Recommended)

```dart
// 1. Setup
class ApiService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: Duration(seconds: 5),
      receiveTimeout: Duration(seconds: 3),
    ),
  );
  
  ApiService() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) {
          options.headers['Authorization'] = 'Bearer $token';
          return handler.next(options);
        },
        onError: (error, handler) {
          // Handle errors globally
          return handler.next(error);
        },
      ),
    );
  }
  
  Future<List<Product>> getProducts() async {
    try {
      final response = await _dio.get('/products');
      return (response.data as List)
          .map((json) => Product.fromJson(json))
          .toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  AppException _handleError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
        return NetworkException('Connection timeout');
      case DioExceptionType.badResponse:
        return ServerException('Server error: ${error.response?.statusCode}');
      default:
        return UnknownException('Unknown error');
    }
  }
}
```

---

## Performance Optimization

### Best Practices

```dart
// 1. Use const constructors
const Text('Hello'); // Not Text('Hello')

// 2. ListView.builder for long lists
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
);

// 3. RepaintBoundary for expensive widgets
RepaintBoundary(
  child: ExpensiveWidget(),
);

// 4. Cached network images
CachedNetworkImage(
  imageUrl: url,
  placeholder: (context, url) => CircularProgressIndicator(),
  errorWidget: (context, url, error) => Icon(Icons.error),
);

// 5. Keys for list items
ListView.builder(
  itemBuilder: (context, index) => ItemWidget(
    key: ValueKey(items[index].id),
    item: items[index],
  ),
);
```

### Profiling

```bash
# Run in profile mode
flutter run --profile

# Performance overlay
MaterialApp(
  showPerformanceOverlay: true,
)

# DevTools
flutter pub global activate devtools
flutter pub global run devtools
```

---

## Testing

### Unit Tests

```dart
void main() {
  group('Counter', () {
    test('initial value is 0', () {
      final counter = Counter();
      expect(counter.value, 0);
    });
    
    test('increment adds 1', () {
      final counter = Counter();
      counter.increment();
      expect(counter.value, 1);
    });
  });
}
```

### Widget Tests

```dart
void main() {
  testWidgets('Button tap increments counter', (tester) async {
    await tester.pumpWidget(MyApp());
    
    expect(find.text('0'), findsOneWidget);
    
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();
    
    expect(find.text('1'), findsOneWidget);
  });
}
```

### Integration Tests

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  testWidgets('Full user flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();
    
    // Login
    await tester.enterText(find.byKey(Key('email')), 'user@example.com');
    await tester.enterText(find.byKey(Key('password')), 'password');
    await tester.tap(find.text('Login'));
    await tester.pumpAndSettle();
    
    // Verify home screen
    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

---

## Platform Integration

### Method Channels

```dart
// Dart side
class BatteryService {
  static const platform = MethodChannel('com.example/battery');
  
  Future<int> getBatteryLevel() async {
    try {
      final int result = await platform.invokeMethod('getBatteryLevel');
      return result;
    } on PlatformException catch (e) {
      print("Failed to get battery level: '${e.message}'.");
      return -1;
    }
  }
}
```

```kotlin
// Kotlin (Android) side
class MainActivity: FlutterActivity() {
  private val CHANNEL = "com.example/battery"
  
  override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)
    
    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
      .setMethodCallHandler { call, result ->
        if (call.method == "getBatteryLevel") {
          val batteryLevel = getBatteryLevel()
          
          if (batteryLevel != -1) {
            result.success(batteryLevel)
          } else {
            result.error("UNAVAILABLE", "Battery level not available.", null)
          }
        } else {
          result.notImplemented()
        }
      }
  }
  
  private fun getBatteryLevel(): Int {
    val batteryManager = getSystemService(Context.BATTERY_SERVICE) as BatteryManager
    return batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
  }
}
```

---

## Build & Deployment

### Build Commands

```bash
# Debug build
flutter build apk --debug
flutter build ios --debug

# Release build
flutter build apk --release
flutter build appbundle --release  # Android App Bundle
flutter build ios --release

# Split per ABI (smaller APKs)
flutter build apk --split-per-abi
```

### Release Configuration

**Android (android/app/build.gradle):**
```gradle
android {
    defaultConfig {
        versionCode 1
        versionName "1.0.0"
    }
    
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile file(keystoreProperties['storeFile'])
            storePassword keystoreProperties['storePassword']
        }
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
        }
    }
}
```

**iOS (ios/Runner.xcodeproj):**
- Open in Xcode
- Select Runner > Signing & Capabilities
- Configure team and provisioning profile
- Archive and upload to App Store Connect

---

## Common Issues & Solutions

### Build Errors

**"Gradle build failed":**
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
```

**"CocoaPods error":**
```bash
cd ios
rm Podfile.lock
rm -rf Pods
pod install
cd ..
```

### Performance Issues

1. Use `flutter run --profile` to test
2. Check DevTools timeline
3. Look for:
   - Long frame render times (> 16ms)
   - Frequent rebuilds
   - Large image sizes
   - Too many widgets in tree

### Hot Reload Not Working

```bash
flutter clean
flutter pub get
# Restart IDE
# Restart device/emulator
```

---

**See Also:**
- Main SKILL.md for architecture patterns
- `assets/templates/Flutter/` for project templates
- `scripts/analyze_deps.py` for dependency analysis

**Last Updated:** January 2025
