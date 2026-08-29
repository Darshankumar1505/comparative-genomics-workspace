import os
from Bio import PDB

def get_chem_class(aa):
    aa = aa.upper()
    hydrophobic = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO", "A", "V", "L", "I", "M", "F", "W", "P"}
    charged = {"ARG", "HIS", "LYS", "ASP", "GLU", "R", "H", "K", "D", "E"}
    polar = {"SER", "THR", "ASN", "GLN", "CYS", "TYR", "S", "T", "N", "Q", "C", "Y"}
    if aa in hydrophobic: return "Hydrophobic"
    if aa in charged: return "Charged"
    if aa in polar: return "Polar"
    if aa in {"GLY", "G"}: return "Glycine"
    return "Unknown"

# 1. Extract 1N4M Interface Residues (Chain A vs Chains C, D, E)
pdb_path = os.path.expanduser("~/rb1_project/af_structures/1N4M.pdb")
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("1N4M", pdb_path)
model = structure[0]

rb1_atoms = [atom for atom in model['A'].get_atoms() if atom.get_name() == 'CA']
e2f_atoms = [atom for chain_id in ['C', 'D', 'E'] for atom in model[chain_id].get_atoms() if atom.get_name() == 'CA']

contacts = set()
for r_atom in rb1_atoms:
    for e_atom in e2f_atoms:
        if r_atom - e_atom <= 5.0:
            contacts.add(r_atom.get_parent().get_id()[1])
            break

contacts = sorted(list(contacts))
print(f"=== 1N4M INTERFACE EXTRACTION ===")
print(f"Extracted {len(contacts)} contact residues on RB1 Chain A: {contacts}\n")

# 2. Gap-Aware Alignment Mapping Function
def analyze_alignment(tab_path, species_name):
    if not os.path.exists(tab_path):
        print(f"File not found: {tab_path}")
        return
    
    with open(tab_path, "r") as f:
        line = f.readline().strip()
        if not line:
            return
        cols = line.split("\t")
        
    qstart = int(cols[6])
    tstart = int(cols[8])
    tmscore = float(cols[14])
    rmsd = float(cols[12])
    qaln = cols[15]
    taln = cols[16]
    
    print(f"--> Target: {species_name}")
    print(f"    Query Window: {qstart} | Target Window: {tstart} | TM-Score: {tmscore:.3f} | RMSD: {rmsd:.2f} Å")
    
    q_pos = qstart
    t_pos = tstart
    
    mapping = []
    for q_char, t_char in zip(qaln, taln):
        curr_q = q_pos if q_char != '-' else None
        curr_t = t_pos if t_char != '-' else None
        mapping.append((curr_q, curr_t, q_char, t_char))
        
        if q_char != '-': q_pos += 1
        if t_char != '-': t_pos += 1
        
    print(f"    {'RB1_Res':<8} {'RB1_AA':<8} {'Target_Res':<12} {'Target_AA':<10} {'RB1_Chem':<14} {'Target_Chem':<14} {'Match?'}")
    print("-" * 80)
    
    match_count = 0
    for q_res, t_res, q_aa, t_aa in mapping:
        if q_res is not None and q_res in contacts:
            q_chem = get_chem_class(q_aa)
            t_chem = get_chem_class(t_aa) if t_char != '-' else "Gap"
            is_match = "YES" if q_chem == t_chem else "NO"
            if is_match == "YES": match_count += 1
            print(f"    {q_res:<8} {q_aa:<8} {str(t_res):<12} {t_aa:<10} {q_chem:<14} {t_chem:<14} {is_match}")
            
    print(f"\n    Summary: Found matching interface residues mapped. Chemical class conservation matches: {match_count}\n")

analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_arabidopsis.tab"), "Arabidopsis (P56711)")
analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_volvox.tab"), "Volvox (D8U5W5)")
