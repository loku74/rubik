use super::Y_ROTATIONS;
use super::algorithms::PLL;
use crate::cube::Cube;
use crate::moves::{Face, Move, Token};

const U_TURNS: [Move; 3] = [
    Move::new(Face::U, 1),
    Move::new(Face::U, 3),
    Move::new(Face::U, 2),
];

pub fn solve(cube: &Cube) -> Vec<Move> {
    if cube.is_solved() {
        return Vec::new();
    }

    for u in U_TURNS {
        let mut attempt = *cube;
        attempt.apply(u);
        if attempt.is_solved() {
            return vec![u];
        }
    }

    let finishes = std::iter::once(None).chain(U_TURNS.map(Some));
    for alg in PLL.iter() {
        for y in Y_ROTATIONS {
            for finish in finishes.clone() {
                let tokens: Vec<Token> = std::iter::once(Token::Y(y))
                    .chain(alg.iter().copied())
                    .chain(finish.map(Token::Turn))
                    .collect();
                let mut attempt = *cube;
                let moves = attempt.apply_tokens(&tokens);
                if attempt.is_solved() {
                    return moves;
                }
            }
        }
    }
    Vec::new()
}
