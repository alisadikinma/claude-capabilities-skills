# Mobile Architect Pro - Template Files

## Available Templates

All template examples and starter files are documented here. Copy the relevant code to your project.

---

## Flutter Templates

### 1. BLoC + Clean Architecture

**product_bloc.dart**
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

// Events
abstract class ProductEvent extends Equatable {
  @override
  List<Object> get props => [];
}

class LoadProducts extends ProductEvent {}
class RefreshProducts extends ProductEvent {}

// States
abstract class ProductState extends Equatable {
  @override
  List<Object> get props => [];
}

class ProductInitial extends ProductState {}
class ProductLoading extends ProductState {}
class ProductLoaded extends ProductState {
  final List<Product> products;
  ProductLoaded(this.products);
  @override
  List<Object> get props => [products];
}
class ProductError extends ProductState {
  final String message;
  ProductError(this.message);
  @override
  List<Object> get props => [message];
}

// BLoC
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final GetProductsUseCase getProductsUseCase;
  
  ProductBloc(this.getProductsUseCase) : super(ProductInitial()) {
    on<LoadProducts>((event, emit) async {
      emit(ProductLoading());
      final result = await getProductsUseCase();
      result.fold(
        (failure) => emit(ProductError(failure.message)),
        (products) => emit(ProductLoaded(products)),
      );
    });
  }
}
```

**product_repository.dart (Domain)**
```dart
abstract class ProductRepository {
  Future<Either<Failure, List<Product>>> getProducts();
  Future<Either<Failure, Product>> getProduct(String id);
}
```

**injection_container.dart**
```dart
import 'package:get_it/get_it.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // BLoCs
  sl.registerFactory(() => ProductBloc(sl()));
  
  // Use cases
  sl.registerLazySingleton(() => GetProductsUseCase(sl()));
  
  // Repositories
  sl.registerLazySingleton<ProductRepository>(
    () => ProductRepositoryImpl(sl(), sl())
  );
  
  // Data sources
  sl.registerLazySingleton<ProductRemoteDataSource>(
    () => ProductRemoteDataSourceImpl(sl())
  );
}
```

---

## React Native Templates

### 1. Redux Toolkit

**productSlice.ts**
```typescript
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { productApi } from '../../services/api';

interface ProductState {
  products: Product[];
  loading: boolean;
  error: string | null;
}

const initialState: ProductState = {
  products: [],
  loading: false,
  error: null,
};

export const fetchProducts = createAsyncThunk(
  'products/fetchProducts',
  async () => {
    const { data } = await productApi.getProducts();
    return data;
  }
);

const productSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {
    clearProducts: (state) => {
      state.products = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.loading = false;
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch';
      });
  },
});

export const { clearProducts } = productSlice.actions;
export default productSlice.reducer;
```

**ProductsScreen.tsx**
```typescript
import React, { useEffect } from 'react';
import { View, FlatList, Text } from 'react-native';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { fetchProducts } from '../store/slices/productSlice';
import ProductCard from '../components/ProductCard';

const ProductsScreen = () => {
  const dispatch = useAppDispatch();
  const { products, loading, error } = useAppSelector(state => state.products);
  
  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);
  
  if (loading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error}</Text>;
  
  return (
    <View>
      <FlatList
        data={products}
        renderItem={({ item }) => <ProductCard product={item} />}
        keyExtractor={item => item.id}
      />
    </View>
  );
};

export default ProductsScreen;
```

---

## Kotlin Templates

### 1. Jetpack Compose + Clean Architecture

**ProductsViewModel.kt**
```kotlin
@HiltViewModel
class ProductsViewModel @Inject constructor(
    private val getProductsUseCase: GetProductsUseCase
) : ViewModel() {
    
    private val _uiState = MutableStateFlow<ProductsUiState>(ProductsUiState.Loading)
    val uiState: StateFlow<ProductsUiState> = _uiState.asStateFlow()
    
    init {
        loadProducts()
    }
    
    fun loadProducts() {
        viewModelScope.launch {
            _uiState.value = ProductsUiState.Loading
            getProductsUseCase().collect { result ->
                _uiState.value = when (result) {
                    is Resource.Success -> ProductsUiState.Success(result.data)
                    is Resource.Error -> ProductsUiState.Error(result.message)
                    is Resource.Loading -> ProductsUiState.Loading
                }
            }
        }
    }
}

