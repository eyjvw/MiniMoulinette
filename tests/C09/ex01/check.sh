#!/bin/sh
# Build-check for C09/ex01 (Makefile).
# $1 = student exercise directory (must contain Makefile).
# Provides srcs/ + includes/, runs `make`, checks libft.a is produced at the
# root, links a test main against it and diffs its output. Also checks the
# clean/fclean/re rules exist. Exit 0 = pass.

STUDENT="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"
FIX="$HERE/fixtures"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

if [ ! -f "$STUDENT/Makefile" ]; then
	echo "Makefile not found"
	exit 1
fi

mkdir -p "$WORK/srcs" "$WORK/includes"
cp "$FIX"/ft_putchar.c "$FIX"/ft_swap.c "$FIX"/ft_putstr.c \
   "$FIX"/ft_strlen.c "$FIX"/ft_strcmp.c "$WORK/srcs/"
cp "$FIX/ft.h" "$WORK/includes/"
cp "$STUDENT/Makefile" "$WORK/"
cd "$WORK" || exit 1

if ! make >/dev/null 2>&1; then
	echo "make failed"
	exit 1
fi
if [ ! -f libft.a ]; then
	echo "libft.a was not created at the root"
	exit 1
fi
if ! cc -Wall -Wextra -Werror "$FIX/main.c" -Iincludes -L. -lft -o prog 2>/dev/null; then
	echo "linking a program against libft.a failed"
	exit 1
fi
./prog > out.txt 2>/dev/null
if ! diff -q out.txt "$FIX/expected.txt" >/dev/null 2>&1; then
	echo "program output differs from expected"
	exit 1
fi
# rules must exist
if ! make fclean >/dev/null 2>&1; then
	echo "fclean rule missing or failed"
	exit 1
fi
if [ -f libft.a ]; then
	echo "fclean did not remove libft.a"
	exit 1
fi
if ! make re >/dev/null 2>&1 || [ ! -f libft.a ]; then
	echo "re rule missing or failed"
	exit 1
fi
echo "Makefile builds a working libft.a (all/clean/fclean/re OK)"
exit 0
