//! Solves random cubes and reports timing and solution length.
//!
//! Usage: benchmark [CUBES] (default: 1000)

use std::io::Write;
use std::time::Instant;

use rubik::Cube;
use rubik::moves::format_moves;

fn main() {
    let total: usize = match std::env::args().nth(1) {
        Some(arg) => arg.parse().unwrap_or_else(|_| {
            eprintln!("usage: benchmark [CUBES]");
            std::process::exit(2);
        }),
        None => 1000,
    };

    let start = Instant::now();
    let mut solve_moves = 0;
    for count in 1..=total {
        let (scrambled, shuffle) = Cube::random(20);
        let mut cube = scrambled;
        let solution = cube.solve();

        let mut replay = scrambled;
        replay.apply_all(&solution);
        if !cube.is_solved() || !replay.is_solved() {
            eprintln!("\nFailed to solve cube");
            eprintln!("shuffle moves: {}", format_moves(&shuffle));
            eprintln!("{scrambled}");
            eprintln!("solve moves: {}", format_moves(&solution));
            eprintln!("{replay}");
            std::process::exit(1);
        }

        solve_moves += solution.len();
        print!("\r{count}/{total}");
        std::io::stdout().flush().ok();
    }

    let elapsed = start.elapsed();
    println!();
    println!("Number of rubiks cube solved: {total}");
    println!(
        "Average time per solve: {:.3} ms",
        elapsed.as_secs_f64() * 1000.0 / total as f64
    );
    println!(
        "Average number of solve moves: {:.2}",
        solve_moves as f64 / total as f64
    );
}
