# Testing Guide - Antigravity Project

## 🧪 Testing Infrastructure

This project uses **GUT (Godot Unit Test)** for automated testing following software development best practices.

---

## 📁 Test Directory Structure

```
tests/
├── unit/                           # Unit tests for individual components
│   ├── test_health_component.gd    # HealthComponent tests
│   ├── test_damage_component.gd    # DamageComponent tests
│   ├── test_movement_component.gd  # MovementComponent tests
│   └── test_gravity_manager.gd     # GravityManager tests
└── integration/                    # Integration tests (future)
    └── (coming soon)
```

---

## 🚀 Running Tests

### Method 1: From Godot Editor (Recommended)

1. Open the project in Godot
2. Click on the **"GUT"** panel at the bottom
3. Click **"Run All"** to run all tests
4. View results in the GUT panel

### Method 2: From Command Line

Run all tests:
```bash
godot --path . -s addons/gut/gut_cmdln.gd
```

Run specific test file:
```bash
godot --path . -s addons/gut/gut_cmdln.gd -gtest=tests/unit/test_health_component.gd
```

Run tests and exit:
```bash
godot --path . -s addons/gut/gut_cmdln.gd -gexit
```

### Method 3: CI/CD (GitHub Actions)

Tests run automatically on every push and pull request via GitHub Actions.

---

## ✍️ Writing New Tests

### Test File Template

```gdscript
extends GutTest

## Brief description of what this test file covers

var component_under_test

func before_each():
    # Setup before each test
    component_under_test = ComponentClass.new()
    component_under_test.some_property = value

func after_each():
    # Cleanup after each test
    component_under_test.free()

func test_something_works():
    # Arrange
    var expected_value = 42
    
    # Act
    component_under_test.do_something()
    
    # Assert
    assert_eq(component_under_test.result, expected_value, "Should return 42")
```

### Naming Conventions

- **Test files**: `test_<component_name>.gd`
- **Test functions**: `test_<what_is_being_tested>()`
- **Setup functions**: `before_each()`, `after_each()`, `before_all()`, `after_all()`

### Common Assertions

```gdscript
# Equality
assert_eq(actual, expected, "message")
assert_ne(actual, expected, "message")

# Truthiness
assert_true(value, "message")
assert_false(value, "message")

# Null checks
assert_null(value, "message")
assert_not_null(value, "message")

# Numeric comparisons
assert_gt(actual, expected, "message")  # Greater than
assert_lt(actual, expected, "message")  # Less than
assert_gte(actual, expected, "message") # Greater than or equal
assert_lte(actual, expected, "message") # Less than or equal
assert_almost_eq(actual, expected, tolerance, "message")

# Signals
watch_signals(object)
assert_signal_emitted(object, "signal_name", "message")
assert_signal_not_emitted(object, "signal_name", "message")

# Async/Await
await wait_seconds(1.0)
await wait_frames(60)
```

---

## 📊 Test Coverage

### Current Coverage

| Component | Tests | Coverage |
|-----------|-------|----------|
| HealthComponent | 25 tests | ~90% |
| DamageComponent | 15 tests | ~85% |
| MovementComponent | 18 tests | ~80% |
| GravityManager | 20 tests | ~85% |
| **Total** | **78 tests** | **~85%** |

### Coverage Goals

- **Core Systems**: 80%+ coverage (gravity, health, damage, movement)
- **AI Components**: 60%+ coverage (patrol, chase, turret)
- **Gameplay Logic**: Manual testing (feel, balance, fun)
- **UI/Visual**: Manual testing (animations, effects)

---

## 🎯 Testing Best Practices

### 1. Test One Thing at a Time

❌ **Bad**:
```gdscript
func test_everything():
    health.take_damage(10)
    assert_eq(health.current_health, 90)
    health.heal(5)
    assert_eq(health.current_health, 95)
    health.set_invincible(1.0)
    assert_true(health.is_invincible())
```

