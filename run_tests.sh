#!/bin/bash

# Test runner script for InkWell project

set -e

echo "🧪 Running InkWell Test Suite"
echo "================================"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not detected. Activating..."
    source inkenv/bin/activate || source inkenv/Scripts/activate
fi

# Install test dependencies if needed
echo "📦 Installing/updating test dependencies..."
pip install -q pytest pytest-django pytest-cov factory-boy

# Run tests with different levels
echo ""
echo "🏃 Running unit tests..."
pytest tests/test_models.py tests/test_forms.py -v

echo ""
echo "🌐 Running view tests..."
pytest tests/test_views.py tests/test_urls.py -v

echo ""
echo "🔗 Running integration tests..."
pytest tests/test_integration.py -v

echo ""
echo "📊 Generating coverage report..."
pytest tests/ --cov=blog --cov=inkwell --cov-report=term-missing --cov-report=html

echo ""
echo "✅ All tests completed!"
echo "📋 Coverage report saved to htmlcov/"
