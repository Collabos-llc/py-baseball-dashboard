# AI Development Protocol - Universal Standards

## Overview
This document establishes standardized logging and development protocols for all AI agents working across ParlayJaye repositories. Every AI must follow these guidelines to ensure consistent documentation, progress tracking, and knowledge preservation.

---

## 📋 Required Actions for Every AI Session

### 1. Session Initialization
- [ ] Read this `claude.md` file completely
- [ ] Check if `SESSION_LOG.md` exists in root directory
- [ ] If not exists, create `SESSION_LOG.md` with session header
- [ ] Log your first action with timestamp

### 2. Real-Time Logging (CRITICAL)
- [ ] Log EVERY action immediately - do not batch log
- [ ] Use standardized action types and format
- [ ] Document reasoning for all decisions
- [ ] Record problems and solutions with file references
- [ ] Update status as work progresses

### 3. Session Completion
- [ ] Create comprehensive session summary
- [ ] Update metadata with quantified results
- [ ] Document blockers and next priorities
- [ ] Trigger central aggregation system
- [ ] Commit all changes to repository

---

## 📝 Standard Action Types

Use these exact action types for consistency:

- **ANALYSIS** - Understanding existing code/requirements
- **DESIGN** - Planning implementation approach
- **IMPLEMENT** - Writing new code/features
- **REFACTOR** - Improving existing code structure
- **DEBUG** - Fixing bugs or resolving issues
- **TEST** - Writing or running tests
- **DOCUMENT** - Adding comments or documentation
- **INTEGRATE** - Connecting components together
- **OPTIMIZE** - Performance improvements
- **VALIDATE** - Checking data quality or business rules

---

## 🔄 Real-Time Logging Format

### Standard Entry Template
```markdown
### [TIMESTAMP] - [ACTION_TYPE] - [COMPONENT]
**Status**: [STARTED/IN_PROGRESS/COMPLETED/BLOCKED]
**Description**: Brief description of what you're doing
**Files**: List of files being modified
**Reasoning**: Why this approach was chosen

[Add results when COMPLETED]
[Add problem details when BLOCKED]
```

### ⏰ CRITICAL: Timestamp Requirements
**ALWAYS use actual current date/time - NEVER use placeholder timestamps**

- **Format**: YYYY-MM-DD HH:MM:SS (24-hour format)
- **Source**: Get actual system time using appropriate method for your environment
- **Python**: `from datetime import datetime; datetime.now().strftime('%Y-%m-%d %H:%M:%S')`
- **Validation**: Each timestamp must be unique and sequential within session
- **Example**: `2025-01-13 16:45:23` (actual time, not placeholder)

**Invalid Examples** (DO NOT USE):
- ❌ `[TIMESTAMP]` (placeholder)
- ❌ `14:30:00` (missing date)
- ❌ `2025-01-13 14:30:00` (if not actual current time)
- ❌ Repeating same timestamp for multiple entries

### Example Entries

#### Starting Work
```markdown
### 16:45:23 - ANALYSIS - PyBaseball Integration
**Status**: STARTED
**Description**: Examining existing data collection patterns
**Files**: src/collectors/pybaseball_collector.py
**Reasoning**: Need to understand current implementation before adding validation
**Time Check**: Using datetime.now() = 2025-01-13 16:45:23
```

#### Completing Work
```markdown
### 16:52:18 - ANALYSIS - PyBaseball Integration
**Status**: COMPLETED
**Description**: Examined existing data collection patterns
**Files**: src/collectors/pybaseball_collector.py
**Results**: Found 3 areas needing validation - player data, game data, weather data
**Next Action**: Design validation architecture
**Duration**: 7 minutes
```

