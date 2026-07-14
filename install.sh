#!/bin/sh
# MiniMoulinette installer.
#
#   curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/install.sh | sh
#
# Downloads the prebuilt binary + test suites from the latest GitHub release
# into ~/.mini-moulinette and links the binary into ~/.local/bin.
# No cargo/rust needed. Falls back to a cargo build if no prebuilt binary
# exists for this platform.
set -e

REPO="eyjvw/MiniMoulinette"
INSTALL_DIR="${MINI_MOULINETTE_DIR:-$HOME/.mini-moulinette}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

info() { printf '\033[1;36m==>\033[0m %s\n' "$1"; }
err() { printf '\033[1;31merror:\033[0m %s\n' "$1" >&2; }

os="$(uname -s)"
arch="$(uname -m)"
case "$os" in
	Linux)
		case "$arch" in
			x86_64) target="x86_64-unknown-linux-musl" ;;
			aarch64 | arm64) target="aarch64-unknown-linux-musl" ;;
			*) target="" ;;
		esac
		;;
	Darwin)
		case "$arch" in
			x86_64) target="x86_64-apple-darwin" ;;
			arm64) target="aarch64-apple-darwin" ;;
			*) target="" ;;
		esac
		;;
	*) target="" ;;
esac

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fetched=0
if [ -n "$target" ]; then
	url="https://github.com/$REPO/releases/latest/download/mini-moulinette-$target.tar.gz"
	info "Downloading mini-moulinette ($target)..."
	if curl -fsSL "$url" -o "$tmp/mm.tar.gz" 2>/dev/null; then
		fetched=1
	else
		err "no prebuilt binary at $url"
	fi
fi

if [ "$fetched" -eq 1 ]; then
	mkdir -p "$tmp/pkg"
	tar -xzf "$tmp/mm.tar.gz" -C "$tmp/pkg"
else
	# fallback: build from source (needs cargo + git)
	if ! command -v cargo >/dev/null 2>&1; then
		err "no prebuilt binary for $os/$arch and cargo is not installed."
		err "install rust (https://rustup.rs) and re-run, or build manually."
		exit 1
	fi
	info "Building from source with cargo (this can take a minute)..."
	git clone --depth 1 "https://github.com/$REPO" "$tmp/src" >/dev/null 2>&1
	(cd "$tmp/src" && cargo build --release --quiet)
	mkdir -p "$tmp/pkg"
	cp "$tmp/src/target/release/MiniMoulinette" "$tmp/pkg/mini-moulinette"
	cp -r "$tmp/src/tests" "$tmp/pkg/tests"
fi

info "Installing into $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
rm -rf "$INSTALL_DIR/tests"
cp -r "$tmp/pkg/tests" "$INSTALL_DIR/tests"
cp "$tmp/pkg/mini-moulinette" "$INSTALL_DIR/mini-moulinette"
chmod +x "$INSTALL_DIR/mini-moulinette"

mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/mini-moulinette" "$BIN_DIR/mini-moulinette"

info "Installed: $BIN_DIR/mini-moulinette"

# add BIN_DIR to PATH in the shell rc files if missing
add_path_to_rc()
{
	rc="$1"
	line="export PATH=\"$BIN_DIR:\$PATH\""
	[ -f "$rc" ] || return 0
	if ! grep -Fq "$line" "$rc"; then
		printf '\n# added by mini-moulinette installer\n%s\n' "$line" >> "$rc"
		info "Added $BIN_DIR to PATH in $rc"
		UPDATED_RC=1
	fi
}

case ":$PATH:" in
	*":$BIN_DIR:"*) ;;
	*)
		UPDATED_RC=0
		add_path_to_rc "$HOME/.zshrc"
		add_path_to_rc "$HOME/.bashrc"
		# no rc file at all -> create one for the current shell
		if [ "$UPDATED_RC" -eq 0 ]; then
			case "${SHELL:-}" in
				*zsh) touch "$HOME/.zshrc" && add_path_to_rc "$HOME/.zshrc" ;;
				*) touch "$HOME/.bashrc" && add_path_to_rc "$HOME/.bashrc" ;;
			esac
		fi
		printf '\033[1;33mnote:\033[0m open a new terminal (or run: export PATH="%s:$PATH")\n' "$BIN_DIR"
		;;
esac

printf '\nUsage:\n'
printf '    cd <dossier du rendu>   # contient ex00/, ex01/, ...\n'
printf '    mini-moulinette C07\n'
printf '    mini-moulinette run C07 --path <dossier> --strict\n'
