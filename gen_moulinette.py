#!/usr/bin/env python3
"""Generate mini-moulinette test cases for the gap exercises (C00-C07, C06 skipped).

For each test: write test_NNN.c (a main that exercises the function and prints a
stable, comparable result), compile it together with the reference solution(s)
from sandbox/, run it, and capture stdout as test_NNN.out.

The reference solutions are trusted; the .out therefore reflects a correct impl.
"""
import os
import subprocess
import tempfile
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(ROOT, "tests")
SANDBOX = os.path.join(ROOT, "sandbox")

CC = ["cc", "-Wall", "-Wextra", "-Werror"]


def ref(*parts):
    return os.path.join(SANDBOX, *parts)


# ---------------------------------------------------------------------------
# helpers to build C test mains
# ---------------------------------------------------------------------------

def cstr(s):
    """Escape a python string into a C string literal body.

    A \\xHH escape is greedy in C, so if a real hex digit follows it we close and
    reopen the literal ("...\\x7f" "ed...") to keep the escape at two digits.
    """
    HEXD = "0123456789abcdefABCDEF"
    out = []
    prev_hex_escape = False
    for ch in s:
        if prev_hex_escape and ch in HEXD:
            out.append('" "')
        prev_hex_escape = False
        if ch == "\\":
            out.append("\\\\")
        elif ch == '"':
            out.append('\\"')
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        elif 32 <= ord(ch) < 127:
            out.append(ch)
        else:
            out.append("\\x%02x" % ord(ch))
            prev_hex_escape = True
    return '"' + "".join(out) + '"'


# ---------------------------------------------------------------------------
# per-exercise test generators -> list of C source strings
# ---------------------------------------------------------------------------

def t_putchar():
    chars = ['A', 'z', '0', '!', ' ', '~', '\n', '\t', '@', '9']
    tests = []
    for c in chars:
        lit = "'\\n'" if c == '\n' else "'\\t'" if c == '\t' else "'%s'" % c
        tests.append(
            "#include <unistd.h>\nvoid ft_putchar(char c);\n"
            "int main(void){ft_putchar(%s);return 0;}\n" % lit)
    return tests


def t_void_print(proto_name):
    return ["void %s(void);\nint main(void){%s();return 0;}\n" % (proto_name, proto_name)]


def t_is_negative():
    vals = [-1, 0, 1, -2147483648, 2147483647, -42, 42, 100, -100]
    return ["void ft_is_negative(int n);\n"
            "int main(void){ft_is_negative(%d);return 0;}\n" % v for v in vals]


def t_putnbr():
    vals = [0, 1, -1, 42, -42, 2147483647, -2147483648, 100, -100, 7, -7, 123456, -987654]
    return ["void ft_putnbr(int nb);\n"
            "int main(void){ft_putnbr(%d);return 0;}\n" % v for v in vals]


def t_print_combn():
    return ["void ft_print_combn(int n);\n"
            "int main(void){ft_print_combn(%d);return 0;}\n" % n
            for n in [1, 2, 3, 4, 5, 7, 8, 9]]


def t_str_is_printable():
    strs = ["", "Hello", "Rick and Morty", "abc\n", "tab\there", "\x01\x02",
            "1234567890", "with space", "!@#~", "\x7f", "printable~ ", "line\r"]
    return ["#include <stdio.h>\nint ft_str_is_printable(char *str);\n"
            "int main(void){printf(\"%%d\", ft_str_is_printable(%s));return 0;}\n" % cstr(s)
            for s in strs]


def t_putstr_non_printable():
    strs = ["Hello", "Coucou\ntu vas bien ?", "tab\there", "\x01\x02\x03",
            "mix\x7fed", "normal text", "", "end\n", "\x00hidden", "abc"]
    # note: \x00 truncates a C string, so drop it
    strs = [s for s in strs if "\x00" not in s]
    return ["void ft_putstr_non_printable(char *str);\n"
            "int main(void){char s[] = %s; ft_putstr_non_printable(s);return 0;}\n" % cstr(s)
            for s in strs]


def t_print_memory():
    bufs = [
        "Bonjour les amis, comment allez vous ? Ceci est un long texte de test.",
        "short",
        "1234567890ABCDEF1234567890",
        "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10",
        "Exactly sixteen",
        "Rick and Morty forever, wubba lubba dub dub!",
    ]
    out = []
    for b in bufs:
        out.append(
            "#include <stdlib.h>\nvoid *ft_print_memory(void *addr, unsigned int size);\n"
            "int main(void){char s[] = %s; ft_print_memory(s, sizeof(s) - 1);return 0;}\n" % cstr(b))
    return out


