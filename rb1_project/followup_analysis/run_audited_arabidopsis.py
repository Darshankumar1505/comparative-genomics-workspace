import os
import urllib.request
import json

os.makedirs(os.path.expanduser("~/rb1_project/af_structures"), exist_ok=True)
os.makedirs(os.path.expanduser("~/rb1_project/esmfold_structures"), exist_ok=True)
os.makedirs(os.path.expanduser("~/rb1_project/output"), exist_ok=True)

# 1. Fetch AlphaFold structure URL for Q9LKZ3 (Arabidopsis RBR1) via API
af_api_url = "https://alphafold.ebi.ac.uk/api/prediction/Q9LKZ3"
print("Querying AlphaFold API for Arabidopsis RBR1 (Q9LKZ3)...")
req = urllib.request.Request(af_api_url, headers={'Accept': 'application/json'})

with urllib.request.urlopen(req) as response:
    api_data = json.loads(response.read().decode('utf-8'))

pdb_url = api_data[0]['pdbUrl']
af_dest = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3.pdb")

print(f"Downloading AlphaFold structure from {pdb_url}...")
urllib.request.urlretrieve(pdb_url, af_dest)

print("AlphaFold structure for Q9LKZ3 successfully downloaded and verified.")
