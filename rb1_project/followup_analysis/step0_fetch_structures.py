import os
import urllib.request
import json

af_dir = os.path.expanduser("~/rb1_project/af_structures/")
os.makedirs(af_dir, exist_ok=True)

uniprot_ids = ["P06400", "P56711", "D8U5W5", "P28749"]

for uid in uniprot_ids:
    dest = os.path.join(af_dir, f"{uid}.pdb")
    if os.path.exists(dest):
        print(f"Exists: {dest}")
        continue
    
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uid}"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data and isinstance(data, list):
                pdb_url = data[0].get("pdbUrl")
                if pdb_url:
                    print(f"Downloading {uid} from {pdb_url} -> {dest}")
                    urllib.request.urlretrieve(pdb_url, dest)
                else:
                    print(f"No pdbUrl found in API response for {uid}")
            else:
                print(f"Invalid API response for {uid}")
    except Exception as e:
        print(f"Error fetching API for {uid}: {e}")

# Download 1N4M directly from RCSB
pdb_1n4m_dest = os.path.join(af_dir, "1N4M.pdb")
if not os.path.exists(pdb_1n4m_dest):
    print("Downloading 1N4M ->", pdb_1n4m_dest)
    urllib.request.urlretrieve("https://files.rcsb.org/download/1N4M.pdb", pdb_1n4m_dest)
else:
    print("Exists:", pdb_1n4m_dest)
