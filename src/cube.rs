use std::fmt;
use std::sync::LazyLock;

use crate::geometry::{Vec3, dot};
use crate::moves::{Face, Move, Token, random_move, resolve};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Color {
    White,
    Yellow,
    Red,
    Green,
    Blue,
    Orange,
}

impl Color {
    /// The face whose center has this color.
    pub fn home(self) -> Face {
        match self {
            Color::White => Face::D,
            Color::Yellow => Face::U,
            Color::Red => Face::R,
            Color::Green => Face::B,
            Color::Blue => Face::F,
            Color::Orange => Face::L,
        }
    }

    fn of_face(face: Face) -> Color {
        match face {
            Face::D => Color::White,
            Face::U => Color::Yellow,
            Face::R => Color::Red,
            Face::B => Color::Green,
            Face::F => Color::Blue,
            Face::L => Color::Orange,
        }
    }

    pub fn letter(self) -> char {
        match self {
            Color::White => 'W',
            Color::Yellow => 'Y',
            Color::Red => 'R',
            Color::Green => 'G',
            Color::Blue => 'B',
            Color::Orange => 'O',
        }
    }

    fn emoji(self) -> &'static str {
        match self {
            Color::White => "⬜️",
            Color::Yellow => "🟨",
            Color::Red => "🟥",
            Color::Green => "🟩",
            Color::Blue => "🟦",
            Color::Orange => "🟧",
        }
    }
}

const STICKERS: usize = 54;

/// Where a sticker lives in space: the center of its cubie (each coordinate in
/// `{-1, 0, 1}`) and the outward normal of the face it is glued on.
#[derive(Clone, Copy, PartialEq, Eq)]
struct Sticker {
    position: Vec3,
    normal: Vec3,
}

/// Sticker `index` (0..9, row-major) of `face`.
///
/// Every face is read as seen from outside the cube. Side faces have their
/// first row against U, U has its first row against B, and D has its first
/// row against F.
fn sticker(face: Face, index: usize) -> Sticker {
    let row = (index / 3) as i32;
    let col = (index % 3) as i32;
    let position = match face {
        Face::U => [col - 1, 1, row - 1],
        Face::D => [col - 1, -1, 1 - row],
        Face::F => [col - 1, 1 - row, 1],
        Face::B => [1 - col, 1 - row, -1],
        Face::L => [-1, 1 - row, col - 1],
        Face::R => [1, 1 - row, 1 - col],
    };
    Sticker {
        position,
        normal: face.normal(),
    }
}

fn slot(face: Face, index: usize) -> usize {
    face.index() * 9 + index
}

fn sticker_at(slot: usize) -> Sticker {
    sticker(Face::ALL[slot / 9], slot % 9)
}

fn slot_of(target: Sticker) -> usize {
    (0..STICKERS)
        .find(|&slot| sticker_at(slot) == target)
        .expect("rotation produced an invalid sticker")
}

/// For every move (`face * 3 + turns - 1`), `table[dest] = source`: the sticker
/// that ends up in slot `dest`.
///
/// The tables are derived once by rotating each sticker of the turned layer
/// with the move's rotation matrix.
static MOVE_TABLES: LazyLock<Vec<[u8; STICKERS]>> = LazyLock::new(|| {
    let mut tables = Vec::with_capacity(18);
    for face in Face::ALL {
        for turns in 1..=3 {
            let rotation = Move::new(face, turns).matrix();
            let mut table: [u8; STICKERS] = std::array::from_fn(|slot| slot as u8);
            for source in 0..STICKERS {
                let s = sticker_at(source);
                if dot(s.position, face.normal()) == 1 {
                    let dest = slot_of(Sticker {
                        position: rotation.apply(s.position),
                        normal: rotation.apply(s.normal),
                    });
                    table[dest] = source as u8;
                }
            }
            tables.push(table);
        }
    }
    tables
});

#[derive(Clone, Copy, PartialEq, Eq)]
pub struct Cube {
    stickers: [Color; STICKERS],
}

impl Default for Cube {
    fn default() -> Self {
        Cube::new()
    }
}

impl Cube {
    /// A solved cube.
    pub fn new() -> Cube {
        Cube {
            stickers: std::array::from_fn(|slot| Color::of_face(Face::ALL[slot / 9])),
        }
    }