sealed interface ProductsUiState {
    object Loading : ProductsUiState
    data class Success(val products: List<Product>) : ProductsUiState
    data class Error(val message: String) : ProductsUiState
}
```

**ProductsScreen.kt**
```kotlin
@Composable
fun ProductsScreen(
    viewModel: ProductsViewModel = hiltViewModel(),
    onProductClick: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Products") })
        }
    ) { paddingValues ->
        when (val state = uiState) {
            is ProductsUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }
            is ProductsUiState.Success -> {
                LazyColumn(
                    modifier = Modifier.padding(paddingValues),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(state.products) { product ->
                        ProductCard(
                            product = product,
                            onClick = { onProductClick(product.id) }
                        )
                    }
                }
            }
            is ProductsUiState.Error -> {
                ErrorScreen(message = state.message)
            }
        }
    }
}
```

**AppModule.kt (Hilt)**
```kotlin
@Module
@InstallIn(SingletonComponent::class)
object AppModule {
    
    @Provides
    @Singleton
    fun provideRetrofit(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://api.example.com/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
    
    @Provides
    @Singleton
    fun provideProductApi(retrofit: Retrofit): ProductApi {
        return retrofit.create(ProductApi::class.java)
    }
    
    @Provides
    @Singleton
    fun provideAppDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }
}
```

---

## Xamarin/MAUI Templates

### 1. MVVM Pattern

**ProductViewModel.cs**
```csharp
public class ProductViewModel : ObservableObject
{
    private readonly IProductService _productService;
    
    [ObservableProperty]
    private ObservableCollection<Product> _products;
    
    [ObservableProperty]
    private bool _isLoading;
    
    [ObservableProperty]
    private string _errorMessage;
    
    public ProductViewModel(IProductService productService)
    {
        _productService = productService;
        Products = new ObservableCollection<Product>();
    }
    
    [RelayCommand]
    private async Task LoadProducts()
    {
        IsLoading = true;
        ErrorMessage = string.Empty;
        
        try
        {
            var products = await _productService.GetProductsAsync();
            Products.Clear();
            foreach (var product in products)
            {
                Products.Add(product);
            }
        }
        catch (Exception ex)
        {
            ErrorMessage = $"Error: {ex.Message}";
        }
        finally
        {
            IsLoading = false;
        }
    }
    
    [RelayCommand]
    private async Task DeleteProduct(Product product)
    {
        await _productService.DeleteProductAsync(product.Id);
        Products.Remove(product);
    }
}
```

**ProductsPage.xaml**
```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProductsPage"
             Title="Products">
    
    <ContentPage.BindingContext>
        <vm:ProductViewModel />
    </ContentPage.BindingContext>
    
    <Grid RowDefinitions="Auto,*">
        <ActivityIndicator 
            Grid.Row="0"
            IsRunning="{Binding IsLoading}"
            IsVisible="{Binding IsLoading}" />
        
        <CollectionView 
            Grid.Row="1"
            ItemsSource="{Binding Products}">
            <CollectionView.ItemTemplate>
                <DataTemplate>
                    <SwipeView>
                        <SwipeView.RightItems>
                            <SwipeItems>
                                <SwipeItem 
                                    Text="Delete"
                                    BackgroundColor="Red"
                                    Command="{Binding Source={RelativeSource AncestorType={x:Type vm:ProductViewModel}}, Path=DeleteProductCommand}"
                                    CommandParameter="{Binding .}" />
                            </SwipeItems>
                        </SwipeView.RightItems>
                        
                        <Grid Padding="10" ColumnDefinitions="*,Auto">
                            <Label Text="{Binding Name}" FontSize="18" />
                            <Label Grid.Column="1" Text="{Binding Price, StringFormat='${0:N2}'}" />
                        </Grid>
                    </SwipeView>
                </DataTemplate>
            </CollectionView.ItemTemplate>
        </CollectionView>
    </Grid>
</ContentPage>
```

---

## Ionic Templates

### 1. Angular + Ionic

**products.page.ts**
```typescript
@Component({
  selector: 'app-products',
  templateUrl: './products.page.html',
  styleUrls: ['./products.page.scss'],
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

**products.page.html**
```html
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

## Usage Instructions

1. **Choose your framework template** from above
2. **Copy the relevant code** to your project
3. **Adapt** package names, imports, and business logic
4. **Run** dependency installation commands
5. **Test** the template implementation

## Notes

- All templates follow **production-ready patterns**
- Use as **starting points**, not complete solutions
- Adapt to your **specific requirements**
- Follow framework-specific **best practices**

---

**Last Updated:** January 2025
