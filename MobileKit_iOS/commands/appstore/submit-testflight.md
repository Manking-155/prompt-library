# Submit to TestFlight Command

Automate TestFlight beta distribution with AI-powered release management.

## Usage
```bash
mki submit-testflight [options]
```

## Options
- `--notes <text>` - Release notes for beta testers
- `--groups <list>` - Target test groups (comma-separated)
- `--auto-notify` - Automatically notify testers
- `--external` - Submit for external testing

## AI Workflow
1. **appstore-manager** - Validates build and metadata
2. **ios-copywriter** - Generates release notes
3. **ios-project-tracker** - Updates release timeline
4. **swift-reviewer** - Final compliance check

## Examples
```bash
# Basic TestFlight submission
mki submit-testflight --notes "New user profile feature"

# Submit to specific groups
mki submit-testflight --groups "Beta Users,QA Team" --auto-notify

# External beta testing
mki submit-testflight --external --notes "Public beta release"
```
