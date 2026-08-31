import pandas as pd
import subprocess
import os

tab_path = "/home/hp/rb1_project/output/result_full_arabidopsis_audited.tab"
cols = ["query", "target", "fident", "alnlen", "mismatch", "gapopen", 
        "qstart", "qend", "tstart", "tend", "evalue", "bits", 
        "tcov", "qcov", "lddt", "rmsd", "qaln", "taln"]

df = pd.read_csv(tab_path, sep="\t", names=cols)
print("=== FOLDSEEK ALIGNMENT SUMMARY ===")
print(df[["query", "target", "fident", "alnlen", "rmsd", "lddt", "evalue"]].to_string())

# Re-run foldseek with TM-score extraction if needed, or inspect US-align/TM-align directly on pocket domains
print("\n--- Next Step: Extracting Pocket-Specific Coordinates ---")
print("Arabidopsis RBR1 (Q9LKZ3) Retinoblastoma Pocket Domain (InterPro): ~Residues 380 - 850")
print("Human RB1 (P06400) Retinoblastoma Pocket Domain: ~Residues 380 - 790")
