#!/bin/sh
# Build-check for C10/ex00 (ft_display_file).
# $1 = student exercise directory (Makefile + sources).
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../common.sh"
build_student "$1" ft_display_file

# valid files: stdout must be exactly the file content
for f in hello.txt empty.txt lines.txt rand.bin nonl.txt; do
	run_diff "display $f" "$WORK/fix/$f" ./ft_display_file "$WORK/fix/$f"
done

# no argument -> "File name missing." on error output, nothing on stdout
./ft_display_file > "$WORK/out.txt" 2> "$WORK/err.txt"
if [ -s "$WORK/out.txt" ] && ! grep -q "File name missing." "$WORK/out.txt"; then
	echo "case failed: no-arg wrote unexpected data on stdout"
	FAILED=1
fi
if ! grep -q "File name missing." "$WORK/out.txt" "$WORK/err.txt"; then
	echo "case failed: missing 'File name missing.' message"
	FAILED=1
fi

# too many arguments
./ft_display_file a b > "$WORK/out.txt" 2> "$WORK/err.txt"
if ! grep -q "Too many arguments." "$WORK/out.txt" "$WORK/err.txt"; then
	echo "case failed: missing 'Too many arguments.' message"
	FAILED=1
fi

# unreadable file
./ft_display_file "$WORK/fix/does_not_exist" > "$WORK/out.txt" 2> "$WORK/err.txt"
if ! grep -q "Cannot read file." "$WORK/out.txt" "$WORK/err.txt"; then
	echo "case failed: missing 'Cannot read file.' message"
	FAILED=1
fi

# Makefile rules clean / fclean must exist and work
if ! make fclean >/dev/null 2>&1 || [ -e ./ft_display_file ]; then
	echo "case failed: make fclean did not remove the binary"
	FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
	echo "ft_display_file behaves correctly"
	exit 0
fi
exit 1
