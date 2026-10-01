//! CFOP solver: white cross, F2L, OLL and PLL.

mod algorithms;
mod f2l;
mod oll;
mod pll;
mod white_cross;

use crate::cube::Cube;
use crate::moves::{Move, simplify};

/// Solves `cube` in place and returns the moves used.
pub fn solve(cube: &mut Cube) -> Vec<Move> {
    let stages: [fn(&Cube) -> Vec<Move>; 4] =
        [white_cross::solve, f2l::solve, oll::solve, pll::solve];

    let mut moves = Vec::new();
    for stage in stages {
        let stage_moves = stage(cube);
        cube.apply_all(&stage_moves);
        moves.extend(stage_moves);
    }
    simplify(&moves)
}

/// The `y` rotations to try when matching a case, in the order they are tried.
const Y_ROTATIONS: [u8; 4] = [0, 1, 3, 2];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn solves_random_cubes() {
        for _ in 0..200 {
            let (scrambled, _) = Cube::random(20);
            let mut cube = scrambled;
            let moves = solve(&mut cube);
            assert!(cube.is_solved(), "unsolved cube: {cube:?}");

            let mut replay = scrambled;
            replay.apply_all(&moves);
            assert!(replay.is_solved(), "simplified solution is wrong");
        }
    }

    #[test]
    fn solved_cube_needs_no_moves() {
        assert!(solve(&mut Cube::new()).is_empty());
    }
}
