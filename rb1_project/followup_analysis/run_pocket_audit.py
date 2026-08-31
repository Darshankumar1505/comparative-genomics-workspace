import os
import subprocess
import pandas as pd
from Bio import PDB

# Verified Pocket Domain Coordinates (Pfam PF01857/PF01858 & InterPro IPR006691):
# Human RB1 (P06400): 380 - 787
# Arabidopsis RBR1 (Q9LKZ3): 382 - 842

p06400_raw = os.path.expanduser("~/rb1_project/af_structures/P06400.pdb")
q9lkz3_raw = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3.pdb")

p06400_pocket = os.path.expanduser("~/rb1_project/af_structures/P06400_pocket.pdb")
q9lkz3_pocket = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3_pocket.pdb")

class ResRangeSelect(PDB.Select):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def accept_residue(self, residue):
        return self.start <= residue.get_id()[1] <= self.end

parser = PDB.PDBParser(QUIET=True)
writer = PDB.PDBIO()

# Truncate Human RB1
struct_h = parser.get_structure("P06400", p06400_raw)
writer.set_structure(struct_h)
writer.save(p06400_pocket, ResRangeSelect(380, 787))

# Truncate Arabidopsis RBR1
struct_a = parser.get_structure("Q9LKZ3", q9lkz3_raw)
writer.set_structure(struct_a)
writer.save(q9lkz3_pocket, ResRangeSelect(382, 842))

print("Successfully created truncated pocket domain PDB files.")

# Run Foldseek on pocket domains
out_tab = os.path.expanduser("~/rb1_project/output/result_pocket_arabidopsis.tab")
tmp_dir = os.path.expanduser("~/rb1_project/output/tmp_pocket")

cmd = [
    "foldseek", "easy-search",
    q9lkz3_pocket,
    p06400_pocket,
    out_tab,
    tmp_dir,
    "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,tcov,qcov,lddt,rmsd,qaln,taln"
]

subprocess.run(cmd, check=True)

cols = ["query", "target", "fident", "alnlen", "mismatch", "gapopen", 
        "qstart", "qend", "tstart", "tend", "evalue", "bits", 
        "tcov", "qcov", "lddt", "rmsd", "qaln", "taln"]

df = pd.read_csv(out_tab, sep="\t", names=cols)
print("\n=== POCKET-RESTRICTED ALIGNMENT METRICS ===")
print(df[["query", "target", "fident", "alnlen", "rmsd", "lddt", "evalue"]].to_string())

# Calculate TM-score via USalign / TMalign if installed, or via python structural alignment
try:
    tm_out = subprocess.check_output(["TMalign", q9lkz3_pocket, p06400_pocket]).decode()
    print("\n=== TM-ALIGN RESULTS ===")
    for line in tm_out.splitlines():
        if "TM-score" in line or "RMSD" in line:
            print(line)
except Exception:
    print("\nNote: Standard TMalign executable not found in PATH. Run 'TMalign Q9LKZ3_pocket.pdb P06400_pocket.pdb' to view normalized TM-score.")