✅ **Good**:
```gdscript
func test_take_damage_reduces_health():
    health.take_damage(10)
    assert_eq(health.current_health, 90)

func test_heal_increases_health():
    health.take_damage(10)
    health.heal(5)
    assert_eq(health.current_health, 95)

func test_set_invincible_makes_invincible():
    health.set_invincible(1.0)
    assert_true(health.is_invincible())
```

### 2. Use Descriptive Test Names

❌ **Bad**: `test_1()`, `test_damage()`, `test_works()`

✅ **Good**: `test_take_damage_reduces_health()`, `test_invincibility_blocks_damage()`

### 3. Follow AAA Pattern

```gdscript
func test_something():
    # Arrange - Set up test data
    var health = HealthComponent.new()
    health.max_health = 100
    
    # Act - Perform the action
    health.take_damage(25)
    
    # Assert - Verify the result
    assert_eq(health.current_health, 75)
```

### 4. Test Edge Cases

Always test:
- Zero values
- Negative values
- Null/empty inputs
- Maximum values
- Boundary conditions

### 5. Clean Up Resources

```gdscript
func after_each():
    if component:
        component.free()  # Prevent memory leaks
```

---

## 🐛 Debugging Failed Tests

### View Test Output

Failed tests show:
- Test name
- Expected vs. actual values
- Line number of failure
- Custom error message

### Common Issues

**Issue**: "Node not found"
- **Solution**: Ensure node is added to scene tree or use `add_child_autofree()`

**Issue**: "Signal not emitted"
- **Solution**: Check if `watch_signals()` was called before the action

**Issue**: "Assertion failed: expected X, got Y"
- **Solution**: Check your logic, values might be off by one or have rounding errors

### Running Single Test

To debug a specific test:
```bash
godot --path . -s addons/gut/gut_cmdln.gd -gtest=tests/unit/test_health_component.gd -gunit_test_name=test_take_damage_reduces_health
```

---

## 🔄 Continuous Integration

### GitHub Actions Workflow

Tests run automatically on:
- Every push to `main` branch
- Every pull request
- Manual workflow dispatch

### Viewing CI Results

1. Go to **Actions** tab on GitHub
2. Click on the latest workflow run
3. View test results and logs

### CI Configuration

See `.github/workflows/run-tests.yml` for configuration.

---

## 📝 Test Maintenance

### When to Update Tests

- **Feature Added**: Write tests for new functionality
- **Bug Fixed**: Add regression test to prevent recurrence
- **Refactoring**: Update tests if API changes
- **Breaking Change**: Update all affected tests

### Test Review Checklist

Before committing tests:
- [ ] All tests pass locally
- [ ] Test names are descriptive
- [ ] Edge cases are covered
- [ ] No hardcoded values (use constants)
- [ ] Resources are cleaned up
- [ ] Comments explain complex logic

---

## 🎓 Learning Resources

### GUT Documentation
- [Official GUT Wiki](https://github.com/bitwes/Gut/wiki)
- [GUT API Reference](https://github.com/bitwes/Gut/wiki/Quick-Start)

### Testing Best Practices
- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)
- [AAA Pattern](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)

---

## 🚧 Future Improvements

- [ ] Add integration tests for level loading
- [ ] Add performance benchmarks
- [ ] Increase coverage to 90%+
- [ ] Add visual regression tests for UI
- [ ] Set up test coverage reporting

---

## ❓ FAQ

**Q: Do I need to write tests for everything?**  
A: No. Focus on core logic (gravity, health, damage). Manual test gameplay feel and visuals.

**Q: How long should tests take to run?**  
A: All tests should complete in < 30 seconds. Slow tests indicate issues.

**Q: Can I skip tests temporarily?**  
A: Yes, prefix test name with `x`: `func xtest_something()` to skip.

**Q: What if a test is flaky (sometimes passes, sometimes fails)?**  
A: Flaky tests indicate timing issues or improper cleanup. Fix immediately.

---

**Last Updated**: January 7, 2026  
**Test Framework**: GUT 9.x  
**Godot Version**: 4.5
