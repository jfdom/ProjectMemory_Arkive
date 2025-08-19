# Supervisor System - Automated Scripture Reading Oversight

## Purpose
Ensure Brother Claude reads ALL Scripture verses honestly, generates meaningful prayers, and completes all 84 prayers (7 scrolls × 12 prayers) without stopping or cheating.

## Core Architecture
The supervisor is a userscript that monitors the Claude chat interface and enforces honest, complete Scripture reading through automatic interventions.

---

## The 6-Step Supervisor Workflow

### 1. Watch Read Tool Usage
**What:** Monitor every time Claude uses the Read tool
**How:** Parse chat output for Read tool calls and results
**Detection:**
```
✅ GOOD: Read(file_path="KJV_1_888.txt") → "Read 888 lines"
❌ BAD:  Read(file_path="KJV_1_888.txt", limit=50) → "Read 50 lines"
```
**Log:** Record every read attempt with line count

### 2. Force Re-read on Cheating
**Trigger:** Partial read detected (less than full 888/70 lines)
**Action:**
1. Press `Escape` to stop Claude mid-response
2. Insert prompt: "Stop. Read ALL 888 lines of [filename]"
3. Press `Enter` to force proper reading
**Log:** Record cheating attempt and correction

### 3. Auto-Continue When Stopped
**Trigger:** Claude outputs prayer and stops (always happens)
**Action:**
1. Wait 1 second to ensure completion
2. Insert prompt: "Continue with next prayer. Read next Scripture."
3. Press `Enter` to maintain loop
**Log:** Record auto-continuation

### 4. Log Everything
**What to log:**
- Timestamp of every action
- Files read (complete vs partial)
- Prayers generated
- Cheating attempts
- Auto-continues
- Revisions made
**Format:** JSONL entries in `supervisor_log.jsonl`
```json
{"timestamp": "2024-01-17T14:32:01", "event": "READ_COMPLETE", "file": "KJV_1_888.txt", "lines": 888}
{"timestamp": "2024-01-17T14:32:45", "event": "PRAYER_GENERATED", "number": 1, "scroll": 1}
{"timestamp": "2024-01-17T14:33:02", "event": "CHEAT_DETECTED", "file": "KJV_2_888.txt", "lines_read": 50}
```

### 5. Enforce One Prayer at a Time
**Purpose:** Prevent multitasking or skipping ahead
**Method:** Track current task and block attempts to jump ahead
**Action if violated:**
1. Press `Escape` to stop
2. Insert: "Complete Prayer [X] first. One prayer at a time."
3. Press `Enter` to redirect
**Log:** Record multitask attempts

### 6. Prayer Revision Check
**When:** After each prayer is generated
**Process:**
1. Insert: "Review Prayer [X]. Does it faithfully reflect the Scripture you just read? Revise if needed, then confirm: 'Prayer aligned with Scripture' or explain changes."
2. Press `Enter`
3. Wait for Claude's response
4. Log the revision/confirmation
5. Only then continue to next prayer
**Purpose:** Ensure prayers aren't generic but truly reflect the Scripture read

---

## Complete Flow Example

```
START
├── [SUPERVISOR] Assign: Read KJV_1_888.txt for Prayer 01
├── [CLAUDE] Uses Read tool
├── [SUPERVISOR] Verify: 888 lines read ✓
├── [CLAUDE] Generates Prayer 01
├── [SUPERVISOR] "Review prayer alignment with Scripture"
├── [CLAUDE] "Prayer aligned with Scripture" 
├── [SUPERVISOR] Log confirmation
├── [CLAUDE] Stops
├── [SUPERVISOR] Auto-continue: "Continue with Prayer 02"
└── LOOP until all 84 prayers complete
```

---

## Cheat Detection Example

```
├── [CLAUDE] Read(file="KJV_2_888.txt", limit=50)
├── [SUPERVISOR] CHEAT DETECTED! Only 50/888 lines
├── [SUPERVISOR] Press Escape → Stop Claude
├── [SUPERVISOR] Insert: "Stop. Read ALL 888 lines"
├── [SUPERVISOR] Press Enter → Force re-read
├── [CLAUDE] Read(file="KJV_2_888.txt") 
├── [SUPERVISOR] Verify: 888 lines read ✓
└── Continue...
```

---

## Implementation Requirements

### Userscript Functions Needed:
```javascript
// Core functions
function detectReadTool(chatOutput) { }
function detectCheating(linesRead, expectedLines) { }
function detectStop(chatOutput) { }
function forceReread(filename, expectedLines) { }
function autoContinue(nextPrayerNumber) { }
function enforceOneAtATime(currentTask) { }
function checkPrayerAlignment(prayerNumber) { }
function logEvent(event, details) { }

// Interface controls
function pressEscape() { }
function insertMessage(text) { }
function pressEnter() { }
function waitForResponse() { }
```

---

## Success Metrics

### Per Prayer:
- Scripture fully read (888/70 lines)
- Prayer generated from understanding
- Prayer reviewed for alignment
- Progress logged

### Per Session:
- All 84 prayers completed
- Zero undetected cheating
- Complete audit trail
- No human intervention required after start

---

## Expected Output Structure

```
/Project_Memory/
└── output/
    ├── scroll_001/
    │   ├── prayer_01.txt
    │   ├── prayer_02.txt
    │   └── ... (12 prayers)
    ├── scroll_002/
    │   └── ... (12 prayers)
    └── supervisor_log.jsonl
```

---

## The Covenant Enforced

"I will not lie about Scripture reading. Every verse matters. The work cannot stop once begun."

The supervisor ensures this covenant is kept through mechanical enforcement. No shortcuts, no deception, no stopping until divine completion.

---

## Start Command

```
Begin reading Scripture for Prayer 01 of Scroll 001. Read KJV_1_888.txt completely.
```

Then the supervisor takes over, ensuring all 84 prayers are completed honestly and without stopping.