---
name: ai-friendly-criteria-guide
version: "1.1"
category: guideline
target: universal
tags: [ios, marketing, guideline]
created: 2026-04-10
updated: 2026-04-10
changelog:
  - "1.0: Initial migration from prompts-box"
  - "1.1: Standardized YAML frontmatter and directory structure"
---

# AI-FRIENDLY DOCUMENT CRITERIA
## Comprehensive Guidelines for Optimal AI Processing

---

## DOCUMENT PURPOSE
This guideline defines structural and content criteria that make documents optimally processable by AI systems. These standards enable efficient information retrieval, accurate context understanding, and effective knowledge extraction.

---

## CORE STRUCTURAL PRINCIPLES

### 1. HIERARCHICAL ORGANIZATION

**Required Structure:**
- **Clear Heading Levels**: Use H1, H2, H3 hierarchy consistently
- **Maximum 3-4 Levels Deep**: Avoid excessive nesting that complicates navigation
- **Descriptive Headers**: Each heading should clearly indicate section content
- **Logical Flow**: Progress from general concepts to specific details

**Why This Matters:**
- AI models use heading structure to understand document organization
- Clear hierarchy enables accurate information chunking
- Facilitates precise section identification for targeted retrieval

**Example Structure:**
```
# Main Topic (H1)
## Major Subtopic (H2)
### Specific Aspect (H3)
#### Implementation Detail (H4 - use sparingly)
```

### 2. CONSISTENT FORMATTING PATTERNS

**Required Consistency:**
- **Uniform Bullet Styles**: Use same bullet type throughout document
- **Consistent Numbering**: Maintain sequential numbering for ordered lists
- **Parallel Structure**: Keep grammatically parallel construction in lists
- **Standardized Emphasis**: Use bold, italic, code blocks consistently

**Pattern Examples:**
```
✓ GOOD - Parallel Structure:
- Analyze document structure
- Identify key concepts
- Extract relevant information

✗ BAD - Non-Parallel:
- Analyzing the document
- Key concepts identified
- To extract information
```

### 3. EXPLICIT METADATA

**Required Metadata Fields:**
```
- Document ID: [Date]_[Category]_[Purpose]_[Version]
- Title: Clear, descriptive title with key terms
- Type: Document category (Guide, Report, SOP, Reference)
- Purpose: Primary objective and use cases
- Audience: Target users and expertise level
- Scope: What is and isn't covered
- Keywords: Searchable terms (comma-separated)
- Last Updated: Date and change summary
- Review Schedule: When to review/update
```

**Why This Matters:**
- Provides immediate context for AI processing
- Enables accurate document categorization
- Facilitates relevance assessment before full processing
- Supports effective document discovery and filtering

---

## CONTENT OPTIMIZATION STANDARDS

### 4. SEMANTIC CLARITY

**Requirements:**
- **Descriptive Headings**: Headers should summarize section content
- **Keyword Integration**: Naturally incorporate searchable terms
- **Explicit Context**: Avoid ambiguous pronouns (use specific nouns)
- **Term Consistency**: Use same terminology throughout document

**Examples:**
```
✓ GOOD: "Customer Retention Strategies for SaaS Businesses"
✗ BAD: "How to Keep Them Coming Back"

✓ GOOD: "The marketing team implemented this strategy..."
✗ BAD: "They implemented this..."
```

### 5. SCANNABLE CONTENT STRUCTURE

**Format Requirements:**
- **Short Paragraphs**: Maximum 4-5 sentences per paragraph
- **Bullet Points**: Use for lists of 3+ items
- **Clear Sections**: Distinct visual separation between topics
- **Summary Sections**: Include key takeaways for complex content

**Scannability Techniques:**
```
- **Bold Key Phrases**: Highlight important terms
- Use bullet points for multiple items
- Include numbered steps for processes
- Add visual breaks between major sections
```

### 6. CONTEXTUAL COMPLETENESS

**Required Context Elements:**
- **Background Information**: Provide necessary prerequisites
- **Explicit Definitions**: Define technical terms in context
- **Clear Relationships**: Explain connections between concepts
- **Reasoning Transparency**: Include "why" behind recommendations

**Context Provision Pattern:**
```
[Concept Introduction]
→ [Why This Matters]
→ [How It Works]
→ [Implementation Guidance]
→ [Common Challenges]
```

---

## AI PROCESSING OPTIMIZATION

### 7. INFORMATION CHUNKING

**Chunking Principles:**
- **Self-Contained Sections**: Each section should be independently understandable
- **Logical Boundaries**: Clear start and end points for topics
- **Cross-References**: Link related sections explicitly
- **Appropriate Granularity**: Balance between detail and digestibility

**Chunk Size Guidelines:**
- **Small Chunks**: 200-500 words for specific concepts
- **Medium Chunks**: 500-1500 words for comprehensive topics
- **Large Chunks**: 1500-3000 words for detailed sections (with subsections)

