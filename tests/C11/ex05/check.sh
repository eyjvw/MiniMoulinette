#!/bin/sh
# Build-check for C11/ex05 (do-op).
# $1 = student exercise directory. Builds with make if a Makefile is present,
# otherwise compiles every .c file. Then compares stdout for the subject cases.
STUDENT="$1"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

mkdir -p "$WORK/src"
cp -r "$STUDENT"/. "$WORK/src/"
cd "$WORK/src" || exit 1

if [ -f Makefile ]; then
	if ! make >/dev/null 2>&1; then
		echo "make failed"
		exit 1
	fi
else
	if ! cc -Wall -Wextra -Werror ./*.c -o do-op 2>/dev/null; then
		echo "compilation of *.c failed"
		exit 1
	fi
fi
if [ ! -x ./do-op ]; then
	echo "binary do-op was not created"
	exit 1
fi

FAILED=0
# expect <expected_stdout> [args...]
expect()
{
	exp="$1"; shift
	got="$(./do-op "$@" 2>/dev/null)"
	if [ "$got" != "$exp" ]; then
		echo "case failed: do-op $* -> [$got], expected [$exp]"
		FAILED=1
	fi
}

expect ""
expect "2" 1 + 1
expect "62" 42amis - --+-20toto12
expect "0" 1 p 1
expect "1" 1 + toto3
expect "4" toto3 + 4
expect "0" foo plus bar
expect "Stop : division by zero" 25 / 0
expect "Stop : modulo by zero" 25 % 0
expect "882" 42 "*" 21
expect "2" 42 / 21
expect "0" 42 % 21
expect "-63" -42 - 21
expect "21" " +42" - "  21"
expect "" 1 +
expect "" 1 + 2 3

if [ "$FAILED" -eq 0 ]; then
	echo "do-op behaves correctly"
	exit 0
fi
exit 1
