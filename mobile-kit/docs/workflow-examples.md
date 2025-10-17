# MobileKit Workflow Examples

This guide provides practical examples of using MobileKit workflows for common mobile development scenarios.

## Workflow Types

### Sequential Workflows
Execute agents one after another in a defined order.

### Parallel Workflows
Execute multiple agents simultaneously for faster processing.

### Fan-Out Workflows
Generate multiple solutions in parallel and compare results.

## Example Workflows

### 1. New Feature Development

**Scenario**: Adding a user authentication system to a Flutter app.

**Workflow**: `new-feature.yaml`

```bash
mk workflow run new-feature
```

**Process**:
1. **Mobile Planner** analyzes requirements and defines architecture
2. **Mobile Researcher** finds best authentication packages
3. **UI/UX Designer** creates login/register screens
4. **Mobile Tester** creates comprehensive test suite
5. **Code Reviewer** reviews implementation
6. **Docs Manager** updates documentation

**Input Example**:
```yaml
feature_name: "user_authentication"
requirements:
  - email_password_login
  - social_login
  - biometric_authentication
  - secure_token_storage
platforms: ["ios", "android"]
timeline: "2_weeks"
```

**Expected Output**:
- Complete authentication flow implementation
- UI components for login/register
- Secure token management
- Test suite with 90%+ coverage
- Updated API documentation

### 2. Bug Fix Release

**Scenario**: Fixing a critical crash in production iOS app.

**Workflow**: `bug-fix-release.yaml`

```bash
mk workflow run bug-fix-release
```

**Process**:
1. **Mobile Debugger** analyzes crash reports
2. **Mobile Tester** creates regression tests
3. **Code Reviewer** reviews the fix
4. **Git Manager** manages release branch
5. **Release Manager** handles App Store submission

**Input Example**:
```yaml
crash_type: "memory_leak"
platform: "ios"
affected_users: 1000
priority: "critical"
crash_logs:
  - "crash_report_2024_01_15.txt"
  - "firebase_crashlytics_export.json"
```

**Expected Output**:
- Root cause analysis report
- Fix implementation
- Regression test suite
- Hot release package
- App Store submission status

### 3. UI/UX Iteration

**Scenario**: Redesigning the onboarding flow based on user feedback.

**Workflow**: `ui-ux-iteration.yaml`

```bash
mk workflow run ui-ux-iteration
```

**Process**:
1. **UI/UX Designer** creates new designs
2. **Mobile Planner** plans implementation
3. **Mobile Tester** tests new flow
4. **Code Reviewer** reviews changes
5. **Docs Manager** updates user guides

**Input Example**:
```yaml
current_flow: "5_step_onboarding"
issues:
  - "high_dropoff_rate_step_3"
  - "confusing_navigation"
  - "slow_loading_screens"
user_feedback:
  - "too_many_steps"
  - "unclear_value_proposition"
target_metrics:
  - completion_rate: "85%"
  - time_to_complete: "2_minutes"
```

**Expected Output**:
- Redesigned 3-step onboarding
- Improved loading performance
- A/B test setup
- Updated analytics tracking

### 4. App Store Release

**Scenario**: Releasing version 2.0 with major features.

**Workflow**: `app-store-release.yaml`

```bash
mk workflow run app-store-release
```

**Process**:
1. **Mobile Tester** performs final QA
2. **Code Reviewer** conducts security review
3. **Content Writer** creates store descriptions
4. **Release Manager** handles submission
5. **Git Manager** tags release
6. **Project Tracker** monitors metrics

**Input Example**:
```yaml
version: "2.0.0"
release_type: "major"
features:
  - "real_time_chat"
  - "offline_mode"
  - "dark_mode"
app_store_targets:
  - "ios_app_store"
  - "google_play"
marketing_launch: true
```

**Expected Output**:
- Complete release package
- App store submissions
- Marketing materials
- Release notes
- Post-launch monitoring setup

## Custom Workflow Examples

### 5. Performance Optimization Workflow

Create a custom workflow for app performance optimization:

**File**: `workflows/performance-optimization.yaml`