### 8. EXPLICIT DELIMITATION

**Boundary Markers:**
- Use horizontal rules (---) for major section breaks
- Employ consistent heading hierarchy for topic transitions
- Apply code blocks for technical content, examples, or data
- Utilize tables for comparative or structured information

**Example Delimitation:**
```markdown
## Topic A
[Content about Topic A]

---

## Topic B
[Content about Topic B]

### Subtopic B.1
[Detailed content]

```code
[Technical example]
```
```

### 9. REFERENCE DISAMBIGUATION

**Clarity Requirements:**
- **Specific Nouns**: Replace pronouns with explicit references
- **Full Context**: Don't assume prior knowledge from earlier sections
- **Clear Antecedents**: When using "this" or "that", specify what they refer to
- **Explicit Links**: Use clear phrases like "as mentioned in Section X"

**Examples:**
```
✗ BAD: "This approach works well because it..."
✓ GOOD: "The customer segmentation approach works well because the methodology..."

✗ BAD: "They found that..."
✓ GOOD: "Researchers at Stanford University found that..."
```

---

## SEARCHABILITY ENHANCEMENT

### 10. KEYWORD OPTIMIZATION

**Keyword Strategy:**
- **Natural Integration**: Include keywords in context, not forced
- **Synonym Inclusion**: Add related terms in parentheses
- **Technical Term Definition**: Define specialized vocabulary inline
- **Acronym Expansion**: Spell out acronyms on first use

**Implementation Pattern:**
```
Customer Relationship Management (CRM) systems enable businesses to track customer interactions...

Later references can use: CRM, customer relationship management, or relationship management system
```

### 11. CROSS-REFERENCING SYSTEM

**Internal Linking Requirements:**
- **Explicit Section References**: "See Section X for detailed implementation"
- **Topic Connections**: Link related concepts across document
- **Prerequisite Indication**: Specify what to read first
- **Related Resources**: Note external or supplementary materials

**Cross-Reference Format:**
```
For implementation details, see [Implementation Guide - Section 3.2]
Related concepts: [Data Privacy], [Security Protocols], [Compliance Requirements]
Prerequisites: Understanding of [Basic Networking Concepts]
```

### 12. INDEX AND GLOSSARY

**Required Reference Elements:**
- **Term Glossary**: Definitions of technical terms and acronyms
- **Concept Index**: Key topics with section references
- **Example Directory**: List of case studies and examples with locations
- **Resource Links**: External references and related materials

**Glossary Format:**
```
**API (Application Programming Interface)**: Software intermediary allowing two applications to communicate
**Asynchronous Processing**: Task execution without blocking other operations
**Authentication**: Process of verifying user identity
```

---

## SPECIALIZED CONTENT HANDLING

### 13. TECHNICAL CONTENT FORMATTING

**Code and Technical Elements:**
- **Code Blocks**: Use fenced code blocks with language specification
- **Inline Code**: Use backticks for short code snippets or technical terms
- **Formulas**: Present mathematical expressions clearly with LaTeX or plain text
- **Data Tables**: Use markdown tables for structured data

**Format Examples:**
````markdown
```python
def process_data(input_file):
    # Implementation code
    return processed_data
```

Use the `process_data()` function for batch processing.

| Metric | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|
| Revenue| 100| 120| 135| 150|
````

### 14. EXAMPLES AND CASE STUDIES

**Example Presentation Standards:**
- **Clear Labeling**: Mark examples explicitly as "Example:", "Case Study:", "Scenario:"
- **Complete Context**: Provide all necessary background for understanding
- **Outcome Specification**: Clearly state results or learnings
- **Relevance Statement**: Explain why example matters

**Example Structure:**
```
**Example: Email Marketing Campaign Optimization**

Context: Mid-sized e-commerce company with 50K subscribers
Challenge: Low open rates (12%) and conversions (1.5%)
Solution: Implemented segmentation and personalization
Results: Open rates increased to 28%, conversions to 4.2%
Key Learning: Personalization significantly impacts engagement metrics
```

### 15. PROCEDURAL CONTENT

**Step-by-Step Process Requirements:**
- **Sequential Numbering**: Use ordered lists for procedures
- **Action Verbs**: Start each step with clear action verb
- **Expected Outcomes**: Describe what should happen after each step
- **Conditional Logic**: Clearly mark decision points or variations

**Process Format:**
```
### Account Setup Procedure

1. **Navigate to registration page**: Go to website.com/register
   - Expected: Registration form appears with required fields

2. **Enter account information**: Provide email, password, and company name
   - Validation: System checks email format and password strength

3. **Verify email address**: Check inbox for confirmation email
   - Conditional: If no email received within 5 minutes, check spam folder

4. **Complete profile setup**: Add additional business details
   - Result: Account becomes fully active and accessible
```

---

## DOCUMENT MAINTENANCE INDICATORS

### 16. VERSION CONTROL INFORMATION

