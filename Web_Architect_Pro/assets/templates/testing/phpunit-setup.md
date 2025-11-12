# PHPUnit Setup - Laravel/PHP Testing

**For:** Laravel 10+, PHP 8.1+  
**Coverage:** Unit, Feature, Browser testing  
**Tools:** PHPUnit, Laravel Testing, Pest (optional)

---

## 📦 Installation

```bash
# PHPUnit (included in Laravel)
composer require --dev phpunit/phpunit

# Laravel testing tools
composer require --dev laravel/dusk  # Browser testing

# Pest (modern alternative)
composer require --dev pestphp/pest
composer require --dev pestphp/pest-plugin-laravel
```

---

## 📂 Project Structure

```
laravel-app/
├── tests/
│   ├── Unit/
│   │   ├── Models/
│   │   │   ├── UserTest.php
│   │   │   └── ProductTest.php
│   │   ├── Services/
│   │   │   ├── PaymentServiceTest.php
│   │   │   └── EmailServiceTest.php
│   │   └── Helpers/
│   │       └── StringHelperTest.php
│   ├── Feature/
│   │   ├── Auth/
│   │   │   ├── LoginTest.php
│   │   │   └── RegistrationTest.php
│   │   ├── API/
│   │   │   ├── UserApiTest.php
│   │   │   └── ProductApiTest.php
│   │   └── Http/
│   │       └── Controllers/
│   │           └── UserControllerTest.php
│   ├── Browser/
│   │   └── ExampleTest.php  # Dusk tests
│   ├── CreatesApplication.php
│   └── TestCase.php
├── phpunit.xml
└── .env.testing
```

---

## ⚙️ Configuration Files

### phpunit.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
         failOnWarning="true"
         failOnRisky="true"
         failOnEmptyTestSuite="true"
         beStrictAboutOutputDuringTests="true"
         cacheDirectory=".phpunit.cache"
         backupStaticProperties="false">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory>tests/Feature</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <include>
            <directory suffix=".php">./app</directory>
        </include>
        <exclude>
            <directory>./app/Console/Kernel.php</directory>
            <directory>./app/Http/Middleware</directory>
        </exclude>
        <report>
            <html outputDirectory="coverage"/>
            <text outputFile="coverage.txt"/>
        </report>
    </coverage>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="CACHE_DRIVER" value="array"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
        <env name="TELESCOPE_ENABLED" value="false"/>
    </php>
</phpunit>
```

### .env.testing

```env
APP_ENV=testing
APP_KEY=base64:test-key-here
APP_DEBUG=true

DB_CONNECTION=sqlite
DB_DATABASE=:memory:

CACHE_DRIVER=array
SESSION_DRIVER=array
QUEUE_CONNECTION=sync
MAIL_MAILER=array

BCRYPT_ROUNDS=4
```

---

## 🔧 Base TestCase

### tests/TestCase.php

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;
    use RefreshDatabase;  // Reset DB after each test
    use WithFaker;        // Faker helper

    protected function setUp(): void
    {
        parent::setUp();
        
        // Run migrations
        $this->artisan('migrate');
        
        // Seed if needed
        // $this->seed();
    }

    protected function tearDown(): void
    {
        parent::tearDown();
    }

    /**
     * Create authenticated user
     */
    protected function authenticatedUser()
    {
        $user = User::factory()->create();
        $this->actingAs($user);
        return $user;
    }

    /**
     * Assert JSON structure
     */
    protected function assertJsonStructure($response, array $structure)
    {
        $response->assertJsonStructure($structure);
    }
}
```

---

## 📝 Test Examples

### 1. Unit Test - Models

```php
<?php
// tests/Unit/Models/UserTest.php

namespace Tests\Unit\Models;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserTest extends TestCase
{
    public function test_user_has_fillable_attributes()
    {
        $user = new User();
        
        $this->assertEquals(
            ['name', 'email', 'password'],
            $user->getFillable()
        );
    }

    public function test_user_password_is_hashed()
    {
        $user = User::factory()->create([
            'password' => 'password123'
        ]);
        
        $this->assertNotEquals('password123', $user->password);
        $this->assertTrue(Hash::check('password123', $user->password));
    }

    public function test_user_has_many_posts()
    {
        $user = User::factory()
            ->hasPosts(3)
            ->create();
        
        $this->assertCount(3, $user->posts);
    }

    public function test_user_full_name_attribute()
    {
        $user = User::factory()->create([
            'first_name' => 'John',
            'last_name' => 'Doe'
        ]);
        
        $this->assertEquals('John Doe', $user->full_name);
    }
}
```

### 2. Unit Test - Services

