# MiniMoulinette

**[English](#english)** · **[Français](#français)**

---

## English

Parallel test runner for the 42 C Piscine exercises. For each exercise it
compiles a test `main` together with the student's file (`cc -Wall -Wextra
-Werror`), runs the binary and diffs standard output against the expected
output. Build-oriented modules (Makefile, scripts) are graded by a dedicated
`check.sh`.

### Quick install (no Rust needed)

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

### Auto-update

The installed binary checks the latest GitHub release at most once a day.
When a newer version exists it asks (oh-my-zsh style) before doing anything:

```
⟳ v0.4.0 available (current v0.3.0). Update now? [Y/n]
```

`y`/Enter updates then re-runs your command; `n` just continues. Without a
terminal (scripts, CI) it only prints a notice.

- `mini-moulinette update` — update now, no questions
- `MINI_MOULINETTE_NO_UPDATE=1` — disable the automatic check
- Dev builds (run from `target/release/`) are never auto-updated.

### Uninstall

```sh
mini-moulinette uninstall
```

or without the binary:

```sh
curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/uninstall.sh | sh
```

Removes `~/.mini-moulinette`, the command, and the PATH lines the installer
added to `~/.zshrc` / `~/.bashrc`. Nothing else.

### Building from source

Requirements: `cc` (gcc/clang), Rust + Cargo (`curl https://sh.rustup.rs -sSf | sh`).

```sh
cargo build --release
```

The binary is produced at `target/release/MiniMoulinette`.

### Usage

```sh
# grade a module in the current directory
mini-moulinette C07

# explicit form with a student directory + strict mode
mini-moulinette run C07 --path sandbox/C07 --strict
```

- `--path <dir>`: directory containing the submissions (`exNN/ft_xxx.c`).
  Default: `.`
- `--strict`: stop grading as soon as one exercise fails.

### Coverage

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

### Regenerating the tests

The test cases (`tests/<module>/<ex>/test_*.c` + `.out`) are produced by:

```sh
python3 gen_moulinette.py
```

Each `.out` is captured by compiling the test against the reference solution
in `sandbox/`, so the expected output reflects a correct implementation.

### Test modes

- **Stdout diff** (default): `test_*.c` + `.out` in the exercise directory;
  `files.txt` lists the file(s) to submit (several lines allowed).
- **Build-check**: if the test directory contains `check.sh`, the harness runs
  it (`bash check.sh <student_dir>`, 30 s timeout) and grades on its exit
  code. Used for C09 ex00 (script), ex01 (Makefile), all of C10, and C11 ex05
  (do-op).

Per-test execution timeout: 5 s (infinite-loop guard).

### Cheating checks

- **Forbidden functions**: each student `.c` is compiled to an object and its
  undefined symbols (`nm`) are compared against the subject's authorized
  functions (`allowed.txt` in the test dir). Any other external call fails
  the exercise — like the real moulinette's -42. `_`-prefixed runtime symbols
  and compiler-generated `memset`/`memcpy`/`memmove` are tolerated.
- **Extra files**: any file in the turn-in directory that is not required by
  the subject triggers a warning (the real moulinette grades 0 for this).

### Error trace

Console output only shows the first errors, truncated. When at least one test
fails, the full details (complete compiler errors, full expected/got outputs,
the source of each failing test main, full `check.sh` output) are written to a
trace file — its path is printed at the end of the run:

```
📄 Full error trace: /tmp/mini-moulinette-C11-7ea75552.trace
```

---

## Français

Testeur parallèle pour les exercices de la Piscine C 42. Pour chaque exercice,
il compile un `main` de test avec le fichier de l'étudiant (`cc -Wall -Wextra
-Werror`), exécute le binaire et compare la sortie standard à la sortie
attendue. Les modules de build (Makefile, scripts) sont validés par un
`check.sh` dédié.

### Installation rapide (sans Rust)

```sh
curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/install.sh | sh
```

Télécharge le binaire précompilé (Linux x86_64/arm64, macOS Intel/Apple
Silicon) + les suites de tests dans `~/.mini-moulinette`, crée la commande
`mini-moulinette` dans `~/.local/bin` et ajoute ce dossier au `PATH` dans
`~/.zshrc` / `~/.bashrc` si nécessaire. Seul `cc` est requis pour lancer les
tests. S'il n'existe pas de binaire pour la plateforme, le script recompile
avec cargo si disponible.

```sh
cd ~/piscine/C07        # dossier contenant ex00/, ex01/, ...
mini-moulinette C07
```

### Mise à jour automatique

Le binaire installé vérifie la dernière release GitHub au plus une fois par
jour. Si une version plus récente existe, il demande d'abord (style
oh-my-zsh) :

```
⟳ v0.4.0 available (current v0.3.0). Update now? [Y/n]
```

`y`/Entrée met à jour puis relance ta commande ; `n` continue simplement.
Sans terminal (scripts, CI), simple notification, pas de blocage.

- `mini-moulinette update` — mettre à jour tout de suite, sans question
- `MINI_MOULINETTE_NO_UPDATE=1` — désactiver la vérification automatique
- Les builds de dev (lancés depuis `target/release/`) ne sont jamais mis à jour.

### Désinstaller

```sh
mini-moulinette uninstall
```

ou sans le binaire :

```sh
curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/uninstall.sh | sh
```

Supprime `~/.mini-moulinette`, la commande, et les lignes PATH ajoutées par
l'installeur dans `~/.zshrc` / `~/.bashrc`. Rien d'autre.

### Build depuis les sources

Prérequis : `cc` (gcc/clang), Rust + Cargo (`curl https://sh.rustup.rs -sSf | sh`).

```sh
cargo build --release
```

Le binaire est produit dans `target/release/MiniMoulinette`.

### Lancer

```sh
# tester un module dans le dossier courant
mini-moulinette C07

# forme explicite avec dossier étudiant + mode strict
mini-moulinette run C07 --path sandbox/C07 --strict
```

- `--path <dir>` : dossier contenant les rendus (`exNN/ft_xxx.c`). Défaut : `.`
- `--strict` : arrête la notation dès qu'un exercice échoue.

### Couverture

| Module | Contenu | Testé |
|--------|---------|-------|
| C00–C05, C07 | fonctions | ✅ diff stdout |
| C08 | headers / macros / structs | ✅ (`.h` via `-I`) |
| C09 | ft_split + libft_creator.sh + Makefile | ✅ (dont build-check) |
| C10 | programmes (ft_display_file, ft_cat, ft_tail, ft_hexdump) | ✅ build-check, diff vs `cat`/`tail`/`hexdump` système |
| C11 | pointeurs de fonction + do-op | ✅ (do-op via build-check) |
| C12 | listes chaînées (`ft_list.h` étudiant via `-I`) | ✅ |
| C13 | arbres binaires (`ft_btree.h` étudiant via `-I`) | ✅ |
| C06 | arguments (main étudiant) | ⚠️ non testé |

Note C12/C13 : compilés avec gcc ≥ 15 (C23 par défaut), les prototypes
historiques `int (*cmp)()` du sujet ne compilent plus — les tests utilisent
`int (*cmp)(void *, void *)`. Le rendu étudiant doit faire pareil.

`sandbox/` contient une solution de référence par exercice (sert à générer les
`.out` et à vérifier l'absence de crash).

### Régénérer les tests

Les cas de test (`tests/<module>/<ex>/test_*.c` + `.out`) sont produits par :

```sh
python3 gen_moulinette.py
```

Chaque `.out` est capturé en compilant le test contre la solution de référence
de `sandbox/`, donc la sortie attendue reflète une implémentation correcte.

### Modes de test

- **Diff stdout** (défaut) : `test_*.c` + `.out` dans le dossier de l'exercice ;
  `files.txt` liste le(s) fichier(s) à rendre (plusieurs lignes possibles).
- **Build-check** : si le dossier de test contient `check.sh`, le harness
  l'exécute (`bash check.sh <dir_étudiant>`, timeout 30 s) et note sur son code
  de sortie. Utilisé pour C09 ex00 (script), ex01 (Makefile), tout C10 et
  C11 ex05 (do-op).

Timeout d'exécution par test : 5 s (anti-boucle infinie).

### Checks anti-triche

- **Fonctions interdites** : chaque `.c` du rendu est compilé en objet et ses
  symboles indéfinis (`nm`) sont comparés aux fonctions autorisées du sujet
  (`allowed.txt` dans le dossier de test). Tout autre appel externe fait
  échouer l'exercice — comme le -42 de la vraie moulinette. Les symboles
  runtime préfixés `_` et les `memset`/`memcpy`/`memmove` générés par le
  compilateur sont tolérés.
- **Fichiers en trop** : tout fichier du rendu non demandé par le sujet
  déclenche un warning (la vraie moulinette met 0 pour ça).

### Trace d'erreurs

La console n'affiche que les premières erreurs, tronquées. Dès qu'un test
échoue, le détail complet (erreurs de compilation entières, sorties
attendues/obtenues complètes, source du main de test qui échoue, sortie
complète des `check.sh`) est écrit dans un fichier de trace — son chemin
s'affiche en fin de run :

```
📄 Full error trace: /tmp/mini-moulinette-C11-7ea75552.trace
```
