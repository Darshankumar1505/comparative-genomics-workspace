import os
import requests

def get_fasta_seq(acc):
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
    res = requests.get(url)
    lines = res.text.splitlines()
    return "".join(l.strip() for l in lines if not l.startswith(">"))

targets = {"P56711": "Arabidopsis_ESM.pdb", "D8U5W5": "Volvox_ESM.pdb"}
esm_dir = os.path.expanduser("~/rb1_project/esmfold_structures/")
os.makedirs(esm_dir, exist_ok=True)

for acc, out_name in targets.items():
    out_path = os.path.join(esm_dir, out_name)
    if not os.path.exists(out_path):
        print(f"Fetching sequence & predicting ESMFold for {acc}...")
        seq = get_fasta_seq(acc)
        res = requests.post("https://api.esmatlas.com/foldSequence/v1/pdb/", data=seq)
        if res.status_code == 200:
            with open(out_path, "w") as f:
                f.write(res.text)
            print(f"Saved: {out_path}")
        else:
            print(f"Failed ESMFold for {acc} (Status: {res.status_code})")
    else:
        print(f"Exists: {out_path}")
