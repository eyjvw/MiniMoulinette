# MiniMoulinette

Testeur parallèle pour les exercices de la Piscine C 42. Pour chaque exercice,
il compile un `main` de test avec le fichier de l'étudiant (`cc -Wall -Wextra
-Werror`), exécute le binaire et compare la sortie standard à la sortie
attendue. Les modules de build (Makefile, scripts) sont validés par un
`check.sh` dédié.

## Installation rapide (sans Rust)

```sh
curl -fsSL https://raw.githubusercontent.com/eyjvw/MiniMoulinette/main/install.sh | sh
```

Télécharge le binaire précompilé (Linux x86_64/arm64, macOS Intel/Apple
Silicon) + les suites de tests dans `~/.mini-moulinette`, et crée la commande
`mini-moulinette` dans `~/.local/bin`. Seul `cc` est requis pour lancer les
tests. S'il n'existe pas de binaire pour la plateforme, le script recompile
avec cargo si disponible.

```sh
cd ~/piscine/C07        # dossier contenant ex00/, ex01/, ...
mini-moulinette C07
```

## Build depuis les sources

### Prérequis

- `cc` (gcc/clang)
- Rust + Cargo (`curl https://sh.rustup.rs -sSf | sh`)

### Build

```sh
cargo build --release
```

Le binaire est produit dans `target/release/MiniMoulinette`.

## Lancer

```sh
# tester un module dans le dossier courant
./target/release/MiniMoulinette C07

# forme explicite avec dossier étudiant + mode strict
./target/release/MiniMoulinette run C07 --path sandbox/C07 --strict
```

- `--path <dir>` : dossier contenant les rendus (`exNN/ft_xxx.c`). Défaut : `.`
- `--strict` : arrête la notation dès qu'un exercice échoue.

Exemple contre les solutions de référence :

```sh
./target/release/MiniMoulinette run C08 --path sandbox/C08
```

## Couverture

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

## Régénérer les tests

Les cas de test (`tests/<module>/<ex>/test_*.c` + `.out`) sont produits par :

```sh
python3 gen_moulinette.py
```

Chaque `.out` est capturé en compilant le test contre la solution de référence
de `sandbox/`, donc la sortie attendue reflète une implémentation correcte.

## Modes de test

- **Diff stdout** (défaut) : `test_*.c` + `.out` dans le dossier de l'exercice ;
  `files.txt` liste le(s) fichier(s) à rendre (plusieurs lignes possibles).
- **Build-check** : si le dossier de test contient `check.sh`, le harness
  l'exécute (`bash check.sh <dir_étudiant>`, timeout 30 s) et note sur son code
  de sortie. Utilisé pour C09 ex00 (script) et ex01 (Makefile).

Timeout d'exécution par test : 5 s (anti-boucle infinie).
