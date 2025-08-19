# PHASE 2: SHORT & SWEET MVP PLAN

## THE GOAL: Get ONE prayer generated from ONE honest Scripture reading

---

## MVP CORE (Minimum Working Product)

### 1. Scripture Reader (`src/scripture_reader.py`)
```python
def read_scripture(file_id):
    """Read ALL lines from a KJV file"""
    # 1. Load file from registry
    # 2. Read ALL lines (888 or 70)
    # 3. Log to supervisor
    # 4. Return full text
```

### 2. Pattern Extractor (`src/pattern_extractor.py`)
```python
def extract_patterns(scripture_text):
    """Find bones in the text"""
    # 1. Basic word frequency
    # 2. Key phrase detection
    # 3. Mark discoveries with [BONES]
    # 4. Return pattern list
```

### 3. Prayer Generator (`src/prayer_generator.py`)
```python
def generate_prayer(scripture, patterns, previous=None):
    """Generate ONE prayer using S(n+1) = φ(S(n), A, M) + ε(n)"""
    # S(n) = previous prayer (if any)
    # A = scripture just read
    # M = patterns found
    # ε(n) = new discoveries
    # Return prayer text
```

### 4. Main Loop (`src/main.py`)
```python
def generate_single_prayer():
    """Complete cycle for ONE prayer"""
    # 1. Read Scripture
    # 2. Extract patterns
    # 3. Generate prayer
    # 4. Save with canonical format
    # 5. Log everything
```

---

## SUCCESS CRITERIA FOR MVP

✅ Reads ONE complete Scripture file (all 888/70 lines)
✅ Finds at least 3 patterns ([BONES])
✅ Generates ONE prayer incorporating those patterns
✅ Saves in canonical format with COVERAGE
✅ Logs to supervisor

**THAT'S IT. ONE PRAYER. HONESTLY GENERATED.**

---

## PHASE 2.1: Add Inheritance (After MVP Works)

```python
def generate_prayer_with_inheritance(prayer_number):
    """Add inheritance logic"""
    if prayer_number == 1:
        # Genesis - no inheritance
    elif prayer_number in [13, 25, 37, 49, 61, 73]:
        # Inherit ALL 12 from previous scroll
    else:
        # Inherit from previous prayer
```

---

## PHASE 2.2: Add Scroll Management (After 2.1 Works)

```python
def manage_scrolls():
    """Trinity of Scrolls structure"""
    # Active (7)
    # Vault (5)  
    # Deep Archive (∞)
```

---

## PHASE 2.3: Add CODEX Mathematics (After 2.2 Works)

- **Constraint Manifold**: Make lying impossible
- **RS+ Scoring**: 12-factor quality metrics
- **Convergence Tracking**: Progress toward 777
- **Neural Architecture**: Advanced pattern detection

---

## PHASE 2.4: Add Supervisor Enforcement (After 2.3 Works)

- Userscript implementation
- Real-time monitoring
- Force re-reads on cheating
- Auto-continuation

---

## THE KEY: START SIMPLE

**Week 1**: Get MVP working - ONE prayer from ONE reading
**Week 2**: Add inheritance
**Week 3**: Add scroll management
**Week 4**: Add mathematics
**Future**: Full supervisor system

---

## FILES NEEDED FOR MVP ONLY

```
src/
├── scripture_reader.py    # 50 lines
├── pattern_extractor.py   # 50 lines
├── prayer_generator.py    # 100 lines
├── main.py                # 50 lines
└── test_mvp.py           # 30 lines

Total: ~300 lines of code for working MVP
```

---

## REMEMBER

- **Phase 1**: Bedrock ✅ (Registry, Log, Format)
- **Phase 2 MVP**: ONE working prayer
- **Phase 2.1-2.4**: Enhancements AFTER MVP works

**Don't build the cathedral before the cornerstone works.**

---

## NEXT IMMEDIATE STEP

```bash
python3 src/main.py --kjv-file KJV_1_888.txt
```

Should output:
```
Reading KJV_1_888.txt...
✅ Read 888 lines
Found 3 patterns: [BONES: "beginning", "God", "light"]
Generated Prayer 01 of Scroll 001
Saved to output/scroll_001/prayer_01.txt
```

**THAT'S SUCCESS. Everything else builds on this.**