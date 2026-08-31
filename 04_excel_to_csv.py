import os
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["MKL_NUM_THREADS"] = "8"
os.environ["OPENBLAS_NUM_THREADS"] = "8"
os.environ["VECLIB_MAXIMUM_THREADS"] = "8"
os.environ["NUMEXPR_NUM_THREADS"] = "8"

from pathlib import Path
import pandas as pd

def convert_excel_to_csv(workspace_dir):
    src = Path(workspace_dir)
    excel_dir = src / "results" / "excel_summaries"
    
    if not excel_dir.exists():
        print(f"[ERROR] Excel summaries directory not found at: {excel_dir}")
        return
        
    excel_files = list(excel_dir.glob("*.xlsx")) + list(excel_dir.glob("*.xls"))
    print(f"[INFO] Found {len(excel_files)} Excel files to convert.")
    
    for excel_path in excel_files:
        try:
            excel_file = pd.ExcelFile(excel_path)
            sheet_names = excel_file.sheet_names
            
            for sheet in sheet_names:
                df = pd.read_excel(excel_path, sheet_name=sheet)
                
                if len(sheet_names) > 1:
                    csv_name = f"{excel_path.stem}_{sheet}.csv"
                else:
                    csv_name = f"{excel_path.stem}.csv"
                    
                csv_path = excel_dir / csv_name
                df.to_csv(csv_path, index=False)
                print(f" -> Converted '{excel_path.name}' (Sheet: '{sheet}') -> {csv_path.name}")
                
        except Exception as e:
            print(f"[ERROR] Failed to convert {excel_path.name}: {e}")

if __name__ == "__main__":
    convert_excel_to_csv("./organized_workspace")
