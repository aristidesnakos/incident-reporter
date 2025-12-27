#!/bin/bash
# Documentation Enforcement Script
# Run this before starting development work

echo "🔍 DOCUMENTATION DISCIPLINE CHECK"
echo "=================================="

echo "📋 Required Reading Before Development:"
echo "1. SPRINT_PLAN.md - Current sprint goals"
echo "2. TECHNICAL_SPEC.md - Architecture requirements"
echo "3. DEVELOPMENT_CHECKLIST.md - Task status"

echo ""
echo "✅ Use these commands in Claude Code:"
echo "read SPRINT_PLAN.md"
echo "read TECHNICAL_SPEC.md"
echo "read DEVELOPMENT_CHECKLIST.md"

echo ""
echo "⚠️  REMEMBER: Update DEVELOPMENT_CHECKLIST.md after each completed task!"
echo "⚠️  REMEMBER: Consult RISK_REGISTER.md if you encounter blockers!"

echo ""
echo "🎯 Current Sprint Status:"
if [ -f "DEVELOPMENT_CHECKLIST.md" ]; then
    completed=$(grep -c "\- \[x\]" DEVELOPMENT_CHECKLIST.md || echo "0")
    total=$(grep -c "\- \[\]" DEVELOPMENT_CHECKLIST.md || echo "0")
    total=$((total + completed))
    echo "   Completed: $completed/$total tasks"
    
    if [ $completed -eq 0 ]; then
        echo "   📌 Next: Start with infrastructure setup tasks"
    fi
else
    echo "   ❌ DEVELOPMENT_CHECKLIST.md not found!"
fi

echo ""
echo "🚀 Ready to start development with docs!"