# Canonical Prayer Format Specification

## Core Structure

Each prayer must follow this exact format:

```
=== Prayer {number} of Scroll {scroll_id} ===

{prayer_text}

---
COVERAGE: {start_line}-{end_line}  # {filename}
CHECKSUM: {sha256_hash}
BONES: {count} discovered
INHERITANCE: {type}
===
```

## Field Definitions

### Header
- `Prayer {number}`: Sequential 1-84 across all scrolls
- `Scroll {scroll_id}`: Sequential scroll ID (001, 002, etc.)

### Body
- `{prayer_text}`: The generated prayer incorporating Scripture patterns
- Must reflect actual verses read
- Marks discoveries with [BONES] tags
- Inherits from previous prayers per inheritance rules

### Footer Metadata
- `COVERAGE`: Line range actually read from Scripture file
- `CHECKSUM`: SHA256 hash of the Scripture file
- `BONES`: Count of new patterns discovered
- `INHERITANCE`: Type of inheritance applied
  - "GENESIS" - Prayer 1 (no inheritance)
  - "SIMPLE" - Regular prayers (from previous prayer)
  - "FULL_SCROLL" - First prayer of new scroll (all 12 from previous)

## Inheritance Rules

| Prayer Numbers | Inheritance Pattern |
|---------------|-------------------|
| 1 | No inheritance (GENESIS) |
| 2-12 | Each from previous prayer (SIMPLE) |
| 13 | ALL 12 from Scroll 1 (FULL_SCROLL) |
| 14-24 | Each from previous prayer (SIMPLE) |
| 25 | ALL 12 from Scroll 2 (FULL_SCROLL) |
| 26-36 | Each from previous prayer (SIMPLE) |
| 37 | ALL 12 from Scroll 3 (FULL_SCROLL) |
| ... | ... continues pattern |

## Validation Requirements

1. **Coverage Integrity**: Must match actual lines read
2. **Checksum Match**: Must match registry checksum
3. **Sequential Numbering**: No gaps or duplicates
4. **Inheritance Verification**: Correct pattern per rules
5. **Bone Discovery**: Marked and counted accurately

## Example

```
=== Prayer 13 of Scroll 002 ===

Lord, as the light broke forth in Genesis and structure emerged from chaos,
so too does Your Word build patterns within patterns. [BONES] The sevenfold
completion speaks through every verse, from creation's seven days to the 
seven churches of Revelation...

---
COVERAGE: 1-888  # KJV_2_888.txt
CHECKSUM: abc123def456...
BONES: 3 discovered
INHERITANCE: FULL_SCROLL
===
```

## JSONL Log Format

Each prayer generates a JSONL entry:

```json
{
  "timestamp": "2024-01-17T14:32:45.123Z",
  "event": "PRAYER_GENERATED",
  "prayer_number": 13,
  "scroll_id": "002",
  "coverage": "1-888",
  "filename": "KJV_2_888.txt",
  "checksum": "abc123...",
  "bones_count": 3,
  "inheritance": "FULL_SCROLL"
}
```

## Immutability

Once generated, prayers are NEVER modified. The canonical format ensures:
- Verifiable Scripture coverage
- Traceable inheritance chain
- Auditable pattern discovery
- Permanent record in Deep Archive

---

**SEAL: This format is the bedrock of honest Scripture saturation.**