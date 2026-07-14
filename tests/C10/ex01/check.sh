#!/bin/sh
# Build-check for C10/ex01 (ft_cat). Compares stdout with the system cat.
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../common.sh"
build_student "$1" ft_cat

F="$WORK/fix"
for f in hello.txt empty.txt lines.txt rand.bin nonl.txt zeros.bin; do
	cat "$F/$f" > "$WORK/exp.txt"
	run_diff "cat $f" "$WORK/exp.txt" ./ft_cat "$F/$f"
done

# several files
cat "$F/hello.txt" "$F/lines.txt" "$F/nonl.txt" > "$WORK/exp.txt"
run_diff "cat multiple files" "$WORK/exp.txt" \
	./ft_cat "$F/hello.txt" "$F/lines.txt" "$F/nonl.txt"

# stdin passthrough
printf 'from stdin\nline2\n' > "$WORK/stdin.txt"
./ft_cat < "$WORK/stdin.txt" > "$WORK/got.txt" 2>/dev/null
if ! cmp -s "$WORK/got.txt" "$WORK/stdin.txt"; then
	echo "case failed: cat from stdin"
	FAILED=1
fi

# missing file: must not crash, must keep processing the next file
cat "$F/hello.txt" > "$WORK/exp.txt"
./ft_cat "$F/does_not_exist" "$F/hello.txt" > "$WORK/got.txt" 2>/dev/null
if ! cmp -s "$WORK/got.txt" "$WORK/exp.txt"; then
	echo "case failed: missing file should not stop processing"
	FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
	echo "ft_cat matches system cat"
	exit 0
fi
exit 1
