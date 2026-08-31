import os
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["OPENBLAS_NUM_THREADS"] = "8"
os.environ["VECLIB_MAXIMUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"

from pathlib import Path
import datetime

def classify_pipeline_step(filename):
    fname = filename.lower()
    if "blast" in fname or any(fname.endswith(f"{i}.tab") for i in ["4932", "7227", "9606", "10090", "7955"]):
        return "BLAST Analysis (NCBI Ortholog Hits)"
    elif "hmmer" in fname:
        return "HMMER Profile Search"
    elif "foldseek" in fname:
        return "Foldseek Structural Alignment"
    elif "phylostratr" in fname or "checkpoint" in fname:
        return "Phylostratr Phylogenomic Profiling"
    elif "enrichment" in fname or "go" in fname or "pathway" in fname:
        return "Functional & GO Enrichment Analysis"
    elif "expression" in fname or "tissue" in fname or "proteinatlas" in fname:
        return "Tissue Expression Reference (HPA)"
    else:
        return "General Workspace Output"

def generate_readme(workspace_dir):
    root_path = Path(workspace_dir)
    readme_path = root_path / "README.md"
    
    lines = [
        "# Organized Reproducible Workspace: Comparative Genomics & Phylostratigraphy",
        "",
        f"**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This repository contains structured, reproducible outputs and analysis artifacts generated across multiple computational pipelines (BLAST, HMMER, Foldseek, Phylostratr, and functional enrichment). Large binary checkpoints and data files have been organized for distribution across GitHub and Zenodo.",
        "",
        "---",
        "",
        "## Directory Structure & File Manifest",
        ""
    ]
    
    if not root_path.exists():
        print(f"[ERROR] Workspace directory not found at: {root_path}")
        return

    for path in sorted(root_path.rglob("*")):
        if path.name == "README.md" or path.name.startswith("."):
            continue
            
        rel_path = path.relative_to(root_path)
        
        if path.is_dir():
            lines.append(f"### 📁 `{rel_path}/`")
        else:
            file_size_mb = path.stat().st_size / (1024 * 1024)
            step_source = classify_pipeline_step(path.name)
            
            lines.append(f"* **`{path.name}`**")
            lines.append(f"  * **Path:** `{rel_path}`")
            lines.append(f"  * **Size:** `{file_size_mb:.2f} MB`")
            lines.append(f"  * **Pipeline Origin:** {step_source}")
            
    lines.extend([
        "",
        "---",
        "",
        "## Pipeline Methodology Summary",
        "1. **BLAST & Orthology Search:** Raw tabular files containing sequence alignments mapped by NCBI Taxonomy IDs.",
        "2. **HMMER & Foldseek:** Hidden Markov Model homology profiles and 3D structural comparisons.",
        "3. **Phylostratr Checkpoints:** Evolutionary phylogenomic profiling checkpoints exported to plain-text CSV for transparent version control.",
        "4. **Enrichment & Expression:** Gene Ontology (GO), KEGG pathways, and Human Protein Atlas (HPA) expression datasets."
    ])
    
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"[INFO] Successfully generated README.md at: {readme_path}")

if __name__ == "__main__":
    generate_readme("./organized_workspace")
