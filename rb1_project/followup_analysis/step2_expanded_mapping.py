import os
from Bio import PDB

pdb_path = os.path.expanduser("~/rb1_project/af_structures/1N4M.pdb")
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("1N4M", pdb_path)
model = structure[0]

rb1_chain = model['A']
other_chains = [chain.id for chain in model if chain.id != 'A']

rb1_atoms = [atom for atom in rb1_chain.get_atoms() if atom.get_name() == 'CA']
partner_atoms = [atom for cid in other_chains for atom in model[cid].get_atoms() if atom.get_name() == 'CA']

# Expand cutoff to 6.0 Å to capture more proximal pocket residues
contacts = set()
for r_atom in rb1_atoms:
    for p_atom in partner_atoms:
        if r_atom - p_atom <= 6.0:
            contacts.add(r_atom.get_parent().get_id()[1])
            break

contacts = sorted(list(contacts))
print(f"Expanded 6.0Å Interface Residues on RB1 Chain A ({len(contacts)} residues): {contacts}\n")

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

def analyze_alignment(tab_path, species_name):
    if not os.path.exists(tab_path): return
    with open(tab_path, "r") as f:
        cols = f.readline().strip().split("\t")
    
    qstart = int(cols[6])
    tstart = int(cols[8])
    qaln = cols[15]
    taln = cols[16]
    
    print(f"--> Target: {species_name}")
    print(f"    {'RB1_Res':<8} {'RB1_AA':<8} {'Target_Res':<12} {'Target_AA':<10} {'RB1_Chem':<14} {'Target_Chem':<14} {'Match?'}")
    print("-" * 80)
    
    q_pos = qstart
    t_pos = tstart
    for q_char, t_char in zip(qaln, taln):
        curr_q = q_pos if q_char != '-' else None
        curr_t = t_pos if t_char != '-' else None
        
        if curr_q is not None and curr_q in contacts:
            q_chem = get_chem_class(q_char)
            t_chem = get_chem_class(t_char) if t_char != '-' else "Gap"
            is_match = "YES" if q_chem == t_chem else "NO"
            print(f"    {curr_q:<8} {q_char:<8} {str(curr_t):<12} {t_char:<10} {q_chem:<14} {t_chem:<14} {is_match}")
        
        if q_char != '-': q_pos += 1
        if t_char != '-': t_pos += 1
    print("\n")

analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_arabidopsis.tab"), "Arabidopsis (P56711)")
analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_volvox.tab"), "Volvox (D8U5W5)")
