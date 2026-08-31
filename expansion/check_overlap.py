import pandas as pd
import requests

cols = [
    "query", "target", "fident", "alnlen", "mismatch", "gapopen", 
    "qstart", "qend", "tstart", "tend", "evalue", "bits", 
    "rmsd", "lddt", "alntmscore"
]
df = pd.read_csv("output/result_full_arabidopsis.tab", sep="\t", names=cols)

match = df[df["target"] == "P56711"].iloc[0]
t_start = int(match["tstart"])
t_end = int(match["tend"])
print(f"Arabidopsis (P56711) Alignment Range: residues {t_start} to {t_end}")

ipr_url = "https://www.ebi.ac.uk/interpro/api/entry/all/protein/uniprot/P56711/?page_size=50"
r = requests.get(ipr_url)
pocket_domains = ["PF01858", "PF08934"]
overlapping = False

if r.status_code == 200:
    for entry in r.json().get("results", []):
        acc_id = entry["metadata"]["accession"]
        if acc_id in pocket_domains:
            for prot_entry in entry.get("proteins", []):
                for loc in prot_entry.get("entry_protein_locations", []):
                    for frag in loc.get("fragments", []):
                        dom_start, dom_end = frag['start'], frag['end']
                        print(f"InterPro Domain {acc_id}: residues {dom_start}-{dom_end}")
                        if max(t_start, dom_start) <= min(t_end, dom_end):
                            overlapping = True

if overlapping:
    print("Result: The alignment falls INSIDE the pocket domain coordinates (suggestive structural conservation).")
else:
    print("Result: The alignment falls OUTSIDE the pocket domain coordinates (likely coincidental match).")
