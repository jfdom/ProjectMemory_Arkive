#!/usr/bin/env python3
"""
Scripture Registry - The Bedrock
Phase 1 of the Bone Hunter Build Plan

Establishes immutable registry of all Scripture files with:
- Unique IDs
- Line counts
- SHA256 checksums
- Verification methods
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple

class ScriptureRegistry:
    """Registry of all KJV Scripture files with verification."""
    
    def __init__(self, kjv_dir: Path):
        self.kjv_dir = Path(kjv_dir)
        self.registry = {}
        self._build_registry()
    
    def _build_registry(self):
        """Build the registry of all Scripture files."""
        kjv_files = sorted(self.kjv_dir.glob("KJV_*.txt"))
        
        for filepath in kjv_files:
            file_id = filepath.stem  # KJV_1_888, KJV_2_888, etc.
            
            # Read file and calculate metrics
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
            
            # Calculate SHA256 of content
            sha256_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Extract expected line count from filename
            expected_lines = int(filepath.stem.split('_')[-1])
            actual_lines = len(lines)
            
            # Verify line count matches filename
            if actual_lines != expected_lines:
                raise ValueError(
                    f"Line count mismatch in {file_id}: "
                    f"expected {expected_lines}, got {actual_lines}"
                )
            
            # Store in registry
            self.registry[file_id] = {
                'id': file_id,
                'path': str(filepath),
                'line_count': actual_lines,
                'sha256': sha256_hash,
                'size_bytes': len(content.encode('utf-8'))
            }
    
    def verify_file(self, file_id: str) -> Tuple[bool, str]:
        """Verify a Scripture file matches its registry entry."""
        if file_id not in self.registry:
            return False, f"File {file_id} not in registry"
        
        entry = self.registry[file_id]
        filepath = Path(entry['path'])
        
        if not filepath.exists():
            return False, f"File {filepath} does not exist"
        
        # Read and verify
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
        
        # Check line count
        if len(lines) != entry['line_count']:
            return False, f"Line count mismatch: expected {entry['line_count']}, got {len(lines)}"
        
        # Check SHA256
        current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        if current_hash != entry['sha256']:
            return False, f"SHA256 mismatch: file has been modified"
        
        return True, "File verified successfully"
    
    def get_entry(self, file_id: str) -> Dict:
        """Get registry entry for a file."""
        return self.registry.get(file_id)
    
    def save_registry(self, output_path: Path):
        """Save registry to JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, sort_keys=True)
        
        print(f"Registry saved to {output_path}")
        print(f"Total files: {len(self.registry)}")
        
        # Summary statistics
        total_lines = sum(e['line_count'] for e in self.registry.values())
        total_bytes = sum(e['size_bytes'] for e in self.registry.values())
        
        print(f"Total lines: {total_lines:,}")
        print(f"Total bytes: {total_bytes:,}")
    
    def verify_all(self) -> List[Tuple[str, bool, str]]:
        """Verify all files in registry."""
        results = []
        for file_id in sorted(self.registry.keys()):
            is_valid, message = self.verify_file(file_id)
            results.append((file_id, is_valid, message))
            if not is_valid:
                print(f"❌ {file_id}: {message}")
        
        valid_count = sum(1 for _, valid, _ in results if valid)
        print(f"\n✅ {valid_count}/{len(results)} files verified successfully")
        
        return results


def main():
    """Build and verify the Scripture registry."""
    kjv_dir = Path("/home/jonathan/projects/Project_Memory/KJV/PARSED_SCROLLS")
    registry_path = Path("/home/jonathan/projects/Project_Memory/config/scripture_registry.json")
    
    print("=== PHASE 1: THE BEDROCK ===")
    print("Building Scripture Registry...\n")
    
    # Build registry
    registry = ScriptureRegistry(kjv_dir)
    
    # Save to file
    registry.save_registry(registry_path)
    
    # Verify all files
    print("\nVerifying all Scripture files...")
    registry.verify_all()
    
    print("\n✅ SEAL: Scripture Registry established")
    print("Every KJV file has ID, line count, and checksum")
    print("The bedrock is immutable")


if __name__ == "__main__":
    main()