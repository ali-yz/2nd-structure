#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------------
# Usage check
# ------------------------------------------------------------------
if [[ $# -ne 4 ]]; then
  echo "Usage: $0 <input_file> <output_file> <download_dir> <parallel_downloads>"
  exit 1
fi

INPUT_FILE=$1          # e.g. ./data/small/pdb_ids.txt
OUTPUT_FILE=$2         # e.g. ./data/small/pdb_urls.txt
DOWNLOAD_DIR=$3        # e.g. ./data/small/mmCIF
PARALLEL_DOWNLOADS=$4  # e.g. 10

# ------------------------------------------------------------------
# 1) Generate the list of mmCIF URLs
# ------------------------------------------------------------------
awk '{
  # substr($1,2,2) picks the 2nd & 3rd characters of the PDB ID
  printf "https://files.rcsb.org/pub/pdb/data/structures/divided/mmCIF/%s/%s.cif.gz\n",
         substr($1,2,2), $1
}' "$INPUT_FILE" > "$OUTPUT_FILE"

URL_COUNT=$(wc -l < "$OUTPUT_FILE")
echo "Generated $URL_COUNT URLs and saved to $OUTPUT_FILE."

# ------------------------------------------------------------------
# 2) Create (or clean) download directory
# ------------------------------------------------------------------
mkdir -p "$DOWNLOAD_DIR"
echo "Download directory is $DOWNLOAD_DIR."

# ------------------------------------------------------------------
# 3) Download in parallel via xargs → curl
# ------------------------------------------------------------------
echo "Starting downloads of $URL_COUNT files (up to $PARALLEL_DOWNLOADS in parallel)…"

# Export so child bash instances see it
export DOWNLOAD_DIR

# Run xargs without -a (BSD/macOS compatible):
#  • -n1       → one URL per exec
#  • -P        → parallelism
#  • -I{}      → substitute {} with each URL
#  • bash -c   → executes the curl+echo; '_' is $0 inside that shell
#  • success.log captures URLs that returned 0
#  • errors.log captures any curl failures (stdout+stderr from curl)
cat "$OUTPUT_FILE" \
  | xargs -n1 -P"$PARALLEL_DOWNLOADS" -I{} bash -c \
      'curl -sSf -O -J -L --output-dir "$DOWNLOAD_DIR" "{}" && echo "{}"' _ \
      > "$DOWNLOAD_DIR/success.log" \
      2> "$DOWNLOAD_DIR/errors.log"

# ------------------------------------------------------------------
# 4) Summary
# ------------------------------------------------------------------
SUCCESS=$(wc -l < "$DOWNLOAD_DIR/success.log")
echo "Downloaded $SUCCESS out of $URL_COUNT files successfully to $DOWNLOAD_DIR."

if [[ -s "$DOWNLOAD_DIR/errors.log" ]]; then
  FAILURES=$(( URL_COUNT - SUCCESS ))
  echo "  ↳ $FAILURES failed downloads. See $DOWNLOAD_DIR/errors.log for details."
fi

exit 0
