#!/bin/bash
set -e

# ZMK Development Environment Setup Script
# Run this once to set up your build environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$HOME/zmk-workspace"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║     ZMK Development Environment       ║"
echo "║           Setup Script                ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    log_error "Homebrew not found. Please install it first:"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install dependencies
log_info "Installing dependencies via Homebrew..."
brew install cmake ninja python3 dtc

# Install ARM toolchain
log_info "Checking ARM toolchain..."
if ! command -v arm-none-eabi-gcc &> /dev/null; then
    log_info "Installing ARM GCC toolchain..."
    brew install --cask gcc-arm-embedded
else
    log_success "ARM toolchain already installed"
fi

# Create workspace and virtual environment
log_info "Setting up Python virtual environment..."
mkdir -p "$WORKSPACE_DIR"
cd "$WORKSPACE_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install west

# Initialize west workspace
log_info "Initializing west workspace..."
cd "$WORKSPACE_DIR"

if [ ! -d "$PROJECT_DIR/.west" ]; then
    west init -l "$PROJECT_DIR/config"
fi

# Update west modules
log_info "Fetching ZMK and Zephyr (this may take a while)..."
cd "$PROJECT_DIR"
west update

# Export Zephyr
log_info "Exporting Zephyr CMake package..."
west zephyr-export

# Install Python requirements
log_info "Installing Python requirements..."
pip install -r zephyr/scripts/requirements.txt

# Create module.yml if missing
if [ ! -f "$PROJECT_DIR/zephyr/module.yml" ]; then
    log_info "Creating zephyr/module.yml..."
    mkdir -p "$PROJECT_DIR/zephyr"
    cat > "$PROJECT_DIR/zephyr/module.yml" << 'EOF'
build:
  settings:
    board_root: .
EOF
fi

echo ""
log_success "Setup complete!"
echo ""
echo "To build firmware, run:"
echo "  ./scripts/build.sh"
echo ""
echo "To flash firmware, run:"
echo "  ./scripts/flash.sh left"
echo "  ./scripts/flash.sh right"
echo ""
