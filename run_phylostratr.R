dir.create("C:/blast_work", showWarnings = FALSE)
setwd("C:/blast_work")

# Re-link to your downloaded proteome files
proteome_dir <- "C:/Users/HP/OneDrive/Documents/proteomes"
key_taxids <- c("9606", "10090", "7955", "7227", "4932") # Human, Mouse, Zebrafish, Fly, Yeast

library(phylostratr)
library(ape)

# Build initial small strata object
strata <- uniprot_strata("9606", from = 2)
strata@tree <- ape::keep.tip(strata@tree, intersect(strata@tree$tip.label, key_taxids))

strata@data$faa <- list()
for (tid in strata@tree$tip.label) {
  out_file <- file.path(proteome_dir, paste0(tid, ".faa"))
  if (file.exists(out_file) && file.info(out_file)$size > 100) {
    strata@data$faa[[tid]] <- out_file
  }
}

# Run BLAST and stratify across the targeted tree
strata <- strata_blast(strata)
