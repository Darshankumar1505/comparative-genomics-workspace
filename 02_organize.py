import shutil
from pathlib import Path
import pandas as pd

TAXID_MAP = {
    "9606.tab": "9606_homo_sapiens_blast_hits.tab",
    "10090.tab": "10090_mus_musculus_blast_hits.tab",
    "7955.tab": "7955_danio_rerio_blast_hits.tab",
    "7227.tab": "7227_drosophila_melanogaster_blast_hits.tab",
    "4932.tab": "4932_saccharomyces_cerevisiae_blast_hits.tab"
}

def organize_files(source_dir, target_dir):
    src = Path(source_dir)
    tgt = Path(target_dir)
    log = []
    
    dirs = {
        "raw_blast": tgt / "data" / "raw_blast",
        "checkpoints": tgt / "results" / "phylostratr_checkpoints",
        "excel": tgt / "results" / "excel_summaries",
        "misc": tgt / "data" / "misc"
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)
        
    for path in src.rglob("*"):
        if "organized_workspace" in path.parts:
            continue
        if not path.is_file():
            continue
            
        filename = path.name
        dest_path = None
        
        if filename.endswith(".tab"):
            new_name = TAXID_MAP.get(filename, filename)
            dest_path = dirs["raw_blast"] / new_name
        elif "phylostratr" in filename and path.suffix in [".RData", ".Rdata"]:
            dest_path = dirs["checkpoints"] / filename
        elif "Excel Outputs" in path.parts or path.suffix in [".xlsx", ".xls"]:
            dest_path = dirs["excel"] / filename
        else:
            dest_path = dirs["misc"] / filename
            
        if dest_path:
            shutil.copy2(path, dest_path)
            log.append({"old_path": str(path), "new_path": str(dest_path)})
            print(f"Copied: {path.name} -> {dest_path}")
            
    pd.DataFrame(log).to_csv(tgt / "reorganization_log.csv", index=False)
    print(f"\nOrganization complete. Log saved to {tgt / 'reorganization_log.csv'}")

if __name__ == "__main__":
    organize_files(".", "./organized_workspace")
