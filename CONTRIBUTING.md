# Contributing to Inkwell

Thank you for your interest in contributing to Inkwell! We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use a clear title** that describes the bug
3. **Provide detailed steps** to reproduce the issue
4. **Include system information** (OS, Python version, Django version)
5. **Add screenshots** if applicable

### Suggesting Enhancements

1. **Check existing issues** for similar suggestions
2. **Use a clear title** that describes the enhancement
3. **Provide detailed description** of the proposed feature
4. **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow coding standards** (see below)
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass**
6. **Write clear commit messages**

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install -r requirements-dev.txt`
5. Run migrations: `python manage.py migrate`
6. Run tests: `pytest`

## Coding Standards

### Python Code Style

- Follow **PEP 8** style guide
- Use **Black** for code formatting: `black .`
- Use **isort** for import sorting: `isort .`
- Use **flake8** for linting: `flake8 .`
- Use **mypy** for type checking: `mypy .`

### Testing

- Write tests for all new features
- Maintain high test coverage (aim for >90%)
- Use **pytest** and **factory-boy** for testing
- Run tests with: `pytest --cov=blog --cov=inkwell`

### Git Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
- `feat(auth): add password reset functionality`
- `fix(models): resolve post slug generation issue`
- `docs(readme): update installation instructions`

### Branch Naming

- `feature/description-of-feature`
- `bugfix/description-of-bug`
- `hotfix/description-of-hotfix`
- `docs/description-of-docs-change`

## Development Workflow

1. **Create an issue** or choose an existing one
2. **Create a branch** from `main`
3. **Make your changes** following coding standards
4. **Write/update tests** for your changes
5. **Run the test suite** to ensure everything passes
6. **Update documentation** if needed
7. **Submit a pull request** with clear description

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=blog --cov=inkwell --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run tests matching pattern
pytest -k "test_post"
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both positive and negative cases
- Use factory-boy for creating test data
- Mock external dependencies

Example test structure:
```python
def test_post_creation():
    """Test that a post can be created successfully."""
    post = PostFactory()
    assert post.title
    assert post.slug
    assert post.author
```

## Code Review Process

1. **Automated checks** must pass (CI/CD pipeline)
2. **At least one approval** from a maintainer
3. **All conversations resolved**
4. **No merge conflicts**

## Getting Help

- **Documentation**: Check the README and code comments
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers directly

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow GitHub's Community Guidelines

## Recognition

Contributors will be:
- Listed in the README acknowledgments
- Mentioned in release notes for significant contributions
- Invited to become maintainers for consistent, high-quality contributions

Thank you for contributing to Inkwell! 🚀
