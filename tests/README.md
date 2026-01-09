# Test Suite for Character-Agent Integration

This directory contains the comprehensive test suite for the character-agent-integration package.

## Test Structure

### Test Files

- **test_agent_roles.py** - Tests for all 8 agent roles
  - ConversationPartner
  - Mentor
  - Collaborator
  - Analyst
  - Creator
  - Companion
  - Teacher
  - Leader

- **test_memory_decisions.py** - Tests for memory-augmented decision making
  - Memory retrieval
  - Decision strategies
  - Action evaluation
  - Learning from outcomes

- **test_personality_learning.py** - Tests for personality-driven learning
  - Learning styles
  - Personality influences
  - Retention calculation
  - Personality development

- **test_emotion_intelligence.py** - Tests for emotional intelligence
  - Emotion recognition
  - Emotional context
  - Response generation
  - Emotion regulation

- **test_integration.py** - End-to-end integration tests
  - Full workflows
  - Cross-component integration
  - Factory functions
  - State management

### Fixtures

**conftest.py** contains comprehensive pytest fixtures:
- Agent role instances
- Memory system mocks
- Personality profiles
- Emotional states
- Integration contexts

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=character_agent_integration --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_agent_roles.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_agent_roles.py::TestConversationPartner -v
```

### Run Specific Test Function
```bash
pytest tests/test_agent_roles.py::TestConversationPartner::test_initialization -v
```

### Using Test Scripts

**Python script:**
```bash
python run_tests.py              # Run all tests
python run_tests.py unit         # Run unit tests only
python run_tests.py integration  # Run integration tests only
python run_tests.py coverage     # Run with coverage report
python run_tests.py fast         # Run fast tests only
```

**Bash script:**
```bash
./tests/run_tests.sh all         # Run all tests
./tests/run_tests.sh unit        # Run unit tests
./tests/run_tests.sh coverage    # Run with coverage
```

### Run Tests by Marker

```bash
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests only
pytest -m "not slow"        # Exclude slow tests
```

## Test Coverage

Target coverage: **80%+**

Current coverage can be checked with:
```bash
pytest --cov=character_agent_integration --cov-report=term-missing
```

HTML coverage report is generated in `htmlcov/` directory.

## Test Organization

### Unit Tests
- Test individual components in isolation
- Use mocks for external dependencies
- Fast execution

### Integration Tests
- Test component interactions
- Test end-to-end workflows
- May use real or mocked dependencies

### Test Categories

Markers are used to categorize tests:
- `unit` - Unit tests
- `integration` - Integration tests
- `slow` - Slow-running tests
- `memory` - Memory system tests
- `emotion` - Emotional intelligence tests
- `personality` - Personality system tests
- `roles` - Agent role tests

## Writing New Tests

1. **Test Naming:**
   - Use descriptive names: `test_<functionality>_<condition>`
   - Group related tests in classes

2. **Use Fixtures:**
   - Leverage existing fixtures from conftest.py
   - Create new fixtures for common test data

3. **Structure:**
   ```python
   class TestFeature:
       def test_initialization(self):
           """Test that feature initializes correctly."""
           pass

       def test_functionality(self):
           """Test main functionality."""
           pass

       def test_edge_case(self):
           """Test edge cases."""
           pass
   ```

4. **Assertions:**
   - Use specific assertions
   - Include helpful failure messages
   - Test both success and failure cases

## Continuous Integration

Tests are configured to run in CI/CD pipelines:
- GitHub Actions workflow: `.github/workflows/test.yml`
- Runs on every push and pull request
- Enforces coverage requirements
- Runs on Python 3.8, 3.9, 3.10, 3.11

## Troubleshooting

### Import Errors
If you get import errors, ensure the package is installed:
```bash
pip install -e .
```

### Missing Dependencies
Install test dependencies:
```bash
pip install -r requirements-dev.txt
```

### Mock Warnings
Some tests use mocks for external dependencies (character-library, hierarchical-memory).
These are expected and don't affect test validity.

## Test Goals

- **Comprehensive Coverage:** Test all major code paths
- **Fast Execution:** Most tests should run quickly
- **Clear Output:** Easy to understand test results
- **Maintainability:** Easy to update and extend
- **Reliability:** Consistent, reproducible results

## Contributing Tests

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain coverage above 80%
4. Add documentation for complex tests
5. Use appropriate markers and fixtures
