import os
import numpy as np
from Bio import PDB

def get_ca_coords(structure_path):
    parser = PDB.PDBParser(QUIET=True)
    struct = parser.get_structure('protein', structure_path)
    coords = []
    for model in struct:
        for chain in model:
            for residue in chain:
                if 'CA' in residue:
                    coords.append(residue['CA'].get_coord())
    return np.array(coords)

q9_path = os.path.expanduser("~/rb1_project/af_structures/Q9LKZ3_pocket.pdb")
p0_path = os.path.expanduser("~/rb1_project/af_structures/P06400_pocket.pdb")

q9_ca = get_ca_coords(q9_path)
p0_ca = get_ca_coords(p0_path)

L_target = len(p0_ca)
L_common = min(len(q9_ca), len(p0_ca))

# Standard TM-score normalization factor: d0 = 1.24 * (L - 15)^(1/3) - 1.8
d0 = 1.24 * ((L_target - 15) ** (1/3)) - 1.8

# Compute C-alpha distance per aligned pair (aligned 1:1 across pocket)
diffs = q9_ca[:L_common] - p0_ca[:L_common]
distances = np.sqrt(np.sum(diffs**2, axis=1))

tm_score = (1.0 / L_target) * np.sum(1.0 / (1.0 + (distances / d0)**2))

print("=== POCKET DOMAIN STRUCTURAL AUDIT ===")
print(f"Arabidopsis RBR1 Pocket CA Count: {len(q9_ca)}")
print(f"Human RB1 Pocket CA Count       : {len(p0_ca)}")
print(f"Aligned Target Length (L_target) : {L_target}")
print(f"Pocket-Restricted TM-score      : {tm_score:.4f}")

if tm_score >= 0.5:
    print("Verdict: Homology CONFIRMED (TM-score >= 0.5)")
else:
    print("Verdict: Homology NOT CONFIRMED / Inconclusive (TM-score < 0.5)")