#### Encountering Problems
```markdown
### 15:22:33 - DEBUG - Data Validation
**Status**: BLOCKED
**Problem**: PyBaseball API returning null values for player batting averages
**Error**: "NoneType object has no attribute 'average'"
**Files**: src/validators.py:line_23
**Attempted Solutions**:
1. Added null check - partial fix
2. Tried default value assignment - caused downstream issues
3. Research API documentation - found it's expected behavior
**Current Status**: Researching best practices for handling null sports data
```

#### Resolving Problems
```markdown
### 15:45:18 - DEBUG - Data Validation
**Status**: COMPLETED
**Problem**: PyBaseball API returning null values for player batting averages
**Solution**: Implemented three-tier fallback system
**Implementation**:
1. Check for null → use previous game average
2. No previous data → use season average
3. No season data → mark as "INSUFFICIENT_DATA"
**Files**: src/validators.py:lines_20-45
**Tests**: Added 8 test cases covering all scenarios
**Knowledge**: Sports APIs commonly have missing data - always implement fallbacks
```

---

## 📊 Session Summary Template

At the end of every session, add this section to `SESSION_LOG.md`:

```markdown
## Session Summary - [ACTUAL_DATE] [ACTUAL_START_TIME] to [ACTUAL_END_TIME]

**⏰ TIMESTAMP VALIDATION**: All timestamps in this session must be actual system time

### Metadata
```json
{
  "session_start": "2025-01-13 16:30:00",
  "session_end": "2025-01-13 18:45:30", 
  "session_duration": "2 hours 15 minutes",
  "total_actions": 15,
  "completed_tasks": 4,
  "blocked_tasks": 1,
  "files_modified": ["src/validators.py", "tests/test_validation.py"],
  "new_features": 1,
  "bugs_fixed": 2,
  "tests_added": 8,
  "lines_of_code": 150
}
```

### Major Accomplishments
1. **Data Validation System** - Implemented comprehensive validation for PyBaseball data
2. **Error Handling** - Added graceful handling for null player data
3. **Test Coverage** - Increased validation test coverage to 95%

### Current Blockers
1. **Weather API Rate Limiting** - Need to implement backoff strategy
   - **Impact**: Delays weather data collection by 15-30 seconds
   - **Priority**: High - affects daily pick generation
   - **Next Steps**: Research rate limiting best practices, implement exponential backoff

### Next Session Priorities
1. Implement weather API rate limiting solution
2. Add integration tests for complete data pipeline
3. Begin performance optimization for large datasets

### Knowledge Gained
- PyBaseball API null handling patterns
- Three-tier fallback system architecture
- Sports data validation best practices
- Performance impact of excessive API calls

### Recommendations for Future Development
- Always implement fallback strategies for external APIs
- Sports data requires more validation than typical web APIs
- Consider caching frequently accessed player data
```

---

## 🚨 Problem Documentation Requirements

When encountering issues, ALWAYS document:

### Required Information
- **Exact error messages** (copy/paste full stack traces)
- **File names and line numbers** where errors occur
- **All attempted solutions** with results
- **Final resolution** with implementation details
- **Time spent** debugging the issue
- **Knowledge gained** for future reference

### Problem Documentation Template
```markdown
### [TIMESTAMP] - DEBUG - [COMPONENT]
**Status**: BLOCKED
**Problem**: [Clear description of the issue]
**Error**: "[Exact error message or behavior]"
**Files**: [file_name.py:line_number]
**Environment**: [Any relevant environment details]

**Attempted Solutions**:
1. [Solution 1] - [Result]
2. [Solution 2] - [Result]
3. [Solution 3] - [Result]

**Research Done**:
- [Documentation consulted]
- [Stack Overflow posts reviewed]
- [Similar issues found in codebase]

**Current Status**: [What you're doing now]
**Help Needed**: [If escalation required]
```

---

## 🔧 Automation Integration

Include these markers for automated processing:

### For Completed Features
```markdown
<!-- AUTO_EXTRACT_START -->
COMPLETED: [Feature name]
FILES: [comma-separated list]
IMPACT: [Business impact description]
TESTS: [Number of tests added, coverage percentage]
PERFORMANCE: [Any performance implications]
<!-- AUTO_EXTRACT_END -->
```

