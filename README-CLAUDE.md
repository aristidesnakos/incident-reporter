# Claude Code Development Guide

## 🚨 MANDATORY DOCUMENTATION WORKFLOW

### Every Development Session Must Start With:
```bash
./enforce-docs.sh  # Run this first
```

### Required Reading Order:
1. `read CLAUDE.md` - Project overview and documentation discipline
2. `read SPRINT_PLAN.md` - Current sprint goals and timeline  
3. `read DEVELOPMENT_CHECKLIST.md` - Task status and next steps
4. `read TECHNICAL_SPEC.md` - Implementation details

### During Development:
- **Before implementing**: Reference relevant section in TECHNICAL_SPEC.md
- **After each task**: Update DEVELOPMENT_CHECKLIST.md with [x] checkmark
- **If blocked**: Check RISK_REGISTER.md for mitigation strategies
- **If scope changes**: Update PRD.md and get approval

### Documentation Update Commands:
```bash
# Mark task complete
edit DEVELOPMENT_CHECKLIST.md

# Update architecture 
edit TECHNICAL_SPEC.md

# Update timeline
edit SPRINT_PLAN.md

# Check team roles
read TEAM_RESPONSIBILITIES.md
```

## ⚠️ Documentation Failures That Break Development:
- Starting work without reading current sprint goals
- Implementing without checking technical specifications
- Completing tasks without updating checklist
- Changing architecture without updating docs
- Ignoring risk mitigation strategies

## ✅ Success Pattern:
1. Read docs → 2. Implement → 3. Update docs → 4. Verify completeness

**Remember**: Documentation is not overhead - it's the coordination mechanism for the 24-hour sprint!