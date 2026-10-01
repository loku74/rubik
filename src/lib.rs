pub mod cube;
pub mod geometry;
pub mod moves;
pub mod solver;

pub use cube::{Color, Cube};
pub use moves::{Face, Move};

impl Cube {
    /// Solves the cube in place and returns the moves used.
    pub fn solve(&mut self) -> Vec<Move> {
        solver::solve(self)
    }
}
