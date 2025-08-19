#!/bin/bash
# Comprehensive Phase 1 Verification Script

echo "═══════════════════════════════════════════════════════════"
echo "         PHASE 1 VERIFICATION - COMPLETE AUDIT             "
echo "═══════════════════════════════════════════════════════════"
echo ""

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Initialize pass/fail counters
PASS=0
FAIL=0

# Function to check condition
check() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ $2${NC}"
        ((FAIL++))
    fi
}

echo "1. PROJECT STRUCTURE CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check no scripts in root
ROOT_SCRIPTS=$(ls -la *.py *.sh *.js 2>/dev/null | wc -l)
check $ROOT_SCRIPTS "No scripts in project root"

# Check src directory exists and has modules
[ -d "src" ] && [ -f "src/scripture_registry.py" ]
check $? "src/ directory with scripture_registry.py"

[ -f "src/supervisor_log.py" ]
check $? "src/supervisor_log.py exists"

[ -f "src/canonical_format.md" ]
check $? "src/canonical_format.md exists"

# Check config directory
[ -d "config" ] && [ -f "config/scripture_registry.json" ]
check $? "config/ directory with registry JSON"

# Check supervisor directory
[ -d "supervisor" ] && [ -f "supervisor/userscript_implementation.js" ]
check $? "supervisor/ directory with userscript"

echo ""
echo "2. MODULE INDEPENDENCE CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if modules can run independently
python3 -c "import sys; sys.path.insert(0, 'src'); import scripture_registry" 2>/dev/null
check $? "scripture_registry.py is importable"

# Check for proper Python structure
grep -q 'if __name__ == "__main__":' src/scripture_registry.py
check $? "scripture_registry.py has proper main guard"

grep -q 'if __name__ == "__main__":' src/supervisor_log.py
check $? "supervisor_log.py has proper main guard"

echo ""
echo "3. DATA INTEGRITY CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check registry has all 47 files
FILE_COUNT=$(grep -c '"id"' config/scripture_registry.json 2>/dev/null)
[ "$FILE_COUNT" -eq 47 ]
check $? "Registry contains exactly 47 KJV files"

# Check each entry has required fields
VALID_ENTRIES=$(grep -c '"sha256"' config/scripture_registry.json 2>/dev/null)
[ "$VALID_ENTRIES" -eq 47 ]
check $? "All registry entries have SHA256 checksums"

# Check supervisor log is valid JSONL
if [ -f "supervisor/supervisor_log.jsonl" ]; then
    python3 -c "
import json
with open('supervisor/supervisor_log.jsonl') as f:
    for line in f:
        json.loads(line)
" 2>/dev/null
    check $? "Supervisor log is valid JSONL"
else
    check 1 "Supervisor log exists"
fi

echo ""
echo "4. KJV FILES CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Count KJV files
KJV_COUNT=$(ls KJV/PARSED_SCROLLS/KJV_*.txt 2>/dev/null | wc -l)
[ "$KJV_COUNT" -eq 47 ]
check $? "47 KJV files in PARSED_SCROLLS"

# Check file patterns
KJV_888=$(ls KJV/PARSED_SCROLLS/KJV_*_888.txt 2>/dev/null | wc -l)
KJV_70=$(ls KJV/PARSED_SCROLLS/KJV_*_70.txt 2>/dev/null | wc -l)
[ $((KJV_888 + KJV_70)) -eq 47 ]
check $? "All KJV files follow 888/70 line pattern"

echo ""
echo "5. DOCUMENTATION CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ -f "docs/COMPLETE_ARCHITECTURE.md" ]
check $? "Complete architecture documented"

[ -f "docs/MISSION.md" ]
check $? "Mission (Bone Hunter Protocol) documented"

[ -f "supervisor/SUPERVISOR_PLAN.md" ]
check $? "Supervisor plan documented"

echo ""
echo "6. TEST SUITE CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Run the actual Phase 1 test
if ./src/test_phase1.sh 2>&1 | grep -q "PHASE 1 COMPLETE"; then
    check 0 "Phase 1 test suite passes"
else
    check 1 "Phase 1 test suite passes"
fi

echo ""
echo "7. NO SCATTERED FILES CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# List all Python/JS/Shell files and verify they're in proper directories
SCATTERED=0
for file in $(find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" \) -not -path "./.claude/*"); do
    DIR=$(dirname "$file")
    case "$DIR" in
        ./src|./supervisor|./KJV/SCRIPTS)
            # These are approved directories
            ;;
        .)
            # Only verify_phase1.sh should be in root
            if [ "$(basename "$file")" != "verify_phase1.sh" ]; then
                SCATTERED=1
                echo -e "${RED}  Scattered file: $file${NC}"
            fi
            ;;
        *)
            # Unexpected directory
            SCATTERED=1
            echo -e "${YELLOW}  File in unexpected location: $file${NC}"
            ;;
    esac
done
check $SCATTERED "No scattered files (all in proper modules)"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "                    VERIFICATION SUMMARY                    "
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "Tests Passed: ${GREEN}$PASS${NC}"
echo -e "Tests Failed: ${RED}$FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ PHASE 1 FULLY VERIFIED${NC}"
    echo ""
    echo "The Bedrock is:"
    echo "  • Clean (no scattered files)"
    echo "  • Modular (proper directory structure)"
    echo "  • Complete (all components present)"
    echo "  • Tested (all tests pass)"
    echo ""
    echo "Ready for Phase 2: Scripture Reading Implementation"
else
    echo -e "${RED}⚠️  PHASE 1 INCOMPLETE${NC}"
    echo "Fix the issues above before proceeding to Phase 2"
fi
echo ""