def t_strlcat():
    # (dest_initial, dest_capacity, src, size_arg)
    cases = [
        ("foo", 10, "bar", 10),
        ("Hello ", 20, "World", 20),
        ("", 10, "abc", 10),
        ("full", 5, "xxxx", 5),
        ("abc", 20, "", 20),
        ("dest", 20, "src", 3),
        ("dest", 20, "src", 0),
        ("12345", 20, "6789", 4),
        ("aaa", 8, "bbbbbbbb", 8),
        ("start", 20, "-end", 100),
        ("x", 2, "yyyy", 2),
        ("cat", 20, "dog", 1),
    ]
    out = []
    for dest, cap, src, size in cases:
        out.append(
            "#include <stdio.h>\nunsigned int ft_strlcat(char *dest, char *src, unsigned int size);\n"
            "int main(void){char dest[%d] = %s; unsigned int r = ft_strlcat(dest, %s, %d);"
            "printf(\"r=%%u dest=[%%s]\", r, dest);return 0;}\n"
            % (cap, cstr(dest), cstr(src), size))
    return out


def t_putnbr_base():
    bases = {
        "dec": "0123456789",
        "bin": "01",
        "hex": "0123456789ABCDEF",
        "poneyvif": "poneyvif",
    }
    vals = [0, 42, -42, 255, -255, 2147483647, -2147483648, 16, -1]
    # invalid bases: must print nothing
    invalid = ["", "0", "011", "01+", "0-1", "01 2"]
    out = []
    for v in vals:
        for _, b in bases.items():
            out.append(
                "void ft_putnbr_base(int nbr, char *base);\n"
                "int main(void){ft_putnbr_base(%d, %s);return 0;}\n" % (v, cstr(b)))
    for b in invalid:
        out.append(
            "void ft_putnbr_base(int nbr, char *base);\n"
            "int main(void){ft_putnbr_base(42, %s);return 0;}\n" % cstr(b))
    return out


def t_atoi_base():
    bases = {
        "dec": "0123456789",
        "bin": "01",
        "hex": "0123456789abcdef",
    }
    cases = [
        ("42", "dec"), ("-42", "dec"), ("+42", "dec"), ("   ---+--42", "dec"),
        ("101010", "bin"), ("-101010", "bin"),
        ("ff", "hex"), ("-1a", "hex"), ("7fffffff", "hex"),
        ("0", "dec"), ("2147483647", "dec"), ("-2147483648", "dec"),
        ("  \t\n 123abc", "dec"), ("", "dec"),
    ]
    out = []
    for nbr, bk in cases:
        out.append(
            "#include <stdio.h>\nint ft_atoi_base(char *str, char *base);\n"
            "int main(void){printf(\"%%d\", ft_atoi_base(%s, %s));return 0;}\n"
            % (cstr(nbr), cstr(bases[bk])))
    # invalid base -> convention: ft_atoi_base returns 0
    for b in ["", "0", "011", "01 ", "-01", "+01"]:
        out.append(
            "#include <stdio.h>\nint ft_atoi_base(char *str, char *base);\n"
            "int main(void){printf(\"%%d\", ft_atoi_base(%s, %s));return 0;}\n"
            % (cstr("42"), cstr(b)))
    return out


def t_ten_queens():
    return ["#include <stdio.h>\nint ft_ten_queens_puzzle(void);\n"
            "int main(void){int r = ft_ten_queens_puzzle();printf(\"count=%d\", r);return 0;}\n"]


def t_strcapitalize():
    strs = ["hello world", "SALUT LES AMIS", "42school is COOL",
            "a b c d", "wubba-lubba dub_dub", "1st place, 2nd loser",
            "  leading spaces", "MiXeD cAsE hErE", "", "already Capitalized",
            "rick&morty; season4", "one"]
    return ["#include <stdio.h>\nchar *ft_strcapitalize(char *str);\n"
            "int main(void){char s[] = %s; printf(\"[%%s]\", ft_strcapitalize(s));return 0;}\n"
            % cstr(s) for s in strs]


