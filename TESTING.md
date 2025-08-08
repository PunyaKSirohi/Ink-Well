# 🧪 Testing Guide for InkWell

This document provides a comprehensive guide to testing in the InkWell project.

## 📋 Table of Contents

- [Testing Framework](#testing-framework)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [Coverage Reports](#coverage-reports)
- [CI/CD Pipeline](#cicd-pipeline)
- [Code Quality](#code-quality)

## 🛠️ Testing Framework

InkWell uses a comprehensive testing stack:

- **pytest**: Primary testing framework
- **pytest-django**: Django integration for pytest
- **pytest-cov**: Coverage reporting
- **factory-boy**: Test data generation
- **Faker**: Realistic fake data generation

## 🏃 Running Tests

### Quick Test Commands

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=blog --cov=inkwell --cov-report=term-missing

# Run specific test categories
pytest tests/test_models.py -v
pytest tests/test_views.py -v
pytest tests/test_integration.py -v

# Run tests with markers
pytest tests/ -m unit
pytest tests/ -m integration
```

### Using the Test Runner Script

```bash
# Make the script executable (Linux/Mac)
chmod +x run_tests.sh

# Run the comprehensive test suite
./run_tests.sh
```

## 📁 Test Structure

```
tests/
├── __init__.py
├── factories.py          # Test data factories
├── test_models.py         # Model unit tests
├── test_views.py          # View tests
├── test_forms.py          # Form tests
├── test_urls.py           # URL routing tests
└── test_integration.py    # Integration tests
```

### Test Categories

- **Unit Tests** (`@pytest.mark.unit`): Test individual components in isolation
- **Integration Tests** (`@pytest.mark.integration`): Test component interactions
- **Slow Tests** (`@pytest.mark.slow`): Tests that take longer to run

## 📊 Coverage Reports

### Generating Coverage Reports

```bash
# Terminal coverage report
pytest tests/ --cov=blog --cov=inkwell --cov-report=term-missing

# HTML coverage report
pytest tests/ --cov=blog --cov=inkwell --cov-report=html

# XML coverage report (for CI/CD)
pytest tests/ --cov=blog --cov=inkwell --cov-report=xml
```

### Coverage Targets

- **Overall**: > 80%
- **Models**: > 95%
- **Views**: > 85%
- **Forms**: > 90%

## 🔄 CI/CD Pipeline

Our GitHub Actions workflow (`.github/workflows/django.yml`) includes:

### Test Matrix
- Python versions: 3.11, 3.12
- Database: PostgreSQL 15

### Pipeline Stages
1. **Test**: Run full test suite with coverage
2. **Lint**: Code quality checks (flake8, black, isort, mypy)
3. **Security**: Security scans (bandit, safety)
4. **Build**: Docker image build (on main branch)
5. **Deploy**: Production deployment (on main branch)

### Quality Gates
- All tests must pass
- Coverage must be > 80%
- No security vulnerabilities
- Code must pass linting

## 🔍 Code Quality Tools

### Linting and Formatting

```bash
# Format code
black blog/ inkwell/ tests/
isort blog/ inkwell/ tests/

# Lint code
flake8 blog/ inkwell/ tests/
mypy blog/ inkwell/ --ignore-missing-imports

# Security checks
bandit -r blog/ inkwell/
safety check
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code quality:

```bash
pip install pre-commit
pre-commit install
```

## 📝 Writing Tests

### Model Tests Example

```python
import pytest
from tests.factories import UserFactory, PostFactory

@pytest.mark.django_db
class TestPostModel:
    def test_post_creation(self):
        user = UserFactory()
        post = PostFactory(author=user)
        assert post.title
        assert post.author == user
```

### View Tests Example

```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.mark.django_db
class TestPostViews:
    def setup_method(self):
        self.client = Client()
    
    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        assert response.status_code == 200
```

### Using Factories

```python
from tests.factories import PostFactory, UserFactory

# Create a published post
post = PostFactory(status=1)

# Create a draft post
draft = PostFactory(status=0)

# Create multiple posts
posts = PostFactory.create_batch(5, status=1)
```

## 🐛 Debugging Tests

### Running Tests in Debug Mode

```bash
# Verbose output
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Drop into debugger on failure
pytest tests/ --pdb

# Run specific test
pytest tests/test_models.py::TestPostModel::test_post_creation -v
```

### Common Issues

1. **Database State**: Tests use a separate test database that's cleaned between tests
2. **Factory Conflicts**: Ensure unique fields in factories don't conflict
3. **URL Patterns**: Make sure test URLs match your URL patterns exactly

## 📈 Performance Testing

For performance testing, consider:

```bash
# Time test execution
pytest tests/ --durations=10

# Profile slow tests
pytest tests/ --profile
```

## 🎯 Test Best Practices

1. **Isolation**: Each test should be independent
2. **Descriptive Names**: Test names should describe what they test
3. **AAA Pattern**: Arrange, Act, Assert
4. **Use Factories**: Don't create test data manually
5. **Test Edge Cases**: Test boundary conditions and error cases
6. **Mock External Services**: Use mocks for external APIs/services

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [factory-boy Documentation](https://factoryboy.readthedocs.io/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)

---

Happy Testing! 🧪✨
