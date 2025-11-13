# Xamarin & .NET MAUI Development Guide

Comprehensive reference for production Xamarin.Forms and .NET MAUI applications with C#, MVVM, and cross-platform best practices.

---

## Table of Contents

1. [Xamarin vs MAUI](#xamarin-vs-maui)
2. [Project Setup](#project-setup)
3. [MVVM Pattern](#mvvm-pattern)
4. [Data Binding](#data-binding)
5. [Navigation](#navigation)
6. [Data Persistence](#data-persistence)
7. [REST APIs](#rest-apis)
8. [Dependency Injection](#dependency-injection)
9. [Platform-Specific Code](#platform-specific-code)
10. [Build & Deployment](#build--deployment)

---

## Xamarin vs MAUI

### Key Differences

| Feature | Xamarin.Forms | .NET MAUI |
|---------|--------------|-----------|
| **Framework** | .NET Standard 2.0 | .NET 6/7/8 |
| **Project Structure** | Multiple projects | Single project |
| **Performance** | Good | Better (Hot Reload, native) |
| **UI Controls** | XAML | XAML + C# Markup |
| **Platform Support** | iOS, Android, UWP | iOS, Android, macOS, Windows |
| **Status** | Legacy (support until May 2024) | Active development |

### Migration Path

**Recommendation:** New projects should use .NET MAUI. Existing Xamarin apps can migrate gradually.

```bash
# MAUI Upgrade Assistant
dotnet tool install -g upgrade-assistant
upgrade-assistant upgrade MyXamarinApp.sln
```

---

## Project Setup

### .NET MAUI Project

```bash
# Install MAUI workload
dotnet workload install maui

# Create new project
dotnet new maui -n MyMauiApp

# Run
dotnet build
dotnet run
```

### Project Structure

```
MyMauiApp/
├── Platforms/
│   ├── Android/
│   ├── iOS/
│   ├── MacCatalyst/
│   └── Windows/
├── Resources/
│   ├── Images/
│   ├── Fonts/
│   └── Styles/
├── Models/
├── ViewModels/
├── Views/
├── Services/
├── MauiProgram.cs
└── App.xaml
```

### Essential NuGet Packages

```xml
<!-- .csproj -->
<ItemGroup>
  <!-- MVVM -->
  <PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.2" />
  
  <!-- HTTP -->
  <PackageReference Include="Refit" Version="7.0.0" />
  
  <!-- Database -->
  <PackageReference Include="sqlite-net-pcl" Version="1.8.116" />
  <PackageReference Include="SQLitePCLRaw.bundle_green" Version="2.1.6" />
  
  <!-- Dependency Injection -->
  <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
  
  <!-- JSON -->
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
  
  <!-- UI -->
  <PackageReference Include="CommunityToolkit.Maui" Version="7.0.0" />
</ItemGroup>
```

---

## MVVM Pattern

### ViewModel Base (CommunityToolkit.Mvvm)

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public partial class ProductViewModel : ObservableObject
{
    private readonly IProductService _productService;
    
    [ObservableProperty]
    private string _name;
    
    [ObservableProperty]
    private decimal _price;
    
    [ObservableProperty]
    private bool _isLoading;
    
    [ObservableProperty]
    private ObservableCollection<Product> _products;
    
    public ProductViewModel(IProductService productService)
    {
        _productService = productService;
        Products = new ObservableCollection<Product>();
    }
    
    [RelayCommand]
    private async Task LoadProducts()
    {
        IsLoading = true;
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
            // Handle error
            await Shell.Current.DisplayAlert("Error", ex.Message, "OK");
        }
        finally
        {
            IsLoading = false;
        }
    }
    
    [RelayCommand]
    private async Task AddProduct()
    {
        if (string.IsNullOrWhiteSpace(Name))
            return;
            
        var product = new Product 
        { 
            Name = Name, 
            Price = Price 
        };
        
        await _productService.AddProductAsync(product);
        Products.Add(product);
        
        // Clear form
        Name = string.Empty;
        Price = 0;
    }
    
    [RelayCommand]
    private async Task DeleteProduct(Product product)
    {
        await _productService.DeleteProductAsync(product.Id);
        Products.Remove(product);
    }
}
```

### Manual ViewModel (Without Toolkit)

```csharp
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows.Input;

public class ProductViewModel : INotifyPropertyChanged
{
    private string _name;
    private decimal _price;
    private bool _isLoading;
    
    public string Name
    {
        get => _name;
        set
        {
            if (_name != value)
            {
                _name = value;
                OnPropertyChanged();
            }
        }
    }
    
    public decimal Price
    {
        get => _price;
        set
        {
            if (_price != value)
            {
                _price = value;
                OnPropertyChanged();
            }
        }
    }
    
    public bool IsLoading
    {
        get => _isLoading;
        set
        {
            if (_isLoading != value)
            {
                _isLoading = value;
                OnPropertyChanged();
            }
        }
    }
    
    public ICommand LoadProductsCommand { get; }
    public ICommand AddProductCommand { get; }
    
    public ProductViewModel()
    {
        LoadProductsCommand = new Command(async () => await LoadProducts());
        AddProductCommand = new Command(async () => await AddProduct());
    }
    
    private async Task LoadProducts()
    {
        IsLoading = true;
        // Load logic
        IsLoading = false;
    }
    
    private async Task AddProduct()
    {
        // Add logic
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

---

## Data Binding

### XAML View with Bindings

```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:viewmodels="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.ProductPage"
             Title="Products">
    
    <ContentPage.BindingContext>
        <viewmodels:ProductViewModel />
    </ContentPage.BindingContext>
    
    <Grid RowDefinitions="Auto,*" Padding="20">
        
        <!-- Form -->
        <VerticalStackLayout Grid.Row="0" Spacing="10">
            <Entry 
                Placeholder="Product Name"
                Text="{Binding Name}" />
            
            <Entry 
                Placeholder="Price"
                Keyboard="Numeric"
                Text="{Binding Price}" />
            
            <Button 
                Text="Add Product"
                Command="{Binding AddProductCommand}" />
            
            <ActivityIndicator 
                IsRunning="{Binding IsLoading}"
                IsVisible="{Binding IsLoading}" />
        </VerticalStackLayout>
        
        <!-- List -->
        <CollectionView 
            Grid.Row="1"
            ItemsSource="{Binding Products}"
            SelectionMode="None">
            
            <CollectionView.ItemTemplate>
                <DataTemplate>
                    <SwipeView>
                        <SwipeView.RightItems>
                            <SwipeItems>
                                <SwipeItem 
                                    Text="Delete"
                                    BackgroundColor="Red"
                                    Command="{Binding Source={RelativeSource AncestorType={x:Type viewmodels:ProductViewModel}}, Path=DeleteProductCommand}"
                                    CommandParameter="{Binding .}" />
                            </SwipeItems>
                        </SwipeView.RightItems>
                        
                        <Grid Padding="10" ColumnDefinitions="*,Auto">
                            <Label 
                                Text="{Binding Name}"
                                FontSize="18"
                                VerticalOptions="Center" />
                            
                            <Label 
                                Grid.Column="1"
                                Text="{Binding Price, StringFormat='${0:N2}'}"
                                FontSize="16"
                                TextColor="Green"
                                VerticalOptions="Center" />
                        </Grid>
                    </SwipeView>
                </DataTemplate>
            </CollectionView.ItemTemplate>
        </CollectionView>
    </Grid>
</ContentPage>
```

### Value Converters

```csharp
// Converters/BoolToColorConverter.cs
public class BoolToColorConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is bool isActive)
        {
            return isActive ? Colors.Green : Colors.Red;
        }
        return Colors.Gray;
    }
    
    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

// Usage in XAML
<ContentPage.Resources>
    <converters:BoolToColorConverter x:Key="BoolToColorConverter" />
</ContentPage.Resources>

<Label 
    Text="{Binding IsActive, StringFormat='Status: {0}'}"
    TextColor="{Binding IsActive, Converter={StaticResource BoolToColorConverter}}" />
```

---

## Navigation

### Shell Navigation (MAUI)

```xml
<!-- AppShell.xaml -->
<?xml version="1.0" encoding="UTF-8" ?>
<Shell
    xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
    xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
    xmlns:views="clr-namespace:MyApp.Views"
    x:Class="MyApp.AppShell">
    
    <TabBar>
        <ShellContent
            Title="Home"
            Icon="home.png"
            ContentTemplate="{DataTemplate views:HomePage}" />
        
        <ShellContent
            Title="Products"
            Icon="products.png"
            ContentTemplate="{DataTemplate views:ProductsPage}" />
        
        <ShellContent
            Title="Profile"
            Icon="profile.png"
            ContentTemplate="{DataTemplate views:ProfilePage}" />
    </TabBar>
</Shell>
```

```csharp
// AppShell.xaml.cs
public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        
        // Register routes for navigation
        Routing.RegisterRoute(nameof(ProductDetailPage), typeof(ProductDetailPage));
        Routing.RegisterRoute(nameof(EditProductPage), typeof(EditProductPage));
    }
}

// Navigation in ViewModel
await Shell.Current.GoToAsync(nameof(ProductDetailPage));

// With parameters
await Shell.Current.GoToAsync($"{nameof(ProductDetailPage)}?ProductId={productId}");

// Receiving parameters
[QueryProperty(nameof(ProductId), "ProductId")]
public partial class ProductDetailViewModel : ObservableObject
{
    [ObservableProperty]
    private string _productId;
    
    partial void OnProductIdChanged(string value)
    {
        LoadProduct(value);
    }
}
```

---

## Data Persistence

### SQLite with sqlite-net-pcl

```csharp
// Models/Product.cs
using SQLite;

public class Product
{
    [PrimaryKey, AutoIncrement]
    public int Id { get; set; }
    
    [MaxLength(200)]
    public string Name { get; set; }
    
    public decimal Price { get; set; }
    
    public DateTime CreatedAt { get; set; }
}

// Services/DatabaseService.cs
public class DatabaseService
{
    private SQLiteAsyncConnection _database;
    
    public DatabaseService()
    {
    }
    
    private async Task Init()
    {
        if (_database is not null)
            return;
        
        var dbPath = Path.Combine(FileSystem.AppDataDirectory, "products.db");
        _database = new SQLiteAsyncConnection(dbPath);
        await _database.CreateTableAsync<Product>();
    }
    
    public async Task<List<Product>> GetProductsAsync()
    {
        await Init();
        return await _database.Table<Product>().ToListAsync();
    }
    
    public async Task<Product> GetProductAsync(int id)
    {
        await Init();
        return await _database.Table<Product>()
            .Where(p => p.Id == id)
            .FirstOrDefaultAsync();
    }
    
    public async Task<int> SaveProductAsync(Product product)
    {
        await Init();
        
        if (product.Id != 0)
            return await _database.UpdateAsync(product);
        else
            return await _database.InsertAsync(product);
    }
    
    public async Task<int> DeleteProductAsync(Product product)
    {
        await Init();
        return await _database.DeleteAsync(product);
    }
}
```

### Preferences (Key-Value Storage)

```csharp
// Save
Preferences.Set("username", "john_doe");
Preferences.Set("is_logged_in", true);
Preferences.Set("last_sync", DateTime.Now);

// Read
var username = Preferences.Get("username", string.Empty);
var isLoggedIn = Preferences.Get("is_logged_in", false);
var lastSync = Preferences.Get("last_sync", DateTime.MinValue);

// Remove
Preferences.Remove("username");

// Clear all
Preferences.Clear();
```

---

## REST APIs

### Refit (Type-Safe HTTP Client)

```csharp
// Interfaces/IApiService.cs
using Refit;

public interface IApiService
{
    [Get("/products")]
    Task<List<Product>> GetProductsAsync();
    
    [Get("/products/{id}")]
    Task<Product> GetProductAsync(int id);
    
    [Post("/products")]
    Task<Product> CreateProductAsync([Body] Product product);
    
    [Put("/products/{id}")]
    Task UpdateProductAsync(int id, [Body] Product product);
    
    [Delete("/products/{id}")]
    Task DeleteProductAsync(int id);
    
    [Get("/products/search")]
    Task<List<Product>> SearchProductsAsync([Query] string query);
}

// Register in MauiProgram.cs
builder.Services.AddRefitClient<IApiService>()
    .ConfigureHttpClient(c => c.BaseAddress = new Uri("https://api.example.com"));

// Usage in Service
public class ProductService
{
    private readonly IApiService _apiService;
    
    public ProductService(IApiService apiService)
    {
        _apiService = apiService;
    }
    
    public async Task<List<Product>> GetProductsAsync()
    {
        try
        {
            return await _apiService.GetProductsAsync();
        }
        catch (ApiException ex)
        {
            // Handle API errors
            throw new Exception($"API Error: {ex.StatusCode}");
        }
    }
}
```

### HttpClient (Manual Approach)

```csharp
public class ApiService
{
    private readonly HttpClient _httpClient;
    
    public ApiService()
    {
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri("https://api.example.com")
        };
        _httpClient.DefaultRequestHeaders.Add("Authorization", "Bearer token");
    }
    
    public async Task<List<Product>> GetProductsAsync()
    {
        var response = await _httpClient.GetAsync("/products");
        response.EnsureSuccessStatusCode();
        
        var json = await response.Content.ReadAsStringAsync();
        return JsonConvert.DeserializeObject<List<Product>>(json);
    }
    
    public async Task<Product> CreateProductAsync(Product product)
    {
        var json = JsonConvert.SerializeObject(product);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        var response = await _httpClient.PostAsync("/products", content);
        response.EnsureSuccessStatusCode();
        
        var responseJson = await response.Content.ReadAsStringAsync();
        return JsonConvert.DeserializeObject<Product>(responseJson);
    }
}
```

---

## Dependency Injection

### Configuration (MauiProgram.cs)

```csharp
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            });
        
        // Services
        builder.Services.AddSingleton<DatabaseService>();
        builder.Services.AddSingleton<IApiService>(sp => 
            RestService.For<IApiService>("https://api.example.com"));
        builder.Services.AddTransient<IProductService, ProductService>();
        
        // ViewModels
        builder.Services.AddTransient<ProductViewModel>();
        builder.Services.AddTransient<ProductDetailViewModel>();
        
        // Views
        builder.Services.AddTransient<ProductPage>();
        builder.Services.AddTransient<ProductDetailPage>();
        
        return builder.Build();
    }
}

// Usage in View
public partial class ProductPage : ContentPage
{
    public ProductPage(ProductViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}
```

---

## Platform-Specific Code

### Conditional Compilation

```csharp
public void DoSomething()
{
#if ANDROID
    // Android-specific code
    var context = Platform.CurrentActivity;
#elif IOS
    // iOS-specific code
    var viewController = Platform.GetCurrentUIViewController();
#elif WINDOWS
    // Windows-specific code
    var window = Application.Current.Windows[0];
#endif
}
```

### Dependency Service Pattern

```csharp
// Interfaces/IDeviceService.cs
public interface IDeviceService
{
    string GetDeviceId();
    void Vibrate(int milliseconds);
}

// Platforms/Android/Services/DeviceService.cs
using Android.App;
using Android.OS;

public class DeviceService : IDeviceService
{
    public string GetDeviceId()
    {
        return Settings.Secure.GetString(
            Application.Context.ContentResolver, 
            Settings.Secure.AndroidId
        );
    }
    
    public void Vibrate(int milliseconds)
    {
        var vibrator = (Vibrator)Application.Context
            .GetSystemService(Context.VibratorService);
        vibrator.Vibrate(milliseconds);
    }
}

// Register in MauiProgram.cs
#if ANDROID
builder.Services.AddSingleton<IDeviceService, Platforms.Android.Services.DeviceService>();
#elif IOS
builder.Services.AddSingleton<IDeviceService, Platforms.iOS.Services.DeviceService>();
#endif
```

---

## Build & Deployment

### Android Release

```bash
# Build release APK
dotnet build -c Release -f net8.0-android

# Build AAB (App Bundle)
dotnet publish -c Release -f net8.0-android -p:AndroidPackageFormat=aab
```

**Sign Configuration (csproj):**
```xml
<PropertyGroup Condition="'$(Configuration)' == 'Release'">
    <AndroidKeyStore>True</AndroidKeyStore>
    <AndroidSigningKeyStore>myapp.keystore</AndroidSigningKeyStore>
    <AndroidSigningKeyAlias>myapp</AndroidSigningKeyAlias>
    <AndroidSigningKeyPass>password</AndroidSigningKeyPass>
    <AndroidSigningStorePass>password</AndroidSigningStorePass>
</PropertyGroup>
```

### iOS Release

```bash
# Build for iOS
dotnet build -c Release -f net8.0-ios

# Archive (use Xcode or Visual Studio)
```

### Windows Release

```bash
# Build MSIX package
dotnet publish -c Release -f net8.0-windows10.0.19041.0 -p:GenerateAppxPackageOnBuild=true
```

---

## Common Issues & Solutions

### SQLite Initialization

```csharp
// Add to MauiProgram.cs
SQLitePCL.Batteries_V2.Init();
```

### Hot Reload Issues

```bash
# Clean and rebuild
dotnet clean
dotnet build
```

### Platform-Specific Crashes

- Check Platforms/ folder for correct initialization
- Verify permissions in AndroidManifest.xml / Info.plist
- Test on physical devices, not just emulators

---

**See Also:**
- Main SKILL.md for architecture patterns
- `assets/templates/Xamarin/` for project templates
- Microsoft MAUI documentation: https://learn.microsoft.com/dotnet/maui

**Last Updated:** January 2025
