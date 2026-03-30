# Context Management & Optimization Strategies

Chiến lược tối ưu hóa context khi làm việc với AI tools để maximize efficiency.

## 🎯 Token Usage Optimization

### Context Compression Techniques

#### Information Hierarchization
```markdown
## Context Priority Framework

### Essential (Always Include)
- Current task objective
- Key constraints and requirements
- Critical technical specifications
- Immediate decision factors

### Important (Include When Relevant)
- Related previous decisions
- Technical architecture context
- Business context and goals
- Performance requirements

### Nice-to-Have (Include If Space Allows)
- Background information
- Alternative approaches considered
- Historical context
- Future planning considerations

### Reference Only (Link, Don't Include)
- Detailed technical documentation
- Complete specifications
- Comprehensive research data
- Full conversation histories
```

#### Context Templates for Common Tasks
```markdown
## Technical Problem Solving Context
**Objective**: [Specific technical goal]
**Current Stack**: Flutter 3.x, MySQL, Oracle Cloud, Claude API
**Constraints**: [Budget, timeline, performance requirements]
**Context**: [.agent documentation references]
**Previous Solutions**: [Link to relevant past solutions]

## Business Decision Context  
**Decision**: [Specific choice to make]
**Options**: [Available alternatives]
**Criteria**: [Decision factors and weights]
**Constraints**: [Vietnamese market, solo developer limitations]
**Timeline**: [Decision deadline]

## Learning/Research Context
**Topic**: [Specific learning objective]
**Current Knowledge**: [What you already know]
**Application**: [How you'll use this knowledge]
**Depth Needed**: [Surface level vs deep expertise]
**Time Available**: [Learning time constraints]
```

### Multi-Session Context Continuity

#### Session State Management
```markdown
## Session Continuation Template

### Previous Session Summary
**Last Topic**: [What was being discussed]
**Key Decisions**: [Important conclusions reached]
**Open Questions**: [Unresolved issues]
**Next Steps**: [Planned actions]

### Current Session Goals
**Primary Objective**: [Main goal for this session]
**Secondary Goals**: [Additional outcomes desired]
**Session Constraints**: [Time, complexity limitations]

### Context References
**Documentation**: [Relevant .agent files]
**Previous Conversations**: [Key insights to remember]
**External Resources**: [Important references]
```

#### Knowledge Base Integration
```python
# Context management system
class ContextManager:
    def __init__(self):
        self.session_history = []
        self.key_decisions = {}
        self.active_projects = {}

    def create_session_context(self, task_type: str) -> str:
        """Generate optimized context for specific task type"""
        context_template = self.get_template(task_type)
        relevant_history = self.get_relevant_history(task_type)
        active_context = self.get_active_project_context()

        return self.combine_context(context_template, relevant_history, active_context)

    def compress_context(self, full_context: str, token_limit: int) -> str:
        """Intelligently compress context to fit token limits"""
        # Priority-based compression logic
        pass

    def update_session_memory(self, insights: dict):
        """Capture key insights for future reference"""
        self.session_history.append(insights)
        self.extract_key_decisions(insights)
```

## 🔄 Context Switching Strategies

### Project Context Templates

#### Mobile Development Context
```markdown
## Flutter Development Context
**Project**: [App name and purpose]
**Architecture**: Clean Architecture with Riverpod
**Current Feature**: [Specific feature being developed]
**Database**: Hive (local) + MySQL (backend)
**AI Integration**: [Claude API/offline models]
**Status**: [Current development stage]
**Blockers**: [Current challenges]
**Next Milestone**: [Upcoming goals]
```

#### Business Development Context
```markdown
## Business Development Context
**Focus Area**: [Product/client/marketing]
**Current Initiative**: [Specific project]
**Target Market**: [Vietnamese/international]
**Revenue Stream**: [Primary income source]
**Stage**: [Validation/MVP/growth/optimization]
**Key Metrics**: [Success measurements]
**Immediate Goals**: [Short-term objectives]
```

#### Learning Context
```markdown
## Learning Session Context
**Subject**: [Technology/business skill]
**Learning Goal**: [Specific objective]
**Current Level**: [Beginner/intermediate/advanced]
**Application**: [How it fits your projects]
**Resources**: [Learning materials being used]
**Practice Project**: [Hands-on application]
**Timeline**: [Learning schedule]
```

