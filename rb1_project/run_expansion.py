import os
import subprocess
import urllib.request
import json
import pandas as pd

PROJECT_DIR = os.path.expanduser("~/rb1_project")
EXPANSION_DIR = os.path.join(PROJECT_DIR, "expansion")
STRUCT_DIR = os.path.join(EXPANSION_DIR, "structures")
OUT_DIR = os.path.join(EXPANSION_DIR, "output")
TEMP_DIR = os.path.join(EXPANSION_DIR, "tmp")

os.makedirs(STRUCT_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Target Uniprot IDs for Arabidopsis RBR1 and Volvox MAT3/RBR
TARGETS = {
    "P56711": {"organism": "Arabidopsis_thaliana", "taxon_id": 3702},
    "D8U5W5": {"organism": "Volvox_carteri", "taxon_id": 3067}
}

print("--- STEP 1: Fetching AlphaFold Models via EBI API ---")
for acc, info in TARGETS.items():
    dest_path = os.path.join(STRUCT_DIR, f"{acc}.pdb")
    
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        print(f"[INFO] Model for {info['organism']} ({acc}) already exists locally.")
        continue
        
    print(f"[DOWNLOAD] Querying API for {info['organism']} ({acc})...")
    try:
        api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{acc}"
        req = urllib.request.urlopen(api_url)
        data = json.loads(req.read().decode())
        
        # Extract the correct PDB file URL from API response
        pdb_url = data[0]["pdbUrl"]
        print(f"[DOWNLOAD] Downloading PDB from {pdb_url}...")
        urllib.request.urlretrieve(pdb_url, dest_path)
        
        file_size = os.path.getsize(dest_path)
        if file_size < 5000:
            raise ValueError(f"Downloaded file {acc}.pdb is too small ({file_size} bytes).")
        print(f"[SUCCESS] Verified {acc}.pdb ({file_size // 1024} KB)")
    except Exception as e:
        print(f"[ERROR] Failed to fetch {acc}: {e}")

HUMAN_STRUCT_DIR = os.path.join(PROJECT_DIR, "structures")
foldseek_db_out = os.path.join(OUT_DIR, "human_vs_plants_algae.tab")

print(f"\n--- STEP 2: Running Foldseek Structural Alignment ---")
cmd = [
    "foldseek", "easy-search",
    HUMAN_STRUCT_DIR,
    STRUCT_DIR,
    foldseek_db_out,
    TEMP_DIR,
    "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore",
    "-e", "10",
    "--threads", "4"
]

print(f"Executing: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode != 0:
    print(f"[ERROR] Foldseek execution failed:\n{result.stderr}")
else:
    print("[SUCCESS] Foldseek alignment completed successfully.")

print(f"\n--- STEP 3: Formatting Output to Match Schema ---")
if os.path.exists(foldseek_db_out) and os.path.getsize(foldseek_db_out) > 0:
    cols = [
        "query", "target", "fident", "alnlen", "mismatch", "gapopen", 
        "qstart", "qend", "tstart", "tend", "evalue", "bits", "rmsd", "lddt", "alntmscore"
    ]
    raw_df = pd.read_csv(foldseek_db_out, sep="\t", names=cols)
    
    formatted_rows = []
    for _, row in raw_df.iterrows():
        q_name = os.path.splitext(os.path.basename(str(row["query"])))[0]
        t_name = os.path.splitext(os.path.basename(str(row["target"])))[0]
        taxon_id = TARGETS.get(t_name, {}).get("taxon_id", "NA")
        
        formatted_rows.append({
            "query": q_name,
            "domain": "full_protein" if "RB" in q_name else "pocket_domain",
            "species": taxon_id,
            "target_id": t_name,
            "gene": "RBR1" if taxon_id == 3702 else ("MAT3" if taxon_id == 3067 else "NA"),
            "bit_score": row["bits"],
            "evalue": f"{row['evalue']:.3E}",
            "note": "foldseek_hit"
        })
    
    formatted_df = pd.DataFrame(formatted_rows)
    existing_csv_path = os.path.join(PROJECT_DIR, "summary", "rb_pathway_foldseek_summary.csv")
    output_csv_path = os.path.join(EXPANSION_DIR, "rb_pathway_foldseek_summary_with_plants.csv")
    
    if os.path.exists(existing_csv_path):
        orig_df = pd.read_csv(existing_csv_path)
        combined_df = pd.concat([orig_df, formatted_df], ignore_index=True)
    else:
        combined_df = formatted_df
        
    combined_df.to_csv(output_csv_path, index=False)
    print(f"[SUCCESS] Expanded summary successfully written to: {output_csv_path}")
    print(formatted_df.to_string(index=False))
else:
    print("[WARNING] Foldseek output file is empty or missing.")
