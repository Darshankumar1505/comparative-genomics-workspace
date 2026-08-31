import os
import subprocess
import requests

print("--- RESTARTING PIPELINE: Locating PDB files ---")
# Search for PDB files recursively from project root
pfiles = {}
for root, dirs, files in os.walk("/home/hp/rb1_project"):
    for f in files:
        if f.endswith(".pdb"):
            pfiles[f] = os.path.join(root, f)

print(f"Found PDB files: {list(pfiles.keys())}")

# Ensure required PDBs are copied locally
target_pdbs = {"P06400.pdb": "human", "D8U5W5.pdb": "volvox", "P56711.pdb": "arabidopsis"}
for pdb_name in target_pdbs:
    if pdb_name in pfiles:
        subprocess.run(["cp", pfiles[pdb_name], "."])
        print(f"Copied {pdb_name} to current directory.")
    else:
        print(f"[WARNING] Could not find {pdb_name} automatically!")

os.makedirs("output", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

if os.path.exists("P06400.pdb") and os.path.exists("D8U5W5.pdb"):
    print("\nRunning Foldseek for Volvox (D8U5W5)...")
    subprocess.run([
        "foldseek", "easy-search",
        "P06400.pdb", "D8U5W5.pdb",
        "output/result_full_volvox.tab",
        "tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)

if os.path.exists("P06400.pdb") and os.path.exists("P56711.pdb"):
    print("Running Foldseek for Arabidopsis (P56711)...")
    subprocess.run([
        "foldseek", "easy-search",
        "P06400.pdb", "P56711.pdb",
        "output/result_full_arabidopsis.tab",
        "tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)

print("\n[SUCCESS] Fresh pipeline execution completed!")
