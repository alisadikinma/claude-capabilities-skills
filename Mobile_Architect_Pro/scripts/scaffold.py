#!/usr/bin/env python3
"""
Mobile Project Scaffolding Tool
Generates boilerplate structure for Flutter, React Native, Xamarin, Ionic, and Kotlin projects
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Dict, List


class ProjectScaffolder:
    """Generate boilerplate project structures"""
    
    def __init__(self, framework: str, project_path: str, template: str = 'default'):
        self.framework = framework.lower()
        self.project_path = Path(project_path)
        self.template = template
        self.project_name = self.project_path.name
    
    def scaffold(self):
        """Main scaffolding method"""
        print(f"\n🚀 Scaffolding {self.framework} project: {self.project_name}")
        print(f"📁 Location: {self.project_path}")
        print(f"📋 Template: {self.template}\n")
        
        if not self.project_path.exists():
            print(f"❌ Project path does not exist: {self.project_path}")
            print("   Please create the project first using framework CLI")
            return False
        
        scaffolders = {
            'flutter': self._scaffold_flutter,
            'react-native': self._scaffold_react_native,
            'xamarin': self._scaffold_xamarin,
            'ionic': self._scaffold_ionic,
            'kotlin': self._scaffold_kotlin,
        }
        
        scaffolder = scaffolders.get(self.framework)
        if not scaffolder:
            print(f"❌ Unsupported framework: {self.framework}")
            return False
        
        try:
            scaffolder()
            print("\n✅ Scaffolding complete!")
            self._print_next_steps()
            return True
        except Exception as e:
            print(f"\n❌ Error during scaffolding: {e}")
            return False
    
    def _scaffold_flutter(self):
        """Scaffold Flutter project structure"""
        base = self.project_path / 'lib'
        
        structure = {
            'core/constants': [],
            'core/theme': ['app_theme.dart'],
            'core/utils': ['extensions.dart'],
            'core/network': ['api_client.dart'],
            'data/models': ['product.dart'],
            'data/repositories': ['product_repository_impl.dart'],
            'data/datasources/local': ['local_datasource.dart'],
            'data/datasources/remote': ['remote_datasource.dart'],
            'domain/entities': ['product.dart'],
            'domain/repositories': ['product_repository.dart'],
            'domain/usecases': ['get_products_usecase.dart'],
            'presentation/blocs': ['product_bloc.dart', 'product_event.dart', 'product_state.dart'],
            'presentation/pages': ['home_page.dart', 'product_page.dart'],
            'presentation/widgets': ['product_card.dart'],
        }
        
        self._create_structure(base, structure)
        
        # Create injection container
        self._create_file(
            base / 'injection_container.dart',
            self._flutter_injection_container()
        )
        
        print("✅ Flutter Clean Architecture structure created")
    
    def _scaffold_react_native(self):
        """Scaffold React Native project structure"""
        base = self.project_path / 'src'
        
        structure = {
            'components': ['ProductCard.tsx', 'LoadingSpinner.tsx'],
            'screens': ['HomeScreen.tsx', 'ProductScreen.tsx', 'ProductDetailScreen.tsx'],
            'navigation': ['AppNavigator.tsx'],
            'hooks': ['useProducts.ts', 'useAuth.ts'],
            'services': ['api.ts'],
            'store/slices': ['authSlice.ts', 'productSlice.ts'],
            'utils': ['constants.ts', 'helpers.ts'],
            'types': ['index.ts'],
        }
        
        self._create_structure(base, structure)
        
        # Create store index
        self._create_file(
            base / 'store' / 'index.ts',
            self._react_native_store()
        )
        
        print("✅ React Native Redux structure created")
    
    def _scaffold_xamarin(self):
        """Scaffold Xamarin/MAUI project structure"""
        base = self.project_path
        
        structure = {
            'Models': ['Product.cs'],
            'ViewModels': ['ProductViewModel.cs', 'BaseViewModel.cs'],
            'Views': ['ProductsPage.xaml', 'ProductsPage.xaml.cs'],
            'Services': ['IProductService.cs', 'ProductService.cs', 'IApiService.cs'],
            'Helpers': ['Constants.cs'],
            'Converters': ['BoolToColorConverter.cs'],
        }
        
        self._create_structure(base, structure)
        
        print("✅ Xamarin MVVM structure created")
    
    def _scaffold_ionic(self):
        """Scaffold Ionic project structure"""
        base = self.project_path / 'src'
        
        # Detect framework variant
        if (base.parent / 'angular.json').exists():
            variant = 'angular'
        elif 'react' in str(self.project_path):
            variant = 'react'
        else:
            variant = 'vue'
        
        if variant == 'angular':
            structure = {
                'app/core/services': ['product.service.ts', 'auth.service.ts'],
                'app/core/guards': ['auth.guard.ts'],
                'app/core/interceptors': ['api.interceptor.ts'],
                'app/shared/components': ['product-card.component.ts'],
                'app/pages/home': ['home.page.ts', 'home.page.html', 'home.page.scss'],
                'app/pages/products': ['products.page.ts', 'products.page.html', 'products.page.scss'],
            }
        elif variant == 'react':
            structure = {
                'components': ['ProductCard.tsx'],
                'pages': ['Home.tsx', 'Products.tsx', 'ProductDetail.tsx'],
                'hooks': ['useProducts.ts'],
                'services': ['api.ts'],
                'store': ['useStore.ts'],
            }
        else:  # vue
            structure = {
                'components': ['ProductCard.vue'],
                'views': ['Home.vue', 'Products.vue', 'ProductDetail.vue'],
                'composables': ['useProducts.ts'],
                'services': ['api.ts'],
                'stores': ['products.ts'],
            }
        
        self._create_structure(base, structure)
        
        print(f"✅ Ionic {variant.capitalize()} structure created")
    
    def _scaffold_kotlin(self):
        """Scaffold Kotlin Android project structure"""
        base = self.project_path / 'app' / 'src' / 'main' / 'java' / 'com' / 'mycompany' / 'myapp'
        
        structure = {
            'di': ['AppModule.kt', 'NetworkModule.kt'],
            'data/local/dao': ['ProductDao.kt'],
            'data/local/database': ['AppDatabase.kt'],
            'data/remote/api': ['ProductApi.kt'],
            'data/remote/dto': ['ProductDto.kt'],
            'data/repository': ['ProductRepositoryImpl.kt'],
            'domain/model': ['Product.kt'],
            'domain/repository': ['ProductRepository.kt'],
            'domain/usecase': ['GetProductsUseCase.kt'],
            'presentation/products': ['ProductsScreen.kt', 'ProductsViewModel.kt'],
            'presentation/theme': ['Theme.kt', 'Color.kt', 'Type.kt'],
            'util': ['Resource.kt', 'Extensions.kt'],
        }
        
        self._create_structure(base, structure)
        
        print("✅ Kotlin Clean Architecture + Compose structure created")
    
    def _create_structure(self, base: Path, structure: Dict[str, List[str]]):
        """Create directory structure and files"""
        for dir_path, files in structure.items():
            full_path = base / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created: {dir_path}/")
            
            for file_name in files:
                file_path = full_path / file_name
                if not file_path.exists():
                    self._create_file(file_path, self._get_file_template(file_name))
                    print(f"   📄 {file_name}")
    
    def _create_file(self, path: Path, content: str):
        """Create file with content"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
    
    def _get_file_template(self, filename: str) -> str:
        """Get basic template for file"""
        if filename.endswith('.dart'):
            return "// TODO: Implement\n"
        elif filename.endswith('.ts') or filename.endswith('.tsx'):
            return "// TODO: Implement\nexport {};\n"
        elif filename.endswith('.cs'):
            return "// TODO: Implement\n"
        elif filename.endswith('.kt'):
            return "// TODO: Implement\n"
        elif filename.endswith('.vue'):
            return "<template>\n  <!-- TODO -->\n</template>\n\n<script setup lang=\"ts\">\n// TODO\n</script>\n"
        elif filename.endswith('.html'):
            return "<!-- TODO: Implement -->\n"
        else:
            return "# TODO: Implement\n"
    
    def _flutter_injection_container(self) -> str:
        """Generate Flutter dependency injection setup"""
        return """import 'package:get_it/get_it.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // BLoCs
  // sl.registerFactory(() => ProductBloc(sl()));
  
  // Use cases
  // sl.registerLazySingleton(() => GetProductsUseCase(sl()));
  
  // Repositories
  // sl.registerLazySingleton<ProductRepository>(
  //   () => ProductRepositoryImpl(sl(), sl())
  // );
  
  // Data sources
  // sl.registerLazySingleton<RemoteDataSource>(() => RemoteDataSourceImpl(sl()));
  // sl.registerLazySingleton<LocalDataSource>(() => LocalDataSourceImpl());
  
  // External
  // final sharedPreferences = await SharedPreferences.getInstance();
  // sl.registerLazySingleton(() => sharedPreferences);
}
"""
    
    def _react_native_store(self) -> str:
        """Generate React Native Redux store"""
        return """import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import productReducer from './slices/productSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    product: productReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
"""
    
    def _print_next_steps(self):
        """Print next steps for user"""
        steps = {
            'flutter': [
                "1. Run: flutter pub get",
                "2. Implement business logic in domain/usecases",
                "3. Implement data sources in data/datasources",
                "4. Set up dependency injection in injection_container.dart",
                "5. Run: flutter run"
            ],
            'react-native': [
                "1. Run: npm install (or yarn install)",
                "2. Implement API calls in src/services/api.ts",
                "3. Create Redux slices in src/store/slices",
                "4. Build screens in src/screens",
                "5. Run: npm start"
            ],
            'xamarin': [
                "1. Implement ViewModels",
                "2. Create XAML views",
                "3. Set up services and repositories",
                "4. Configure dependency injection",
                "5. Build and run"
            ],
            'ionic': [
                "1. Run: npm install",
                "2. Implement services",
                "3. Create pages/components",
                "4. Set up state management",
                "5. Run: ionic serve"
            ],
            'kotlin': [
                "1. Sync Gradle",
                "2. Implement ViewModels and UseCases",
                "3. Set up Room database and Retrofit",
                "4. Configure Hilt modules",
                "5. Build screens with Jetpack Compose"
            ]
        }
        
        print("\n📝 Next Steps:")
        for step in steps.get(self.framework, []):
            print(f"   {step}")


def main():
    parser = argparse.ArgumentParser(
        description='Scaffold mobile project structure'
    )
    parser.add_argument(
        'framework',
        choices=['flutter', 'react-native', 'xamarin', 'ionic', 'kotlin'],
        help='Framework to scaffold'
    )
    parser.add_argument(
        'project_path',
        help='Path to existing project'
    )
    parser.add_argument(
        '--template',
        default='default',
        help='Template to use (default, bloc, redux, mvvm, etc.)'
    )
    
    args = parser.parse_args()
    
    scaffolder = ProjectScaffolder(
        framework=args.framework,
        project_path=args.project_path,
        template=args.template
    )
    
    success = scaffolder.scaffold()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
