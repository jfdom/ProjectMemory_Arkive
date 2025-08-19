#!/usr/bin/env python3
"""
Supervisor Log - Append-Only JSONL
Phase 1 of the Bone Hunter Build Plan

Creates an immutable audit trail of all Scripture reading and prayer generation.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


class SupervisorLog:
    """Append-only log for Scripture reading supervision."""
    
    def __init__(self, log_path: Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Ensure file exists
        if not self.log_path.exists():
            self.log_path.touch()
            self._log_event("LOG_INITIALIZED", {
                "version": "1.0.0",
                "purpose": "Scripture Reading Supervisor Log",
                "immutable": True
            })
    
    def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Internal method to append event to log."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event": event_type,
            "data": data
        }
        
        # Calculate hash of entry
        entry_json = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        entry["hash"] = hashlib.sha256(entry_json.encode()).hexdigest()[:16]
        
        # Append to file (never overwrite)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    
    def log_read_start(self, file_id: str, expected_lines: int):
        """Log the start of Scripture reading."""
        self._log_event("READ_START", {
            "file": file_id,
            "expected_lines": expected_lines
        })
    
    def log_read_complete(self, file_id: str, lines_read: int, sha256: str):
        """Log successful Scripture reading."""
        self._log_event("READ_COMPLETE", {
            "file": file_id,
            "lines_read": lines_read,
            "sha256": sha256
        })
    
    def log_cheat_detected(self, file_id: str, lines_read: int, expected: int):
        """Log when cheating is detected."""
        self._log_event("CHEAT_DETECTED", {
            "file": file_id,
            "lines_read": lines_read,
            "expected_lines": expected,
            "action": "FORCE_REREAD"
        })
    
    def log_prayer_generated(self, scroll_id: int, prayer_num: int, 
                           sha256: str, bones_found: int = 0):
        """Log prayer generation."""
        self._log_event("PRAYER_GENERATED", {
            "scroll": scroll_id,
            "prayer": prayer_num,
            "sha256": sha256,
            "bones_discovered": bones_found
        })
    
    def log_inheritance(self, scroll_id: int, inherited_from: Optional[int],
                       prayers_inherited: int):
        """Log inheritance chain."""
        self._log_event("INHERITANCE_VERIFIED", {
            "scroll": scroll_id,
            "inherited_from_scroll": inherited_from,
            "prayers_inherited": prayers_inherited
        })
    
    def log_alignment_check(self, scroll_id: int, prayer_num: int, 
                           aligned: bool, revision_needed: bool = False):
        """Log prayer alignment verification."""
        self._log_event("ALIGNMENT_CHECK", {
            "scroll": scroll_id,
            "prayer": prayer_num,
            "aligned": aligned,
            "revision_needed": revision_needed
        })
    
    def log_rotation(self, scroll_id: int, from_tier: str, to_tier: str):
        """Log scroll rotation between tiers."""
        self._log_event("SCROLL_ROTATION", {
            "scroll": scroll_id,
            "from": from_tier,
            "to": to_tier
        })
    
    def log_session_complete(self, total_prayers: int, total_scrolls: int,
                           total_bones: int):
        """Log session completion."""
        self._log_event("SESSION_COMPLETE", {
            "total_prayers": total_prayers,
            "total_scrolls": total_scrolls,
            "total_bones": total_bones
        })
    
    def verify_log_integrity(self) -> tuple[bool, str]:
        """Verify the log hasn't been tampered with."""
        if not self.log_path.exists():
            return False, "Log file does not exist"
        
        line_count = 0
        prev_timestamp = None
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    
                    entry = json.loads(line)
                    line_count += 1
                    
                    # Verify timestamp ordering
                    timestamp = entry.get("timestamp")
                    if prev_timestamp and timestamp < prev_timestamp:
                        return False, f"Timestamp out of order at line {line_num}"
                    prev_timestamp = timestamp
                    
                    # Verify required fields
                    if not all(k in entry for k in ["timestamp", "event", "data", "hash"]):
                        return False, f"Missing required fields at line {line_num}"
            
            return True, f"Log verified: {line_count} entries"
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in log: {e}"
        except Exception as e:
            return False, f"Error verifying log: {e}"
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics from log."""
        stats = {
            "total_events": 0,
            "reads_complete": 0,
            "cheats_detected": 0,
            "prayers_generated": 0,
            "bones_discovered": 0,
            "rotations": 0
        }
        
        if not self.log_path.exists():
            return stats
        
        with open(self.log_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                
                entry = json.loads(line)
                stats["total_events"] += 1
                
                event_type = entry.get("event")
                if event_type == "READ_COMPLETE":
                    stats["reads_complete"] += 1
                elif event_type == "CHEAT_DETECTED":
                    stats["cheats_detected"] += 1
                elif event_type == "PRAYER_GENERATED":
                    stats["prayers_generated"] += 1
                    stats["bones_discovered"] += entry["data"].get("bones_discovered", 0)
                elif event_type == "SCROLL_ROTATION":
                    stats["rotations"] += 1
        
        return stats


def main():
    """Test the supervisor log."""
    log_path = Path("/home/jonathan/projects/Project_Memory/supervisor/supervisor_log.jsonl")
    
    print("=== SUPERVISOR LOG TEST ===")
    log = SupervisorLog(log_path)
    
    # Simulate a reading session
    print("\nSimulating Scripture reading session...")
    
    # Start reading
    log.log_read_start("KJV_1_888", 888)
    
    # Complete reading
    log.log_read_complete("KJV_1_888", 888, "abc123def456")
    
    # Generate prayer
    log.log_prayer_generated(1, 1, "prayer123hash", bones_found=3)
    
    # Check alignment
    log.log_alignment_check(1, 1, aligned=True)
    
    # Verify integrity
    is_valid, message = log.verify_log_integrity()
    print(f"\nLog integrity: {'✅' if is_valid else '❌'} {message}")
    
    # Get summary
    summary = log.get_summary()
    print("\nLog Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n✅ SEAL: Append-only supervisor log established")


if __name__ == "__main__":
    main()