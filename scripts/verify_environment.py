#!/usr/bin/env python3
import hashlib
import os
import shutil
import subprocess
import sys

def verify_tmalign():
    print("=== ENVIRONMENT VERIFICATION: TM-ALIGN BINARY ===")
    tmalign_path = shutil.which("TMalign")
    if not tmalign_path:
        sys.exit(
            "FATAL ERROR: 'TMalign' executable not found in system PATH.\n"
            "Silent fallback to alternative alignment tools is strictly disabled."
        )

    print(f"Path: {tmalign_path}")

    hasher = hashlib.md5()
    with open(tmalign_path, "rb") as f:
        hasher.update(f.read())
    md5_hash = hasher.hexdigest()
    print(f"MD5 Checksum: {md5_hash}")

    try:
        proc = subprocess.run(
            [tmalign_path], capture_output=True, text=True, check=False
        )
        version_line = "Unknown"
        for line in proc.stdout.splitlines():
            if "TM-align" in line or "Version" in line:
                version_line = line.strip()
                break
        print(f"Version Header: {version_line}")
    except Exception as e:
        print(f"Warning: Could not extract version string: {e}")

    print("=== ENVIRONMENT VERIFICATION COMPLETE ===\n")

if __name__ == "__main__":
    verify_tmalign()

