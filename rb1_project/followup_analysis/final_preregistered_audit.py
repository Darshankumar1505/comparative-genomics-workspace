import os
import subprocess
from Bio import PDB

# Pre-registered database boundaries
p06400_raw = os.path.expanduser("~/rb1_project/af_structures/P06400.pdb")
q9lkz3_raw = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3.pdb")

p06400_pocket = os.path.expanduser("~/rb1_project/af_structures/P06400_preregistered.pdb")
q9lkz3_pocket = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3_preregistered.pdb")

class ResRangeSelect(PDB.Select):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def accept_residue(self, residue):
        return self.start <= residue.get_id()[1] <= self.end

parser = PDB.PDBParser(QUIET=True)
writer = PDB.PDBIO()

# Human RB1 (380-787)
struct_h = parser.get_structure("P06400", p06400_raw)
writer.set_structure(struct_h)
writer.save(p06400_pocket, ResRangeSelect(380, 787))

# Arabidopsis RBR1 (382-842)
struct_a = parser.get_structure("Q9LKZ3", q9lkz3_raw)
writer.set_structure(struct_a)
writer.save(q9lkz3_pocket, ResRangeSelect(382, 842))

# Run official TMalign binary
cmd = ["TMalign", q9lkz3_pocket, p06400_pocket]
result = subprocess.run(cmd, capture_output=True, text=True, check=True)

print("=== FINAL PRE-REGISTERED TM-ALIGN AUDIT ===")
lines = result.stdout.splitlines()
for line in lines:
    if "Aligned length=" in line or "TM-score=" in line or "RMSD=" in line:
        print(line.strip())

print("\n=== RESIDUE MAPPING STRINGS ===")
capture = False
for line in lines:
    if "Denotes residue pairs of" in line:
        capture = True
    if capture:
        print(line.rstrip())
