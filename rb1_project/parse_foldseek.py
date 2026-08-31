import glob
import os
import re

output_file = "summary/rb_pathway_foldseek_summary.csv"

# Search for .tab, .m8, or .tsv files in foldseek_out
files = glob.glob("foldseek_out/*.[tm]*") + glob.glob("foldseek_out/*.tsv")
files = list(set(files))

os.makedirs("summary", exist_ok=True)

with open(output_file, "w") as out:
    out.write("query,domain,species,target_id,gene,bit_score,evalue,note\n")
    if not files:
        print("Warning: No result files found in foldseek_out/")
    for f in sorted(files):
        filename = os.path.basename(f)
        with open(f) as fh:
            lines = [l.strip() for l in fh if not l.startswith("#") and l.strip()]
        if not lines:
            parts = filename.replace(".tab", "").replace(".m8", "").split("_vs_")
            q = parts[0]
            sp = parts[1] if len(parts) > 1 else "NA"
            out.write(f"{q},full_protein,{sp},NA,NA,NA,NA,zero_hits(n=0)\n")
        else:
            parts = filename.replace(".tab", "").replace(".m8", "").split("_vs_")
            sp = parts[1] if len(parts) > 1 else "NA"
            for line in lines:
                cols = re.split(r"\s+", line)
                if len(cols) < 3:
                    continue
                target = cols[0]
                query = cols[1] if len(cols) > 1 else cols[0]
                evalue = cols[10] if len(cols) > 10 else "NA"
                bit_score = cols[11] if len(cols) > 11 else "NA"
                out.write(f"{query},full_protein,{sp},{target},NA,{bit_score},{evalue},foldseek_hit\n")

print("Foldseek summary successfully written to:", output_file)
