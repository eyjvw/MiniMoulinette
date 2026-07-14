#!/bin/sh
# MiniMoulinette uninstaller.
#
#   curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/uninstall.sh | sh
#
# Removes ~/.mini-moulinette, the mini-moulinette command and the PATH lines
# the installer added to ~/.zshrc / ~/.bashrc. Nothing else is touched.
set -e

INSTALL_DIR="${MINI_MOULINETTE_DIR:-$HOME/.mini-moulinette}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

info() { printf '\033[1;36m==>\033[0m %s\n' "$1"; }

removed=0
if [ -d "$INSTALL_DIR" ]; then
	rm -rf "$INSTALL_DIR"
	info "Removed $INSTALL_DIR"
	removed=1
fi
if [ -e "$BIN_DIR/mini-moulinette" ] || [ -L "$BIN_DIR/mini-moulinette" ]; then
	rm -f "$BIN_DIR/mini-moulinette"
	info "Removed $BIN_DIR/mini-moulinette"
	removed=1
fi

# strip the exact two lines the installer appended, nothing else
marker='# added by mini-moulinette installer'
export_line="export PATH=\"$BIN_DIR:\$PATH\""
for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
	[ -f "$rc" ] || continue
	if grep -qxF "$marker" "$rc" || grep -qxF "$export_line" "$rc"; then
		grep -vxF "$marker" "$rc" | grep -vxF "$export_line" > "$rc.mm_tmp"
		mv "$rc.mm_tmp" "$rc"
		info "Cleaned PATH lines from $rc"
		removed=1
	fi
done

# leftover trace files
rm -f /tmp/mini-moulinette-*.trace 2>/dev/null || true

if [ "$removed" -eq 1 ]; then
	info "mini-moulinette uninstalled. Bye!"
else
	info "nothing to uninstall (mini-moulinette was not installed)"
fi
