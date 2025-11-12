# pytest Setup - Python Backend Testing

**For:** FastAPI, Django, Flask backends  
**Coverage:** Unit, Integration, API testing  
**Tools:** pytest, pytest-asyncio, pytest-cov, httpx

---

## 📦 Installation

```bash
# Core testing
pip install pytest pytest-asyncio pytest-cov

# API testing
pip install httpx pytest-mock

# Database testing (optional)
pip install pytest-django  # Django
pip install pytest-postgresql  # PostgreSQL
```

---

## 📂 Project Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_database.py
│   │   └── test_external_apis.py
│   └── api/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_users.py
│       └── test_products.py
├── pytest.ini
└── .coveragerc
```

---

## ⚙️ Configuration Files

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests
    api: API endpoint tests
    slow: Slow running tests
    smoke: Smoke tests for critical paths
```

### .coveragerc

```ini
[run]
source = app
omit = 
    */tests/*
    */migrations/*
    */__init__.py
    */config/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

---

## 🔧 conftest.py - Shared Fixtures

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

@pytest.fixture(scope="function")
def db_session():
    """Create fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI test client with DB override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Get authenticated user headers"""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
        "full_name": "Test User"
    }
```

---

## 📝 Test Examples

### 1. Unit Test - Models

```python
# tests/unit/test_models.py
import pytest
from app.models import User

@pytest.mark.unit
def test_user_creation():
    """Test user model creation"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashedpass"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.is_active is True

@pytest.mark.unit
def test_user_password_hashing():
    """Test password hashing"""
    user = User(email="test@example.com")
    user.set_password("plainpassword")
    
    assert user.hashed_password != "plainpassword"
    assert user.verify_password("plainpassword") is True
    assert user.verify_password("wrongpassword") is False
```

### 2. Integration Test - Database

```python
# tests/integration/test_database.py
import pytest
from app.models import User
from app.services.user_service import UserService

@pytest.mark.integration
def test_create_user_db(db_session):
    """Test user creation in database"""
    service = UserService(db_session)
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!"
    }
    
    user = service.create_user(**user_data)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.verify_password("SecurePass123!")

@pytest.mark.integration
def test_user_query_operations(db_session, sample_user_data):
    """Test database query operations"""
    service = UserService(db_session)
    
    # Create
    user = service.create_user(**sample_user_data)
    
    # Read
    found = service.get_by_email(sample_user_data["email"])
    assert found.id == user.id
    
    # Update
    service.update_user(user.id, full_name="Updated Name")
    updated = service.get_by_id(user.id)
    assert updated.full_name == "Updated Name"
    
    # Delete
    service.delete_user(user.id)
    deleted = service.get_by_id(user.id)
    assert deleted is None
```

### 3. API Test - Endpoints

```python
# tests/api/test_users.py
import pytest

@pytest.mark.api
def test_register_user(client, sample_user_data):
    """Test user registration endpoint"""
    response = client.post("/users/register", json=sample_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert "password" not in data

@pytest.mark.api
def test_login_user(client, sample_user_data):
    """Test user login endpoint"""
    # Register first
    client.post("/users/register", json=sample_user_data)
    
    # Login
    response = client.post("/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.api
def test_get_current_user(client, auth_headers):
    """Test get current user endpoint"""
    response = client.get("/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "id" in data

@pytest.mark.api
def test_unauthorized_access(client):
    """Test protected endpoint without auth"""
    response = client.get("/users/me")
    assert response.status_code == 401
```

### 4. Async Test - FastAPI

```python
# tests/api/test_async_endpoints.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
@pytest.mark.api
async def test_async_endpoint():
    """Test async API endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
@pytest.mark.api
async def test_concurrent_requests():
    """Test concurrent API requests"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        responses = await asyncio.gather(
            ac.get("/users/1"),
            ac.get("/users/2"),
            ac.get("/users/3")
        )
    
    assert all(r.status_code in [200, 404] for r in responses)
```

