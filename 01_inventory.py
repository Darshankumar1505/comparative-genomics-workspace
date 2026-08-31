import os
from pathlib import Path
import pandas as pd

def inventory_directory(source_dir, output_csv="manifest.csv"):
    src = Path(source_dir)
    records = []
    
    print(f"Scanning directory: {src.resolve()}")
    for path in src.rglob("*"):
        if path.is_file():
            stat = path.stat()
            size_mb = stat.st_size / (1024 * 1024)
            records.append({
                "file_name": path.name,
                "relative_path": str(path.relative_to(src)),
                "size_mb": round(size_mb, 2),
                "type": path.suffix or "no_extension",
                "last_modified": pd.to_datetime(stat.st_mtime, unit='s'),
                "exceeds_github_limit": size_mb > 100
            })
            
    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"Inventory saved to {output_csv}. Total files found: {len(df)}")
    
    heavy_files = df[df["exceeds_github_limit"]]
    if not heavy_files.empty:
        print("\n[WARNING] The following files exceed GitHub's 100MB limit and must go to Zenodo:")
        print(heavy_files[["relative_path", "size_mb"]])
    else:
        print("\n[INFO] All files are under 100MB.")

if __name__ == "__main__":
   inventory_directory(".")

    
