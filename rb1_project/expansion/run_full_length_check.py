import os
import subprocess
import glob

print("--- Searching for PDB files across Windows mounts ---")
search_patterns = [
    "/mnt/c/blast_work/*.pdb",
    "/mnt/c/Users/*/blast_work/*.pdb",
    "/mnt/c/Users/*/Downloads/*.pdb",
    os.path.expanduser("~/rb1_project/**/*.pdb")
]

struct_dir = ""
for pattern in search_patterns:
    matches = glob.glob(pattern, recursive=True)
    if matches:
        struct_dir = os.path.dirname(matches[0])
        break

if not struct_dir and os.path.exists("/mnt/c"):
    # Walk through /mnt/c/Users to find any folder containing P06400.pdb
    for root, dirs, files in os.walk("/mnt/c/Users"):
        if "P06400.pdb" in files:
            struct_dir = root
            break

print(f"Found structures directory: {struct_dir}")

os.makedirs("expansion/output", exist_ok=True)
os.makedirs("expansion/tmp", exist_ok=True)

human_pdb = os.path.join(struct_dir, "P06400.pdb")
volvox_pdb = os.path.join(struct_dir, "D8U5W5.pdb")
arabidopsis_pdb = os.path.join(struct_dir, "P56711.pdb")

if all(os.path.exists(p) for p in [human_pdb, volvox_pdb, arabidopsis_pdb]):
    print("\nRunning Foldseek for Volvox (D8U5W5)...")
    subprocess.run([
        "foldseek", "easy-search",
        human_pdb, volvox_pdb,
        "expansion/output/result_full_volvox.tab",
        "expansion/tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)

    print("\nRunning Foldseek for Arabidopsis (P56711)...")
    subprocess.run([
        "foldseek", "easy-search",
        human_pdb, arabidopsis_pdb,
        "expansion/output/result_full_arabidopsis.tab",
        "expansion/tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)
    print("\n[SUCCESS] Full-length Foldseek searches completed successfully!")
else:
    print(f"\n[ERROR] Could not locate all PDB files automatically. Please copy P06400.pdb, D8U5W5.pdb, and P56711.pdb into your current directory or specify the exact path.")