```php
<?php
// tests/Unit/Services/PaymentServiceTest.php

namespace Tests\Unit\Services;

use Tests\TestCase;
use App\Services\PaymentService;
use App\Models\User;
use Mockery;

class PaymentServiceTest extends TestCase
{
    protected PaymentService $service;

    protected function setUp(): void
    {
        parent::setUp();
        $this->service = new PaymentService();
    }

    public function test_calculate_total_with_tax()
    {
        $amount = 100;
        $taxRate = 0.1;
        
        $total = $this->service->calculateTotal($amount, $taxRate);
        
        $this->assertEquals(110, $total);
    }

    public function test_process_payment_with_mock()
    {
        $mock = Mockery::mock('alias:Stripe\Charge');
        $mock->shouldReceive('create')
            ->once()
            ->andReturn(['status' => 'succeeded', 'id' => 'ch_123']);
        
        $result = $this->service->processPayment(100, 'tok_test');
        
        $this->assertEquals('succeeded', $result['status']);
    }

    protected function tearDown(): void
    {
        Mockery::close();
        parent::tearDown();
    }
}
```

### 3. Feature Test - HTTP

```php
<?php
// tests/Feature/Http/UserControllerTest.php

namespace Tests\Feature\Http;

use Tests\TestCase;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_view_profile()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->get('/profile');
        
        $response->assertOk();
        $response->assertSee($user->name);
        $response->assertViewIs('profile.show');
    }

    public function test_guest_cannot_view_profile()
    {
        $response = $this->get('/profile');
        
        $response->assertRedirect('/login');
    }

    public function test_user_can_update_profile()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->put('/profile', [
                'name' => 'Updated Name',
                'email' => 'updated@example.com'
            ]);
        
        $response->assertRedirect('/profile');
        $this->assertEquals('Updated Name', $user->fresh()->name);
    }

    public function test_profile_update_validation()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->put('/profile', [
                'name' => '',  // Invalid
                'email' => 'not-an-email'  // Invalid
            ]);
        
        $response->assertSessionHasErrors(['name', 'email']);
    }
}
```

### 4. Feature Test - API

```php
<?php
// tests/Feature/API/UserApiTest.php

namespace Tests\Feature\API;

use Tests\TestCase;
use App\Models\User;
use Laravel\Sanctum\Sanctum;

class UserApiTest extends TestCase
{
    public function test_can_register_user()
    {
        $userData = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123'
        ];
        
        $response = $this->postJson('/api/register', $userData);
        
        $response->assertCreated();
        $response->assertJsonStructure([
            'user' => ['id', 'name', 'email'],
            'token'
        ]);
        
        $this->assertDatabaseHas('users', [
            'email' => 'test@example.com'
        ]);
    }

    public function test_can_login()
    {
        $user = User::factory()->create([
            'password' => bcrypt('password123')
        ]);
        
        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => 'password123'
        ]);
        
        $response->assertOk();
        $response->assertJsonStructure([
            'user', 'token'
        ]);
    }

    public function test_authenticated_user_can_get_profile()
    {
        Sanctum::actingAs(
            User::factory()->create(),
            ['*']
        );
        
        $response = $this->getJson('/api/user');
        
        $response->assertOk();
        $response->assertJsonStructure([
            'id', 'name', 'email', 'created_at'
        ]);
    }

    public function test_unauthenticated_request_returns_401()
    {
        $response = $this->getJson('/api/user');
        
        $response->assertUnauthorized();
    }

    public function test_can_paginate_users()
    {
        User::factory()->count(25)->create();
        
        $response = $this->getJson('/api/users?page=1&per_page=10');
        
        $response->assertOk();
        $response->assertJsonStructure([
            'data' => [
                '*' => ['id', 'name', 'email']
            ],
            'current_page',
            'total',
            'per_page'
        ]);
        $response->assertJsonCount(10, 'data');
    }
}
```

### 5. Feature Test - Database

```php
<?php
// tests/Feature/Database/UserDatabaseTest.php

namespace Tests\Feature\Database;

use Tests\TestCase;
use App\Models\User;
use App\Models\Post;

class UserDatabaseTest extends TestCase
{
    public function test_user_creation_in_database()
    {
        $user = User::create([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => bcrypt('password')
        ]);
        
        $this->assertDatabaseHas('users', [
            'email' => 'test@example.com'
        ]);
    }

    public function test_user_deletion_cascades()
    {
        $user = User::factory()
            ->hasPosts(3)
            ->create();
        
        $postIds = $user->posts->pluck('id');
        
        $user->delete();
        
        $this->assertDatabaseMissing('users', ['id' => $user->id]);
        
        foreach ($postIds as $postId) {
            $this->assertDatabaseMissing('posts', ['id' => $postId]);
        }
    }

    public function test_user_relationships()
    {
        $user = User::factory()
            ->hasPosts(5)
            ->hasComments(3)
            ->create();
        
        $this->assertCount(5, $user->posts);
        $this->assertCount(3, $user->comments);
        $this->assertInstanceOf(Post::class, $user->posts->first());
    }
}
```

