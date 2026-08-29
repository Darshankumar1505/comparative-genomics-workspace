import pandas as pd

tab_path = "/home/hp/rb1_project/output/result_full_arabidopsis_audited.tab"
columns = [
    "query", "target", "fident", "alnlen", "mismatch", "gapopen",
    "qstart", "qend", "tstart", "tend", "evalue", "bits",
    "tcov", "qcov", "lddt", "rmsd", "qaln", "taln"
]

df = pd.read_csv(tab_path, sep="\t", names=columns)
print(f"Total alignment rows found: {len(df)}")
if len(df) > 0:
    print(df[["query", "target", "fident", "alnlen", "rmsd", "evalue", "qstart", "qend", "tstart", "tend"]].to_string())
else:
    print("Alignment table is empty. Check foldseek parameters or input PDB files.")