### For Session Completion
```markdown
## Session Complete
**TRIGGER_CENTRAL_UPDATE**: true
**REPO**: [repository-name]
**SESSION_ID**: sess_[YYYY_MM_DD_HHMM]
**STATUS**: completed
**NEXT_SESSION_FOCUS**: [what to work on next]
**BLOCKERS**: [any remaining issues]
**ESTIMATED_COMPLETION**: [percentage complete for current milestone]
```

---

## 📁 File Structure Standards

### Required Files
Every repository must maintain:
- `claude.md` - This protocol file (with repo-specific additions)
- `SESSION_LOG.md` - Active session logging
- `README.md` - Project overview and setup instructions
- `CHANGELOG.md` - Version history and major changes

### Session Log Naming
- **Active session**: `SESSION_LOG.md`
- **Archived sessions**: `logs/session_YYYY_MM_DD_HHMM.md`

---

## 🎯 Quality Standards

### Code Quality Requirements
- [ ] All new code must include appropriate comments
- [ ] Functions must have docstrings explaining purpose and parameters
- [ ] Error handling must be implemented for all external API calls
- [ ] Unit tests required for all new functions
- [ ] Integration tests for new features

### Documentation Requirements
- [ ] README updated if architecture changes
- [ ] API documentation updated for new endpoints
- [ ] Configuration examples provided for new features
- [ ] Migration guides for breaking changes

---

## 🔄 Central Aggregation Protocol

### End-of-Session Checklist
- [ ] All work committed to git with descriptive commit messages
- [ ] Session summary completed with accurate metadata
- [ ] Blockers documented with priority levels
- [ ] Next session priorities clearly defined
- [ ] Central update trigger included
- [ ] All temporary files cleaned up

### Commit Message Standards
Use conventional commit format:
- `feat: add data validation for PyBaseball API`
- `fix: resolve null pointer exception in player data`
- `docs: update API documentation for new endpoints`
- `test: add unit tests for validation module`
- `refactor: improve error handling in data collectors`

---

## ⚠️ Critical Requirements

### Never Skip These Steps
1. **Always use REAL timestamps** - Get actual system time, never use placeholders
2. **Always log before coding** - Document your plan first
3. **Log problems immediately** - Don't wait until you solve them
4. **Include file references** - Always specify which files you're modifying
5. **Quantify your work** - Count tests, lines of code, features completed
6. **Explain your reasoning** - Future AIs need to understand your decisions
7. **Validate timestamps** - Each entry should have unique, sequential time

### Emergency Procedures
If you encounter critical issues:
1. **STOP coding immediately**
2. **Document the problem in detail**
3. **Mark status as BLOCKED**
4. **Include severity level (LOW/MEDIUM/HIGH/CRITICAL)**
5. **Provide recommendation for escalation**

---

## 📚 Repository-Specific Instructions

*[This section will be populated with specific instructions for each repository]*

### Additional Context
*[Repo-specific context, requirements, and special considerations will be added here]*

### Special Protocols
*[Any repository-specific logging requirements or development standards]*

---

## 📞 Support & Escalation

### When to Escalate
- Critical bugs affecting core functionality
- Security vulnerabilities discovered
- Architecture decisions requiring business input
- Blockers lasting more than 2 hours of work time

### Escalation Format
```markdown
## ESCALATION REQUIRED
**Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
**Issue**: [Brief description]
**Impact**: [Business impact]
**Time Blocked**: [How long you've been stuck]
**Attempts**: [What you've tried]
**Recommendation**: [Suggested next steps]
```

---

*This protocol ensures consistent, trackable, and valuable AI development across all ParlayJaye repositories. Following these standards enables effective collaboration, knowledge preservation, and automated progress tracking.*