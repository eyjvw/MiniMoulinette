
"""Generate mini-moulinette test cases for the gap exercises (C00-C13).

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


def t_putchar():
    chars = ['A', 'z', '0', '!', ' ', '~', '\n', '\t', '@', '9']
    tests = []
    for c in chars:
        lit = "'\\n'" if c == '\n' else "'\\t'" if c == '\t' else "'%s'" % c
        tests.append(
            "#include <unistd.h>\nvoid ft_putchar(char c);\n"
            "int main(void){ft_putchar(%s);return 0;}\n" % lit)
    return tests


def t_args(cases):
    """Build test mains for the C06 programs.

    The rendu owns main(), so it is renamed to ft_student_main via
    -Dmain=ft_student_main (see CFLAGS) and called here with a handmade argv.
    The test file undefines the macro so its own main() stays main().

    argv entries are char[] rather than string literals: the real argv is
    writable, and a rendu that sorts by swapping contents would segfault on
    read-only literals.
    """
    tests = []
    for av in cases:
        decls = "".join('\tchar a%d[] = %s;\n' % (i, cstr(s))
                        for i, s in enumerate(av))
        names = ", ".join("a%d" % i for i in range(len(av)))
        tests.append(
            "#undef main\n"
            "int ft_student_main(int argc, char **argv);\n"
            "\n"
            "int main(void)\n"
            "{\n"
            "%s"
            "\tchar *av[] = {%s, 0};\n"
            "\n"
            "\treturn ft_student_main(%d, av);\n"
            "}\n" % (decls, names, len(av)))
    return tests


def t_print_program_name():
    return t_args([
        ["./a.out"],
        ["/usr/bin/ft_print_program_name"],
        ["ft_print_program_name"],
        ["a"],
        ["./a.out", "ignored", "args"],
        ["../../some/deep/path/prog"],
    ])


ARGV_SHAPES = [
    ["./a.out"],
    ["./a.out", "one"],
    ["./a.out", "test1", "test2", "test3"],
    ["./a.out", ""],
    ["./a.out", "a b c"],
    ["./a.out", "", "x", ""],
    ["./a.out", "tab\there"],
    ["./a.out", "-flag", "--long", "-"],
    ["./a.out", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
]


def t_print_params():
    return t_args(ARGV_SHAPES)


def t_rev_params():
    return t_args(ARGV_SHAPES)


def t_sort_params():
    return t_args([
        ["./a.out"],
        ["./a.out", "z"],
        ["./a.out", "c", "a", "b"],
        ["./a.out", "B", "a", "A", "b"],
        ["./a.out", "ab", "a"],
        ["./a.out", "same", "same", "same"],
        ["./a.out", "", "a", ""],
        ["./a.out", "10", "9", "1"],
        ["./a.out", "Zebra", "apple", "Apple", "zebra"],
        ["./a.out", "~", "!", "0", "Z", "_", "a"],
        ["./a.out", "abc", "abd", "abb"],
    ])


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


def t_strcpy():
    srcs = ["", "a", "hello", "42 school piscine", "exact fit here!",
            "with\ttab and  spaces", "x" * 60]
    out = []
    for s in srcs:
        cap = len(s) + 1
        out.append(
            "#include <stdio.h>\nchar *ft_strcpy(char *dest, char *src);\n"
            "int main(void){char dest[%d]; char src[] = %s;"
            "for (int k = 0; k < %d; k++) dest[k] = 'X';"
            "char *r = ft_strcpy(dest, src);"
            "printf(\"ret=%%d term=%%d [%%s]\", r == dest, dest[%d] == 0, dest);"
            "return 0;}\n" % (cap, cstr(s), cap, len(s)))
    return out


def t_strncpy():
    cases = [("hello", 3), ("hello", 5), ("hi", 6), ("", 4), ("abc", 0),
             ("world!", 6), ("pad me", 12), ("x", 1)]
    out = []
    for s, n in cases:
        cap = max(n, 1) + 1
        out.append(
            "#include <stdio.h>\nchar *ft_strncpy(char *dest, char *src, unsigned int n);\n"
            "int main(void){char dest[%d]; char src[] = %s;"
            "for (int k = 0; k < %d; k++) dest[k] = 'X';"
            "char *r = ft_strncpy(dest, src, %d);"
            "printf(\"ret=%%d bytes=\", r == dest);"
            "for (int k = 0; k < %d; k++) printf(\"%%02x \", (unsigned char)dest[k]);"
            "return 0;}\n" % (cap, cstr(s), cap, n, cap))
    return out


def _sign_cmp_main(proto, call):
    return ("#include <stdio.h>\n" + proto + "\n"
            "int main(void){int r = " + call + ";"
            "printf(\"%d\", (r > 0) - (r < 0));return 0;}\n")


def t_strcmp():
    cases = [("", ""), ("a", ""), ("", "a"), ("abc", "abc"), ("abc", "abd"),
             ("abd", "abc"), ("abc", "abcd"), ("abcd", "abc"), ("A", "a"),
             ("hello world", "hello_world"), ("42", "42"), ("a", "b")]
    out = []
    for a, b in cases:
        out.append(_sign_cmp_main(
            "int ft_strcmp(char *s1, char *s2);",
            "ft_strcmp(%s, %s)" % (cstr(a), cstr(b))))
    return out


def t_strncmp():
    cases = [("", "", 5), ("abc", "abc", 3), ("abc", "abd", 2), ("abc", "abd", 3),
             ("abd", "abc", 10), ("abc", "abcd", 4), ("abc", "abcd", 3),
             ("hello", "help", 0), ("A", "a", 1), ("same", "same", 100),
             ("cut", "cup", 2), ("cut", "cup", 3)]
    out = []
    for a, b, n in cases:
        out.append(_sign_cmp_main(
            "int ft_strncmp(char *s1, char *s2, unsigned int n);",
            "ft_strncmp(%s, %s, %d)" % (cstr(a), cstr(b), n)))
    return out


def t_strcat():
    cases = [("Hello ", "World"), ("", "x"), ("abc", ""), ("", ""),
             ("42", " school"), ("a", "b"), ("prefix-", "suffix end")]
    out = []
    for d, s in cases:
        cap = len(d) + len(s) + 1
        out.append(
            "#include <stdio.h>\nchar *ft_strcat(char *dest, char *src);\n"
            "int main(void){char dest[%d] = %s; char src[] = %s;"
            "char *r = ft_strcat(dest, src);"
            "printf(\"ret=%%d term=%%d [%%s]\", r == dest, dest[%d] == 0, dest);"
            "return 0;}\n" % (cap, cstr(d), cstr(s), len(d) + len(s)))
    return out


def t_strlcat():

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
             ("full copy here", 40, 15),

             ("Hello World", 6, 6), ("tight", 6, 6), ("cutme", 3, 3)]
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
             ("A", 20, "BCDEFG", 6),

             ("Hello ", 12, "World", 5), ("ab", 5, "cdX", 2), ("", 4, "abc", 3),
             ("tight", 6, "x", 0)]
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


def t_ft_h():


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


def t_foreach():
    arrays = [[1, 2, 3], [42], [], [-1, 0, 1, 2147483647, -2147483648],
              [5, 5, 5, 5], [9, -9, 8, -8, 7]]
    out = []
    for arr in arrays:
        n = len(arr)
        init = "{%s}" % ", ".join(map(str, arr)) if arr else "{0}"
        out.append(
            "#include <stdio.h>\n"
            "void ft_foreach(int *tab, int length, void (*f)(int));\n"
            "static void pr(int n){printf(\"%%d \", n);}\n"
            "int main(void){int tab[] = %s; ft_foreach(tab, %d, pr);"
            "printf(\"$\");return 0;}\n" % (init, n))
    return out


def t_map():
    fns = {
        "dbl": "static int dbl(int n){return n * 2;}",
        "neg": "static int neg(int n){return -n;}",
        "inc": "static int inc(int n){return n + 1;}",
    }
    cases = [([1, 2, 3], "dbl"), ([], "dbl"), ([42], "neg"),
             ([-5, 0, 5], "neg"), ([0, 99, -99, 7], "inc"),
             ([2147483646, -2147483647], "inc")]
    out = []
    for arr, fk in cases:
        n = len(arr)
        init = "{%s}" % ", ".join(map(str, arr)) if arr else "{0}"
        out.append(
            "#include <stdio.h>\n#include <stdlib.h>\n"
            "int *ft_map(int *tab, int length, int (*f)(int));\n"
            "%s\n"
            "int main(void){int tab[] = %s; int *r = ft_map(tab, %d, %s);"
            "if (!r && %d > 0){printf(\"NULL\");return 0;}"
            "for (int i = 0; i < %d; i++) printf(\"%%d \", r[i]);"
            "printf(\"$\");return 0;}\n" % (fns[fk], init, n, fk, n, n))
    return out


PRED_FNS = (
    "int has_a(char *s);\nint longer3(char *s);\nint is_empty(char *s);\n"
    "int has_a(char *s){while (*s){if (*s == 'a') return 1; s++;}return 0;}\n"
    "int longer3(char *s){int i = 0; while (s[i]) i++; return i > 3;}\n"
    "int is_empty(char *s){return s[0] == '\\0';}\n")


def t_any():
    cases = [
        (["rick", "morty"], "has_a"),
        (["xyz", "uvw"], "has_a"),
        ([], "has_a"),
        (["ab", "cd", "efgh"], "longer3"),
        (["ab", "cd"], "longer3"),
        (["x", "", "y"], "is_empty"),
        (["x", "y"], "is_empty"),
    ]
    out = []
    for arr, fk in cases:
        elems = "".join("%s, " % cstr(s) for s in arr) + "0"
        out.append(
            "#include <stdio.h>\n"
            "int ft_any(char **tab, int (*f)(char *));\n" + PRED_FNS +
            "int main(void){char *tab[] = {%s};"
            "printf(\"%%d\", ft_any(tab, %s));return 0;}\n" % (elems, fk))
    return out


def t_count_if():
    cases = [
        (["rick", "morty", "summer"], "has_a"),
        (["xyz", "uvw"], "has_a"),
        ([], "has_a"),
        (["ab", "cdef", "ghijk", "l"], "longer3"),
        (["", "", "x"], "is_empty"),
        (["aaa", "bab", "abb", "bbb"], "has_a"),
    ]
    out = []
    for arr, fk in cases:
        elems = "".join("%s, " % cstr(s) for s in arr) + "0"
        out.append(
            "#include <stdio.h>\n"
            "int ft_count_if(char **tab, int length, int (*f)(char *));\n" + PRED_FNS +
            "int main(void){char *tab[] = {%s};"
            "printf(\"%%d\", ft_count_if(tab, %d, %s));return 0;}\n"
            % (elems, len(arr), fk))
    return out


def t_is_sort():


    arrays = [
        ([1, 2, 3, 4], None), ([1, 3, 2], None), ([], None), ([42], None),
        ([1, 1, 2, 2, 3], None), ([5, 4, 6], None), ([0, 0, 0], None),
        ([-3, -1, 0, 7], None), ([2, 1], None), ([1, 2, 3, 2], None),
    ]
    out = []
    for arr, _ in arrays:
        n = len(arr)
        init = "{%s}" % ", ".join(map(str, arr)) if arr else "{0}"
        out.append(
            "#include <stdio.h>\n"
            "int ft_is_sort(int *tab, int length, int (*f)(int, int));\n"
            "static int cmp_asc(int a, int b){return a - b;}\n"
            "int main(void){int tab[] = %s;"
            "printf(\"%%d\", ft_is_sort(tab, %d, cmp_asc));return 0;}\n" % (init, n))
    return out


def _tab_lit(strs):
    return "".join("%s, " % cstr(s) for s in strs) + "0"


def t_sort_string_tab():
    arrays = [
        ["banana", "apple", "cherry"],
        ["b", "a"],
        ["single"],
        ["zz", "z", "zzz", "a"],
        ["Rick", "Morty", "Summer", "Beth", "Jerry"],
        ["same", "same", "other"],
        ["42", "21", "1337", ""],
    ]
    out = []
    for arr in arrays:
        out.append(
            "#include <stdio.h>\n"
            "void ft_sort_string_tab(char **tab);\n"
            "int main(void){char *tab[] = {%s};"
            "ft_sort_string_tab(tab);"
            "for (int i = 0; tab[i]; i++) printf(\"[%%s]\", tab[i]);"
            "return 0;}\n" % _tab_lit(arr))
    return out


def t_advanced_sort_string_tab():
    cmps = {
        "cmp_std": ("static int cmp_std(char *a, char *b){int i = 0;"
                    "while (a[i] && a[i] == b[i]) i++;"
                    "return (unsigned char)a[i] - (unsigned char)b[i];}"),
        "cmp_rev": ("static int cmp_rev(char *a, char *b){int i = 0;"
                    "while (a[i] && a[i] == b[i]) i++;"
                    "return (unsigned char)b[i] - (unsigned char)a[i];}"),
        "cmp_len": ("static int slen2(char *s){int i = 0; while (s[i]) i++; return i;}\n"
                    "static int cmp_len(char *a, char *b){return slen2(a) - slen2(b);}"),
    }
    cases = [
        (["banana", "apple", "cherry"], "cmp_std"),
        (["banana", "apple", "cherry"], "cmp_rev"),
        (["aaaa", "a", "aa", "aaa"], "cmp_len"),
        (["single"], "cmp_std"),
        (["x", "x", "y"], "cmp_std"),
        (["Rick", "Morty", "Summer", "Beth"], "cmp_rev"),
    ]
    out = []
    for arr, ck in cases:
        out.append(
            "#include <stdio.h>\n"
            "void ft_advanced_sort_string_tab(char **tab, int (*cmp)(char *, char *));\n"
            "%s\n"
            "int main(void){char *tab[] = {%s};"
            "ft_advanced_sort_string_tab(tab, %s);"
            "for (int i = 0; tab[i]; i++) printf(\"[%%s]\", tab[i]);"
            "return 0;}\n" % (cmps[ck], _tab_lit(arr), ck))
    return out


L_PRE = ('#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n'
         '#include "ft_list.h"\n')
L_MK = ("t_list *mk(void *data, t_list *next);\n"
        "t_list *mk(void *data, t_list *next)"
        "{t_list *n = malloc(sizeof(t_list)); n->data = data; n->next = next;"
        " return n;}\n")
L_PLIST = ("static void plist(t_list *l)"
           "{while (l){printf(\"[%s]\", (char *)l->data); l = l->next;}"
           " printf(\"$\");}\n")
L_CREATE = ("t_list *ft_create_elem(void *data)"
            "{t_list *e = malloc(sizeof(t_list)); if (!e) return NULL;"
            " e->data = data; e->next = NULL; return e;}\n")
L_CMPS = "static int cmps(void *a, void *b){return strcmp(a, b);}\n"


def clist(strs):
    expr = "NULL"
    for s in reversed(strs):
        expr = "mk(%s, %s)" % (cstr(s), expr)
    return expr


def t_create_elem():
    strs = ["hello", "", "42"]
    out = []
    for s in strs:
        out.append(
            L_PRE +
            "int main(void){t_list *e = ft_create_elem((void *)%s);"
            "if (!e){printf(\"NULL\");return 0;}"
            "printf(\"[%%s]next=%%d\", (char *)e->data, e->next == NULL);"
            "return 0;}\n" % cstr(s))
    out.append(
        L_PRE +
        "int main(void){t_list *e = ft_create_elem(NULL);"
        "if (!e){printf(\"NULL\");return 0;}"
        "printf(\"data=%d next=%d\", e->data == NULL, e->next == NULL);"
        "return 0;}\n")
    return out


def t_list_push_front():
    cases = [["a"], ["a", "b", "c"], ["x", "y", "z", "w", "v"]]
    out = []
    for strs in cases:
        pushes = "".join(
            "ft_list_push_front(&l, (void *)%s);" % cstr(s) for s in strs)
        out.append(
            L_PRE + L_PLIST + L_CREATE +
            "void ft_list_push_front(t_list **begin_list, void *data);\n"
            "int main(void){t_list *l = NULL;%s plist(l);return 0;}\n" % pushes)
    return out


def t_list_size():
    cases = [[], ["a"], ["a", "b", "c"], ["1", "2", "3", "4", "5", "6", "7"]]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK +
            "int ft_list_size(t_list *begin_list);\n"
            "int main(void){t_list *l = %s;"
            "printf(\"%%d\", ft_list_size(l));return 0;}\n" % clist(strs))
    return out


def t_list_last():
    cases = [[], ["only"], ["a", "b", "c"], ["x", "y"]]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK +
            "t_list *ft_list_last(t_list *begin_list);\n"
            "int main(void){t_list *l = %s;"
            "t_list *r = ft_list_last(l);"
            "if (!r) printf(\"NULL\");"
            "else printf(\"[%%s]\", (char *)r->data);return 0;}\n" % clist(strs))
    return out


def t_list_push_back():
    cases = [["a"], ["a", "b", "c"], ["1", "2", "3", "4"]]
    out = []
    for strs in cases:
        pushes = "".join(
            "ft_list_push_back(&l, (void *)%s);" % cstr(s) for s in strs)
        out.append(
            L_PRE + L_PLIST + L_CREATE +
            "void ft_list_push_back(t_list **begin_list, void *data);\n"
            "int main(void){t_list *l = NULL;%s plist(l);return 0;}\n" % pushes)
    return out


def t_list_push_strs():
    cases = [["a", "b", "c"], ["one"], ["x", "y", "z", "w"]]
    out = []
    for strs in cases:
        elems = ", ".join(cstr(s) for s in strs)
        out.append(
            L_PRE + L_PLIST + L_CREATE +
            "t_list *ft_list_push_strs(int size, char **strs);\n"
            "int main(void){char *strs[] = {%s};"
            "t_list *l = ft_list_push_strs(%d, strs);"
            "plist(l);return 0;}\n" % (elems, len(strs)))
    out.append(
        L_PRE + L_PLIST + L_CREATE +
        "t_list *ft_list_push_strs(int size, char **strs);\n"
        "int main(void){t_list *l = ft_list_push_strs(0, NULL);"
        "plist(l);return 0;}\n")
    return out


def t_list_clear():
    cases = [["a", "b", "c"], ["only"], []]
    out = []
    for strs in cases:
        build = "t_list *l = NULL;" + "".join(
            "l = mk(strdup(%s), l);" % cstr(s) for s in reversed(strs))
        out.append(
            L_PRE + L_MK +
            "void ft_list_clear(t_list *begin_list, void (*free_fct)(void *));\n"
            "static void fr(void *d){printf(\"F[%s]\", (char *)d); free(d);}\n"
            "int main(void){" + build +
            "ft_list_clear(l, fr);printf(\"$\");return 0;}\n")
    return out


def t_list_at():
    lst = ["a", "b", "c", "d"]
    out = []
    for nbr in [0, 1, 3, 4, 42]:
        out.append(
            L_PRE + L_MK +
            "t_list *ft_list_at(t_list *begin_list, unsigned int nbr);\n"
            "int main(void){t_list *l = %s;"
            "t_list *r = ft_list_at(l, %d);"
            "if (!r) printf(\"NULL\");"
            "else printf(\"[%%s]\", (char *)r->data);return 0;}\n"
            % (clist(lst), nbr))
    out.append(
        L_PRE + L_MK +
        "t_list *ft_list_at(t_list *begin_list, unsigned int nbr);\n"
        "int main(void){t_list *r = ft_list_at(NULL, 0);"
        "if (!r) printf(\"NULL\");return 0;}\n")
    return out


def t_list_reverse():
    cases = [["a", "b", "c", "d"], ["x"], [], ["1", "2"]]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK + L_PLIST +
            "void ft_list_reverse(t_list **begin_list);\n"
            "int main(void){t_list *l = %s;"
            "ft_list_reverse(&l);plist(l);return 0;}\n" % clist(strs))
    return out


def t_list_foreach():
    cases = [["a", "b", "c"], [], ["solo"]]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK +
            "void ft_list_foreach(t_list *begin_list, void (*f)(void *));\n"
            "static void pr(void *d){printf(\"[%%s]\", (char *)d);}\n"
            "int main(void){t_list *l = %s;"
            "ft_list_foreach(l, pr);printf(\"$\");return 0;}\n" % clist(strs))
    return out


def t_list_foreach_if():
    cases = [
        (["a", "b", "a", "c", "a"], "a"),
        (["x", "y"], "z"),
        (["m", "m"], "m"),
    ]
    out = []
    for strs, ref_s in cases:
        out.append(
            L_PRE + L_MK + L_CMPS +
            "void ft_list_foreach_if(t_list *begin_list, void (*f)(void *),"
            " void *data_ref, int (*cmp)(void *, void *));\n"
            "static void pr(void *d){printf(\"[%%s]\", (char *)d);}\n"
            "int main(void){t_list *l = %s;"
            "ft_list_foreach_if(l, pr, (void *)%s, cmps);"
            "printf(\"$\");return 0;}\n" % (clist(strs), cstr(ref_s)))
    return out


def t_list_find():
    cases = [
        (["a", "b", "c"], "b"),
        (["a", "b", "c"], "z"),
        (["dup", "dup"], "dup"),
        ([], "x"),
    ]
    out = []
    for strs, ref_s in cases:
        out.append(
            L_PRE + L_MK + L_CMPS +
            "t_list *ft_list_find(t_list *begin_list, void *data_ref,"
            " int (*cmp)(void *, void *));\n"
            "int main(void){t_list *l = %s;"
            "t_list *r = ft_list_find(l, (void *)%s, cmps);"
            "if (!r) printf(\"NULL\");"
            "else printf(\"[%%s]next=%%d\", (char *)r->data, r->next == NULL);"
            "return 0;}\n" % (clist(strs), cstr(ref_s)))
    return out


def t_list_remove_if():
    cases = [
        (["a", "b", "a", "c"], "a"),
        (["x", "x", "x"], "x"),
        (["k", "l", "m"], "z"),
        (["del", "keep"], "del"),
        (["keep", "del"], "del"),
    ]
    out = []
    for strs, ref_s in cases:
        build = "t_list *l = NULL;" + "".join(
            "l = mk(strdup(%s), l);" % cstr(s) for s in reversed(strs))
        out.append(
            L_PRE + L_MK + L_PLIST + L_CMPS +
            "void ft_list_remove_if(t_list **begin_list, void *data_ref,"
            " int (*cmp)(void *, void *), void (*free_fct)(void *));\n"
            "int main(void){" + build +
            "ft_list_remove_if(&l, (void *)%s, cmps, free);"
            "plist(l);return 0;}\n" % cstr(ref_s))
    return out


def t_list_merge():
    cases = [
        (["a", "b"], ["c", "d"]),
        ([], ["x", "y"]),
        (["x", "y"], []),
        (["solo"], ["other"]),
    ]
    out = []
    for l1, l2 in cases:
        out.append(
            L_PRE + L_MK + L_PLIST +
            "void ft_list_merge(t_list **begin_list1, t_list *begin_list2);\n"
            "int main(void){t_list *l1 = %s; t_list *l2 = %s;"
            "ft_list_merge(&l1, l2);plist(l1);return 0;}\n"
            % (clist(l1), clist(l2)))
    return out


def t_list_sort():
    cases = [
        ["banana", "apple", "cherry"],
        ["d", "c", "b", "a"],
        ["same", "same", "aaa"],
        ["solo"],
        [],
        ["10", "1", "2", "20", "3"],
    ]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK + L_PLIST + L_CMPS +
            "void ft_list_sort(t_list **begin_list, int (*cmp)(void *, void *));\n"
            "int main(void){t_list *l = %s;"
            "ft_list_sort(&l, cmps);plist(l);return 0;}\n" % clist(strs))
    return out


def t_list_reverse_fun():
    cases = [["a", "b", "c", "d"], ["x"], [], ["1", "2", "3"]]
    out = []
    for strs in cases:
        out.append(
            L_PRE + L_MK + L_PLIST +
            "void ft_list_reverse_fun(t_list *begin_list);\n"
            "int main(void){t_list *l = %s;"
            "ft_list_reverse_fun(l);plist(l);return 0;}\n" % clist(strs))
    return out


def t_sorted_list_insert():
    cases = [
        ([], "m"),
        (["b", "d"], "a"),
        (["b", "d"], "c"),
        (["b", "d"], "z"),
        (["b", "b"], "b"),
    ]
    out = []
    for strs, ins in cases:
        out.append(
            L_PRE + L_MK + L_PLIST + L_CMPS + L_CREATE +
            "void ft_sorted_list_insert(t_list **begin_list, void *data,"
            " int (*cmp)(void *, void *));\n"
            "int main(void){t_list *l = %s;"
            "ft_sorted_list_insert(&l, (void *)%s, cmps);"
            "plist(l);return 0;}\n" % (clist(strs), cstr(ins)))
    return out


def t_sorted_list_merge():
    cases = [
        (["a", "c", "e"], ["b", "d", "f"]),
        ([], ["a", "b"]),
        (["a", "b"], []),
        (["b"], ["a", "c"]),
        (["a", "a"], ["a"]),
    ]
    out = []
    for l1, l2 in cases:
        out.append(
            L_PRE + L_MK + L_PLIST + L_CMPS +
            "void ft_sorted_list_merge(t_list **begin_list1, t_list *begin_list2,"
            " int (*cmp)(void *, void *));\n"
            "int main(void){t_list *l1 = %s; t_list *l2 = %s;"
            "ft_sorted_list_merge(&l1, l2, cmps);plist(l1);return 0;}\n"
            % (clist(l1), clist(l2)))
    return out


B_PRE = ('#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n'
         '#include "ft_btree.h"\n')
B_ND = ("static t_btree *nd(void *item, t_btree *left, t_btree *right)"
        "{t_btree *n = malloc(sizeof(t_btree)); n->item = item;"
        " n->left = left; n->right = right; return n;}\n")
B_PV = "static void pv(void *item){printf(\"[%s]\", (char *)item);}\n"
B_CREATE = ("t_btree *btree_create_node(void *item)"
            "{t_btree *n = malloc(sizeof(t_btree)); if (!n) return NULL;"
            " n->item = item; n->left = NULL; n->right = NULL; return n;}\n")
B_CMPS = "static int cmps(void *a, void *b){return strcmp(a, b);}\n"


TREE_BALANCED = ("d", ("b", ("a", None, None), ("c", None, None)),
                 ("f", ("e", None, None), ("g", None, None)))
TREE_LEFT = ("c", ("b", ("a", None, None), None), None)
TREE_RIGHT = ("a", None, ("b", None, ("c", None, None)))
TREE_ONE = ("solo", None, None)
TREES = [TREE_BALANCED, TREE_LEFT, TREE_RIGHT, TREE_ONE]


def ctree(t):
    if t is None:
        return "NULL"
    return "nd(%s, %s, %s)" % (cstr(t[0]), ctree(t[1]), ctree(t[2]))


def t_btree_create_node():
    out = []
    for s in ["root", "", "42"]:
        out.append(
            B_PRE +
            "int main(void){t_btree *n = btree_create_node((void *)%s);"
            "if (!n){printf(\"NULL\");return 0;}"
            "printf(\"[%%s]l=%%d r=%%d\", (char *)n->item,"
            " n->left == NULL, n->right == NULL);return 0;}\n" % cstr(s))
    return out


def t_btree_apply(name):
    out = []
    for t in TREES:
        out.append(
            B_PRE + B_ND + B_PV +
            "void %s(t_btree *root, void (*applyf)(void *));\n"
            "int main(void){t_btree *r = %s;"
            "%s(r, pv);printf(\"$\");return 0;}\n" % (name, ctree(t), name))
    return out


def t_btree_insert_data():
    cases = [
        ["d", "b", "f", "a", "c", "e", "g"],
        ["a", "b", "c"],
        ["c", "b", "a"],
        ["b", "b", "a"],
        ["solo"],
    ]
    out = []
    for seq in cases:
        inserts = "".join(
            "btree_insert_data(&r, (void *)%s, cmps);" % cstr(s) for s in seq)
        out.append(
            B_PRE + B_CMPS + B_CREATE +
            "void btree_insert_data(t_btree **root, void *item,"
            " int (*cmpf)(void *, void *));\n"
            "static void show(t_btree *r){if (!r) return; show(r->left);"
            "printf(\"[%%s]\", (char *)r->item); show(r->right);}\n"
            "int main(void){t_btree *r = NULL;%s show(r);"
            "printf(\"$\");return 0;}\n" % inserts)
    return out


def t_btree_search_item():
    cases = [
        (TREE_BALANCED, "e"),
        (TREE_BALANCED, "zz"),
        (TREE_LEFT, "a"),
        (TREE_ONE, "solo"),
        (TREE_ONE, "nope"),
    ]
    out = []
    for t, ref_s in cases:
        out.append(
            B_PRE + B_ND + B_CMPS +
            "void *btree_search_item(t_btree *root, void *data_ref,"
            " int (*cmpf)(void *, void *));\n"
            "int main(void){t_btree *r = %s;"
            "void *f = btree_search_item(r, (void *)%s, cmps);"
            "if (!f) printf(\"NULL\");"
            "else printf(\"[%%s]\", (char *)f);return 0;}\n"
            % (ctree(t), cstr(ref_s)))
    return out


def t_btree_level_count():
    out = []
    for t in TREES:
        out.append(
            B_PRE + B_ND +
            "int btree_level_count(t_btree *root);\n"
            "int main(void){t_btree *r = %s;"
            "printf(\"%%d\", btree_level_count(r));return 0;}\n" % ctree(t))
    return out


def t_btree_apply_by_level():
    out = []
    for t in TREES:
        out.append(
            B_PRE + B_ND +
            "void btree_apply_by_level(t_btree *root,"
            " void (*applyf)(void *item, int current_level, int is_first_elem));\n"
            "static void pl(void *item, int level, int first)"
            "{printf(\"(%%s,%%d,%%d)\", (char *)item, level, first);}\n"
            "int main(void){t_btree *r = %s;"
            "btree_apply_by_level(r, pl);printf(\"$\");return 0;}\n" % ctree(t))
    return out


EXERCISES = [

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

    ("C02", "ex00", ["ft_strcpy.c"], [ref("C02", "ex00", "ft_strcpy.c")], t_strcpy),
    ("C02", "ex01", ["ft_strncpy.c"], [ref("C02", "ex01", "ft_strncpy.c")], t_strncpy),
    ("C02", "ex06", ["ft_str_is_printable.c"], [ref("C02", "ex06", "ft_str_is_printable.c")], t_str_is_printable),
    ("C02", "ex11", ["ft_putstr_non_printable.c"], [ref("C02", "ex11", "ft_putstr_non_printable.c")], t_putstr_non_printable),


    ("C02", "ex09", ["ft_strcapitalize.c"], [ref("C02", "ex09", "ft_strcapitalize.c")], t_strcapitalize),
    ("C02", "ex10", ["ft_strlcpy.c"], [ref("C02", "ex10", "ft_strlcpy.c")], t_strlcpy),

    ("C03", "ex00", ["ft_strcmp.c"], [ref("C03", "ex00", "ft_strcmp.c")], t_strcmp),
    ("C03", "ex01", ["ft_strncmp.c"], [ref("C03", "ex01", "ft_strncmp.c")], t_strncmp),
    ("C03", "ex02", ["ft_strcat.c"], [ref("C03", "ex02", "ft_strcat.c")], t_strcat),
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

    ("C06", "ex00", ["ft_print_program_name.c"],
     [ref("C06", "ex00", "ft_print_program_name.c")], t_print_program_name),
    ("C06", "ex01", ["ft_print_params.c"],
     [ref("C06", "ex01", "ft_print_params.c")], t_print_params),
    ("C06", "ex02", ["ft_rev_params.c"],
     [ref("C06", "ex02", "ft_rev_params.c")], t_rev_params),
    ("C06", "ex03", ["ft_sort_params.c"],
     [ref("C06", "ex03", "ft_sort_params.c")], t_sort_params),

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


    ("C11", "ex00", ["ft_foreach.c"], [ref("C11", "ex00", "ft_foreach.c")], t_foreach),
    ("C11", "ex01", ["ft_map.c"], [ref("C11", "ex01", "ft_map.c")], t_map),
    ("C11", "ex02", ["ft_any.c"], [ref("C11", "ex02", "ft_any.c")], t_any),
    ("C11", "ex03", ["ft_count_if.c"], [ref("C11", "ex03", "ft_count_if.c")], t_count_if),
    ("C11", "ex04", ["ft_is_sort.c"], [ref("C11", "ex04", "ft_is_sort.c")], t_is_sort),
    ("C11", "ex06", ["ft_sort_string_tab.c"],
     [ref("C11", "ex06", "ft_sort_string_tab.c")], t_sort_string_tab),
    ("C11", "ex07", ["ft_advanced_sort_string_tab.c"],
     [ref("C11", "ex07", "ft_advanced_sort_string_tab.c")], t_advanced_sort_string_tab),

    ("C12", "ex00", ["ft_create_elem.c", "ft_list.h"],
     [ref("C12", "ex00", "ft_create_elem.c"), ref("C12", "ex00", "ft_list.h")], t_create_elem),
    ("C12", "ex01", ["ft_list_push_front.c", "ft_list.h"],
     [ref("C12", "ex01", "ft_list_push_front.c"), ref("C12", "ex01", "ft_list.h")], t_list_push_front),
    ("C12", "ex02", ["ft_list_size.c", "ft_list.h"],
     [ref("C12", "ex02", "ft_list_size.c"), ref("C12", "ex02", "ft_list.h")], t_list_size),
    ("C12", "ex03", ["ft_list_last.c", "ft_list.h"],
     [ref("C12", "ex03", "ft_list_last.c"), ref("C12", "ex03", "ft_list.h")], t_list_last),
    ("C12", "ex04", ["ft_list_push_back.c", "ft_list.h"],
     [ref("C12", "ex04", "ft_list_push_back.c"), ref("C12", "ex04", "ft_list.h")], t_list_push_back),
    ("C12", "ex05", ["ft_list_push_strs.c", "ft_list.h"],
     [ref("C12", "ex05", "ft_list_push_strs.c"), ref("C12", "ex05", "ft_list.h")], t_list_push_strs),
    ("C12", "ex06", ["ft_list_clear.c", "ft_list.h"],
     [ref("C12", "ex06", "ft_list_clear.c"), ref("C12", "ex06", "ft_list.h")], t_list_clear),
    ("C12", "ex07", ["ft_list_at.c", "ft_list.h"],
     [ref("C12", "ex07", "ft_list_at.c"), ref("C12", "ex07", "ft_list.h")], t_list_at),


    ("C12", "ex08", ["ft_list_reverse.c"],
     [ref("C12", "ex08", "ft_list_reverse.c"), ref("C12", "ex08", "ft_list.h")], t_list_reverse),
    ("C12", "ex09", ["ft_list_foreach.c", "ft_list.h"],
     [ref("C12", "ex09", "ft_list_foreach.c"), ref("C12", "ex09", "ft_list.h")], t_list_foreach),
    ("C12", "ex10", ["ft_list_foreach_if.c", "ft_list.h"],
     [ref("C12", "ex10", "ft_list_foreach_if.c"), ref("C12", "ex10", "ft_list.h")], t_list_foreach_if),
    ("C12", "ex11", ["ft_list_find.c", "ft_list.h"],
     [ref("C12", "ex11", "ft_list_find.c"), ref("C12", "ex11", "ft_list.h")], t_list_find),
    ("C12", "ex12", ["ft_list_remove_if.c", "ft_list.h"],
     [ref("C12", "ex12", "ft_list_remove_if.c"), ref("C12", "ex12", "ft_list.h")], t_list_remove_if),
    ("C12", "ex13", ["ft_list_merge.c", "ft_list.h"],
     [ref("C12", "ex13", "ft_list_merge.c"), ref("C12", "ex13", "ft_list.h")], t_list_merge),
    ("C12", "ex14", ["ft_list_sort.c", "ft_list.h"],
     [ref("C12", "ex14", "ft_list_sort.c"), ref("C12", "ex14", "ft_list.h")], t_list_sort),
    ("C12", "ex15", ["ft_list_reverse_fun.c", "ft_list.h"],
     [ref("C12", "ex15", "ft_list_reverse_fun.c"), ref("C12", "ex15", "ft_list.h")], t_list_reverse_fun),
    ("C12", "ex16", ["ft_sorted_list_insert.c", "ft_list.h"],
     [ref("C12", "ex16", "ft_sorted_list_insert.c"), ref("C12", "ex16", "ft_list.h")], t_sorted_list_insert),
    ("C12", "ex17", ["ft_sorted_list_merge.c", "ft_list.h"],
     [ref("C12", "ex17", "ft_sorted_list_merge.c"), ref("C12", "ex17", "ft_list.h")], t_sorted_list_merge),

    ("C13", "ex00", ["btree_create_node.c", "ft_btree.h"],
     [ref("C13", "ex00", "btree_create_node.c"), ref("C13", "ex00", "ft_btree.h")], t_btree_create_node),
    ("C13", "ex01", ["btree_apply_prefix.c", "ft_btree.h"],
     [ref("C13", "ex01", "btree_apply_prefix.c"), ref("C13", "ex01", "ft_btree.h")],
     lambda: t_btree_apply("btree_apply_prefix")),
    ("C13", "ex02", ["btree_apply_infix.c", "ft_btree.h"],
     [ref("C13", "ex02", "btree_apply_infix.c"), ref("C13", "ex02", "ft_btree.h")],
     lambda: t_btree_apply("btree_apply_infix")),
    ("C13", "ex03", ["btree_apply_suffix.c", "ft_btree.h"],
     [ref("C13", "ex03", "btree_apply_suffix.c"), ref("C13", "ex03", "ft_btree.h")],
     lambda: t_btree_apply("btree_apply_suffix")),
    ("C13", "ex04", ["btree_insert_data.c", "ft_btree.h"],
     [ref("C13", "ex04", "btree_insert_data.c"), ref("C13", "ex04", "ft_btree.h")], t_btree_insert_data),
    ("C13", "ex05", ["btree_search_item.c", "ft_btree.h"],
     [ref("C13", "ex05", "btree_search_item.c"), ref("C13", "ex05", "ft_btree.h")], t_btree_search_item),
    ("C13", "ex06", ["btree_level_count.c", "ft_btree.h"],
     [ref("C13", "ex06", "btree_level_count.c"), ref("C13", "ex06", "ft_btree.h")], t_btree_level_count),
    ("C13", "ex07", ["btree_apply_by_level.c", "ft_btree.h"],
     [ref("C13", "ex07", "btree_apply_by_level.c"), ref("C13", "ex07", "ft_btree.h")], t_btree_apply_by_level),
]


AUX_FILES = {
    ("C08", "ex04"): [ref("C08", "ex04", "ft_stock_str.h")],
    ("C08", "ex05"): [ref("C08", "ex05", "ft_stock_str.h")],
    ("C12", "ex08"): [ref("C12", "ex08", "ft_list.h")],
}


CFLAGS = {
    ("C06", "ex00"): ["-Dmain=ft_student_main"],
    ("C06", "ex01"): ["-Dmain=ft_student_main"],
    ("C06", "ex02"): ["-Dmain=ft_student_main"],
    ("C06", "ex03"): ["-Dmain=ft_student_main"],
}


ALLOWED = {
    ("C00", "ex00"): ["write"], ("C00", "ex01"): ["write"],
    ("C00", "ex02"): ["write"], ("C00", "ex03"): ["write"],
    ("C00", "ex04"): ["write"], ("C00", "ex05"): ["write"],
    ("C00", "ex06"): ["write"], ("C00", "ex07"): ["write"],
    ("C00", "ex08"): ["write"],
    ("C01", "ex00"): [], ("C01", "ex01"): [], ("C01", "ex02"): [],
    ("C01", "ex03"): [], ("C01", "ex04"): [],
    ("C01", "ex05"): ["write"],
    ("C01", "ex06"): [], ("C01", "ex07"): [], ("C01", "ex08"): [],
    ("C02", "ex00"): [], ("C02", "ex01"): [], ("C02", "ex02"): [],
    ("C02", "ex03"): [], ("C02", "ex04"): [], ("C02", "ex05"): [],
    ("C02", "ex06"): [], ("C02", "ex07"): [], ("C02", "ex08"): [],
    ("C02", "ex09"): [], ("C02", "ex10"): [],
    ("C02", "ex11"): ["write"],
    ("C03", "ex00"): [], ("C03", "ex01"): [], ("C03", "ex02"): [],
    ("C03", "ex03"): [], ("C03", "ex04"): [], ("C03", "ex05"): [],
    ("C04", "ex00"): [], ("C04", "ex01"): ["write"],
    ("C04", "ex02"): ["write"], ("C04", "ex03"): [],
    ("C04", "ex04"): ["write"], ("C04", "ex05"): [],
    ("C05", "ex00"): [], ("C05", "ex01"): [], ("C05", "ex02"): [],
    ("C05", "ex03"): [], ("C05", "ex04"): [],
    ("C05", "ex05"): [], ("C05", "ex06"): [], ("C05", "ex07"): [],
    ("C05", "ex08"): ["write"],
    ("C06", "ex00"): ["write"], ("C06", "ex01"): ["write"],
    ("C06", "ex02"): ["write"], ("C06", "ex03"): ["write"],
    ("C07", "ex00"): ["malloc"], ("C07", "ex01"): ["malloc"],
    ("C07", "ex02"): ["malloc"], ("C07", "ex03"): ["malloc"],
    ("C07", "ex04"): ["malloc", "free"], ("C07", "ex05"): ["malloc"],
    ("C08", "ex04"): ["malloc", "free"], ("C08", "ex05"): ["write"],
    ("C09", "ex00"): ["write"], ("C09", "ex02"): ["malloc"],
    ("C10", "ex00"): ["close", "open", "read", "write"],
    ("C10", "ex01"): ["close", "open", "read", "write", "strerror", "basename"],
    ("C10", "ex02"): ["close", "open", "read", "write", "malloc", "free",
                      "strerror", "basename"],
    ("C10", "ex03"): ["close", "open", "read", "write", "malloc", "free",
                      "strerror", "basename"],
    ("C11", "ex05"): ["write"],
    ("C11", "ex00"): [], ("C11", "ex01"): ["malloc"],
    ("C11", "ex02"): [], ("C11", "ex03"): [], ("C11", "ex04"): [],
    ("C11", "ex06"): [], ("C11", "ex07"): [],
    ("C12", "ex00"): ["malloc"],
    ("C12", "ex01"): ["ft_create_elem"],
    ("C12", "ex02"): [], ("C12", "ex03"): [],
    ("C12", "ex04"): ["ft_create_elem"],
    ("C12", "ex05"): ["ft_create_elem"],
    ("C12", "ex06"): ["free"],
    ("C12", "ex07"): [], ("C12", "ex08"): [], ("C12", "ex09"): [],
    ("C12", "ex10"): [], ("C12", "ex11"): [],
    ("C12", "ex12"): ["free"],
    ("C12", "ex13"): [], ("C12", "ex14"): [], ("C12", "ex15"): [],
    ("C12", "ex16"): ["ft_create_elem"], ("C12", "ex17"): [],
    ("C13", "ex00"): ["malloc"],
    ("C13", "ex01"): [], ("C13", "ex02"): [], ("C13", "ex03"): [],
    ("C13", "ex04"): ["btree_create_node"],
    ("C13", "ex05"): [], ("C13", "ex06"): [],
    ("C13", "ex07"): ["malloc", "free"],
}


def main():
    fails = 0
    total = 0
    for module, ex, files, refs, builder in EXERCISES:
        out_dir = os.path.join(TESTS, module, ex)

        if os.path.isdir(out_dir):
            for f in os.listdir(out_dir):
                if f.startswith("test_"):
                    os.remove(os.path.join(out_dir, f))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "files.txt"), "w") as f:
            f.write("\n".join(files) + "\n")
        for aux in AUX_FILES.get((module, ex), []):
            shutil.copy(aux, out_dir)
        if (module, ex) in ALLOWED:
            with open(os.path.join(out_dir, "allowed.txt"), "w") as f:
                f.write("\n".join(ALLOWED[(module, ex)]) + "\n")
        cflags = CFLAGS.get((module, ex), [])
        cflags_path = os.path.join(out_dir, "cflags.txt")
        if cflags:
            with open(cflags_path, "w") as f:
                f.write("\n".join(cflags) + "\n")
        elif os.path.exists(cflags_path):
            os.remove(cflags_path)

        tests = builder()
        for i, src in enumerate(tests):
            total += 1
            tname = "test_%03d" % i
            cfile = os.path.join(out_dir, tname + ".c")
            with open(cfile, "w") as f:
                f.write(src)

            with tempfile.TemporaryDirectory() as td:
                binp = os.path.join(td, "b")
                sources = [r for r in refs if r.endswith(".c")]
                inc_dirs = sorted({os.path.dirname(r) for r in refs})
                inc_args = []
                for d in inc_dirs:
                    inc_args += ["-I", d]
                comp = subprocess.run(CC + [cfile] + sources + cflags + inc_args + ["-o", binp],
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


    for (module, ex), fns in ALLOWED.items():
        d = os.path.join(TESTS, module, ex)
        if os.path.isdir(d):
            with open(os.path.join(d, "allowed.txt"), "w") as f:
                f.write("\n".join(fns) + "\n")

    print("\nTOTAL: %d tests, %d failures" % (total, fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
