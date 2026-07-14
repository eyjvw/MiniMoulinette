#!/bin/sh
# Build-check for C09/ex00 (libft_creator.sh).
# $1 = student exercise directory (must contain libft_creator.sh).
# Provides the reference srcs, runs the student script, then links a test
# main against the produced libft.a and diffs its output. Exit 0 = pass.

STUDENT="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
FIX="$HERE/fixtures"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [ ! -f "$STUDENT/libft_creator.sh" ]; then
	echo "libft_creator.sh not found"
	exit 1
fi

cp "$FIX"/ft_putchar.c "$FIX"/ft_swap.c "$FIX"/ft_putstr.c \
   "$FIX"/ft_strlen.c "$FIX"/ft_strcmp.c "$FIX"/ft.h "$WORK"/
cp "$STUDENT/libft_creator.sh" "$WORK"/
cd "$WORK" || exit 1

if ! sh libft_creator.sh >/dev/null 2>&1; then
	echo "libft_creator.sh exited non-zero"
	exit 1
fi
if [ ! -f libft.a ]; then
	echo "libft.a was not created"
	exit 1
fi
if ! cc -Wall -Wextra -Werror "$FIX/main.c" -I. -L. -lft -o prog 2>/dev/null; then
	echo "linking a program against libft.a failed"
	exit 1
fi
./prog > out.txt 2>/dev/null
if diff -q out.txt "$FIX/expected.txt" >/dev/null 2>&1; then
	echo "libft_creator.sh builds a working libft.a"
	exit 0
fi
echo "program output differs from expected"
exit 1
