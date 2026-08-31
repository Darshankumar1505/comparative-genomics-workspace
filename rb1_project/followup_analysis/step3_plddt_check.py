import os
from Bio import PDB

def evaluate_plddt(pdb_path, tab_path, species_label):
    if not os.path.exists(pdb_path) or not os.path.exists(tab_path):
        print(f"Skipping {species_label}: missing file.")
        return
        
    with open(tab_path, "r") as f:
        cols = f.readline().strip().split("\t")
        tstart = int(cols[8])
        tend = int(cols[9])
        
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure(species_label, pdb_path)
    
    whole_plddts = []
    aligned_plddts = []
    
    for model in structure:
        for chain in model:
            for residue in chain:
                if PDB.is_aa(residue, standard=True):
                    ca = residue['CA']
                    b = ca.get_bfactor()
                    whole_plddts.append(b)
                    resno = residue.get_id()[1]
                    if tstart <= resno <= tend:
                        aligned_plddts.append(b)
                        
    print(f"=== {species_label} ===")
    print(f"    Aligned Region Span: Residues {tstart} to {tend} ({tend - tstart + 1} aa)")
    print(f"    Whole Protein Mean pLDDT : {sum(whole_plddts)/len(whole_plddts):.2f}")
    print(f"    Aligned Region Mean pLDDT: {sum(aligned_plddts)/len(aligned_plddts):.2f}")
    print(f"    Aligned Region Min pLDDT : {min(aligned_plddts):.2f}")
    print(f"    Aligned Region Max pLDDT : {max(aligned_plddts):.2f}")
    low_conf = sum(1 for p in aligned_plddts if p < 70) / len(aligned_plddts) * 100
    print(f"    Proportion < 70 pLDDT    : {low_conf:.2f}%\n")

evaluate_plddt(
    os.path.expanduser("~/rb1_project/af_structures/P56711.pdb"),
    os.path.expanduser("~/rb1_project/output/result_full_arabidopsis.tab"),
    "Arabidopsis (P56711)"
)

evaluate_plddt(
    os.path.expanduser("~/rb1_project/af_structures/D8U5W5.pdb"),
    os.path.expanduser("~/rb1_project/output/result_full_volvox.tab"),
    "Volvox (D8U5W5)"
)
