use std::fmt;
use std::str::FromStr;

use rand::Rng;

use crate::geometry::{Mat3, Vec3};

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Face {
    U,
    D,
    F,
    B,
    L,
    R,
}

impl Face {
    pub const ALL: [Face; 6] = [Face::U, Face::D, Face::F, Face::B, Face::L, Face::R];

    pub fn index(self) -> usize {
        self as usize
    }

    /// Outward normal of the face.
    pub fn normal(self) -> Vec3 {
        match self {
            Face::U => [0, 1, 0],
            Face::D => [0, -1, 0],
            Face::F => [0, 0, 1],
            Face::B => [0, 0, -1],
            Face::L => [-1, 0, 0],
            Face::R => [1, 0, 0],
        }
    }

    pub fn from_normal(normal: Vec3) -> Face {
        Face::ALL
            .into_iter()
            .find(|face| face.normal() == normal)
            .expect("not a face normal")
    }

    fn letter(self) -> char {
        match self {
            Face::U => 'U',
            Face::D => 'D',
            Face::F => 'F',
            Face::B => 'B',
            Face::L => 'L',
            Face::R => 'R',
        }
    }

    fn from_letter(letter: char) -> Option<Face> {
        Face::ALL.into_iter().find(|face| face.letter() == letter)
    }
}

/// A face turn. `turns` counts clockwise quarter turns: 1 = `X`, 2 = `X2`, 3 = `X'`.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Move {
    pub face: Face,
    pub turns: u8,
}

impl Move {
    pub const fn new(face: Face, turns: u8) -> Move {
        Move { face, turns }
    }

    /// The turn that undoes this one.
    pub const fn inverse(self) -> Move {
        Move::new(self.face, 4 - self.turns)
    }

    /// Rotation matrix applied to every sticker of the turned layer.
    pub fn matrix(self) -> Mat3 {
        Mat3::quarter_turn(self.face.normal()).pow(self.turns)
    }
}

impl fmt::Display for Move {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let suffix = match self.turns {
            1 => "",
            2 => "2",
            _ => "'",
        };
        write!(f, "{}{}", self.face.letter(), suffix)
    }
}

fn parse_turns(suffix: &str) -> Option<u8> {
    match suffix {
        "" => Some(1),
        "2" => Some(2),
        "'" => Some(3),
        _ => None,
    }
}

impl FromStr for Move {
    type Err = String;

    fn from_str(s: &str) -> Result<Move, String> {
        let mut chars = s.chars();
        let face = chars.next().and_then(Face::from_letter);
        match (face, parse_turns(chars.as_str())) {
            (Some(face), Some(turns)) => Ok(Move::new(face, turns)),
            _ => Err(format!("Invalid spin: {s}")),
        }
    }
}

/// An element of an algorithm: a face turn, or a whole-cube `y` rotation
/// (same direction as `U`) counted in quarter turns.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Token {
    Turn(Move),
    Y(u8),
}

impl FromStr for Token {
    type Err = String;

    fn from_str(s: &str) -> Result<Token, String> {
        match s.strip_prefix('y') {
            Some(suffix) => parse_turns(suffix)
                .map(Token::Y)
                .ok_or_else(|| format!("Invalid rotation: {s}")),
            None => s.parse().map(Token::Turn),
        }
    }
}

pub fn parse_moves(s: &str) -> Result<Vec<Move>, String> {
    s.split_whitespace().map(str::parse).collect()
}

pub fn parse_tokens(s: &str) -> Result<Vec<Token>, String> {
    s.split_whitespace().map(str::parse).collect()
}

/// Rewrites an algorithm containing `y` rotations into plain face turns.
///
/// The cube is never physically rotated: after a whole-cube rotation `G`, the
/// face named `X` sits where `G⁻¹ · normal(X)` points, so we keep track of
/// `G⁻¹` and map each turn's normal through it.
pub fn resolve(tokens: &[Token]) -> Vec<Move> {
    let y_inverse = Mat3::quarter_turn(Face::U.normal()).transpose();
    let mut orientation = Mat3::IDENTITY;
    let mut moves = Vec::with_capacity(tokens.len());
    for token in tokens {
        match *token {
            Token::Y(turns) => orientation = orientation * y_inverse.pow(turns),
            Token::Turn(m) => {
                let face = Face::from_normal(orientation.apply(m.face.normal()));
                moves.push(Move::new(face, m.turns));
            }
        }
    }
    moves
}

/// Merges consecutive turns of the same face (`R R` → `R2`, `U U'` → nothing).
pub fn simplify(moves: &[Move]) -> Vec<Move> {
    let mut result: Vec<Move> = Vec::with_capacity(moves.len());
    for &m in moves {
        match result.last_mut() {
            Some(last) if last.face == m.face => {
                last.turns = (last.turns + m.turns) % 4;
                if last.turns == 0 {
                    result.pop();
                }
            }
            _ => result.push(m),
        }
    }
    result
}

pub fn format_moves(moves: &[Move]) -> String {
    moves
        .iter()
        .map(Move::to_string)
        .collect::<Vec<_>>()
        .join(" ")
}

/// Picks a random turn of a face other than `previous`.
///
/// With `cross`, F/B/L/R are limited to half turns so the edges already on the
/// down face keep their orientation.
pub fn random_move(rng: &mut impl Rng, previous: Option<Face>, cross: bool) -> Move {
    let face = loop {
        let face = Face::ALL[rng.random_range(0..Face::ALL.len())];
        if Some(face) != previous {
            break face;
        }
    };
    let turns = if cross && !matches!(face, Face::U | Face::D) {
        2
    } else {
        rng.random_range(1..=3)
    };
    Move::new(face, turns)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_and_display_round_trip() {
        let text = "U U' U2 D D' D2 F F' F2 B B' B2 L L' L2 R R' R2";
        assert_eq!(format_moves(&parse_moves(text).unwrap()), text);
        assert!(parse_moves("R X").is_err());
        assert!(parse_moves("R3").is_err());
        assert!(parse_moves("y").is_err());
    }

    #[test]
    fn y_rotations_relabel_faces() {
        let resolve_str = |s: &str| format_moves(&resolve(&parse_tokens(s).unwrap()));
        assert_eq!(resolve_str("y R L F B U D"), "B F R L U D");
        assert_eq!(resolve_str("y2 R' F2"), "L' B2");
        assert_eq!(resolve_str("y' R F"), "F L");
        assert_eq!(resolve_str("y y' R"), "R");
        assert_eq!(resolve_str("R y R y R"), "R B L");
    }

    #[test]
    fn simplify_merges_same_face_turns() {
        let simplify_str = |s: &str| format_moves(&simplify(&parse_moves(s).unwrap()));
        assert_eq!(simplify_str("R R"), "R2");
        assert_eq!(simplify_str("R R'"), "");
        assert_eq!(simplify_str("U R R' U"), "U2");
        assert_eq!(simplify_str("R2 R"), "R'");
        assert_eq!(simplify_str("R L R"), "R L R");
    }
}
