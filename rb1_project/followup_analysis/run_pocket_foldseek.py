import subprocess
import os
import pandas as pd

cmd = [
    "foldseek", "easy-search",
    os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3_pocket.pdb"),
    os.path.expanduser("~/rb1_project/af_structures/P06400_pocket.pdb"),
    os.path.expanduser("~/rb1_project/output/result_pocket_arabidopsis.tab"),
    os.path.expanduser("~/rb1_project/output/tmp_pocket"),
    "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,tcov,qcov,lddt,rmsd,qaln,taln"
]

subprocess.run(cmd, check=True)

cols = ["query", "target", "fident", "alnlen", "mismatch", "gapopen", 
        "qstart", "qend", "tstart", "tend", "evalue", "bits", 
        "tcov", "qcov", "lddt", "rmsd", "qaln", "taln"]

df = pd.read_csv(os.path.expanduser("~/rb1_project/output/result_pocket_arabidopsis.tab"), sep="\t", names=cols)
print("\n=== POCKET-RESTRICTED ALIGNMENT METRICS ===")
print(df[["query", "target", "fident", "alnlen", "rmsd", "lddt", "evalue"]].to_string())
