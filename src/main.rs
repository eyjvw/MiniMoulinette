use anyhow::Result;
use clap::{Parser, Subcommand};
use colored::*;
use console::{pad_str, Alignment};
use rayon::prelude::*;
use std::fs;
use std::path::PathBuf;
use std::process::Command;
use std::os::unix::process::ExitStatusExt;
use std::sync::atomic::{AtomicUsize, Ordering};
use indicatif::{ProgressBar, ProgressStyle};

const REPO: &str = "eyjvw/MiniMoulinette";

#[derive(Parser, Debug)]
#[command(name = "mini-moulinette",
          disable_help_flag = true,
          disable_help_subcommand = true,
          disable_version_flag = true)]
struct Cli {
    #[arg(name = "ASSIGNMENT")]
    assignment: Option<String>,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand, Debug)]
enum Commands {
    #[command(disable_help_flag = true)]
    Run {
        #[arg(name = "ASSIGNMENT")]
        assignment: String,
        #[arg(short, long, default_value = ".")]
        path: PathBuf,
        #[arg(short, long)]
        strict: bool,
    },
    #[command(disable_help_flag = true)]
    Update,
    #[command(disable_help_flag = true)]
    Version,
    #[command(disable_help_flag = true)]
    Help,
}

fn print_help() {
    let v = env!("CARGO_PKG_VERSION");
    println!();
    println!("{}", "╭────────────────────────────────────────────────────────────╮".cyan().bold());
    let title = format!("MiniMoulinette v{}", v);
    println!("{} {} {}", "│".cyan().bold(),
        pad_str(&title, 58, Alignment::Center, None).bold(), "│".cyan().bold());
    let sub = "Testeur local pour la Piscine C (C00 → C13)";
    println!("{} {} {}", "│".cyan().bold(),
        pad_str(sub, 58, Alignment::Center, None), "│".cyan().bold());
    println!("{}", "╰────────────────────────────────────────────────────────────╯".cyan().bold());
    println!();
    let entry = |cmd: &str, w: usize, desc: &str| {
        println!("  {}  {}", pad_str(cmd, w, Alignment::Left, None).bold(), desc.dimmed());
    };
    println!("{}", "USAGE".bold().yellow());
    entry("mini-moulinette <MODULE>", 40, "note le module dans le dossier courant");
    entry("mini-moulinette run <MODULE> [options]", 40, "forme explicite");
    println!();
    println!("{}", "COMMANDES".bold().yellow());
    entry("run <MODULE>", 18, "note un module (ex : C07)");
    entry("update", 18, "met à jour vers la dernière version");
    entry("version", 18, "affiche la version installée");
    entry("help", 18, "affiche cette aide");
    println!();
    println!("{}", "OPTIONS (run)".bold().yellow());
    entry("-p, --path <dir>", 18, "dossier du rendu (défaut : dossier courant)");
    entry("-s, --strict", 18, "s'arrête au premier exercice raté");
    println!();
    println!("{}", "EXEMPLES".bold().yellow());
    println!("  {}", "cd ~/piscine/C07 && mini-moulinette C07".dimmed());
    println!("  {}", "mini-moulinette run C07 --path ~/rendu/C07 --strict".dimmed());
    println!();
    println!("{}", "ENV".bold().yellow());
    println!("  {}   désactive la vérification de mise à jour", "MINI_MOULINETTE_NO_UPDATE=1".bold());
    println!();
}