def t_strlcpy():
    cases = [("Hello World", 20, 6), ("Hello World", 20, 20),
             ("", 10, 5), ("truncated string", 30, 5), ("exact", 20, 6),
             ("overflow", 20, 3), ("42", 10, 100), ("size zero", 20, 1),
             ("full copy here", 40, 15)]
    out = []
    for src, cap, size in cases:
        out.append(
            "#include <stdio.h>\nunsigned int ft_strlcpy(char *dest, char *src, unsigned int size);\n"
            "int main(void){char dest[%d]; for (int k = 0; k < %d; k++) dest[k] = 'X';"
            "unsigned int r = ft_strlcpy(dest, %s, %d);"
            "printf(\"r=%%u dest=[%%s]\", r, dest);return 0;}\n"
            % (cap, cap, cstr(src), size))
    return out


def t_strncat():
    cases = [("Hello ", 20, "World", 5), ("foo", 20, "bar", 10), ("abc", 20, "def", 0),
             ("start", 20, "-end", 2), ("", 20, "full", 4), ("x", 20, "yyyy", 100),
             ("cat", 20, "", 5), ("12345", 20, "6789", 3), ("Rick", 20, "Morty", 3),
             ("A", 20, "BCDEFG", 6)]
    out = []
    for dest, cap, src, nb in cases:
        out.append(
            "#include <stdio.h>\nchar *ft_strncat(char *dest, char *src, unsigned int nb);\n"
            "int main(void){char dest[%d] = %s; char *r = ft_strncat(dest, %s, %d);"
            "printf(\"[%%s]\", r);return 0;}\n" % (cap, cstr(dest), cstr(src), nb))
    return out


def t_strstr():
    cases = [("Hello World", "World"), ("Hello World", "o W"), ("abcdef", "xyz"),
             ("aaa", "aa"), ("find me here", ""), ("", "notempty"),
             ("Rick and Morty", "Morty"), ("mississippi", "issi"),
             ("overlap", "lap"), ("start", "start"), ("abc", "abcd"), ("42school", "school")]
    out = []
    for s, tf in cases:
        out.append(
            "#include <stdio.h>\nchar *ft_strstr(char *str, char *to_find);\n"
            "int main(void){char s[] = %s; char *r = ft_strstr(s, %s);"
            "if (!r) printf(\"NULL\"); else printf(\"[%%s]\", r);return 0;}\n"
            % (cstr(s), cstr(tf)))
    return out


def t_putstr():
    strs = ["Hello, World!", "", "42", "wubba lubba dub dub",
            "line with\ttab", "multi\nline", "special !@#$%^&*()", "single"]
    return ["void ft_putstr(char *str);\n"
            "int main(void){char s[] = %s; ft_putstr(s);return 0;}\n" % cstr(s)
            for s in strs]


def t_atoi():
    strs = ["42", "-42", "+42", "   123", "\t\n 456", "0", "2147483647",
            "-2147483648", "  -+-42", "123abc", "abc123", "", "  +", "0042",
            "-0", "   -7  8"]
    return ["#include <stdio.h>\nint ft_atoi(char *str);\n"
            "int main(void){char s[] = %s; printf(\"%%d\", ft_atoi(s));return 0;}\n" % cstr(s)
            for s in strs]


def t_is_prime():
    vals = [0, 1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 17, 25, 97, 100, 101,
            -5, -1, 7919, 7920, 2147483647, 104729, 104730]
    return ["#include <stdio.h>\nint ft_is_prime(int nb);\n"
            "int main(void){printf(\"%%d\", ft_is_prime(%d));return 0;}\n" % v for v in vals]


def t_find_next_prime():
    vals = [0, 1, 2, 3, 4, 5, 6, 10, 14, 20, 24, 97, 98, 100, -5, 7919, 7920, 104728]
    return ["#include <stdio.h>\nint ft_find_next_prime(int nb);\n"
            "int main(void){printf(\"%%d\", ft_find_next_prime(%d));return 0;}\n" % v for v in vals]


def t_sqrt():
    vals = [0, 1, 2, 3, 4, 8, 9, 15, 16, 24, 25, 36, 49, 63, 64, 100, 144,
            169, 200, 256, 1000, 1024, 2147395600, 2147483647, -4, -1]
    return ["#include <stdio.h>\nint ft_sqrt(int nb);\n"
            "int main(void){printf(\"%%d\", ft_sqrt(%d));return 0;}\n" % v for v in vals]


# ---- C07 ----

