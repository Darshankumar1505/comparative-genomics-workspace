import os
import subprocess

# Define paths
af_arabidopsis = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3.pdb")
human_rb1 = os.path.expanduser("~/rb1_project/af_structures/P06400.pdb") # Assuming human RB1 is present, or use PDB 1N4M
output_tab = os.path.expanduser("~/rb1_project/output/result_full_arabidopsis_audited.tab")

print("Running Foldseek structural alignment for audited Arabidopsis RBR1 (Q9LKZ3)...")
# Ensure foldseek command matches your local environment setup
# foldseek easy-search [target] [query] [output_file] [tmp_dir] --format-output ...
cmd = [
    "foldseek", "easy-search",
    af_arabidopsis,
    human_rb1,
    output_tab,
    os.path.expanduser("~/rb1_project/output/tmp"),
    "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,tcov,qcov,lddt,rmsd,qaln,taln"
]

# If foldseek is installed, run it. Otherwise, print instructions.
try:
    subprocess.run(cmd, check=True)
    print(f"Foldseek search completed successfully. Results saved to {output_tab}")
except Exception as e:
    print(f"Foldseek execution note: {e}")
    print("If foldseek is invoked via a specific module or conda environment, run the equivalent easy-search command manually.")
