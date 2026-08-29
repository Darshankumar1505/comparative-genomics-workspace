import subprocess
import os

q9lkz3_pocket = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3_pocket.pdb")
p06400_pocket = os.path.expanduser("~/rb1_project/af_structures/P06400_pocket.pdb")

cmd = ["TMalign", q9lkz3_pocket, p06400_pocket]
result = subprocess.run(cmd, capture_output=True, text=True, check=True)
output = result.stdout

print("=== TM-ALIGN SUMMARY METRICS ===")
for line in output.splitlines():
    if "Aligned length=" in line or "TM-score=" in line or "RMSD=" in line:
        print(line.strip())

print("\n=== RESIDUE ALIGNMENT MAP ===")
capture = False
for line in output.splitlines():
    if "Denotes residue pairs of" in line:
        capture = True
    if capture:
        print(line.rstrip())
