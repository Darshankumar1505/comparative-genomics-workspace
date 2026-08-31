import os
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["OPENBLAS_NUM_THREADS"] = "8"
os.environ["VECLIB_MAXIMUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"

from pathlib import Path
import subprocess

def prep_git_zenodo(workspace_dir, size_limit_mb=100.0):
    root_path = Path(workspace_dir)
    if not root_path.exists():
        print(f"[ERROR] Workspace directory not found at: {root_path}")
        return

    print("[INFO] Scanning files for GitHub 100MB limit exclusions...")
    excluded_files = []
    
    for path in root_path.rglob("*"):
        if path.is_file():
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > size_limit_mb:
                rel_path = path.relative_to(root_path)
                excluded_files.append((str(rel_path), size_mb))

    gitignore_path = root_path / ".gitignore"
    gitignore_lines = [
        "# Large files > 100MB excluded for GitHub, route to Zenodo",
        "*.RData",
        "*.rdata",
        "*.zip"
    ]
    for rel_path, _ in excluded_files:
        gitignore_lines.append(f"/{rel_path}")
        
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write("\n".join(gitignore_lines) + "\n")
    print(f"[INFO] Created .gitignore at {gitignore_path}")

    cff_path = root_path / "CITATION.cff"
    cff_content = """cff-version: 1.2.0
message: "If you use this software or dataset, please cite it as below."
authors:
  - family-names: "Darshan"
title: "Comparative Genomics & Phylostratigraphy Workspace"
version: "1.0.0"
date-released: 2026-03-31
"""
    with open(cff_path, "w", encoding="utf-8") as f:
        f.write(cff_content)
    print(f"[INFO] Created CITATION.cff at {cff_path}")

    try:
        subprocess.run(["git", "init"], cwd=root_path, check=True)
        subprocess.run(["git", "add", "README.md", "CITATION.cff", ".gitignore", "scripts/"], cwd=root_path, capture_output=True)
        print("[INFO] Initialized local git repository and staged lightweight files.")
    except Exception as e:
        print(f"[WARNING] Git initialization skipped or failed: {e}")

    print("\n" + "="*50)
    print(" ZENODO ARCHIVAL MANIFEST (>100MB FILES)")
    print("="*50)
    if excluded_files:
        for fpath, fsize in excluded_files:
            print(f" -> [EXCLUDED FROM GITHUB] {fpath} ({fsize:.2f} MB) -> Upload to Zenodo")
    else:
        print(" -> No files exceeded the 100MB limit.")
    print("="*50)

if __name__ == "__main__":
    prep_git_zenodo("./organized_workspace")