```yaml
name: "Performance Optimization Workflow"
description: "Optimize app performance and memory usage"

agents:
  - name: "mobile-debugger"
    role: "Analyze performance issues"
    input:
      - performance_metrics
      - memory_profiles
      - user_complaints
    output:
      - bottlenecks_identified
      - optimization_recommendations

  - name: "mobile-researcher"
    role: "Research optimization techniques"
    input:
      - bottlenecks_identified
      - platform_specific_issues
    output:
      - optimization_strategies
      - best_practices

  - name: "code-reviewer"
    role: "Review performance improvements"
    input:
      - implemented_optimizations
      - performance_benchmarks
    output:
      - review_results
      - further_improvements

execution_order:
  - mobile-debugger
  - mobile-researcher
  - code-reviewer
```

**Usage**:
```bash
mk workflow run performance-optimization
```

### 6. API Integration Workflow

Create a workflow for integrating third-party APIs:

**File**: `workflows/api-integration.yaml`

```yaml
name: "API Integration Workflow"
description: "Integrate third-party APIs into mobile app"

agents:
  - name: "mobile-researcher"
    role: "Research API options and SDKs"
    input:
      - api_requirements
      - data_formats
      - security_requirements
    output:
      - api_recommendations
      - sdk_options

  - name: "mobile-planner"
    role: "Plan integration architecture"
    input:
      - api_recommendations
      - existing_codebase
    output:
      - integration_plan
      - data_flow_design

  - name: "database-architect"
    role: "Design local data storage"
    input:
      - api_data_structure
      - offline_requirements
    output:
      - database_schema
      - sync_strategy

  - name: "mobile-tester"
    role: "Create integration tests"
    input:
      - api_specifications
      - integration_code
    output:
      - test_suite
      - mock_scenarios

execution_order:
  - mobile-researcher
  - mobile-planner
  - database-architect
  - mobile-tester
```

**Usage**:
```bash
mk workflow run api-integration
```

## Running Workflows

### Command Line Interface

```bash
# List available workflows
mk workflow list

# Run a specific workflow
mk workflow run <workflow_name>

# Run workflow with custom context
mk workflow run new-feature --context custom_context.yaml

# Run workflow in verbose mode
mk workflow run bug-fix --verbose
```

### Programmatic Usage

```python
from orchestrator.workflow_engine import WorkflowEngine
from pathlib import Path

# Initialize workflow engine
engine = WorkflowEngine(Path('my_project'))

# Run workflow with custom input
result = engine.run_workflow(
    'new-feature',
    context={
        'feature_name': 'payment_system',
        'platforms': ['ios', 'android'],
        'timeline': '3_weeks'
    }
)

print(f"Workflow result: {result}")
```

## Monitoring Workflows

### Progress Tracking

Workflows provide real-time progress updates:

```bash
# Monitor running workflow
mk workflow status <workflow_id>

# View workflow logs
mk workflow logs <workflow_id>

# Cancel running workflow
mk workflow cancel <workflow_id>
```

### Success Metrics

Track workflow effectiveness:

- **Completion Rate**: Percentage of workflows that complete successfully
- **Execution Time**: Average time to complete workflows
- **Error Rate**: Frequency of workflow failures
- **Agent Performance**: Individual agent success rates

## Best Practices

### 1. Workflow Design
- Keep workflows focused on specific objectives
- Define clear input/output contracts
- Include error handling and retry logic
- Set appropriate timeouts for each agent

### 2. Context Management
- Provide sufficient context for agents
- Use consistent data formats
- Include relevant project information
- Validate inputs before execution

### 3. Error Handling
- Implement fallback strategies
- Log errors for debugging
- Provide clear error messages
- Allow workflow recovery

### 4. Performance Optimization
- Use parallel execution when possible
- Cache expensive operations
- Optimize agent input size
- Monitor resource usage

## Troubleshooting

### Common Workflow Issues

1. **Agent Failures**: Check agent configuration and input data
2. **Timeout Issues**: Increase timeouts or optimize agent performance
3. **Context Errors**: Validate input data and context format
4. **Integration Problems**: Verify workflow engine setup

### Debugging Tools

```bash
# Run workflow in debug mode
mk workflow run <workflow_name> --debug

# View detailed execution trace
mk workflow trace <workflow_id>

# Validate workflow configuration
mk workflow validate <workflow_name>
```

## Next Steps

1. **Explore Pre-built Workflows**: Use existing workflows as templates
2. **Create Custom Workflows**: Design workflows for your specific needs
3. **Integrate with CI/CD**: Automate workflow execution in pipelines
4. **Monitor Performance**: Track and optimize workflow effectiveness
5. **Share Workflows**: Contribute workflows to the community