def t_strdup():
    strs = ["", "a", "Rick", "Hello, World!", "42 is the answer",
            "wubba lubba dub dub", "  spaces  ", "tab\tnewline\n", "1234567890", "!@#$%^&*()"]
    return ["#include <stdio.h>\nchar *ft_strdup(char *src);\n"
            "int main(void){char s[] = %s; char *d = ft_strdup(s);"
            "printf(\"[%%s]\", d);return 0;}\n" % cstr(s) for s in strs]


def t_range():
    cases = [(0, 5), (-3, 3), (5, 5), (6, 2), (0, 1), (-2147483648, -2147483645),
             (10, 20), (-5, 0), (100, 100), (-1, 1), (42, 47), (0, 10)]
    out = []
    for mn, mx in cases:
        out.append(
            "#include <stdio.h>\nint *ft_range(int min, int max);\n"
            "int main(void){int *r = ft_range(%d, %d);"
            "if (!r){printf(\"NULL\");return 0;}"
            "for (int i = 0; i < %d - %d; i++) printf(\"%%d \", r[i]);return 0;}\n"
            % (mn, mx, mx, mn))
    return out


def t_ultimate_range():
    cases = [(0, 5), (-3, 3), (5, 5), (6, 2), (0, 1), (-5, 0),
             (10, 15), (100, 100), (-1, 1), (7, 12), (0, 10), (-10, -5)]
    out = []
    for mn, mx in cases:
        out.append(
            "#include <stdio.h>\nint ft_ultimate_range(int **range, int min, int max);\n"
            "int main(void){int *r = (void *)0; int n = ft_ultimate_range(&r, %d, %d);"
            "printf(\"n=%%d:\", n);"
            "if (r) for (int i = 0; i < n; i++) printf(\"%%d \", r[i]);"
            "else printf(\"NULL\");return 0;}\n" % (mn, mx))
    return out


def t_strjoin():
    cases = [
        (["Hello", "World"], "-"),
        (["a", "b", "c", "d"], ", "),
        (["one"], "XXX"),
        ([], "sep"),
        (["", "", ""], "-"),
        (["Rick", "Morty"], ""),
        (["1", "2", "3"], " + "),
        (["wubba", "lubba", "dub", "dub"], " "),
        (["long string here", "another one"], " | "),
        (["x"], ""),
    ]
    out = []
    for strs, sep in cases:
        size = len(strs)
        if size == 0:
            arr = "char **arr = (void *)0;"
        else:
            elems = ", ".join(cstr(s) for s in strs)
            arr = "char *arr[] = {%s};" % elems
        out.append(
            "#include <stdio.h>\nchar *ft_strjoin(int size, char **strs, char *sep);\n"
            "int main(void){%s char *r = ft_strjoin(%d, arr, %s);"
            "printf(\"[%%s]\", r);return 0;}\n" % (arr, size, cstr(sep)))
    return out


def t_convert_base():
    cases = [
        ("42", "0123456789", "01"),
        ("-101010", "01", "0123456789"),
        ("ff", "0123456789abcdef", "0123456789"),
        ("255", "0123456789", "0123456789abcdef"),
        ("  ---+42", "0123456789", "0123456789"),
        ("0", "0123456789", "01"),
        ("-2147483648", "0123456789", "0123456789abcdef"),
        ("2147483647", "0123456789", "01"),
        ("101", "01", "01"),
        ("z", "0123456789abcdefghijklmnopqrstuvwxyz", "0123456789"),
        # invalid bases -> NULL
        ("42", "00", "0123456789"),
        ("42", "0123456789", "0"),
        ("42", "01+", "0123456789"),
        ("42", "0123456789", "01 2"),
        ("42", "", "0123456789"),
    ]
    out = []
    for nbr, bf, bt in cases:
        out.append(
            "#include <stdio.h>\nchar *ft_convert_base(char *nbr, char *base_from, char *base_to);\n"
            "int main(void){char *r = ft_convert_base(%s, %s, %s);"
            "if (!r) printf(\"NULL\"); else printf(\"[%%s]\", r);return 0;}\n"
            % (cstr(nbr), cstr(bf), cstr(bt)))
    return out