### Context Optimization Patterns

#### For Technical Tasks
1. **Start with Architecture**: Reference .agent system docs
2. **Define Scope**: Clear boundaries and requirements
3. **Specify Constraints**: Technical and business limitations
4. **Reference Patterns**: Link to similar previous solutions
5. **Set Success Criteria**: Measurable outcomes

#### For Business Tasks
1. **Market Context**: Vietnamese market specifics
2. **Business Stage**: Solo developer vs scaling business
3. **Resource Constraints**: Time, budget, skills
4. **Strategic Alignment**: Long-term goals alignment
5. **Decision Framework**: Evaluation criteria

#### For Research Tasks
1. **Research Scope**: Specific questions to answer
2. **Knowledge Level**: Current understanding baseline
3. **Application Context**: How insights will be used
4. **Time Constraints**: Research timeline
5. **Depth Requirements**: Surface vs comprehensive

## 📊 Context Performance Metrics

### Efficiency Measurements
```python
class ContextEfficiencyTracker:
    def __init__(self):
        self.metrics = {
            'avg_tokens_per_session': 0,
            'task_completion_rate': 0,
            'context_reuse_rate': 0,
            'session_effectiveness': 0
        }

    def track_session(self, tokens_used: int, task_completed: bool, 
                     context_reused: float, effectiveness_score: int):
        """Track context usage efficiency"""
        pass

    def analyze_patterns(self):
        """Identify optimization opportunities"""
        pass

    def suggest_improvements(self):
        """Recommend context optimization strategies"""
        pass
```

### Quality Indicators
- **Task Completion Rate**: Percentage of sessions achieving objectives
- **Context Relevance**: How much provided context was actually useful
- **Token Efficiency**: Value extracted per token used
- **Session Effectiveness**: Quality of outcomes achieved

## 🛠️ Tools Integration

### Claude API Optimization
```python
# Claude API context optimization
def optimize_claude_context(task_type: str, full_context: str) -> str:
    """Optimize context for Claude API usage"""

    context_limits = {
        'code_generation': 15000,
        'business_analysis': 20000,
        'research': 25000,
        'general': 10000
    }

    limit = context_limits.get(task_type, 10000)

    if len(full_context) <= limit:
        return full_context

    # Intelligent compression based on task type
    return compress_context_by_priority(full_context, limit, task_type)
```

### Cursor IDE Integration
```json
// Cursor IDE context configuration
{
  "contextOptimization": {
    "maxTokens": 200000,
    "compressionStrategy": "priority-based",
    "sessionContinuity": true,
    "documentationIntegration": {
      "agentFolder": ".agent/",
      "autoInclude": ["readme.md", "current_task.md"],
      "smartReferences": true
    }
  }
}
```

### Cross-Tool Context Sharing
```yaml
# Context sharing configuration
context_sync:
  tools:
    - claude_api
    - cursor_ide
    - z_ai

  shared_context:
    - project_architecture
    - current_objectives
    - key_decisions
    - active_constraints

  tool_specific:
    claude_api:
      - research_context
      - business_analysis
    cursor_ide:
      - code_context
      - technical_specs
    z_ai:
      - specialized_tasks
      - workflow_automation
```

## 🎯 Best Practices

### Context Preparation Checklist
- [ ] Define clear session objective
- [ ] Identify essential context elements
- [ ] Remove irrelevant information
- [ ] Reference documentation instead of copying
- [ ] Set up continuation plan for long tasks
- [ ] Prepare fallback context for token limits

### Session Management
- [ ] Start with context summary
- [ ] Track key decisions made
- [ ] Note insights for future reference
- [ ] Plan next session continuation
- [ ] Update knowledge base with learnings

### Quality Assurance
- [ ] Verify context relevance to task
- [ ] Check for redundant information
- [ ] Ensure all constraints are mentioned
- [ ] Validate success criteria clarity
- [ ] Confirm continuation plan feasibility

## Related Documentation
- Prompt Templates: `prompts/technical_research.md`
- Workflow Management: `workflows/business_validation.md`
- Knowledge System: `knowledge/learning_system.md`
- AI Tools Integration: `automation/tool_optimization.md`