### 5. Mocking External Services

```python
# tests/integration/test_external_apis.py
import pytest
from unittest.mock import Mock, patch
from app.services.email_service import EmailService

@pytest.mark.integration
@patch('app.services.email_service.smtplib.SMTP')
def test_send_email_mock(mock_smtp):
    """Test email sending with mocked SMTP"""
    mock_server = Mock()
    mock_smtp.return_value = mock_server
    
    service = EmailService()
    result = service.send_email(
        to="test@example.com",
        subject="Test",
        body="Test email"
    )
    
    assert result is True
    mock_server.send_message.assert_called_once()

@pytest.mark.integration
@pytest.fixture
def mock_payment_gateway():
    """Mock payment gateway for testing"""
    with patch('app.services.payment.stripe.Charge') as mock_charge:
        mock_charge.create.return_value = {
            "id": "ch_test123",
            "status": "succeeded",
            "amount": 5000
        }
        yield mock_charge

def test_process_payment(mock_payment_gateway):
    """Test payment processing with mock"""
    from app.services.payment import PaymentService
    
    service = PaymentService()
    result = service.charge(amount=5000, token="tok_test")
    
    assert result["status"] == "succeeded"
    mock_payment_gateway.create.assert_called_once()
```

---

## 🚀 Running Tests

```bash
# All tests
pytest

# Specific marker
pytest -m unit
pytest -m api
pytest -m "not slow"

# Specific file
pytest tests/api/test_users.py

# Specific test
pytest tests/api/test_users.py::test_login_user

# With coverage
pytest --cov=app --cov-report=html

# Parallel execution
pytest -n auto  # requires pytest-xdist

# Verbose output
pytest -vv

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

---

## 📊 Coverage Reports

```bash
# Terminal report
pytest --cov=app --cov-report=term-missing

# HTML report (opens in browser)
pytest --cov=app --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=app --cov-report=xml
```

---

## 🔍 Advanced Patterns

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("invalid.email", False),
    ("missing@domain", False),
    ("@nodomain.com", False),
])
def test_email_validation(email, expected):
    """Test email validation with multiple inputs"""
    from app.utils.validators import is_valid_email
    assert is_valid_email(email) == expected
```

### Database Rollback

```python
@pytest.fixture
def db_transaction(db_session):
    """Rollback transaction after test"""
    transaction = db_session.begin_nested()
    yield db_session
    transaction.rollback()
```

### Test Data Factories

```python
import factory
from app.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Faker('email')
    username = factory.Faker('user_name')
    full_name = factory.Faker('name')

# Usage
def test_with_factory():
    user = UserFactory()
    assert user.email is not None
```

---

## ✅ Best Practices

1. **Isolation:** Each test independent, use fixtures
2. **Naming:** Descriptive test names (test_action_expected)
3. **AAA Pattern:** Arrange → Act → Assert
4. **Markers:** Tag tests by type/speed
5. **Coverage:** Aim for 80%+ critical paths
6. **Fast Tests:** Mock external services
7. **Clean DB:** Fresh database per test
8. **Fixtures:** Reuse common setup
9. **Async Tests:** Use pytest-asyncio for async code
10. **CI/CD Ready:** XML reports for automation

---

## 🐛 Common Issues

**Issue:** `asyncio.run() cannot be called from a running event loop`  
**Fix:** Use `pytest-asyncio` and `@pytest.mark.asyncio`

**Issue:** `Database locked` in SQLite tests  
**Fix:** Use `check_same_thread=False` in engine config

**Issue:** Tests pass individually but fail together  
**Fix:** Ensure proper test isolation with `scope="function"`

**Issue:** Slow tests  
**Fix:** Use markers, run unit tests first, parallelize with `-n auto`

---

**Ready for:** FastAPI, Django, Flask backends  
**Next:** Run `pytest -v` to validate setup
