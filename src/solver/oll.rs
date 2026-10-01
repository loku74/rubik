use super::Y_ROTATIONS;
use super::algorithms::OLL;
use crate::cube::Cube;
use crate::moves::{Face, Move, Token};

pub fn solve(cube: &Cube) -> Vec<Move> {
    if cube.face_solved(Face::U) {
        return Vec::new();
    }

    for alg in OLL.iter() {
        for y in Y_ROTATIONS {
            let mut attempt = *cube;
            let tokens: Vec<Token> = std::iter::once(Token::Y(y))
                .chain(alg.iter().copied())
                .collect();
            let moves = attempt.apply_tokens(&tokens);
            if attempt.face_solved(Face::U) {
                return moves;
            }
        }
    }
    Vec::new()
}
