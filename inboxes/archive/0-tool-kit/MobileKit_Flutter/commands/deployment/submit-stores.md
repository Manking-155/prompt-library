# Submit to Stores Command

Automate multi-store submission with AI-powered release management.

## Usage
```bash
mkf submit-stores [options]
```

## Options
- `--stores <list>` - Target stores: google-play, app-store, both
- `--track <track>` - Release track: internal, alpha, beta, production
- `--notes <text>` - Release notes
- `--rollout <percent>` - Staged rollout percentage
- `--auto-promote` - Auto-promote after successful rollout

## AI Workflow
1. **flutter-release-manager** - Prepares multi-store submission
2. **flutter-copywriter** - Generates store-specific descriptions
3. **flutter-project-tracker** - Updates release timeline
4. **dart-reviewer** - Final compliance check

## Examples
```bash
# Submit to both stores (beta track)
mkf submit-stores --stores both --track beta

# Google Play internal testing
mkf submit-stores --stores google-play --track internal

# Production with staged rollout
mkf submit-stores --stores both --track production --rollout 10
```
