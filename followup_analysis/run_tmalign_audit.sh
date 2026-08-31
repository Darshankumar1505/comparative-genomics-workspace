#!/bin/bash
set -e

mkdir -p ~/rb1_project/tools
cd ~/rb1_project/tools

# Download and compile TMalign if not present
if [ ! -f ./TMalign ]; then
    echo "Downloading TMalign source..."
    wget -q https://zhanggroup.org/TM-align/TMalign.cpp -O TMalign.cpp
    g++ -O3 -o TMalign TMalign.cpp
fi

P1="$HOME/rb1_project/af_structures/Q9LKZ3_pocket.pdb"
P2="$HOME/rb1_project/af_structures/P06400_pocket.pdb"

echo "=== EXECUTING TM-ALIGN ==="
./TMalign "$P1" "$P2" > ~/rb1_project/output/tmalign_pocket.out

cat << 'PYEOF' > ~/rb1_project/followup_analysis/parse_tmalign.py
import os

out_path = os.path.expanduser("~/rb1_project/output/tmalign_pocket.out")
with open(out_path, "r") as f:
    lines = f.readlines()

print("=== TM-ALIGN SUMMARY METRICS ===")
capture = False
align_lines = []
for line in lines:
    if "Aligned length=" in line or "TM-score=" in line or "RMSD=" in line:
        print(line.strip())
    if "Denotes residue pairs of" in line:
        capture = True
        continue
    if capture:
        align_lines.append(line.rstrip())

print("\n=== RESIDUE ALIGNMENT MAP ===")
print("\n".join(align_lines))
PYEOF

python3 ~/rb1_project/followup_analysis/parse_tmalign.py