### 6. Browser Test - Laravel Dusk

```php
<?php
// tests/Browser/LoginTest.php

namespace Tests\Browser;

use Tests\DuskTestCase;
use Laravel\Dusk\Browser;
use App\Models\User;

class LoginTest extends DuskTestCase
{
    public function test_user_can_login()
    {
        $user = User::factory()->create([
            'email' => 'test@example.com',
            'password' => bcrypt('password')
        ]);

        $this->browse(function (Browser $browser) use ($user) {
            $browser->visit('/login')
                    ->type('email', $user->email)
                    ->type('password', 'password')
                    ->press('Login')
                    ->assertPathIs('/dashboard')
                    ->assertSee('Welcome');
        });
    }

    public function test_login_with_invalid_credentials()
    {
        $this->browse(function (Browser $browser) {
            $browser->visit('/login')
                    ->type('email', 'invalid@example.com')
                    ->type('password', 'wrongpassword')
                    ->press('Login')
                    ->assertPathIs('/login')
                    ->assertSee('credentials do not match');
        });
    }
}
```

---

## 🚀 Running Tests

```bash
# All tests
php artisan test
# or
vendor/bin/phpunit

# Specific suite
php artisan test --testsuite=Unit
php artisan test --testsuite=Feature

# Specific file
php artisan test tests/Feature/UserApiTest.php

# Specific method
php artisan test --filter=test_user_can_login

# Parallel testing (Laravel 10+)
php artisan test --parallel

# With coverage
php artisan test --coverage
php artisan test --coverage --min=80

# Stop on failure
php artisan test --stop-on-failure

# Browser tests (Dusk)
php artisan dusk
```

---

## 📊 Coverage Reports

```bash
# HTML coverage report
vendor/bin/phpunit --coverage-html coverage

# Text coverage
vendor/bin/phpunit --coverage-text

# Coverage with minimum threshold
php artisan test --coverage --min=80
```

---

## 🔍 Advanced Patterns

### Database Transactions

```php
use Illuminate\Foundation\Testing\DatabaseTransactions;

class MyTest extends TestCase
{
    use DatabaseTransactions;  // Rollback after each test
    
    public function test_something()
    {
        // Changes rolled back automatically
    }
}
```

### Factories & Seeders

```php
// Use factories
$users = User::factory()->count(10)->create();

// With relationships
$user = User::factory()
    ->hasPosts(3)
    ->hasComments(5)
    ->create();

// With custom attributes
$admin = User::factory()->create([
    'role' => 'admin',
    'is_active' => true
]);
```

### Mocking

```php
use Illuminate\Support\Facades\Mail;
use App\Mail\WelcomeEmail;

// Mock facade
Mail::fake();

// Perform action
$user = User::factory()->create();

// Assert email sent
Mail::assertSent(WelcomeEmail::class, function ($mail) use ($user) {
    return $mail->hasTo($user->email);
});
```

### Time Manipulation

```php
use Illuminate\Support\Facades\Date;

// Travel to specific time
$this->travel(5)->days();
$this->travelTo(now()->addMonth());

// Travel back
$this->travelBack();

// Freeze time
Date::setTestNow(now());
```

---

## ✅ Best Practices

1. **Isolation:** Use `RefreshDatabase` trait
2. **Factories:** Generate test data with factories
3. **Arrange-Act-Assert:** Clear test structure
4. **Descriptive Names:** `test_user_can_register_with_valid_data()`
5. **One Assertion:** Focus tests on single behavior
6. **Mock External Services:** Use facades fakes
7. **Feature vs Unit:** Feature for workflows, Unit for logic
8. **Database Assertions:** Use `assertDatabaseHas/Missing`
9. **API Testing:** Use `postJson()`, `getJson()`
10. **Coverage:** Aim for 80%+ on critical paths

---

## 🐛 Common Issues

**Issue:** `Base table or view not found`  
**Fix:** Run `php artisan migrate --env=testing`

**Issue:** Tests affecting production DB  
**Fix:** Ensure `.env.testing` uses separate DB

**Issue:** `Class 'Tests\Feature\ExampleTest' not found`  
**Fix:** Run `composer dump-autoload`

**Issue:** Slow test suite  
**Fix:** Use `--parallel` flag, SQLite in memory

---

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: 8.2
      - name: Install Dependencies
        run: composer install
      - name: Run Tests
        run: php artisan test --coverage --min=80
```

---

**Ready for:** Laravel 10+, PHP 8.1+  
**Next:** Run `php artisan test` to validate
