library(tools)

extract_checkpoints <- function(source_dir, output_dir) {
  # Find all .RData or .rdata files recursively
  rdata_files <- list.files(source_dir, pattern = "\\.[Rr][Dd]ata$", recursive = TRUE, full.names = TRUE)
  
  # Exclude files already in the output directory to avoid self-referencing loops
  rdata_files <- rdata_files[!grepl(output_dir, rdata_files)]
  
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  
  cat(sprintf("[INFO] Found %d RData checkpoint files to process.\n", length(rdata_files)))
  
  for (file_path in rdata_files) {
    cat(sprintf("\n--------------------------------------------------\n"))
    cat(sprintf("Processing: %s\n", file_path))
    
    # Create a temporary environment to load objects into without polluting global workspace
    temp_env <- new.env()
    
    tryCatch({
      loaded_objs <- load(file_path, envir = temp_env)
      cat(sprintf("Objects found inside: %s\n", paste(loaded_objs, collapse = ", ")))
      
      # Export each data frame or matrix object to CSV
      for (obj_name in loaded_objs) {
        obj <- get(obj_name, envir = temp_env)
        
        if (is.data.frame(obj) || is.matrix(obj)) {
          out_name <- sprintf("%s_%s.csv", file_path_sans_ext(basename(file_path)), obj_name)
          out_path <- file.path(output_dir, out_name)
          
          write.csv(obj, out_path, row.names = TRUE)
          cat(sprintf(" -> Exported '%s' to %s\n", obj_name, out_path))
        } else {
          cat(sprintf(" -> Skipped '%s' (class: %s is not a data.frame or matrix)\n", obj_name, paste(class(obj), collapse=", ")))
        }
      }
    }, error = function(e) {
      cat(sprintf("[ERROR] Failed to process %s: %s\n", file_path, e$message))
    })
  }
}

# Run the extraction on your workspace pointing to the checkpoints folder
extract_checkpoints("./organized_workspace", "./organized_workspace/results/extracted_checkpoints_csv")