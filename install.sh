#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"

show_usage() {
    echo "Usage: $0 [original|modified|all] [-s]"
    echo ""
    echo "Arguments:"
    echo "  original  - Install original variant"
    echo "  modified  - Install modified variant"
    echo "  all       - Install both variants (default)"
    echo ""
    echo "Options:"
    echo "  -s        - Install system-wide to /usr/share/icons/"
    echo "              (default: install to ~/.icons/)"
    echo "  -h        - Show this help"
}

SYSTEM_WIDE=false
VARIANT="${1:-all}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -s)
            SYSTEM_WIDE=true
            shift
            ;;
        -h)
            show_usage
            exit 0
            ;;
        original|modified|all)
            VARIANT="$1"
            shift
            ;;
        *)
            echo "Error: Unknown option $1"
            show_usage
            exit 1
            ;;
    esac
done

if [ "$SYSTEM_WIDE" = true ]; then
    if [ "$(id -u)" -ne 0 ]; then
        echo "Error: System-wide install requires root. Use sudo or run as root."
        exit 1
    fi
    ICON_DIR="/usr/share/icons"
else
    ICON_DIR="$HOME/.icons"
fi

install_variant() {
    local variant=$1
    local src="$DIST_DIR/zune-cursors-$variant"
    local dest="$ICON_DIR/zune-cursors-$variant"
    
    if [ ! -d "$src" ]; then
        echo "Error: $src does not exist. Run ./build.sh first."
        return 1
    fi
    
    echo "Installing $variant to $dest..."
    
    mkdir -p "$dest"
    cp -r "$src"/* "$dest/"
}

case "$VARIANT" in
    original)
        install_variant "original"
        ;;
    modified)
        install_variant "modified"
        ;;
    all)
        install_variant "original"
        install_variant "modified"
        ;;
esac

echo ""
echo "To use the cursor theme:"
echo "  1. Open GNOME Tweaks or System Settings"
echo "  2. Go to Appearance/Customize"
echo "  3. Select 'Zune Cursors - original' or 'Zune Cursors - modified'"
echo ""
echo "Or run: gsettings set org.gnome.desktop.interface cursor-theme 'zune-cursors-$VARIANT'"