    /// A cube scrambled with `spins` random moves, along with the scramble.
    pub fn random(spins: usize) -> (Cube, Vec<Move>) {
        let mut rng = rand::rng();
        let mut cube = Cube::new();
        let mut moves = Vec::with_capacity(spins);
        let mut previous = None;
        for _ in 0..spins {
            let m = random_move(&mut rng, previous, false);
            previous = Some(m.face);
            cube.apply(m);
            moves.push(m);
        }
        (cube, moves)
    }

    pub fn get(&self, face: Face, index: usize) -> Color {
        self.stickers[slot(face, index)]
    }

    pub fn apply(&mut self, m: Move) {
        let table = &MOVE_TABLES[m.face.index() * 3 + m.turns as usize - 1];
        let old = self.stickers;
        for (dest, &source) in table.iter().enumerate() {
            self.stickers[dest] = old[source as usize];
        }
    }

    pub fn apply_all(&mut self, moves: &[Move]) {
        for &m in moves {
            self.apply(m);
        }
    }

    /// Applies an algorithm that may contain `y` rotations and returns the
    /// equivalent face turns.
    pub fn apply_tokens(&mut self, tokens: &[Token]) -> Vec<Move> {
        let moves = resolve(tokens);
        self.apply_all(&moves);
        moves
    }

    pub fn face_solved(&self, face: Face) -> bool {
        (0..9).all(|i| self.get(face, i) == Color::of_face(face))
    }

    pub fn is_solved(&self) -> bool {
        Face::ALL.into_iter().all(|face| self.face_solved(face))
    }

    /// The unfolded cube: B on top, then L | U | R, then F and finally D.
    pub fn format(&self, colors: bool) -> String {
        let paint = |face: Face, index: usize| {
            let color = self.get(face, index);
            if colors {
                color.emoji().to_string()
            } else {
                color.letter().to_string()
            }
        };
        let indent = " ".repeat(11);
        let separator = format!("{indent}{}", "-".repeat(8));
        let lone_face = |face: Face| {
            (0..3)
                .map(|row| {
                    let cells: String =
                        (0..3).map(|col| paint(face, row * 3 + col) + " ").collect();
                    format!("{indent}{cells}")
                })
                .collect::<Vec<_>>()
                .join("\n")
        };
        let middle: String = (0..3)
            .map(|row| {
                let faces = [Face::L, Face::U, Face::R].map(|face| {
                    (0..3)
                        .map(|col| paint(face, row * 3 + col))
                        .collect::<Vec<_>>()
                        .join(" ")
                });
                faces.join(" | ") + "\n"
            })
            .collect();

        format!(
            "{}\n{separator}\n{middle}{separator}\n{}\n{separator}\n{}",
            lone_face(Face::B),
            lone_face(Face::F),
            lone_face(Face::D),
        )
    }
}

impl fmt::Display for Cube {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str(&self.format(true))
    }
}

impl fmt::Debug for Cube {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "\n{}", self.format(false))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::moves::{parse_moves, parse_tokens};

    /// Stickers in the order of the original Python implementation (W Y R G B O).
    fn python_state(cube: &Cube) -> String {
        [Face::D, Face::U, Face::R, Face::B, Face::F, Face::L]
            .into_iter()
            .flat_map(|face| (0..9).map(move |i| cube.get(face, i).letter()))
            .collect()
    }

    #[test]
    fn matches_python_implementation() {
        let fixtures = include_str!("../tests/fixtures/python_states.txt");
        for line in fixtures.lines() {
            let (sequence, expected) = line.split_once('|').unwrap();
            let mut cube = Cube::new();
            cube.apply_tokens(&parse_tokens(sequence).unwrap());
            assert_eq!(python_state(&cube), expected, "sequence: {sequence}");
        }
    }

    #[test]
    fn every_move_has_order_four() {
        for face in Face::ALL {
            let mut cube = Cube::new();
            cube.apply_all(&parse_moves("R U F' D2").unwrap());
            let scrambled = cube;
            for _ in 0..4 {
                cube.apply(Move::new(face, 1));
            }
            assert_eq!(cube, scrambled);
        }
    }

    #[test]
    fn sexy_move_has_order_six() {
        let sexy = parse_moves("R U R' U'").unwrap();
        let mut cube = Cube::new();
        for i in 1..=6 {
            cube.apply_all(&sexy);
            assert_eq!(cube.is_solved(), i == 6);
        }
    }
}
