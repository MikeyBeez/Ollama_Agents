# 🧪 Ollama_Agents Testing Strategy

This document outlines our approach to testing Ollama_Agents.

## Testing Philosophy

We believe in thorough testing to ensure reliability and maintainability. Our testing strategy includes:

1. Unit Tests
2. Integration Tests
3. End-to-End Tests

## Test Structure

Tests are located in the `src/tests/` directory, mirroring the structure of the `src/` directory.

## Running Tests

To run all tests:

```bash
python -m unittest discover src/tests
```

To run a specific test file:

```bash
python -m unittest src/tests/test_file_name.py
```

## Writing Tests

### Guidelines

1. Each module should have a corresponding test file.
2. Use descriptive test method names.
3. Follow the Arrange-Act-Assert pattern.
4. Mock external dependencies.
5. Aim for high code coverage, but prioritize meaningful tests over coverage percentage.

### Example Test

```python
import unittest
from unittest.mock import patch
from src.modules.example_module import example_function

class TestExampleModule(unittest.TestCase):
    def test_example_function(self):
        # Arrange
        input_data = "test input"
        expected_output = "expected result"

        # Act
        result = example_function(input_data)

        # Assert
        self.assertEqual(result, expected_output)

    @patch('src.modules.example_module.external_dependency')
    def test_example_function_with_mock(self, mock_dependency):
        # Arrange
        mock_dependency.return_value = "mocked value"
        input_data = "test input"

        # Act
        result = example_function(input_data)

        # Assert
        self.assertEqual(result, "expected result with mocked value")
        mock_dependency.assert_called_once_with(input_data)
```

## Continuous Integration

We use GitHub Actions for continuous integration. Tests are automatically run on every push and pull request.

## Code Coverage

We use coverage.py to measure code coverage. Aim for at least 80% coverage.

```bash pip install coverage

To run tests with coverage:

```bash
coverage run -m unittest discover src/tests
coverage report -m
```

Remember, 100% coverage doesn't guarantee bug-free code. Focus on writing meaningful tests that cover critical paths and edge cases.
