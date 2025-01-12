#!/bin/zsh

# Check if correct arguments are provided
if [[ $# -ne 4 ]]; then
  echo "Usage: $0 <input_file> <output_file> <download_dir> <parallel_downloads>"
  exit 1
fi

# Parse arguments
INPUT_FILE=$1          # File containing PDB IDs (e.g., pdb_ids.txt)
OUTPUT_FILE=$2         # File to save generated URLs (e.g., pdb_urls.txt)
DOWNLOAD_DIR=$3        # Directory to download files (e.g., mmCIF)
PARALLEL_DOWNLOADS=$4  # Number of parallel downloads (e.g., 10)

# Step 1: Generate the list of URLs
awk '{printf "https://files.rcsb.org/pub/pdb/data/structures/divided/mmCIF/%s/%s.cif.gz\n", substr($1, 2, 2), $1}' "$INPUT_FILE" > "$OUTPUT_FILE" &&
echo "Generated URLs and saved to $OUTPUT_FILE."

# Step 2: Create the download directory if it doesn't exist
mkdir -p "$DOWNLOAD_DIR" &&
echo "Created download directory: $DOWNLOAD_DIR."

# Step 3: Download files using curl with parallel processing
SUCCESS_COUNT=0
TOTAL_COUNT=0

# Function to download a single file and count success
_download_file() {
  URL=$1
  OUTPUT_DIR=$2

  if curl -O -J -L --output-dir "$OUTPUT_DIR" "$URL"; then
    ((SUCCESS_COUNT++))
  fi
  ((TOTAL_COUNT++))
}

export -f _download_file
export DOWNLOAD_DIR
export SUCCESS_COUNT
export TOTAL_COUNT

# Download files in parallel
cat "$OUTPUT_FILE" | xargs -n 1 -P "$PARALLEL_DOWNLOADS" bash -c '_download_file "$@"' _

# Display summary
echo "Downloaded $SUCCESS_COUNT out of $TOTAL_COUNT files successfully to $DOWNLOAD_DIR."

exit 0
