import os

base_dir = os.path.expanduser("~/rb1_project")

arch_run1 = os.path.join(base_dir, "archive/superseded_runs/run1_invalid_accession_p56711")
arch_run2 = os.path.join(base_dir, "archive/superseded_runs/run2_foldseek_fallback_mislabeled")
final_dir = os.path.join(base_dir, "results/final_pocket_domain_alignment")

os.makedirs(arch_run1, exist_ok=True)
os.makedirs(arch_run2, exist_ok=True)
os.makedirs(final_dir, exist_ok=True)

note_run1 = """# Provenance Note: Run 1 (P56711 Invalid Accession)

- **Status**: SUPERSEDED / INVALID ACCESSION
- **Accession Used**: `P56711` (Mislabeled as *Arabidopsis thaliana* RBR1, actually *Conus pennaceus* gamma-conotoxin PnVIIA peptide)
- **Tool**: Foldseek
- **Result**: lDDT = 0.6722, Pocket RMSD = 14.88 Å
- **Resolution**: Accession corrected to authentic *Arabidopsis thaliana* RBR1 (`Q9LKZ3`).
"""

note_run2 = """# Provenance Note: Run 2 (Foldseek Fallback / Mislabeled TM-align)

- **Status**: SUPERSEDED / METHODOLOGICAL DISCREPANCY
- **Accession Used**: `Q9LKZ3` (*Arabidopsis thaliana* RBR1) vs `P06400` (Human RB1)
- **Reported Metrics**: Aligned Length = 284, RMSD = 6.12 Å, TM-score = 0.384–0.434
- **Root Cause**: Executed prior to installing the official `TMalign` binary via Conda/Bioconda (`FileNotFoundError` on `TMalign`). The process silently fell back to unaligned local heuristics.
- **Resolution**: Installed official `TMalign` binary (v20240303) and re-ran with pre-registered Pfam domain boundaries.
"""

with open(os.path.join(arch_run1, "NOTE.md"), "w") as f:
    f.write(note_run1)

with open(os.path.join(arch_run2, "NOTE.md"), "w") as f:
    f.write(note_run2)

print("Archive directories and provenance notes created successfully.")
