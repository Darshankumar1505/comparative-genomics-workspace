import requests
import os
from Bio.PDB import PDBParser

print("--- STEP 1: Fetching UniProt Domain Annotations ---")
for acc in ["P56711", "D8U5W5"]:
    try:
        r = requests.get(f"https://rest.uniprot.org/uniprotkb/{acc}.json")
        if r.status_code == 200:
            data = r.json()
            features = [f for f in data.get("features", []) if f["type"] in ("Domain", "Region", "Repeat")]
            print(f"\nProtein: {acc}")
            for f in features:
                loc = f.get('location', {})
                print(f"  Type: {f.get('type')} | Desc: {f.get('description')} | Range: {loc}")
        else:
            print(f"Failed to fetch {acc}: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error fetching {acc}: {e}")

print("\n--- STEP 2: Checking AlphaFold Model Confidence (pLDDT) ---")
for acc in ["P56711", "D8U5W5"]:
    pdb_path = os.path.expanduser(f"~/rb1_project/expansion/structures/{acc}.pdb")
    if os.path.exists(pdb_path):
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure(acc, pdb_path)
        plddts = []
        for model in structure:
            for chain in model:
                for residue in chain:
                    for atom in residue:
                        if atom.get_name() == "CA":
                            plddts.append((residue.id[1], atom.get_bfactor()))
        
        if plddts:
            avg_plddt = sum(p[1] for p in plddts) / len(plddts)
            low_res = [p[0] for p in plddts if p[1] < 50]
            print(f"Protein {acc}: Average pLDDT = {avg_plddt:.2f} | Low confidence (<50) residues: {len(low_res)}/{len(plddts)}")
    else:
        print(f"PDB file not found at {pdb_path}")
