# MiniMoulinette

🇫🇷 [Version française](README.fr.md)

Parallel test runner for the 42 C Piscine exercises. For each exercise it
compiles a test `main` together with the student's file (`cc -Wall -Wextra
-Werror`), runs the binary and diffs standard output against the expected
output. Build-oriented modules (Makefile, scripts) are graded by a dedicated
`check.sh`.

## Quick install (no Rust needed)

```sh
curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/install.sh | sh
```

Downloads the prebuilt binary (Linux x86_64/arm64, macOS Intel/Apple Silicon)
plus the test suites into `~/.mini-moulinette`, creates the `mini-moulinette`
command in `~/.local/bin` and adds that directory to your `PATH` in
`~/.zshrc` / `~/.bashrc` if needed. Only `cc` is required to run the tests.
If no prebuilt binary exists for your platform, the script falls back to a
cargo build when available.

```sh
cd ~/piscine/C07        # directory containing ex00/, ex01/, ...
mini-moulinette C07
```

## Building from source

### Requirements

- `cc` (gcc/clang)
- Rust + Cargo (`curl https://sh.rustup.rs -sSf | sh`)

### Build

```sh
cargo build --release
```

The binary is produced at `target/release/MiniMoulinette`.

## Usage

```sh
# grade a module in the current directory
./target/release/MiniMoulinette C07

# explicit form with a student directory + strict mode
./target/release/MiniMoulinette run C07 --path sandbox/C07 --strict
```

- `--path <dir>`: directory containing the submissions (`exNN/ft_xxx.c`).
  Default: `.`
- `--strict`: stop grading as soon as one exercise fails.

Example against the reference solutions:

```sh
./target/release/MiniMoulinette run C08 --path sandbox/C08
```

## Coverage

| Module | Content | Tested |
|--------|---------|--------|
| C00–C05, C07 | functions | ✅ stdout diff |
| C08 | headers / macros / structs | ✅ (`.h` via `-I`) |
| C09 | ft_split + libft_creator.sh + Makefile | ✅ (incl. build-check) |
| C10 | programs (ft_display_file, ft_cat, ft_tail, ft_hexdump) | ✅ build-check, diff vs system `cat`/`tail`/`hexdump` |
| C11 | function pointers + do-op | ✅ (do-op via build-check) |
| C12 | linked lists (student `ft_list.h` via `-I`) | ✅ |
| C13 | binary trees (student `ft_btree.h` via `-I`) | ✅ |
| C06 | program arguments (student main) | ⚠️ not tested |

C12/C13 note: with gcc ≥ 15 (C23 by default) the subject's historical
`int (*cmp)()` prototypes no longer compile — the tests use
`int (*cmp)(void *, void *)`. Student submissions must do the same.

`sandbox/` holds one reference solution per exercise (used to generate the
`.out` files and to check for crashes).

## Regenerating the tests

The test cases (`tests/<module>/<ex>/test_*.c` + `.out`) are produced by:

```sh
python3 gen_moulinette.py
```

Each `.out` is captured by compiling the test against the reference solution
in `sandbox/`, so the expected output reflects a correct implementation.

## Test modes

- **Stdout diff** (default): `test_*.c` + `.out` in the exercise directory;
  `files.txt` lists the file(s) to submit (several lines allowed).
- **Build-check**: if the test directory contains `check.sh`, the harness runs
  it (`bash check.sh <student_dir>`, 30 s timeout) and grades on its exit
  code. Used for C09 ex00 (script), ex01 (Makefile), all of C10, and C11 ex05
  (do-op).

Per-test execution timeout: 5 s (infinite-loop guard).
