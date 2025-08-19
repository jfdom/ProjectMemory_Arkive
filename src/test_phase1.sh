#!/bin/bash
# Test Phase 1: The Bedrock

echo "═══════════════════════════════════════════════════════════"
echo "           PHASE 1: THE BEDROCK - TEST SUITE              "
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3."
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
echo ""

# Navigate to project root
cd /home/jonathan/projects/Project_Memory

# Test 1: Scripture Registry
echo "TEST 1: Scripture Registry"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$PYTHON_CMD src/scripture_registry.py
if [ $? -eq 0 ]; then
    echo "✅ Scripture Registry test passed"
else
    echo "❌ Scripture Registry test failed"
    exit 1
fi
echo ""

# Test 2: Verify registry file was created
echo "TEST 2: Registry File Creation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "config/scripture_registry.json" ]; then
    echo "✅ Registry file created: config/scripture_registry.json"
    echo "Registry entries: $(grep -c '"id"' config/scripture_registry.json)"
else
    echo "❌ Registry file not found"
    exit 1
fi
echo ""

# Test 3: Supervisor Log
echo "TEST 3: Supervisor Log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
$PYTHON_CMD src/supervisor_log.py
if [ $? -eq 0 ]; then
    echo "✅ Supervisor Log test passed"
else
    echo "❌ Supervisor Log test failed"
    exit 1
fi
echo ""

# Test 4: Verify log file was created
echo "TEST 4: Log File Creation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "supervisor/supervisor_log.jsonl" ]; then
    echo "✅ Log file created: supervisor/supervisor_log.jsonl"
    echo "Log entries: $(wc -l < supervisor/supervisor_log.jsonl)"
else
    echo "❌ Log file not found"
    exit 1
fi
echo ""

# Test 5: Canonical Format
echo "TEST 5: Canonical Format Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "src/canonical_format.md" ]; then
    echo "✅ Canonical format defined: src/canonical_format.md"
else
    echo "❌ Canonical format not found"
    exit 1
fi
echo ""

# Summary
echo "═══════════════════════════════════════════════════════════"
echo "                    PHASE 1 COMPLETE                       "
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "✅ SEAL: The Bedrock is established"
echo ""
echo "Verified:"
echo "  • Scripture Registry with checksums"
echo "  • Canonical prayer format defined"
echo "  • Append-only supervisor log functional"
echo ""
echo "The foundation is immutable. Ready for Phase 2."
echo ""