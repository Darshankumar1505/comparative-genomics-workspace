suppressPackageStartupMessages({
  library(bio3d)
})

pdb_path <- path.expand("~/rb1_project/af_structures/1N4M.pdb")
if (!file.exists(pdb_path)) {
  stop("1N4M.pdb not found!")
}

pdb <- read.pdb(pdb_path)

# Test 1: Vector chain selection in bio3d
rb1_indices <- atom.select(pdb, chain="A", elety="CA")
e2f_indices <- atom.select(pdb, chain=c("C", "D"), elety="CA")

cat("=== BIO3D SELECTION TEST ===\n")
cat("RB1 Chain A CA atoms count:", length(rb1_indices$atom), "\n")
cat("E2F/DP Chains C+D CA atoms count:", length(e2f_indices$atom), "\n")
cat("Chains captured in e2f_indices:", paste(unique(pdb$atom$chain[e2f_indices$atom]), collapse=", "), "\n\n")

# Test 2: Matrix dimension orientation test
rb1_coords <- pdb$xyz[rb1_indices$xyz]
e2f_coords <- pdb$xyz[e2f_indices$xyz]

dmat <- dist.xyz(matrix(rb1_coords, ncol=3, byrow=TRUE), 
                 matrix(e2f_coords, ncol=3, byrow=TRUE))

cat("=== MATRIX DIMENSION TEST ===\n")
cat("Expected dimensions (RB1 x E2F):", length(rb1_indices$atom), "x", length(e2f_indices$atom), "\n")
cat("Actual dmat dimensions        :", nrow(dmat), "x", ncol(dmat), "\n")
