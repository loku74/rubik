use clap::error::ErrorKind;
use clap::{ArgGroup, CommandFactory, Parser};

use rubik::Cube;
use rubik::moves::{format_moves, parse_moves};

/// Rubik's Cube solver - Apply spin sequences or generate random cubes
#[derive(Parser)]
#[command(
    group(ArgGroup::new("input").required(true).args(["sequence", "random"])),
    after_help = "\
Examples:
  rubik \"U R U' L'\"
  rubik --random
  rubik --random 30
  rubik -r 50

Valid spins: U, U', U2, D, D', D2, F, F', F2, B, B', B2, L, L', L2, R, R', R2"
)]
struct Args {
    /// Spin sequence (e.g., "U R U' L'")
    sequence: Option<String>,

    /// Generate a random cube with optional number of spins (default: 20)
    #[arg(
        short,
        long,
        value_name = "SPINS",
        num_args = 0..=1,
        default_missing_value = "20",
        value_parser = clap::value_parser!(u32).range(1..),
    )]
    random: Option<u32>,

    /// Display the cube
    #[arg(short, long)]
    display: bool,
}

fn main() {
    let args = Args::parse();

    let mut cube = match (args.random, args.sequence) {
        (Some(spins), _) => {
            let (cube, moves) = Cube::random(spins as usize);
            let shuffle = format_moves(&moves);
            println!("Shuffle: {shuffle}");
            println!("{}", "-".repeat(shuffle.len() + 9));
            cube
        }
        (None, Some(sequence)) => {
            let moves = parse_moves(&sequence)
                .unwrap_or_else(|e| Args::command().error(ErrorKind::InvalidValue, e).exit());
            let mut cube = Cube::new();
            cube.apply_all(&moves);
            cube
        }
        (None, None) => unreachable!("clap requires one of the inputs"),
    };

    if args.display {
        println!("{cube}");
    }

    let solution = cube.solve();
    println!(
        "Solution: {} [{} spins]",
        format_moves(&solution),
        solution.len()
    );

    if args.display {
        println!("{cube}");
    }
}