fn main() -> Result<()> {
    // -h/--help/-V/--version are disabled in clap (the subcommands replace
    // them); catch them here so they show the custom help instead of an error
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if raw.iter().any(|a| a == "-h" || a == "--help") {
        print_help();
        return Ok(());
    }
    if raw.iter().any(|a| a == "-V" || a == "--version") {
        println!("mini-moulinette {}", env!("CARGO_PKG_VERSION"));
        return Ok(());
    }

    let cli = Cli::parse();
    match &cli.command {
        Some(Commands::Run { assignment, path, strict }) => {
            maybe_auto_update();
            run_assignment(assignment, path, *strict)?
        }
        Some(Commands::Update) => run_update(true)?,
        Some(Commands::Version) => println!("mini-moulinette {}", env!("CARGO_PKG_VERSION")),
        Some(Commands::Help) => print_help(),
        None => {
            if let Some(assignment) = &cli.assignment {
                maybe_auto_update();
                run_assignment(assignment, &PathBuf::from("."), false)?;
            } else {
                print_help();
            }
        }
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// self-update
// ---------------------------------------------------------------------------

/// The install root (~/.mini-moulinette) if this binary was installed there
/// by install.sh. Dev builds (target/release/...) are never auto-updated.
fn install_root() -> Option<PathBuf> {
    let home = std::env::var("HOME").ok()?;
    let root = PathBuf::from(home).join(".mini-moulinette");
    let exe = std::env::current_exe().ok()?.canonicalize().ok()?;
    if exe.starts_with(root.canonicalize().ok()?) {
        Some(root)
    } else {
        None
    }
}

/// Latest release tag, resolved from the /releases/latest redirect (no API
/// rate limit, no JSON). Returns e.g. "0.2.0".
fn latest_version() -> Option<String> {
    let out = Command::new("curl")
        .args(["-fsSLI", "--retry", "2", "--retry-all-errors",
               "-o", "/dev/null", "-w", "%{url_effective}", "--max-time", "8",
               &format!("https://github.com/{}/releases/latest", REPO)])
        .output()
        .ok()?;
    if !out.status.success() {
        return None;
    }
    let url = String::from_utf8_lossy(&out.stdout);
    let tag = url.trim().rsplit('/').next()?.trim_start_matches('v').to_string();
    if tag.is_empty() || tag == "latest" { None } else { Some(tag) }
}

fn parse_semver(v: &str) -> (u64, u64, u64) {
    let mut it = v.split('.').map(|p| p.trim().parse::<u64>().unwrap_or(0));
    (it.next().unwrap_or(0), it.next().unwrap_or(0), it.next().unwrap_or(0))
}

/// Re-run the installer. `verbose` prints its output (manual `update`);
/// otherwise it runs quietly (auto-update path).
fn run_update(verbose: bool) -> Result<()> {
    let cmd = format!(
        "curl -fsSL https://raw.githubusercontent.com/{}/main/install.sh | sh", REPO);
    let status = if verbose {
        Command::new("sh").arg("-c").arg(&cmd).status()?
    } else {
        Command::new("sh").arg("-c").arg(&cmd)
            .stdout(std::process::Stdio::null())
            .stderr(std::process::Stdio::null())
            .status()?
    };
    if !status.success() {
        anyhow::bail!("update failed (installer exited with an error)");
    }
    Ok(())
}

/// Once a day, compare the running version to the latest release. If newer,
/// reinstall and re-exec the fresh binary with the same arguments.
/// Opt-out: MINI_MOULINETTE_NO_UPDATE=1. Dev builds are skipped.
fn maybe_auto_update() {
    if std::env::var("MINI_MOULINETTE_NO_UPDATE").is_ok() {
        return;
    }
    let Some(root) = install_root() else { return };

    // throttle: at most one remote check per 24h
    let stamp = root.join(".last_update_check");
    if let Ok(meta) = fs::metadata(&stamp) {
        if let Ok(modified) = meta.modified() {
            if let Ok(age) = modified.elapsed() {
                if age.as_secs() < 24 * 3600 {
                    return;
                }
            }
        }
    }
    let _ = fs::write(&stamp, "");

    let Some(latest) = latest_version() else { return };
    let current = env!("CARGO_PKG_VERSION");
    if parse_semver(&latest) <= parse_semver(current) {
        return;
    }

    // oh-my-zsh style: ask, don't force. Without a tty (scripts, CI) just
    // print a notice and keep going.
    use std::io::{IsTerminal, Write};
    if !std::io::stdin().is_terminal() {
        println!("{} v{} available (current v{}) — run {} to upgrade\n",
            "⟳".cyan().bold(), latest, current, "mini-moulinette update".bold());
        return;
    }
    print!("{} v{} available (current v{}). Update now? [Y/n] ",
        "⟳".cyan().bold(), latest, current);
    let _ = std::io::stdout().flush();
    let mut answer = String::new();
    let _ = std::io::stdin().read_line(&mut answer);
    let answer = answer.trim().to_lowercase();
    if !(answer.is_empty() || answer == "y" || answer == "yes" || answer == "o" || answer == "oui") {
        println!("{} skipped — run {} whenever you want\n",
            "▸".dimmed(), "mini-moulinette update".bold());
        return;
    }

    println!("{} updating to v{}...", "⟳".cyan().bold(), latest);
    if run_update(false).is_err() {
        println!("{} update failed, run {} manually\n",
            "⚠".yellow(), "mini-moulinette update".bold());
        return;
    }
    println!("{} updated to v{}\n", "✓".green().bold(), latest);

    // re-exec the freshly installed binary with the original arguments
    let exe = root.join("mini-moulinette");
    use std::os::unix::process::CommandExt;
    let args: Vec<String> = std::env::args().skip(1).collect();
    let _ = Command::new(exe)
        .args(args)
        .env("MINI_MOULINETTE_NO_UPDATE", "1")
        .exec();
    // exec only returns on failure; grading continues on the old version
}

/// Locate the bundled test suites. Priority: ./tests (working from a clone),
/// then $MINI_MOULINETTE_DIR/tests, then ~/.mini-moulinette/tests (curl install).
fn find_tests_root() -> PathBuf {
    let local = PathBuf::from("tests");
    if local.is_dir() {
        return local;
    }
    if let Ok(dir) = std::env::var("MINI_MOULINETTE_DIR") {
        let p = PathBuf::from(dir).join("tests");
        if p.is_dir() {
            return p;
        }
    }
    if let Ok(home) = std::env::var("HOME") {
        let p = PathBuf::from(home).join(".mini-moulinette").join("tests");
        if p.is_dir() {
            return p;
        }
    }
    local
}

fn run_assignment(assignment: &str, path: &PathBuf, is_strict: bool) -> Result<()> {
    println!("\n{}", "╭────────────────────────────────────────────────────────────╮".cyan().bold());
    
    let title = format!("TESTING ASSIGNMENT: {}", assignment);
    let padded_title = pad_str(&title, 58, Alignment::Center, None);
    println!("{} {} {}", "│".cyan().bold(), padded_title.bold(), "│".cyan().bold());
    
    let subtitle = format!("Directory: {}", path.display());
    let padded_subtitle = pad_str(&subtitle, 58, Alignment::Center, None);
    println!("{} {} {}", "│".cyan().bold(), padded_subtitle, "│".cyan().bold());
    
    if is_strict {
        let strict_txt = format!("{}", "STRICT MODE ENABLED".red().bold());
        let padded_strict = pad_str(&strict_txt, 58, Alignment::Center, None);
        println!("{} {} {}", "│".cyan().bold(), padded_strict, "│".cyan().bold());
    }
    println!("{}\n", "╰────────────────────────────────────────────────────────────╯".cyan().bold());

    let tests_dir = find_tests_root().join(assignment);
    
    if !tests_dir.exists() {
        println!("{} No tests found for {}", "✗".red(), assignment);
        return Ok(());
    }

    let mut exercises: Vec<String> = fs::read_dir(&tests_dir)?
        .filter_map(Result::ok)
        .filter(|e| e.path().is_dir())
        .map(|e| e.file_name().to_string_lossy().to_string())
        .collect();
    exercises.sort();

    let total_exercises = exercises.len();
    if total_exercises == 0 {
        println!("{} No exercises found for {}", "✗".red(), assignment);
        return Ok(());
    }

    let mut score = 0;
    let max_score = total_exercises * 100;
    let points_per_ex = 100;
    let mut strict_mode_failed = false;
    // full failure details go here; written to a trace file at the end
    let mut trace = String::new();

    for ex in exercises {
        if is_strict && strict_mode_failed {
            println!(" ▶ {} {}", ex.bold(), "[SKIPPED]".yellow().bold());
            println!("   ╰── {}\n", "Strict mode triggered: previous exercise failed".yellow());
            continue;
        }

        let test_ex_dir = tests_dir.join(&ex);
        let student_ex_dir = path.join(&ex);

        let passed = run_exercise_parallel(&ex, &test_ex_dir, &student_ex_dir, &mut trace)?;

        if passed {
            score += points_per_ex;
        } else if is_strict {
            strict_mode_failed = true;
        }
    }

    let grade = (score as f64 / max_score as f64) * 100.0;
    println!("{}", "╭────────────────────────────────────────────────────────────╮".magenta().bold());
    
    if grade >= 80.0 {
        let sc = format!("{}", format!("FINAL SCORE: {}/100", grade.round()).green().bold());
        println!("{} {} {}", "│".magenta().bold(), pad_str(&sc, 58, Alignment::Center, None), "│".magenta().bold());
    } else if grade >= 50.0 {
        let sc = format!("{}", format!("FINAL SCORE: {}/100", grade.round()).yellow().bold());
        println!("{} {} {}", "│".magenta().bold(), pad_str(&sc, 58, Alignment::Center, None), "│".magenta().bold());
    } else {
        let sc = format!("{}", format!("FINAL SCORE: {}/100", grade.round()).red().bold());
        println!("{} {} {}", "│".magenta().bold(), pad_str(&sc, 58, Alignment::Center, None), "│".magenta().bold());
    }
    
    println!("{}\n", "╰────────────────────────────────────────────────────────────╯".magenta().bold());

    if !trace.is_empty() {
        let trace_path = std::env::temp_dir().join(format!(
            "mini-moulinette-{}-{}.trace",
            assignment,
            &uuid::Uuid::new_v4().to_string()[..8]
        ));
        let header = format!(
            "mini-moulinette v{} — {} — dir: {}\nscore: {}/100\n\n",
            env!("CARGO_PKG_VERSION"), assignment, path.display(), grade.round());
        if fs::write(&trace_path, header + &trace).is_ok() {
            println!("{} Full error trace: {}\n",
                "📄".bold(), trace_path.display().to_string().cyan());
        }
    }

    Ok(())
}

// ---------------------------------------------------------------------------
// forbidden functions
// ---------------------------------------------------------------------------

/// gcc emits calls to these on its own (struct init, array copies...), so a
/// student can't be failed for them showing up in the symbol table.
const COMPILER_SYMS: &[&str] = &["memset", "memcpy", "memmove"];

/// Compile each student .c alone and inspect its undefined symbols with nm.
/// Anything not defined by another student file, not in allowed.txt, not a
/// compiler-generated helper and not a `_`-prefixed runtime symbol is a
/// forbidden function. Returns None when the check can't run (compile error,
/// nm missing) — the normal tests will report those cases themselves.
fn find_forbidden(sources: &[&PathBuf], allowed: &[String], inc_dirs: &[&PathBuf]) -> Option<Vec<String>> {
    use std::collections::HashSet;

    let tmp = std::env::temp_dir();
    let mut undefined: HashSet<String> = HashSet::new();
    let mut defined: HashSet<String> = HashSet::new();

    for src in sources {
        let obj = tmp.join(format!(".mm_nm_{}.o", uuid::Uuid::new_v4()));
        let mut cmd = Command::new("cc");
        cmd.arg("-c").arg(src);
        for d in inc_dirs {
            cmd.arg("-I").arg(d);
        }
        cmd.arg("-o").arg(&obj);
        let ok = cmd.output().map(|o| o.status.success()).unwrap_or(false);
        if !ok {
            let _ = fs::remove_file(&obj);
            return None;
        }
        let nm = Command::new("nm").arg(&obj).output();
        let _ = fs::remove_file(&obj);
        let nm = nm.ok()?;
        if !nm.status.success() {
            return None;
        }
        for line in String::from_utf8_lossy(&nm.stdout).lines() {
            let parts: Vec<&str> = line.split_whitespace().collect();
            let (kind, name) = match parts.as_slice() {
                [k, n] => (*k, *n),
                [_, k, n] => (*k, *n),
                _ => continue,
            };
            if kind == "U" {
                undefined.insert(name.to_string());
            } else {
                defined.insert(name.to_string());
            }
        }
    }

    let mut forbidden: Vec<String> = undefined
        .into_iter()
        .filter(|s| !defined.contains(s))
        .filter(|s| !s.starts_with('_'))
        .filter(|s| !COMPILER_SYMS.contains(&s.as_str()))
        .filter(|s| !allowed.iter().any(|a| a == s))
        .collect();
    forbidden.sort();
    Some(forbidden)
}

/// Read allowed.txt (one authorized function per line). None = no file, so
/// the check is skipped. An existing empty file means nothing is allowed.
fn read_allowed(test_ex_dir: &PathBuf) -> Option<Vec<String>> {
    let p = test_ex_dir.join("allowed.txt");
    let content = fs::read_to_string(p).ok()?;
    Some(content
        .lines()
        .flat_map(|l| l.split_whitespace())
        .map(|s| s.to_string())
        .collect())
}

/// Forbidden-function gate shared by both grading modes. Returns true when
/// the exercise must be failed (and prints + traces the reason).
fn forbidden_gate(ex_name: &str, sources: &[&PathBuf], test_ex_dir: &PathBuf,
                  student_ex_dir: &PathBuf, trace: &mut String) -> bool {
    let Some(allowed) = read_allowed(test_ex_dir) else { return false };
    if sources.is_empty() {
        return false;
    }
    let inc_dirs = [student_ex_dir, test_ex_dir];
    match find_forbidden(sources, &allowed, &inc_dirs) {
        Some(forb) if !forb.is_empty() => {
            println!("   ╰── {} forbidden function(s): {}\n",
                "✗".red().bold(), forb.join(", ").red().bold());
            let allowed_str = if allowed.is_empty() {
                "(none)".to_string()
            } else {
                allowed.join(", ")
            };
            trace_block(trace, &format!("{}: forbidden functions", ex_name),
                "cheating check failed",
                &format!("called but not authorized: {}\nauthorized functions: {}",
                    forb.join(", "), allowed_str));
            true
        }
        _ => false,
    }
}

/// Append one failure block to the trace buffer (full, untruncated).
fn trace_block(trace: &mut String, location: &str, kind: &str, body: &str) {
    trace.push_str(&"=".repeat(79));
    trace.push('\n');
    trace.push_str(&format!("{} — {}\n", location, kind));
    trace.push_str(&"-".repeat(79));
    trace.push('\n');
    trace.push_str(body.trim_end());
    trace.push_str("\n\n");
}

struct TestCase {
    c_file: PathBuf,
    out_file: PathBuf,
}

enum TestResult {
    Passed,
    FailedOutput(String, String), // expected, actual
    Segfault,
    Killed(i32),
    Timeout,
    CompilationError(String),
}

const TEST_TIMEOUT_SECS: u64 = 5;

const BUILD_TIMEOUT_SECS: u64 = 30;

fn run_build_check(ex_name: &str, check_script: &PathBuf, student_ex_dir: &PathBuf, trace: &mut String) -> Result<bool> {
    use std::process::Stdio;
    use std::time::{Duration, Instant};

    if !student_ex_dir.exists() {
        println!("   ╰── {} directory missing\n", "✗".red());
        return Ok(false);
    }

    let out_path = std::env::temp_dir().join(format!(".build_check_{}", uuid::Uuid::new_v4()));
    let child = std::fs::File::create(&out_path).ok().and_then(|f| {
        let err = f.try_clone().ok();
        let mut cmd = Command::new("bash");
        cmd.arg(check_script).arg(student_ex_dir).stdout(Stdio::from(f));
        if let Some(e) = err {
            cmd.stderr(Stdio::from(e));
        }
        cmd.spawn().ok()
    });

    let (passed, timed_out) = match child {
        None => {
            println!("   ╰── {} could not launch check.sh\n", "✗".red());
            let _ = fs::remove_file(&out_path);
            return Ok(false);
        }
        Some(mut ch) => {
            let start = Instant::now();
            loop {
                match ch.try_wait() {
                    Ok(Some(st)) => break (st.success(), false),
                    Ok(None) => {
                        if start.elapsed() > Duration::from_secs(BUILD_TIMEOUT_SECS) {
                            let _ = ch.kill();
                            let _ = ch.wait();
                            break (false, true);
                        }
                        std::thread::sleep(Duration::from_millis(20));
                    }
                    Err(_) => break (false, false),
                }
            }
        }
    };

    let output = String::from_utf8_lossy(&fs::read(&out_path).unwrap_or_default()).to_string();
    let _ = fs::remove_file(&out_path);

    if passed {
        let msg = output.lines().last().unwrap_or("build check passed");
        println!("   ╰── {} {}\n", "✓".green().bold(), msg);
        Ok(true)
    } else {
        if timed_out {
            println!("   ╰── {} build check timed out after {}s\n", "✗".red().bold(), BUILD_TIMEOUT_SECS);
            trace_block(trace, &format!("{} (build check)", ex_name),
                &format!("timed out after {}s", BUILD_TIMEOUT_SECS), &output);
        } else {
            println!("   ╰── {} build check failed", "✗".red().bold());
            for line in output.lines().take(6) {
                println!("        {}", line.dimmed());
            }
            println!();
            trace_block(trace, &format!("{} (build check)", ex_name),
                "build check failed (full check.sh output below)", &output);
        }
        Ok(false)
    }
}

fn run_exercise_parallel(ex_name: &str, test_ex_dir: &PathBuf, student_ex_dir: &PathBuf, trace: &mut String) -> Result<bool> {
    // Build-check exercises (Makefile, shell scripts, libraries) can't be graded by
    // compiling test_*.c against a single source. A check.sh does the build/link/run.
    let check_script = test_ex_dir.join("check.sh");
    if check_script.exists() {
        println!(" ▶ {} {}", ex_name.bold(), "(build check)".cyan());
        // forbidden-function gate on every .c of the rendu (file list is free
        // in these program exercises, so no extra-file warning here)
        if student_ex_dir.exists() && test_ex_dir.join("allowed.txt").exists() {
            let all_c: Vec<PathBuf> = fs::read_dir(student_ex_dir)?
                .filter_map(Result::ok)
                .map(|e| e.path())
                .filter(|p| p.extension().map_or(false, |e| e == "c"))
                .collect();
            let refs: Vec<&PathBuf> = all_c.iter().collect();
            if forbidden_gate(ex_name, &refs, test_ex_dir, student_ex_dir, trace) {
                return Ok(false);
            }
        }
        return run_build_check(ex_name, &check_script, student_ex_dir, trace);
    }

    let files_req_path = test_ex_dir.join("files.txt");
    let required_files: Vec<String> = if files_req_path.exists() {
        fs::read_to_string(&files_req_path)?
            .lines()
            .map(|l| l.trim().to_string())
            .filter(|l| !l.is_empty())
            .collect()
    } else {
        vec!["Unknown.c".to_string()]
    };

    println!(" ▶ {} {}", ex_name.bold(), format!("({})", required_files.join(", ")).cyan());

    if !student_ex_dir.exists() {
        println!("   ╰── {} directory missing\n", "✗".red());
        return Ok(false);
    }

    let student_files: Vec<PathBuf> = required_files.iter().map(|f| student_ex_dir.join(f)).collect();
    for (req, sf) in required_files.iter().zip(student_files.iter()) {
        if !sf.exists() {
            println!("   ╰── {} file not found: {}", "✗".red(), req);
            println!();
            return Ok(false);
        }
    }

    // the subject forbids leaving any extra file in the turn-in directory;
    // warn (the real moulinette grades 0 for this)
    let mut extras: Vec<String> = fs::read_dir(student_ex_dir)?
        .filter_map(Result::ok)
        .map(|e| e.file_name().to_string_lossy().to_string())
        .filter(|n| !n.starts_with('.') && !required_files.contains(n))
        // files the moulinette itself provides (e.g. ft_stock_str.h,
        // C12/ex08's ft_list.h) may legitimately mirror the test dir
        .filter(|n| !test_ex_dir.join(n).exists())
        .collect();
    extras.sort();
    if !extras.is_empty() {
        println!("   {} extra file(s) in the turn-in dir (real moulinette grades 0): {}",
            "⚠".yellow().bold(), extras.join(", ").yellow());
    }

    // forbidden-function gate (allowed.txt in the test dir drives it)
    {
        let srcs: Vec<&PathBuf> = student_files
            .iter()
            .filter(|p| p.extension().map_or(false, |e| e == "c"))
            .collect();
        if forbidden_gate(ex_name, &srcs, test_ex_dir, student_ex_dir, trace) {
            return Ok(false);
        }
    }

    // Find all tests
    let mut test_cases = Vec::new();
    for entry in fs::read_dir(test_ex_dir)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_file() && path.extension().unwrap_or_default() == "c" {
            let filename = path.file_name().unwrap_or_default().to_string_lossy();
            if filename.starts_with("test_") {
                let out_file = path.with_extension("out");
                if out_file.exists() {
                    test_cases.push(TestCase { c_file: path.clone(), out_file });
                }
            }
        }
    }

    if test_cases.is_empty() {
        println!("   ╰── {} No valid test cases (test_*.c / .out) found\n", "⚠".yellow());
        return Ok(false);
    }

    let pb = ProgressBar::new(test_cases.len() as u64);
    pb.set_style(ProgressStyle::default_bar()
        .template("   │ {spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} tests ({eta})")?
        .progress_chars("━> "));

    let passed_count = AtomicUsize::new(0);
    let failed_count = AtomicUsize::new(0);
    let segfault_count = AtomicUsize::new(0);

    // Only .c files are compiled; headers (.h) are made available via -I instead.
    let source_files: Vec<&PathBuf> = student_files
        .iter()
        .filter(|p| p.extension().map_or(false, |e| e == "c"))
        .collect();

    let results: Vec<(&TestCase, TestResult)> = test_cases.par_iter().map(|tc| {
        let expected_output = fs::read_to_string(&tc.out_file).unwrap_or_default();
        let bin_name = format!(".test_bin_{}", uuid::Uuid::new_v4());
        let output_bin = student_ex_dir.join(&bin_name);

        let compile_status = Command::new("cc")
            .arg("-Wall")
            .arg("-Wextra")
            .arg("-Werror")
            .arg(&tc.c_file)
            .args(&source_files)
            .arg("-I").arg(student_ex_dir)
            .arg("-I").arg(test_ex_dir)
            .arg("-o")
            .arg(&output_bin)
            .output();

        let res = match compile_status {
            Ok(output) if !output.status.success() => {
                TestResult::CompilationError(String::from_utf8_lossy(&output.stderr).to_string())
            }
            Ok(_) => {
                use std::process::Stdio;
                use std::time::{Duration, Instant};
                // Redirect stdout to a file (not a pipe) so a program that writes a
                // lot cannot deadlock while we poll, and we can still read it after kill.
                let stdout_path = student_ex_dir.join(format!("{}.stdout", bin_name));
                let child = std::fs::File::create(&stdout_path).ok().and_then(|f| {
                    Command::new(&output_bin)
                        .stdout(Stdio::from(f))
                        .stderr(Stdio::null())
                        .spawn()
                        .ok()
                });
                match child {
                    None => {
                        let _ = fs::remove_file(&output_bin);
                        let _ = fs::remove_file(&stdout_path);
                        TestResult::CompilationError("Failed to run binary".to_string())
                    }
                    Some(mut ch) => {
                        let start = Instant::now();
                        let status = loop {
                            match ch.try_wait() {
                                Ok(Some(st)) => break Some(st),
                                Ok(None) => {
                                    if start.elapsed() > Duration::from_secs(TEST_TIMEOUT_SECS) {
                                        let _ = ch.kill();
                                        let _ = ch.wait();
                                        break None;
                                    }
                                    std::thread::sleep(Duration::from_millis(5));
                                }
                                Err(_) => break None,
                            }
                        };
                        let _ = fs::remove_file(&output_bin);
                        let res = match status {
                            None => TestResult::Timeout,
                            Some(st) => {
                                if let Some(signal) = st.signal() {
                                    if signal == 11 { TestResult::Segfault }
                                    else { TestResult::Killed(signal) }
                                } else {
                                    let actual_output = String::from_utf8_lossy(
                                        &fs::read(&stdout_path).unwrap_or_default()).to_string();
                                    if actual_output == expected_output { TestResult::Passed }
                                    else { TestResult::FailedOutput(expected_output, actual_output) }
                                }
                            }
                        };
                        let _ = fs::remove_file(&stdout_path);
                        res
                    }
                }
            }
            Err(e) => {
                TestResult::CompilationError(e.to_string())
            }
        };

        match res {
            TestResult::Passed => { passed_count.fetch_add(1, Ordering::SeqCst); },
            TestResult::Segfault => { segfault_count.fetch_add(1, Ordering::SeqCst); },
            _ => { failed_count.fetch_add(1, Ordering::SeqCst); },
        }

        pb.inc(1);
        (tc, res)
    }).collect();

    pb.finish_and_clear();

    let p = passed_count.load(Ordering::SeqCst);
    let f = failed_count.load(Ordering::SeqCst);
    let s = segfault_count.load(Ordering::SeqCst);
    let total = test_cases.len();

    if p == total {
        println!("   ╰── {} {}/{} tests passed\n", "✓".green().bold(), p, total);
    } else {
        println!("   ╰── {} {}/{} tests passed | {} failed | {} segfault(s)", "✗".red().bold(), p, total, f, s);
        
        let mut printed_errors = 0;
        let mut truncated_notice = false;
        for (tc, res) in &results {
            let tc_name = tc.c_file.file_name().unwrap().to_string_lossy();
            let loc = format!("{}: {}", ex_name, tc_name);
            let print_it = printed_errors < 3;
            if !print_it && !truncated_notice && !matches!(res, TestResult::Passed) {
                println!("        ... and more errors. (Full details in the trace file)");
                truncated_notice = true;
            }
            match res {
                TestResult::Segfault => {
                    if print_it {
                        println!("        ╭── [{}] {}", tc_name.yellow(), "Segfault (Signal 11)".bold().red());
                        println!("        ╰── The program crashed attempting to access invalid memory.\n");
                    }
                    let src = fs::read_to_string(&tc.c_file).unwrap_or_default();
                    trace_block(trace, &loc, "Segfault (signal 11)",
                        &format!("test main:\n{}", src));
                    printed_errors += 1;
                }
                TestResult::Killed(sig) => {
                    if print_it {
                        println!("        ╭── [{}] {}", tc_name.yellow(), "Killed by signal".bold().red());
                        println!("        ╰── Process terminated via signal {}\n", sig);
                    }
                    let src = fs::read_to_string(&tc.c_file).unwrap_or_default();
                    trace_block(trace, &loc, &format!("killed by signal {}", sig),
                        &format!("test main:\n{}", src));
                    printed_errors += 1;
                }
                TestResult::Timeout => {
                    if print_it {
                        println!("        ╭── [{}] {}", tc_name.yellow(), "Timeout".bold().red());
                        println!("        ╰── The program ran longer than {}s (possible infinite loop).\n", TEST_TIMEOUT_SECS);
                    }
                    let src = fs::read_to_string(&tc.c_file).unwrap_or_default();
                    trace_block(trace, &loc,
                        &format!("timeout after {}s (possible infinite loop)", TEST_TIMEOUT_SECS),
                        &format!("test main:\n{}", src));
                    printed_errors += 1;
                }
                TestResult::FailedOutput(exp, act) => {
                    if print_it {
                        println!("        ╭── [{}] {}", tc_name.yellow(), "Output mismatch".bold().red());
                        println!("        │ Expected: {}", format!("{:?}", exp).green());
                        println!("        ╰── Got     : {}\n", format!("{:?}", act).red());
                    }
                    let src = fs::read_to_string(&tc.c_file).unwrap_or_default();
                    trace_block(trace, &loc, "output mismatch",
                        &format!("--- expected ---\n{}\n--- got ---\n{}\n--- test main ---\n{}",
                            exp, act, src));
                    printed_errors += 1;
                }
                TestResult::CompilationError(err) => {
                    if print_it {
                        println!("        ╭── [{}] {}", tc_name.yellow(), "Compilation / Execution Error".bold().red());
                        for line in err.lines().take(2) {
                            println!("        │  {}", line.dimmed());
                        }
                        println!("        ╰── (Full error log in the trace file)\n");
                    }
                    trace_block(trace, &loc, "compilation / execution error", err);
                    printed_errors += 1;
                }
                TestResult::Passed => {}
            }
        }
    }

    Ok(p == total)
}
