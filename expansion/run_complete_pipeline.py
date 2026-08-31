import requests
import os
import subprocess

print("--- STEP 1: Fetching UniProt Length and Domain Features ---")
accessions = ["P56711", "D8U5W5"]
for acc in accessions:
    try:
        r = requests.get(f"https://rest.uniprot.org/uniprotkb/{acc}.json")
        if r.status_code == 200:
            data = r.json()
            length = data.get("sequence", {}).get("length", "Unknown")
            print(f"\nProtein {acc} | Total Length: {length}")
            features = data.get("features", [])
            relevant = [f for f in features if f["type"] in ("Domain", "Region", "Motif", "Site")]
            if not relevant:
                print("  No Domain/Region/Motif/Site features annotated in UniProt.")
            for f in relevant:
                loc = f.get("location", {})
                start = loc.get("start", {}).get("value", "?")
                end = loc.get("end", {}).get("value", "?")
                print(f"  [UniProt Feature] Type: {f['type']} | Desc: {f.get('description')} | Range: {start}-{end}")
        else:
            print(f"Failed to fetch UniProt for {acc}: HTTP {r.status_code}")
    except Exception as e:
        print(f"Error fetching UniProt for {acc}: {e}")

    # InterPro API check
    try:
        ipr_url = f"https://www.ebi.ac.uk/interpro/api/entry/all/protein/uniprot/{acc}/?page_size=50"
        r_ipr = requests.get(ipr_url)
        if r_ipr.status_code == 200:
            ipr_data = r_ipr.json()
            print(f"--- InterPro Domains for {acc} ---")
            for entry in ipr_data.get("results", []):
                acc_id = entry["metadata"]["accession"]
                name = entry["metadata"]["name"]
                for prot_entry in entry.get("proteins", []):
                    for loc in prot_entry.get("entry_protein_locations", []):
                        for frag in loc.get("fragments", []):
                            print(f"  {acc_id} ({name}): residues {frag['start']}-{frag['end']}")
    except Exception as e:
        print(f"Error fetching InterPro for {acc}: {e}")

print("\n--- STEP 2: Running Full-Length Foldseek Comparisons ---")
os.makedirs("output", exist_ok=True)
os.makedirs("tmp", exist_ok=True)

struct_dir = "."
for d in [".", "../structures", "../"]:
    if os.path.exists(os.path.join(d, "P06400.pdb")):
        struct_dir = d
        break

human_pdb = os.path.join(struct_dir, "P06400.pdb")
volvox_pdb = os.path.join(struct_dir, "D8U5W5.pdb")
arabidopsis_pdb = os.path.join(struct_dir, "P56711.pdb")

if all(os.path.exists(p) for p in [human_pdb, volvox_pdb, arabidopsis_pdb]):
    print("Running Foldseek for Volvox (D8U5W5)...")
    subprocess.run([
        "foldseek", "easy-search",
        human_pdb, volvox_pdb,
        "output/result_full_volvox.tab",
        "tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)

    print("Running Foldseek for Arabidopsis (P56711)...")
    subprocess.run([
        "foldseek", "easy-search",
        human_pdb, arabidopsis_pdb,
        "output/result_full_arabidopsis.tab",
        "tmp",
        "--alignment-type", "1", "-e", "10",
        "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,rmsd,lddt,alntmscore"
    ], check=True)
    print("\n[SUCCESS] Full-length Foldseek searches completed successfully!")
else:
    print(f"[ERROR] Could not find all required PDB files in {struct_dir}.")
