#!/bin/bash
# =============================================================================
# Multi-Language Test Dataset Setup Script
# =============================================================================
# This script clones open-source projects and generates Ground Truth documentation
# for evaluating the RAG documentation generation system.
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directories
BASE_DIR="test_data"
GROUND_TRUTH_DIR="ground_truth"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Multi-Language Test Dataset Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# -----------------------------------------------------------------------------
# Phase 1: Create directories and clone repositories
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[Phase 1] Cloning repositories...${NC}\n"

mkdir -p "$BASE_DIR"/{c,cpp,rust,go,python}
mkdir -p "$GROUND_TRUTH_DIR"/{c,cpp,rust,go,python}

# C - SQLite (small, well-documented)
if [ ! -d "$BASE_DIR/c/sqlite" ]; then
    echo -e "${GREEN}Cloning SQLite...${NC}"
    gh repo clone sqlite/sqlite "$BASE_DIR/c/sqlite" -- --depth 1 --single-branch
else
    echo -e "${YELLOW}SQLite already exists, skipping...${NC}"
fi

# C++ - nlohmann/json (popular, excellent docs)
if [ ! -d "$BASE_DIR/cpp/json" ]; then
    echo -e "${GREEN}Cloning nlohmann/json...${NC}"
    gh repo clone nlohmann/json "$BASE_DIR/cpp/json" -- --depth 1 --single-branch
else
    echo -e "${YELLOW}nlohmann/json already exists, skipping...${NC}"
fi

# Rust - Tokio (async runtime, good rustdoc)
if [ ! -d "$BASE_DIR/rust/tokio" ]; then
    echo -e "${GREEN}Cloning Tokio...${NC}"
    gh repo clone tokio-rs/tokio "$BASE_DIR/rust/tokio" -- --depth 1 --single-branch
else
    echo -e "${YELLOW}Tokio already exists, skipping...${NC}"
fi

# Go - Gin (web framework, well-documented)
if [ ! -d "$BASE_DIR/go/gin" ]; then
    echo -e "${GREEN}Cloning Gin...${NC}"
    gh repo clone gin-gonic/gin "$BASE_DIR/go/gin" -- --depth 1 --single-branch
else
    echo -e "${YELLOW}Gin already exists, skipping...${NC}"
fi

# Python - Requests (HTTP library, great docstrings)
if [ ! -d "$BASE_DIR/python/requests" ]; then
    echo -e "${GREEN}Cloning Requests...${NC}"
    gh repo clone psf/requests "$BASE_DIR/python/requests" -- --depth 1 --single-branch
else
    echo -e "${YELLOW}Requests already exists, skipping...${NC}"
fi

echo -e "\n${GREEN}✅ All repositories cloned!${NC}"

# -----------------------------------------------------------------------------
# Phase 2: Generate Ground Truth Documentation
# -----------------------------------------------------------------------------
echo -e "\n${YELLOW}[Phase 2] Generating Ground Truth documentation...${NC}\n"

# --- C/C++ with Doxygen ---
generate_doxygen_docs() {
    local src_dir=$1
    local output_dir=$2
    local project_name=$3
    
    if command -v doxygen &> /dev/null; then
        echo -e "${GREEN}Generating Doxygen docs for $project_name...${NC}"
        
        # Create minimal Doxyfile
        cat > "$src_dir/Doxyfile.tmp" << EOF
PROJECT_NAME           = "$project_name"
OUTPUT_DIRECTORY       = "$output_dir"
INPUT                  = "$src_dir"
RECURSIVE              = YES
GENERATE_HTML          = NO
GENERATE_LATEX         = NO
GENERATE_XML           = YES
FILE_PATTERNS          = *.c *.cpp *.h *.hpp
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = NO
EXTRACT_STATIC         = YES
EOF
        
        (cd "$src_dir" && doxygen Doxyfile.tmp 2>/dev/null) || echo -e "${YELLOW}Doxygen warning for $project_name${NC}"
        rm -f "$src_dir/Doxyfile.tmp"
    else
        echo -e "${RED}Doxygen not installed. Install with: brew install doxygen${NC}"
    fi
}

# --- Rust with cargo doc ---
generate_rust_docs() {
    local src_dir=$1
    local output_dir=$2
    
    if command -v cargo &> /dev/null; then
        echo -e "${GREEN}Generating Rust docs for Tokio...${NC}"
        (cd "$src_dir" && cargo doc --no-deps 2>/dev/null) || echo -e "${YELLOW}Rust doc warning${NC}"
        
        # Copy the generated docs
        if [ -d "$src_dir/target/doc" ]; then
            cp -r "$src_dir/target/doc"/* "$output_dir/" 2>/dev/null || true
        fi
    else
        echo -e "${RED}Cargo not installed. Install Rust toolchain.${NC}"
    fi
}

# --- Go with gomarkdoc ---
generate_go_docs() {
    local src_dir=$1
    local output_dir=$2
    
    if command -v gomarkdoc &> /dev/null; then
        echo -e "${GREEN}Generating Go docs for Gin...${NC}"
        gomarkdoc --output "$output_dir/gin.md" "$src_dir/..." 2>/dev/null || echo -e "${YELLOW}gomarkdoc warning${NC}"
    else
        echo -e "${RED}gomarkdoc not installed. Install with: go install github.com/princjef/gomarkdoc/cmd/gomarkdoc@latest${NC}"
    fi
}

# --- Python with pydoc ---
generate_python_docs() {
    local src_dir=$1
    local output_dir=$2
    
    echo -e "${GREEN}Generating Python docs for Requests...${NC}"
    
    # Extract docstrings from main modules
    python3 << EOF
import os
import ast
import sys

src_dir = "$src_dir/src/requests"
output_dir = "$output_dir"

if not os.path.exists(src_dir):
    src_dir = "$src_dir/requests"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(src_dir):
    if filename.endswith('.py') and not filename.startswith('_'):
        filepath = os.path.join(src_dir, filename)
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            
            doc = ast.get_docstring(tree) or "No module docstring"
            
            with open(os.path.join(output_dir, filename.replace('.py', '.md')), 'w') as out:
                out.write(f"# {filename}\n\n{doc}\n")
            
        except Exception as e:
            print(f"Warning: Could not process {filename}: {e}", file=sys.stderr)

print("Python docs generated.")
EOF
}

# Run documentation generation
generate_doxygen_docs "$BASE_DIR/c/sqlite" "$GROUND_TRUTH_DIR/c" "SQLite"
generate_doxygen_docs "$BASE_DIR/cpp/json" "$GROUND_TRUTH_DIR/cpp" "nlohmann_json"
generate_rust_docs "$BASE_DIR/rust/tokio" "$GROUND_TRUTH_DIR/rust"
generate_go_docs "$BASE_DIR/go/gin" "$GROUND_TRUTH_DIR/go"
generate_python_docs "$BASE_DIR/python/requests" "$GROUND_TRUTH_DIR/python"

echo -e "\n${GREEN}✅ Ground Truth documentation generated!${NC}"

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo -e "\n${BLUE}========================================${NC}"
echo -e "${BLUE}  Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "\nTest data location: ${GREEN}$BASE_DIR/${NC}"
echo -e "Ground truth docs:  ${GREEN}$GROUND_TRUTH_DIR/${NC}"
echo -e "\nNext steps:"
echo -e "  1. Run ingest_data.py to add test data to VectorDB"
echo -e "  2. Run generate_docs.py on source files"
echo -e "  3. Run evaluate_ground_truth.py to compare results"
