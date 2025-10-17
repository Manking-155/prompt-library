# Run iOS Tests Command

Execute iOS test suites with comprehensive AI analysis and reporting.

## Usage
```bash
mki run-tests [options]
```

## Options
- `--scheme <name>` - Xcode scheme to test (default: Debug)
- `--coverage` - Generate code coverage reports
- `--devices <list>` - Test on specific devices (comma-separated)
- `--parallel` - Enable parallel testing
- `--ui-only` - Run only UI tests
- `--unit-only` - Run only unit tests

## AI Analysis
- **ios-tester** - Analyzes test results and coverage
- **ios-debugger** - Identifies performance bottlenecks
- **swift-reviewer** - Reviews test code quality
- **ios-project-tracker** - Updates project metrics

## Examples
```bash
# Run all tests with coverage
mki run-tests --coverage

# Test on multiple devices
mki run-tests --devices "iPhone 15,iPad Pro,iPhone SE"

# Run only unit tests
mki run-tests --unit-only --parallel
```
