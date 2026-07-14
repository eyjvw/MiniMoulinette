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

#[derive(Parser, Debug)]
#[command(name = "mini-moulinette", version = "0.1.0", about = "Parallel test runner for 42 assignments", long_about = None)]
struct Cli {
    #[arg(name = "ASSIGNMENT")]
    assignment: Option<String>,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand, Debug)]
enum Commands {
    Run {
        #[arg(name = "ASSIGNMENT")]
        assignment: String,
        #[arg(short, long, default_value = ".")]
        path: PathBuf,
        #[arg(short, long)]
        strict: bool,
    },
    Init,
    Update,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match &cli.command {
        Some(Commands::Run { assignment, path, strict }) => run_assignment(assignment, path, *strict)?,
        Some(Commands::Init) => println!("Initializing..."),
        Some(Commands::Update) => println!("Updating..."),
        None => {
            if let Some(assignment) = &cli.assignment {
                run_assignment(assignment, &PathBuf::from("."), false)?;
            } else {
                println!("{}", "Please provide an assignment name".red());
            }
        }
    }
    Ok(())
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

    for ex in exercises {
        if is_strict && strict_mode_failed {
            println!(" ▶ {} {}", ex.bold(), "[SKIPPED]".yellow().bold());
            println!("   ╰── {}\n", "Strict mode triggered: previous exercise failed".yellow());
            continue;
        }

        let test_ex_dir = tests_dir.join(&ex);
        let student_ex_dir = path.join(&ex);
        
        let passed = run_exercise_parallel(&ex, &test_ex_dir, &student_ex_dir)?;
        
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
    
    Ok(())
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

fn run_build_check(ex_name: &str, check_script: &PathBuf, student_ex_dir: &PathBuf) -> Result<bool> {
    use std::process::Stdio;
    use std::time::{Duration, Instant};

    println!(" ▶ {} {}", ex_name.bold(), "(build check)".cyan());

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
        } else {
            println!("   ╰── {} build check failed", "✗".red().bold());
            for line in output.lines().take(6) {
                println!("        {}", line.dimmed());
            }
            println!();
        }
        Ok(false)
    }
}

fn run_exercise_parallel(ex_name: &str, test_ex_dir: &PathBuf, student_ex_dir: &PathBuf) -> Result<bool> {
    // Build-check exercises (Makefile, shell scripts, libraries) can't be graded by
    // compiling test_*.c against a single source. A check.sh does the build/link/run.
    let check_script = test_ex_dir.join("check.sh");
    if check_script.exists() {
        return run_build_check(ex_name, &check_script, student_ex_dir);
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
        for (tc, res) in results {
            if printed_errors >= 3 {
                println!("        ... and more errors. (Truncated for readability)");
                break;
            }
            let tc_name = tc.c_file.file_name().unwrap().to_string_lossy();
            match res {
                TestResult::Segfault => {
                    println!("        ╭── [{}] {}", tc_name.yellow(), "Segfault (Signal 11)".bold().red());
                    println!("        ╰── The program crashed attempting to access invalid memory.\n");
                    printed_errors += 1;
                }
                TestResult::Killed(sig) => {
                    println!("        ╭── [{}] {}", tc_name.yellow(), "Killed by signal".bold().red());
                    println!("        ╰── Process terminated via signal {}\n", sig);
                    printed_errors += 1;
                }
                TestResult::Timeout => {
                    println!("        ╭── [{}] {}", tc_name.yellow(), "Timeout".bold().red());
                    println!("        ╰── The program ran longer than {}s (possible infinite loop).\n", TEST_TIMEOUT_SECS);
                    printed_errors += 1;
                }
                TestResult::FailedOutput(exp, act) => {
                    println!("        ╭── [{}] {}", tc_name.yellow(), "Output mismatch".bold().red());
                    println!("        │ Expected: {}", format!("{:?}", exp).green());
                    println!("        ╰── Got     : {}\n", format!("{:?}", act).red());
                    printed_errors += 1;
                }
                TestResult::CompilationError(err) => {
                    println!("        ╭── [{}] {}", tc_name.yellow(), "Compilation / Execution Error".bold().red());
                    for line in err.lines().take(2) {
                        println!("        │  {}", line.dimmed());
                    }
                    println!("        ╰── (Error log truncated)\n");
                    printed_errors += 1;
                }
                _ => {}
            }
        }
    }

    Ok(p == total)
}
