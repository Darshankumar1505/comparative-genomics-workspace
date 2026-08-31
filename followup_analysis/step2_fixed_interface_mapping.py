import os
from Bio import PDB

# 1. Inspect all chains in 1N4M
pdb_path = os.path.expanduser("~/rb1_project/af_structures/1N4M.pdb")
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("1N4M", pdb_path)
model = structure[0]

print("=== 1N4M CHAIN INSPECTION ===")
for chain in model:
    print(f"Chain ID: {chain.id}, Residue Count: {len(list(chain.get_residues()))}")

# Let's collect all non-RB1 chains as interacting partners (or check all chain pairs)
rb1_chain = model['A']
other_chains = [chain.id for chain in model if chain.id != 'A']
print(f"Assumed RB1 Chain: A | Interacting Chains to test: {other_chains}\n")

rb1_atoms = [atom for atom in rb1_chain.get_atoms() if atom.get_name() == 'CA']
partner_atoms = [atom for cid in other_chains for atom in model[cid].get_atoms() if atom.get_name() == 'CA']

contacts = set()
for r_atom in rb1_atoms:
    for p_atom in partner_atoms:
        if r_atom - p_atom <= 5.0:
            contacts.add(r_atom.get_parent().get_id()[1])
            break

contacts = sorted(list(contacts))
print(f"Extracted {len(contacts)} contact residues on RB1 Chain A: {contacts}\n")

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
    if not os.path.exists(tab_path):
        print(f"File not found: {tab_path}")
        return
    
    with open(tab_path, "r") as f:
        line = f.readline().strip()
        if not line: return
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
            t_chem = get_chem_class(t_aa) if t_aa != '-' else "Gap"
            is_match = "YES" if q_chem == t_chem else "NO"
            if is_match == "YES": match_count += 1
            print(f"    {q_res:<8} {q_aa:<8} {str(t_res):<12} {t_aa:<10} {q_chem:<14} {t_chem:<14} {is_match}")
            
    print(f"\n    Chemical class conservation matches: {match_count}\n")

analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_arabidopsis.tab"), "Arabidopsis (P56711)")
analyze_alignment(os.path.expanduser("~/rb1_project/output/result_full_volvox.tab"), "Volvox (D8U5W5)")