def t_split():
    cases = [
        ("hello world foo", " "),
        ("  leading and trailing  ", " "),
        ("a,b,,c,,,d", ","),
        ("one, two, three", ", "),
        ("no-separators-here", "|"),
        ("", " "),
        ("     ", " "),
        ("mix\tof\ndifferent seps", " \t\n"),
        ("Rick;Morty;Summer;Beth", ";"),
        ("aXbYcXdY", "XY"),
        ("split.this.string", "."),
        ("wubba lubba dub dub", " "),
    ]
    out = []
    for s, cs in cases:
        out.append(
            "#include <stdio.h>\nchar **ft_split(char *str, char *charset);\n"
            "int main(void){char s[] = %s; char **r = ft_split(s, %s);"
            "if (!r){printf(\"NULL\");return 0;}"
            "for (int i = 0; r[i]; i++) printf(\"[%%s]\", r[i]);return 0;}\n"
            % (cstr(s), cstr(cs)))
    return out


# ---- C08 (headers / structs) ----

def t_ft_h():
    # Uses all 5 prototypes; impls defined after main so the calls rely on the
    # header's declarations (a missing prototype fails -Werror).
    return ["#include <unistd.h>\n#include \"ft.h\"\n"
            "int main(void){int a = 1; int b = 2; ft_swap(&a, &b);"
            "ft_putchar('0' + a); ft_putchar('0' + b); ft_putchar('\\n');"
            "ft_putstr(\"hi\"); ft_putchar('0' + ft_strlen(\"hello\"));"
            "ft_putchar('0' + (ft_strcmp(\"a\", \"a\") == 0));"
            "ft_putchar('\\n'); return 0;}\n"
            "void ft_putchar(char c){write(1, &c, 1);}\n"
            "void ft_putstr(char *s){while (*s) write(1, s++, 1);}\n"
            "void ft_swap(int *a, int *b){int t = *a; *a = *b; *b = t;}\n"
            "int ft_strlen(char *s){int i = 0; while (s[i]) i++; return i;}\n"
            "int ft_strcmp(char *a, char *b){int i = 0;"
            "while (a[i] && a[i] == b[i]) i++;"
            "return (unsigned char)a[i] - (unsigned char)b[i];}\n"]


def t_ft_boolean():
    # The exact main from the subject; 0 extra args -> even.
    return ["#include \"ft_boolean.h\"\n"
            "void ft_putstr(char *str){while (*str) write(1, str++, 1);}\n"
            "t_bool ft_is_even(int nbr){return (EVEN(nbr)) ? TRUE : FALSE;}\n"
            "int main(int argc, char **argv){(void)argv;"
            "if (ft_is_even(argc - 1) == TRUE) ft_putstr(EVEN_MSG);"
            "else ft_putstr(ODD_MSG); return SUCCESS;}\n"]


def t_ft_abs():
    vals = [0, 5, -5, 42, -42, 2147483647, -2147483647, 1, -1, 100, -100]
    return ["#include <stdio.h>\n#include \"ft_abs.h\"\n"
            "int main(void){printf(\"%%d\", ABS(%d));return 0;}\n" % v for v in vals]


def t_ft_point():
    return ["#include <stdio.h>\n#include \"ft_point.h\"\n"
            "void set_point(t_point *p){p->x = 42; p->y = 21;}\n"
            "int main(void){t_point p; set_point(&p);"
            "printf(\"%d %d\", p.x, p.y);return 0;}\n"]


def t_strs_to_tab():
    # Provide a few argv-like arrays; print each element's fields.
    arrays = [
        ["Rick", "Morty", "Summer"],
        ["one"],
        ["", "nonempty", ""],
        ["42", "school", "piscine", "C08"],
        ["a", "bb", "ccc", "dddd"],
    ]
    out = []
    struct = ("typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;\n"
              "struct s_stock_str *ft_strs_to_tab(int ac, char **av);\n")
    for arr in arrays:
        elems = ", ".join(cstr(s) for s in arr)
        out.append(
            "#include <stdio.h>\n" + struct +
            "int main(void){char *av[] = {%s}; int ac = %d;"
            "t_stock_str *t = ft_strs_to_tab(ac, av);"
            "if (!t){printf(\"NULL\");return 0;}"
            "for (int i = 0; t[i].str; i++)"
            "printf(\"[%%d|%%s|%%s]\", t[i].size, t[i].str, t[i].copy);"
            "return 0;}\n" % (elems, len(arr)))
    return out


