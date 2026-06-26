#!/bin/bash
set -e

# ZMK Flash Script
# Usage: ./scripts/flash.sh [left|right|both]
#
# Flashes ./firmware/<KEYBOARD>_<side>.uf2 to a nice!nano in bootloader mode.
# Override the keyboard (e.g. the older do52pro) with: KEYBOARD=do52pro ...

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
FIRMWARE_DIR="$PROJECT_DIR/firmware"

# Must match scripts/build.sh
KEYBOARD="${KEYBOARD:-do52}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Wait for bootloader volume to appear
wait_for_bootloader() {
    local timeout=60
    local count=0
    
    echo -e "${CYAN}" >&2
    echo "╔═══════════════════════════════════════════════════════╗" >&2
    echo "║  Double-tap the RESET button on your nice!nano now!   ║" >&2
    echo "║  Waiting for NICENANO drive to appear...              ║" >&2
    echo "╚═══════════════════════════════════════════════════════╝" >&2
    echo -e "${NC}" >&2
    
    while [ $count -lt $timeout ]; do
        # Check for common bootloader volume names
        for vol in "/Volumes/NICENANO" "/Volumes/NRF52BOOT" "/Volumes/NICE!NANO"; do
            if [ -d "$vol" ]; then
                echo "$vol"
                return 0
            fi
        done
        
        sleep 1
        count=$((count + 1))
        printf "\r${YELLOW}Waiting... %ds${NC}  " $count >&2
    done

    echo "" >&2
    return 1
}

# Flash firmware
flash_firmware() {
    local side=$1
    local firmware_file="$FIRMWARE_DIR/${KEYBOARD}_${side}.uf2"

    if [ ! -f "$firmware_file" ]; then
        log_error "Firmware file not found: $firmware_file"
        log_info "Run './scripts/build.sh $side' first"
        exit 1
    fi

    log_info "Ready to flash: ${KEYBOARD}_${side}"
    echo "Firmware: $firmware_file"
    echo ""

    local volume
    volume=$(wait_for_bootloader)

    if [ $? -ne 0 ] || [ -z "$volume" ]; then
        echo ""
        log_error "Timeout waiting for bootloader"
        log_info "Make sure to double-tap the reset button quickly"
        exit 1
    fi

    echo ""
    log_info "Found bootloader at: $volume"
    log_info "Copying firmware..."

    # The nice!nano bootloader reboots the instant the UF2 finishes copying,
    # which yanks the drive away mid-write. macOS reports this as an I/O error
    # even though the flash succeeded, so we ignore cp's exit code and instead
    # confirm success by checking that the volume ejected.
    cp "$firmware_file" "$volume/" 2>/dev/null || true
    sleep 2

    if [ ! -d "$volume" ]; then
        log_success "Flashed ${KEYBOARD}_${side} (board rebooted)"
    else
        log_error "Volume still mounted at $volume — flash may have failed"
        exit 1
    fi
}

# Interactive mode - flash both sides
flash_both() {
    echo ""
    echo -e "${GREEN}=== Flashing LEFT side ===${NC}"
    flash_firmware "left"
    
    echo ""
    echo -e "${YELLOW}Unplug the left side and connect the right side${NC}"
    echo "Press Enter when ready..."
    read -r
    
    echo ""
    echo -e "${GREEN}=== Flashing RIGHT side ===${NC}"
    flash_firmware "right"
    
    echo ""
    log_success "Both sides flashed successfully!"
    echo ""
    echo "Your keyboard is ready to use!"
    echo "The halves will automatically pair via Bluetooth."
}

# List available firmware
list_firmware() {
    echo ""
    echo "Available firmware files:"
    echo ""
    if ls "$FIRMWARE_DIR"/*.uf2 1>/dev/null 2>&1; then
        ls -lh "$FIRMWARE_DIR"/*.uf2
    else
        log_warn "No firmware files found"
        log_info "Run './scripts/build.sh' first"
    fi
    echo ""
}

# Show usage
usage() {
    echo ""
    echo "ZMK Flash Script (${KEYBOARD})"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  left      Flash the left half"
    echo "  right     Flash the right half"
    echo "  both      Flash both halves (interactive)"
    echo "  list      List available firmware files"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 left       # Flash left half only"
    echo "  $0 both       # Flash both halves interactively"
    echo ""
}

# Main
main() {
    local command="${1:-help}"
    
    echo ""
    echo "╔═══════════════════════════════════════╗"
    echo "║       ZMK Firmware Flash Script       ║"
    printf  "║   %-35s ║\n" "${KEYBOARD} keyboard"
    echo "╚═══════════════════════════════════════╝"
    
    case "$command" in
        left)
            flash_firmware "left"
            ;;
        right)
            flash_firmware "right"
            ;;
        both)
            flash_both
            ;;
        list)
            list_firmware
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            log_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

main "$@"
