# Provenance Note: Run 2 (Foldseek Fallback / Mislabeled TM-align)

- **Status**: SUPERSEDED / METHODOLOGICAL DISCREPANCY
- **Accession Used**: `Q9LKZ3` (*Arabidopsis thaliana* RBR1) vs `P06400` (Human RB1)
- **Reported Metrics**: Aligned Length = 284, RMSD = 6.12 Å, TM-score = 0.384–0.434
- **Root Cause**: Executed prior to installing the official `TMalign` binary via Conda/Bioconda (`FileNotFoundError` on `TMalign`). The process silently fell back to unaligned local heuristics.
- **Resolution**: Installed official `TMalign` binary (v20240303) and re-ran with pre-registered Pfam domain boundaries.
