#!/bin/bash

# Configuration
SCRIPT_PATH="src/ingest_web.py"
MAX_DEPTH=2
LOG_FILE="ingest_web.log"

# List of URLs to crawl
declare -a URLS=(
    "https://arc42.org/overview"
    "https://mermaid.js.org/intro/"
    "https://dbus.freedesktop.org/doc/dbus-specification.html"
    "https://www.doxygen.nl/manual/markdown.html"
    "https://protobuf.dev/programming-guides/style/"
    "https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html"
    "https://cmake.org/cmake/help/latest/guide/tutorial/index.html"
    "https://google.github.io/styleguide/cppguide.html"
    "https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines"
)

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==========================================" | tee -a "$LOG_FILE"
echo "Starting Bulk Web Ingestion" | tee -a "$LOG_FILE"
echo "Date: $(date)" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}Error: .venv not found. Please setup the environment first.${NC}"
    exit 1
fi

# Main Loop
FAILED_URLS=()

for url in "${URLS[@]}"; do
    echo -e "\n${YELLOW}Processing: $url${NC}" | tee -a "$LOG_FILE"
    
    python "$SCRIPT_PATH" "$url" --max-depth "$MAX_DEPTH" 2>&1 | tee -a "$LOG_FILE"
    
    EXIT_CODE=${PIPESTATUS[0]} # Get exit code of python script
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}✅ Success: $url${NC}" | tee -a "$LOG_FILE"
    else
        echo -e "${RED}❌ Failed: $url (Exit Code: $EXIT_CODE)${NC}" | tee -a "$LOG_FILE"
        FAILED_URLS+=("$url")
    fi
    
    echo "------------------------------------------" | tee -a "$LOG_FILE"
done

# Summary
echo -e "\n==========================================" | tee -a "$LOG_FILE"
echo "Ingestion Summary" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

if [ ${#FAILED_URLS[@]} -eq 0 ]; then
    echo -e "${GREEN}All tasks completed successfully!${NC}" | tee -a "$LOG_FILE"
else
    echo -e "${RED}Some URLs failed to ingest:${NC}" | tee -a "$LOG_FILE"
    for failed in "${FAILED_URLS[@]}"; do
        echo " - $failed" | tee -a "$LOG_FILE"
    done
    exit 1
fi
