#!/bin/bash
# Compile HMMER results into one summary CSV
OUT=summary/rb_pathway_hmmer_summary.csv
echo "query,domain,species,target_id,gene,bit_score,evalue,note" > $OUT

# Yeast nulls (RB1, RBL1, RBL2 vs yeast — jackhmmer)
for query in RB1 RBL1 RBL2; do
  n=$(grep -v "^#" hmmer_out/${query}_vs_4932.tab 2>/dev/null | wc -l)
  echo "${query},full_protein,yeast_4932,NA,NA,NA,NA,zero_hits(n=${n})" >> $OUT
done

# Mouse RB_A domain hits
grep -v "^#" hmmer_out/RB_A_vs_10090.tab 2>/dev/null | awk '{print "RB_A,RB_A,mouse_10090,"$1","$NF","$6","$5",real_hit"}' >> $OUT

# Mouse RB_B domain hits
grep -v "^#" hmmer_out/RB_B_vs_10090.tab 2>/dev/null | awk '{print "RB_B,RB_B,mouse_10090,"$1","$NF","$6","$5",real_hit"}' >> $OUT

# Zebrafish top hits (RB1, RBL1, RBL2 vs zebrafish v2 — fixed proteome)
for query in RB1 RBL1 RBL2; do
  grep -v "^#" hmmer_out/${query}_vs_7955_v2.tab 2>/dev/null | sort -k5,5g | head -3 | \
    awk -v q="$query" '{print q",full_protein,zebrafish_7955,"$1","$NF","$6","$5",real_hit"}' >> $OUT
done

echo "Summary written to $OUT"
wc -l $OUT
