# Run Flutter Tests Command

Execute Flutter test suites with AI-powered analysis across platforms.

## Usage
```bash
mkf run-tests [options]
```

## Options
- `--type <type>` - Test type: unit, widget, integration, golden, all
- `--coverage` - Generate coverage reports
- `--platform <platform>` - Target platform: android, ios, web, all
- `--golden` - Update golden files
- `--devices <list>` - Test on specific devices

## AI Analysis
- **flutter-tester** - Analyzes test results and widget performance
- **flutter-debugger** - Identifies cross-platform issues
- **dart-reviewer** - Reviews test code quality
- **flutter-project-tracker** - Updates project metrics

## Examples
```bash
# Run all tests with coverage
mkf run-tests --coverage

# Widget tests only
mkf run-tests --type widget

# Integration tests on both platforms
mkf run-tests --type integration --platform all

# Update golden files
mkf run-tests --type golden --golden
```