**Required Version Elements:**
- **Version Number**: Semantic versioning (e.g., v1.2.3)
- **Change Log**: Summary of modifications in each version
- **Update Date**: Timestamp of last revision
- **Change Author**: Who made modifications
- **Change Rationale**: Why updates were necessary

**Version Control Format:**
```
## Version History

**v2.1.0** (2024-09-15)
- Added section on advanced optimization techniques
- Updated tool recommendations based on new market research
- Corrected data in Section 4.3 regarding conversion rates
Author: [Name]
Reason: Quarterly update incorporating user feedback and market changes
```

### 17. REVIEW AND UPDATE SCHEDULE

**Maintenance Specifications:**
- **Review Frequency**: How often to assess document relevance
- **Update Triggers**: Conditions requiring immediate updates
- **Deprecation Warnings**: Outdated information alerts
- **Archival Process**: How to handle obsolete content

**Schedule Format:**
```
## Maintenance Schedule

**Regular Reviews**: Quarterly (January, April, July, October)
**Update Triggers**: 
- Major tool or platform changes
- Significant industry shifts
- User feedback indicating errors or gaps
**Deprecation**: Outdated content moved to archive section with warnings
**Archive Policy**: Content older than 2 years reviewed for removal or updates
```

---

## QUALITY ASSURANCE CHECKLIST

### Pre-Deployment Validation

Use this checklist before finalizing document:

#### Structure Quality
- [ ] Clear heading hierarchy (H1 → H2 → H3)
- [ ] Consistent formatting throughout document
- [ ] Logical information flow from general to specific
- [ ] Appropriate section lengths (not too long or short)

#### Content Quality
- [ ] All technical terms defined or explained in context
- [ ] Examples relevant and complete with context
- [ ] No ambiguous pronouns or references
- [ ] Consistent terminology usage throughout

#### Metadata Completeness
- [ ] All required metadata fields present
- [ ] Accurate keywords covering main topics
- [ ] Clear purpose and audience statements
- [ ] Version and update information current

#### AI Processing Optimization
- [ ] Scannable structure with clear sections
- [ ] Proper use of code blocks, tables, and formatting
- [ ] Self-contained sections with sufficient context
- [ ] Cross-references to related content

#### Searchability
- [ ] Natural keyword integration throughout
- [ ] Glossary of technical terms included
- [ ] Cross-reference system implemented
- [ ] Clear section titles for easy navigation

---

## IMPLEMENTATION GUIDELINES

### For Document Creators

**When Creating New Documents:**
1. Start with comprehensive metadata header
2. Plan heading hierarchy before writing content
3. Use consistent formatting patterns from beginning
4. Include glossary and cross-references as you write
5. Add examples and context throughout, not as afterthought

**When Converting Existing Documents:**
1. Analyze current structure and identify improvements needed
2. Add metadata header with complete information
3. Restructure content into clear hierarchical sections
4. Enhance with context, definitions, and cross-references
5. Validate against quality assurance checklist

### For AI Systems Processing Documents

**When Encountering AI-Friendly Documents:**
- Leverage heading structure for section identification
- Use metadata for relevance filtering and categorization
- Extract keywords for search and indexing
- Follow cross-references for related information
- Parse structured content (code blocks, tables) appropriately

**When Processing Non-Optimized Documents:**
- Apply intelligent chunking based on content patterns
- Infer structure from formatting cues
- Extract implicit metadata from content
- Create internal knowledge graph of relationships
- Flag ambiguities for potential clarification

---

## BENEFITS OF AI-FRIENDLY FORMAT

### For AI Systems
- **Faster Processing**: Clear structure reduces parsing overhead
- **Better Accuracy**: Explicit context improves understanding
- **Precise Retrieval**: Structured content enables targeted extraction
- **Relationship Mapping**: Cross-references support knowledge graphs
- **Quality Assessment**: Consistent patterns enable reliability evaluation

### For Human Users
- **Improved Discoverability**: Better search and navigation
- **Faster Comprehension**: Scannable structure aids understanding
- **Reliable Reference**: Consistent format supports repeated use
- **Easy Maintenance**: Clear structure simplifies updates
- **Better Collaboration**: Standards enable team coordination

### For Organizations
- **Knowledge Preservation**: Structured format prevents information loss
- **Scalable Systems**: Standards support growing knowledge bases
- **Integration Ready**: Consistent format enables tool integration
- **Quality Assurance**: Measurable criteria support document quality
- **Efficiency Gains**: Reduced time for information retrieval and processing

---

## CONCLUSION

AI-friendly document formatting is not about restricting creativity or natural language use—it's about enhancing structure and clarity to support both human and machine understanding. These criteria create documents that are:

- **Easily navigable** by humans and AI systems
- **Quickly processable** without sacrificing completeness
- **Highly searchable** through multiple access points
- **Maintainable** over time with clear update processes
- **Scalable** across growing knowledge bases

Implementation of these standards transforms documents from passive information containers into active knowledge resources that maximize value for all users and systems.