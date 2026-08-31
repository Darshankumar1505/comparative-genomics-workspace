import os
from Bio import PDB

pdb_path = os.path.expanduser("~/rb1_project/af_structures/1N4M.pdb")
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("1N4M", pdb_path)

print("=== 1N4M CHAIN & RESIDUE SUMMARY ===")
for model in structure:
    for chain in model:
        res_list = list(chain.get_residues())
        first_res = res_list[0].get_id()[1]
        last_res = res_list[-1].get_id()[1]
        print(f"Chain {chain.id}: {len(res_list)} residues (Residue ID range in file: {first_res} to {last_res})")

print("\n=== DBREF RECORDS (PDB Numbering vs UniProt Mapping) ===")
with open(pdb_path, "r") as f:
    for line in f:
        if line.startswith("DBREF"):
            print(line.strip())
