# Shared helpers for C10 build-checks. Sourced by each check.sh.
# build_student <student_dir> <binary_name>
#   Copies the rendu into $WORK, runs make, checks the binary exists.
#   Leaves the caller cd'ed into $WORK. Also creates the shared fixtures.

build_student()
{
	STUDENT="$1"
	BIN="$2"
	WORK="$(mktemp -d)"
	trap 'rm -rf "$WORK"' EXIT

	if [ ! -f "$STUDENT/Makefile" ]; then
		echo "Makefile not found"
		exit 1
	fi
	mkdir -p "$WORK/src"
	cp -r "$STUDENT"/. "$WORK/src/"
	cd "$WORK/src" || exit 1
	if ! make >/dev/null 2>&1; then
		echo "make failed"
		exit 1
	fi
	if [ ! -x "./$BIN" ]; then
		echo "binary $BIN was not created by make"
		exit 1
	fi
	# fixtures used by the run cases
	mkdir -p "$WORK/fix"
	printf 'Hello, World!\n' > "$WORK/fix/hello.txt"
	printf '' > "$WORK/fix/empty.txt"
	seq 1 200 > "$WORK/fix/lines.txt"
	head -c 10000 /dev/urandom > "$WORK/fix/rand.bin"
	printf 'no trailing newline' > "$WORK/fix/nonl.txt"
	dd if=/dev/zero bs=1 count=100 2>/dev/null > "$WORK/fix/zeros.bin"
}

# run_diff <label> <expected_file> <cmd...>
#   Runs cmd, diffs its stdout against expected_file.
FAILED=0
run_diff()
{
	label="$1"; expected="$2"; shift 2
	"$@" > "$WORK/got.txt" 2>/dev/null
	if ! cmp -s "$WORK/got.txt" "$expected"; then
		echo "case failed: $label"
		FAILED=1
	fi
}
