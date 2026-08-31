import subprocess
import pandas as pd
import os

target_genes = {
    "CDK4": "cdk4_query.fa",
    "CDK6": "cdk6_query.fa",
    "E2F1": "e2f1_query.fa",
    "E2F2": "e2f2_query.fa",
    "E2F3": "e2f3_query.fa",
    "MYCN": "mycn_query.fa",
    "MDM2": "mdm2_query.fa"
}

def run_quantitative_blast(genes_dict, db_path="uniprot_db", num_threads=8):
    print(f"[INFO] Executing quantitative BLASTp across {num_threads} CPU threads...")
    results = []
    
    for gene, query_file in genes_dict.items():
        output_file = f"{gene}_blast_out.tab"
        
        if not os.path.exists(query_file):
            print(f"[WARNING] Query file {query_file} not found. Creating placeholder entry.")
            results.append({
                "Gene": gene,
                "Accession": "Pending_FASTA",
                "Bit_Score": 0.0,
                "E_Value": "N/A",
                "Identity_Pct": 0.0,
                "Description": "Fasta sequence file required"
            })
            continue

        cmd = [
            "blastp",
            "-query", query_file,
            "-db", db_path,
            "-num_threads", str(num_threads),
            "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle",
            "-out", output_file,
            "-max_target_seqs", "1"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                df = pd.read_csv(output_file, sep="\t", header=None)
                df.columns = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 
                              'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 'stitle']
                best_hit = df.iloc[0]
                results.append({
                    "Gene": gene,
                    "Accession": best_hit['sseqid'],
                    "Bit_Score": best_hit['bitscore'],
                    "E_Value": best_hit['evalue'],
                    "Identity_Pct": best_hit['pident'],
                    "Description": best_hit['stitle']
                })
        except Exception as e:
            print(f"[ERROR] BLASTp execution failed for {gene}: {e}")
            
    summary_df = pd.DataFrame(results)
    output_csv = "tables/quantitative_blast_summary_7_genes.csv"
    os.makedirs("tables", exist_ok=True)
    summary_df.to_csv(output_csv, index=False)
    print(f"[INFO] Quantitative results successfully compiled and saved to '{output_csv}'.")
    return summary_df

if __name__ == "__main__":
    run_quantitative_blast(target_genes, num_threads=8)