def t_show_tab():
    # Build the array manually, call ft_show_tab, capture its stdout.
    arrays = [
        ["Rick", "Morty"],
        ["one", "two", "three"],
        ["single"],
        ["", "x"],
    ]
    out = []
    struct = ("typedef struct s_stock_str{int size;char *str;char *copy;}t_stock_str;\n"
              "void ft_show_tab(struct s_stock_str *par);\n"
              "static int slen(char *s){int i=0;while(s[i])i++;return i;}\n")
    for arr in arrays:
        n = len(arr)
        fill = "".join(
            "t[%d].str = %s; t[%d].copy = %s; t[%d].size = slen(%s);\n"
            % (i, cstr(s), i, cstr(s), i, cstr(s)) for i, s in enumerate(arr))
        out.append(
            struct +
            "int main(void){t_stock_str t[%d];\n%s t[%d].str = 0;"
            "ft_show_tab(t);return 0;}\n" % (n + 1, fill, n))
    return out


# ---------------------------------------------------------------------------
# exercise table
# ---------------------------------------------------------------------------

EXERCISES = [
    # module, ex, student files.txt content (list), ref sources (list), test builder
    ("C00", "ex00", ["ft_putchar.c"], [ref("C00", "ex00", "ft_putchar.c")], t_putchar),
    ("C00", "ex01", ["ft_print_alphabet.c"], [ref("C00", "ex01", "ft_print_alphabet.c")],
     lambda: t_void_print("ft_print_alphabet")),
    ("C00", "ex02", ["ft_print_reverse_alphabet.c"], [ref("C00", "ex02", "ft_print_reverse_alphabet.c")],
     lambda: t_void_print("ft_print_reverse_alphabet")),
    ("C00", "ex03", ["ft_print_numbers.c"], [ref("C00", "ex03", "ft_print_numbers.c")],
     lambda: t_void_print("ft_print_numbers")),
    ("C00", "ex04", ["ft_is_negative.c"], [ref("C00", "ex04", "ft_is_negative.c")], t_is_negative),
    ("C00", "ex05", ["ft_print_comb.c"], [ref("C00", "ex05", "ft_print_comb.c")],
     lambda: t_void_print("ft_print_comb")),
    ("C00", "ex06", ["ft_print_comb2.c"], [ref("C00", "ex06", "ft_print_comb2.c")],
     lambda: t_void_print("ft_print_comb2")),
    ("C00", "ex07", ["ft_putnbr.c"], [ref("C00", "ex07", "ft_putnbr.c")], t_putnbr),
    ("C00", "ex08", ["ft_print_combn.c"], [ref("C00", "ex08", "ft_print_combn.c")], t_print_combn),

    ("C02", "ex06", ["ft_str_is_printable.c"], [ref("C02", "ex06", "ft_str_is_printable.c")], t_str_is_printable),
    ("C02", "ex11", ["ft_putstr_non_printable.c"], [ref("C02", "ex11", "ft_putstr_non_printable.c")], t_putstr_non_printable),
    # C02/ex12 ft_print_memory: prints the real runtime memory address -> output is
    # non-deterministic and cannot be validated by exact stdout diff. Skipped.
    # ("C02", "ex12", ["ft_print_memory.c"], [ref("C02", "ex12", "ft_print_memory.c")], t_print_memory),

    ("C02", "ex09", ["ft_strcapitalize.c"], [ref("C02", "ex09", "ft_strcapitalize.c")], t_strcapitalize),
    ("C02", "ex10", ["ft_strlcpy.c"], [ref("C02", "ex10", "ft_strlcpy.c")], t_strlcpy),

    ("C03", "ex03", ["ft_strncat.c"], [ref("C03", "ex03", "ft_strncat.c")], t_strncat),
    ("C03", "ex04", ["ft_strstr.c"], [ref("C03", "ex04", "ft_strstr.c")], t_strstr),
    ("C03", "ex05", ["ft_strlcat.c"], [ref("C03", "ex05", "ft_strlcat.c")], t_strlcat),

    ("C04", "ex01", ["ft_putstr.c"], [ref("C04", "ex01", "ft_putstr.c")], t_putstr),
    ("C04", "ex03", ["ft_atoi.c"], [ref("C04", "ex03", "ft_atoi.c")], t_atoi),
    ("C04", "ex04", ["ft_putnbr_base.c"], [ref("C04", "ex04", "ft_putnbr_base.c")], t_putnbr_base),
    ("C04", "ex05", ["ft_atoi_base.c"], [ref("C04", "ex05", "ft_atoi_base.c")], t_atoi_base),

    ("C05", "ex05", ["ft_sqrt.c"], [ref("C05", "ex05", "ft_sqrt.c")], t_sqrt),
    ("C05", "ex06", ["ft_is_prime.c"], [ref("C05", "ex06", "ft_is_prime.c")], t_is_prime),
    ("C05", "ex07", ["ft_find_next_prime.c"], [ref("C05", "ex07", "ft_find_next_prime.c")], t_find_next_prime),
    ("C05", "ex08", ["ft_ten_queens_puzzle.c"], [ref("C05", "ex08", "ft_ten_queens_puzzle.c")], t_ten_queens),

    ("C07", "ex00", ["ft_strdup.c"], [ref("C07", "ex00", "ft_strdup.c")], t_strdup),
    ("C07", "ex01", ["ft_range.c"], [ref("C07", "ex01", "ft_range.c")], t_range),
    ("C07", "ex02", ["ft_ultimate_range.c"], [ref("C07", "ex02", "ft_ultimate_range.c")], t_ultimate_range),
    ("C07", "ex03", ["ft_strjoin.c"], [ref("C07", "ex03", "ft_strjoin.c")], t_strjoin),
    ("C07", "ex04", ["ft_convert_base.c", "ft_convert_base2.c"],
     [ref("C07", "ex04", "ft_convert_base.c"), ref("C07", "ex04", "ft_convert_base2.c")], t_convert_base),
    ("C07", "ex05", ["ft_split.c"], [ref("C07", "ex05", "ft_split.c")], t_split),

    ("C08", "ex00", ["ft.h"], [ref("C08", "ex00", "ft.h")], t_ft_h),
    ("C08", "ex01", ["ft_boolean.h"], [ref("C08", "ex01", "ft_boolean.h")], t_ft_boolean),
    ("C08", "ex02", ["ft_abs.h"], [ref("C08", "ex02", "ft_abs.h")], t_ft_abs),
    ("C08", "ex03", ["ft_point.h"], [ref("C08", "ex03", "ft_point.h")], t_ft_point),
    ("C08", "ex04", ["ft_strs_to_tab.c"],
     [ref("C08", "ex04", "ft_strs_to_tab.c")], t_strs_to_tab),
    ("C08", "ex05", ["ft_show_tab.c"], [ref("C08", "ex05", "ft_show_tab.c")], t_show_tab),

    ("C09", "ex02", ["ft_split.c"], [ref("C09", "ex02", "ft_split.c")], t_split),
]


