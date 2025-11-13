# Mobile Architect Pro

**Expert guidance for production-grade cross-platform mobile development.**

## Coverage

- ✅ **Flutter** - Dart, BLoC, Provider, Riverpod
- ✅ **React Native** - Redux, Context API, native modules
- ✅ **Xamarin/MAUI** - C#, MVVM, .NET MAUI
- ✅ **Ionic** - Angular/React/Vue, Capacitor
- ✅ **Kotlin Native** - Jetpack Compose, Coroutines, Room

---

## Quick Start

### 1. Framework Selection

```
Read SKILL.md → Framework Selection Matrix
```

**Decision Factors:**
- Team expertise (Dart, JS, C#, Web, Kotlin)
- Performance requirements
- Platform targets (iOS, Android, Web)
- UI consistency needs
- Budget & timeline

### 2. Architecture Setup

**Flutter (BLoC):**
```bash
flutter create my_app
# Copy from assets/templates/Flutter/bloc_clean_architecture/
```

**React Native (Redux):**
```bash
npx react-native init MyApp
# Copy from assets/templates/ReactNative/redux_toolkit/
```

**Kotlin (Compose):**
```
Android Studio > New Project > Empty Compose Activity
# Copy from assets/templates/Kotlin/compose_clean/
```

### 3. State Management

| Framework | Recommended | Alternatives |
|-----------|------------|--------------|
| Flutter | BLoC | Provider, Riverpod, GetX |
| React Native | Redux Toolkit | Context, MobX, Zustand |
| Xamarin | MVVM | Prism, MVVMCross |
| Ionic | Services + RxJS | NgRx, Vuex, Context |
| Kotlin | ViewModel + Flow | LiveData, MVI |

### 4. API Integration

```
1. Define service interface
2. Implement repository pattern
3. Add error handling
4. Cache strategy (offline-first)
5. Test with mock data
```

---

## Available Resources

### Templates (`assets/templates/`)

**Flutter:**
- `bloc_clean_architecture/` - BLoC + Clean Architecture
- `provider_simple/` - Provider state management
- `riverpod_advanced/` - Riverpod with code generation

**React Native:**
- `redux_toolkit/` - Redux Toolkit + RTK Query
- `context_hooks/` - Context API + custom hooks
- `expo_managed/` - Expo managed workflow

**Xamarin:**
- `mvvm_prism/` - Prism framework
- `shell_app/` - Xamarin.Forms Shell
- `maui_migration/` - .NET MAUI template

**Ionic:**
- `angular_tabs/` - Angular with tabs navigation
- `react_capacitor/` - React + Capacitor
- `vue_pinia/` - Vue 3 + Pinia

**Kotlin:**
- `compose_clean/` - Jetpack Compose + Clean Architecture
- `mvvm_hilt/` - MVVM + Hilt DI
- `mvi_flow/` - MVI + Kotlin Flow

### References (`references/`)

- `flutter.md` - Dart, widgets, state management, performance
- `react-native.md` - JS/TS, bridge, native modules, performance
- `xamarin.md` - C#, MVVM, MAUI migration, Xamarin.Forms
- `ionic.md` - Capacitor, plugins, PWA, framework variants
- `kotlin.md` - Compose, Coroutines, Room, Retrofit, Hilt

### Scripts (`scripts/`)

- `analyze_deps.py` - Check package compatibility across platforms
- `scaffold.py` - Generate boilerplate for selected framework

---

## Common Workflows

### New Project

```bash
# 1. Analyze requirements
python scripts/analyze_deps.py --requirements requirements.txt

# 2. Select framework (use SKILL.md matrix)

# 3. Initialize project
flutter create my_app
# OR
npx react-native init MyApp

# 4. Apply architecture template
python scripts/scaffold.py flutter ./my_app --template bloc_clean_architecture
```

### Performance Optimization

**Flutter:**
- Use `const` constructors
- `ListView.builder` for long lists
- `cached_network_image` for images
- Profile with DevTools

**React Native:**
- `FlatList` (not ScrollView)
- Enable Hermes engine
- `React.memo` for components
- Profile with Flipper

**Kotlin:**
- `LazyColumn` in Compose
- `remember` for calculations
- R8/ProGuard for release
- Android Profiler

### Offline-First

```
1. Check local cache
2. Return cached data (if available)
3. Fetch network in background
4. Update cache
5. Notify UI
6. Queue failed requests
```

**Implementation:** See SKILL.md → Offline-First Architecture

### Testing

**Test Pyramid:**
- 70% Unit tests
- 20% Integration tests
- 10% E2E tests

**Tools:**
- Flutter: `flutter_test`, `integration_test`
- React Native: Jest, React Testing Library, Detox
- Kotlin: JUnit, Espresso, Compose Testing

---

## Use Cases

### E-Commerce App
**Recommendation:** Flutter or React Native
- Fast development
- Rich UI components
- Large community packages
- Good performance

### Enterprise LOB
**Recommendation:** Xamarin/MAUI or Kotlin
- Type safety (C#/Kotlin)
- Enterprise integrations
- Strong tooling
- Security compliance

### Content/Media App
**Recommendation:** Ionic or React Native
- Web code reuse
- Fast prototyping
- PWA support
- Simple requirements

### Gaming/AR
**Recommendation:** Kotlin Native or Flutter
- Maximum performance
- Native APIs access
- Complex graphics
- Platform-specific features

---

## Deployment

### iOS (App Store)

```
1. Apple Developer account ($99/year)
2. Xcode with release configuration
3. Archive and upload
4. App Store Connect metadata
5. Submit for review (1-3 days)
```

### Android (Play Store)

```
1. Google Play account ($25 one-time)
2. Generate signed APK/AAB
3. Play Console upload
4. Store listing
5. Submit (few hours - 1 day)
```

### CI/CD

See SKILL.md for GitHub Actions, GitLab CI, Bitrise examples.

---

## Troubleshooting

### Build Fails

```bash
# Flutter
flutter clean && flutter pub get

# React Native
rm -rf node_modules && npm install
npx react-native start --reset-cache

# Kotlin
./gradlew clean
# OR Android Studio > Invalidate Caches
```

### Performance Issues

1. Profile first (DevTools, Flipper, Profiler)
2. Check memory leaks
3. Optimize images
4. Use production builds
5. Implement pagination

### Native Issues

- Check platform-specific logs (Logcat, Console)
- Verify native dependencies versions
- Test on physical devices
- Check permissions (iOS: Info.plist, Android: AndroidManifest.xml)

---

## Learning Path

**Beginner:**
1. Choose one framework based on team skills
2. Start with templates
3. Follow architecture patterns
4. Build simple CRUD app

**Intermediate:**
1. Implement state management
2. Add API integration
3. Handle offline scenarios
4. Write tests

**Advanced:**
1. Custom native modules
2. Performance optimization
3. CI/CD pipelines
4. App Store deployment

---

## Documentation

- **Main Skill:** `SKILL.md`
- **Framework Details:** `references/[framework].md`
- **Templates:** `assets/templates/[Framework]/`
- **Tools:** `scripts/`

---

## Contributing

Found a bug or have suggestions? Contributions welcome!

---

## Author

**Ali Sadikin MA**
- AI Generalist • 17+ years experience
- Portfolio: www.alisadikinma.com

---

**Last Updated:** January 2025  
**Status:** ✅ Ready for Production
