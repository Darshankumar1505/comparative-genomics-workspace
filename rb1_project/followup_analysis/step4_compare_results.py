import os

def parse_tab(path):
    if not os.path.exists(path): return None
    with open(path, "r") as f:
        line = f.readline().strip()
        if not line: return None
        cols = line.split("\t")
        return {
            "tmscore": float(cols[14]),
            "rmsd": float(cols[12]),
            "alnlen": int(cols[3]),
            "evalue": float(cols[10])
        }
    return None

af_ara = parse_tab(os.path.expanduser("~/rb1_project/output/result_full_arabidopsis.tab"))
esm_ara = parse_tab(os.path.expanduser("~/rb1_project/output/result_esm_arabidopsis.tab"))
af_vol = parse_tab(os.path.expanduser("~/rb1_project/output/result_full_volvox.tab"))
esm_vol = parse_tab(os.path.expanduser("~/rb1_project/output/result_esm_volvox.tab"))

print("=== COMPARATIVE STRUCTURAL HOMOLOGY (AlphaFold2 vs ESMFold) ===")
print(f"{'Species':<14} {'Predictor':<12} {'TM-Score':<10} {'RMSD (Å)':<10} {'Aln Len':<10} {'E-Value'}")
print("-" * 65)
if af_ara: print(f"{'Arabidopsis':<14} {'AlphaFold2':<12} {af_ara['tmscore']:<10.3f} {af_ara['rmsd']:<10.2f} {af_ara['alnlen']:<10} {af_ara['evalue']}")
if esm_ara: print(f"{'Arabidopsis':<14} {'ESMFold':<12} {esm_ara['tmscore']:<10.3f} {esm_ara['rmsd']:<10.2f} {esm_ara['alnlen']:<10} {esm_ara['evalue']}")
if af_vol: print(f"{'Volvox':<14} {'AlphaFold2':<12} {af_vol['tmscore']:<10.3f} {af_vol['rmsd']:<10.2f} {af_vol['alnlen']:<10} {af_vol['evalue']}")
if esm_vol: print(f"{'Volvox':<14} {'ESMFold':<12} {esm_vol['tmscore']:<10.3f} {esm_vol['rmsd']:<10.2f} {esm_vol['alnlen']:<10} {esm_vol['evalue']}")