def main():
    fails = 0
    total = 0
    for module, ex, files, refs, builder in EXERCISES:
        out_dir = os.path.join(TESTS, module, ex)
        # wipe existing test_* to regenerate cleanly
        if os.path.isdir(out_dir):
            for f in os.listdir(out_dir):
                if f.startswith("test_"):
                    os.remove(os.path.join(out_dir, f))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "files.txt"), "w") as f:
            f.write("\n".join(files) + "\n")

        tests = builder()
        for i, src in enumerate(tests):
            total += 1
            tname = "test_%03d" % i
            cfile = os.path.join(out_dir, tname + ".c")
            with open(cfile, "w") as f:
                f.write(src)
            # compile test + refs -> run -> capture stdout
            with tempfile.TemporaryDirectory() as td:
                binp = os.path.join(td, "b")
                sources = [r for r in refs if r.endswith(".c")]
                inc_dirs = sorted({os.path.dirname(r) for r in refs})
                inc_args = []
                for d in inc_dirs:
                    inc_args += ["-I", d]
                comp = subprocess.run(CC + [cfile] + sources + inc_args + ["-o", binp],
                                      capture_output=True, text=True)
                if comp.returncode != 0:
                    print("COMPILE FAIL %s/%s %s\n%s" % (module, ex, tname, comp.stderr))
                    fails += 1
                    os.remove(cfile)
                    continue
                run = subprocess.run([binp], capture_output=True, timeout=15)
                if run.returncode < 0:
                    print("CRASH %s/%s %s signal=%d" % (module, ex, tname, -run.returncode))
                    fails += 1
                    os.remove(cfile)
                    continue
                with open(os.path.join(out_dir, tname + ".out"), "wb") as f:
                    f.write(run.stdout)
        print("  %s/%s : %d tests (%s)" % (module, ex, len(tests), ", ".join(files)))

    print("\nTOTAL: %d tests, %d failures" % (total, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
