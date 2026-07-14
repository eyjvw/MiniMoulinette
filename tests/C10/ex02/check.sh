#!/bin/sh
# Build-check for C10/ex02 (ft_tail -c). Compares stdout with the system tail.
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../common.sh"
build_student "$1" ft_tail

F="$WORK/fix"
for n in 1 5 10 100 20000; do
	for f in hello.txt lines.txt rand.bin nonl.txt; do
		tail -c "$n" "$F/$f" > "$WORK/exp.txt"
		run_diff "tail -c $n $f" "$WORK/exp.txt" ./ft_tail -c "$n" "$F/$f"
	done
done

# empty file
tail -c 10 "$F/empty.txt" > "$WORK/exp.txt"
run_diff "tail -c 10 empty" "$WORK/exp.txt" ./ft_tail -c 10 "$F/empty.txt"

# several files -> GNU-style ==> file <== headers
tail -c 12 "$F/hello.txt" "$F/lines.txt" > "$WORK/exp.txt"
run_diff "tail -c 12 two files" "$WORK/exp.txt" \
	./ft_tail -c 12 "$F/hello.txt" "$F/lines.txt"

# stdin
tail -c 25 < "$F/lines.txt" > "$WORK/exp.txt"
./ft_tail -c 25 < "$F/lines.txt" > "$WORK/got.txt" 2>/dev/null
if ! cmp -s "$WORK/got.txt" "$WORK/exp.txt"; then
	echo "case failed: tail -c from stdin"
	FAILED=1
fi

if [ "$FAILED" -eq 0 ]; then
	echo "ft_tail matches system tail -c"
	exit 0
fi
exit 1
