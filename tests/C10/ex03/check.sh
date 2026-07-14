#!/bin/sh
# Build-check for C10/ex03 (ft_hexdump -C). Compares stdout with hexdump -C.
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../common.sh"
build_student "$1" ft_hexdump

F="$WORK/fix"
# zeros.bin exercises the '*' squeeze of repeated lines
for f in hello.txt empty.txt lines.txt rand.bin nonl.txt zeros.bin; do
	hexdump -C "$F/$f" > "$WORK/exp.txt"
	run_diff "hexdump -C $f" "$WORK/exp.txt" ./ft_hexdump -C "$F/$f"
done

# non-multiple-of-16 sizes around the block boundary
for n in 15 16 17 31 32 33; do
	head -c "$n" "$F/rand.bin" > "$WORK/part.bin"
	hexdump -C "$WORK/part.bin" > "$WORK/exp.txt"
	run_diff "hexdump -C $n bytes" "$WORK/exp.txt" ./ft_hexdump -C "$WORK/part.bin"
done

# several files are dumped as one continuous stream
hexdump -C "$F/hello.txt" "$F/nonl.txt" > "$WORK/exp.txt" 2>/dev/null
run_diff "hexdump -C two files" "$WORK/exp.txt" \
	./ft_hexdump -C "$F/hello.txt" "$F/nonl.txt"

# stdin
hexdump -C < "$F/hello.txt" > "$WORK/exp.txt"
./ft_hexdump -C < "$F/hello.txt" > "$WORK/got.txt" 2>/dev/null
if ! cmp -s "$WORK/got.txt" "$WORK/exp.txt"; then
	echo "case failed: hexdump -C from stdin"
	FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
	echo "ft_hexdump matches system hexdump -C"
	exit 0
fi
exit 1
