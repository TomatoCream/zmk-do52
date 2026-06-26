#!/bin/bash
set -e

# ZMK Build Script
# Usage: ./scripts/build.sh [left|right|both]
#
# Builds the do52 (nice!nano v2) firmware into ./firmware/do52_<side>.uf2.
# The RIGHT half is the BLE central and carries the PS/2 trackpoint.
#
# Override the target with env vars, e.g. the older do52pro:
#   KEYBOARD=do52pro BOARD=nice_nano_v2 ./scripts/build.sh both
#
# NOTE: After editing config/west.yml you must run `west update` once before
# building (the toolchain workspace needs to fetch the new zmk fork/modules).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
FIRMWARE_DIR="$PROJECT_DIR/firmware"
VENV_DIR="$HOME/zmk-workspace/.venv"

# Build target (override via environment)
KEYBOARD="${KEYBOARD:-do52}"
BOARD="${BOARD:-nice_nano_v2}"
TOOLCHAIN_PATH="${GNUARMEMB_TOOLCHAIN_PATH:-/Applications/ArmGNUToolchain/15.2.rel1/arm-none-eabi}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Setup environment
setup_env() {
    log_info "Setting up build environment..."

    if [ ! -d "$VENV_DIR" ]; then
        log_error "Virtual environment not found at $VENV_DIR"
        log_info "Run ./scripts/setup.sh first (see CLAUDE.md)"
        exit 1
    fi

    source "$VENV_DIR/bin/activate"
    export GNUARMEMB_TOOLCHAIN_PATH="$TOOLCHAIN_PATH"
    export ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb

    mkdir -p "$FIRMWARE_DIR"
}

# Build function
build_side() {
    local side=$1
    local shield="${KEYBOARD}_${side}"
    log_info "Building ${shield} on ${BOARD}..."

    cd "$PROJECT_DIR"

    west build -s zmk/app -b "$BOARD" --pristine \
        -- -DSHIELD="$shield" \
        -DZMK_CONFIG="$PROJECT_DIR/config" \
        -DBOARD_ROOT="$PROJECT_DIR"

    if [ -f "$PROJECT_DIR/build/zephyr/zmk.uf2" ]; then
        cp "$PROJECT_DIR/build/zephyr/zmk.uf2" "$FIRMWARE_DIR/${shield}.uf2"
        log_success "Built: $FIRMWARE_DIR/${shield}.uf2"
    else
        log_error "Build failed for ${side} side"
        exit 1
    fi
}

# Main
main() {
    local target="${1:-both}"

    echo ""
    echo "╔═══════════════════════════════════════╗"
    echo "║       ZMK Firmware Build Script       ║"
    printf  "║   %-35s ║\n" "${KEYBOARD} @ ${BOARD}"
    echo "╚═══════════════════════════════════════╝"
    echo ""

    setup_env

    case "$target" in
        left)
            build_side "left"
            ;;
        right)
            build_side "right"
            ;;
        both)
            build_side "left"
            echo ""
            build_side "right"
            ;;
        *)
            log_error "Unknown target: $target"
            echo "Usage: $0 [left|right|both]"
            exit 1
            ;;
    esac

    echo ""
    log_success "Build complete!"
    echo ""
    echo "Firmware files:"
    ls -lh "$FIRMWARE_DIR"/*.uf2 2>/dev/null || echo "No firmware files found"
    echo ""
    echo "To flash, run: ./scripts/flash.sh [left|right|both]"
}

main "$@"
