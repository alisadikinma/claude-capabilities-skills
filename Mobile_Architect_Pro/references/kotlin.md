# Kotlin Native Android Development Guide

Comprehensive reference for production native Android applications with Kotlin, Jetpack Compose, and modern Android architecture.

---

## Table of Contents

1. [Setup & Configuration](#setup--configuration)
2. [Jetpack Compose Basics](#jetpack-compose-basics)
3. [MVVM Architecture](#mvvm-architecture)
4. [Dependency Injection](#dependency-injection)
5. [Coroutines & Flow](#coroutines--flow)
6. [Room Database](#room-database)
7. [Retrofit Networking](#retrofit-networking)
8. [Navigation](#navigation)
9. [Testing](#testing)
10. [Build & Release](#build--release)

---

## Setup & Configuration

### Essential Dependencies

```kotlin
// build.gradle.kts (app level)
dependencies {
    // Compose
    implementation("androidx.compose.ui:ui:1.6.0")
    implementation("androidx.compose.material3:material3:1.2.0")
    implementation("androidx.activity:activity-compose:1.8.2")
    
    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0")
    
    // Navigation
    implementation("androidx.navigation:navigation-compose:2.7.6")
    
    // Hilt
    implementation("com.google.dagger:hilt-android:2.50")
    kapt("com.google.dagger:hilt-compiler:2.50")
    
    // Retrofit
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    
    // Room
    implementation("androidx.room:room-runtime:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    
    // Coil (images)
    implementation("io.coil-kt:coil-compose:2.5.0")
}
```

---

## Jetpack Compose Basics

### Simple Screen

```kotlin
@Composable
fun ProductCard(product: Product, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() }
            .padding(8.dp)
    ) {
        Row(modifier = Modifier.padding(16.dp)) {
            Text(text = product.name, style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.weight(1f))
            Text(text = "$${product.price}")
        }
    }
}
```

### LazyColumn

```kotlin
@Composable
fun ProductList(products: List<Product>, onItemClick: (String) -> Unit) {
    LazyColumn {
        items(products, key = { it.id }) { product ->
            ProductCard(
                product = product,
                onClick = { onItemClick(product.id) }
            )
        }
    }
}
```

---

## MVVM Architecture

### ViewModel

```kotlin
@HiltViewModel
class ProductsViewModel @Inject constructor(
    private val repository: ProductRepository
) : ViewModel() {
    
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()
    
    init {
        loadProducts()
    }
    
    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading
            repository.getProducts()
                .onSuccess { products ->
                    _uiState.value = UiState.Success(products)
                }
                .onFailure { error ->
                    _uiState.value = UiState.Error(error.message ?: "Unknown error")
                }
        }
    }
}

sealed interface UiState {
    object Loading : UiState
    data class Success(val products: List<Product>) : UiState
    data class Error(val message: String) : UiState
}
```

### Screen

```kotlin
@Composable
fun ProductsScreen(viewModel: ProductsViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    when (val state = uiState) {
        is UiState.Loading -> CircularProgressIndicator()
        is UiState.Success -> ProductList(products = state.products)
        is UiState.Error -> Text("Error: ${state.message}")
    }
}
```

---

## Dependency Injection

### Hilt Setup

```kotlin
@HiltAndroidApp
class MyApplication : Application()

@AndroidEntryPoint
class MainActivity : ComponentActivity()

@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit = Retrofit.Builder()
        .baseUrl("https://api.example.com/")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
}
```

---

## Coroutines & Flow

### Repository with Flow

```kotlin
class ProductRepository @Inject constructor(private val api: ProductApi) {
    
    fun getProducts(): Flow<List<Product>> = flow {
        val response = api.getProducts()
        emit(response)
    }.flowOn(Dispatchers.IO)
    
    suspend fun createProduct(product: Product): Result<Product> {
        return try {
            val result = api.createProduct(product)
            Result.success(result)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## Room Database

### Entity & DAO

```kotlin
@Entity(tableName = "products")
data class ProductEntity(
    @PrimaryKey val id: String,
    val name: String,
    val price: Double
)

@Dao
interface ProductDao {
    @Query("SELECT * FROM products")
    fun getAll(): Flow<List<ProductEntity>>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(product: ProductEntity)
}

@Database(entities = [ProductEntity::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun productDao(): ProductDao
}
```

---

## Retrofit Networking

### API Interface

```kotlin
interface ProductApi {
    @GET("products")
    suspend fun getProducts(): List<Product>
    
    @GET("products/{id}")
    suspend fun getProduct(@Path("id") id: String): Product
    
    @POST("products")
    suspend fun createProduct(@Body product: Product): Product
}
```

---

## Navigation

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    
    NavHost(navController, startDestination = "products") {
        composable("products") {
            ProductsScreen(onProductClick = { id ->
                navController.navigate("products/$id")
            })
        }
        composable("products/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")
            ProductDetailScreen(productId = id)
        }
    }
}
```

---

## Testing

### Unit Test

```kotlin
@Test
fun `loadProducts updates state correctly`() = runTest {
    val repository = FakeProductRepository()
    val viewModel = ProductsViewModel(repository)
    
    val state = viewModel.uiState.value
    assertTrue(state is UiState.Success)
}
```

---

## Build & Release

### Generate Signed APK

```bash
# Via Android Studio:
Build > Generate Signed Bundle / APK
```

### Gradle Config

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("keystore.jks")
            storePassword = "password"
            keyAlias = "key"
            keyPassword = "password"
        }
    }
}
```

---

**See Also:** Main SKILL.md, templates in `assets/templates/Kotlin/`

**Last Updated:** January 2025
