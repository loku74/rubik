//! First two layers: pairs each white corner with its middle-layer edge and
//! inserts the pair into its slot.

use super::algorithms::{Algorithm, F2L_CORNER_IN_SLOT, F2L_EDGE_IN_SLOT, TOP_F2L};
use crate::cube::{Color, Cube};
use crate::moves::{Face, Move, Token, parse_tokens};

/// A slot of the first two layers, named after the two side faces it touches.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Slot {
    FR,
    BR,
    BL,
    FL,
}

struct SlotInfo {
    /// Side faces in U-turn order: the slot's stickers are `left[5]`, `left[8]`
    /// and `right[3]`, `right[6]`.
    left: Face,
    right: Face,
    /// Sticker of the corner on D.
    down: usize,
    /// Sticker on U of the corner right above the slot.
    up: usize,
    /// `y` rotations that bring the slot to the front right, where the
    /// algorithms are written.
    y: u8,
}

impl Slot {
    const ALL: [Slot; 4] = [Slot::FR, Slot::BR, Slot::BL, Slot::FL];

    fn info(self) -> SlotInfo {
        match self {
            Slot::FR => SlotInfo {
                left: Face::F,
                right: Face::R,
                down: 2,
                up: 8,
                y: 0,
            },
            Slot::BR => SlotInfo {
                left: Face::R,
                right: Face::B,
                down: 8,
                up: 2,
                y: 1,
            },
            Slot::BL => SlotInfo {
                left: Face::B,
                right: Face::L,
                down: 6,
                up: 0,
                y: 2,
            },
            Slot::FL => SlotInfo {
                left: Face::L,
                right: Face::F,
                down: 0,
                up: 6,
                y: 3,
            },
        }
    }

    /// The slot a piece with these two side colors belongs to.
    fn of_colors(a: Color, b: Color) -> Option<Slot> {
        let (a, b) = (a.home(), b.home());
        Slot::ALL.into_iter().find(|slot| {
            let info = slot.info();
            (info.left, info.right) == (a, b) || (info.left, info.right) == (b, a)
        })
    }

    /// The slot a piece belongs to, if it has a white sticker; ignores the white one.
    fn of_white_corner(colors: [Color; 3]) -> Option<Slot> {
        let others: Vec<Color> = colors.into_iter().filter(|&c| c != Color::White).collect();
        match others[..] {
            [a, b] => Slot::of_colors(a, b),
            _ => None,
        }
    }

    fn is_solved(self, cube: &Cube) -> bool {
        let SlotInfo {
            left, right, down, ..
        } = self.info();
        let matches = |face: Face, index: usize| cube.get(face, index) == cube.get(face, 4);
        matches(left, 5)
            && matches(left, 8)
            && matches(right, 3)
            && matches(right, 6)
            && matches(Face::D, down)
    }

    /// Slot of the edge stuck in this slot, if it is not solved and has no yellow.
    fn edge_inside(self, cube: &Cube) -> Option<Slot> {
        let SlotInfo { left, right, .. } = self.info();
        let colors = (cube.get(left, 5), cube.get(right, 3));
        if colors.0 == Color::Yellow || colors.1 == Color::Yellow || self.is_solved(cube) {
            return None;
        }
        Slot::of_colors(colors.0, colors.1)
    }

    /// Slot of the white corner stuck in this slot, if it is not solved.
    fn corner_inside(self, cube: &Cube) -> Option<Slot> {
        let SlotInfo {
            left, right, down, ..
        } = self.info();
        if self.is_solved(cube) {
            return None;
        }
        Slot::of_white_corner([
            cube.get(left, 8),
            cube.get(right, 6),
            cube.get(Face::D, down),
        ])
    }
}

/// Slots of the middle-layer edges (no yellow, no white) sitting on U.
fn top_edges(cube: &Cube) -> Vec<Slot> {
    [(1, Face::B), (3, Face::L), (5, Face::R), (7, Face::F)]
        .into_iter()
        .filter_map(|(index, side)| {
            let colors = [cube.get(Face::U, index), cube.get(side, 1)];
            if colors
                .iter()
                .any(|&c| c == Color::Yellow || c == Color::White)
            {
                return None;
            }
            Slot::of_colors(colors[0], colors[1])
        })
        .collect()
}

/// A white corner sitting on U.
#[derive(Clone, Copy)]
struct TopCorner {
    /// Slot the corner is above.
    above: Slot,
    /// Slot the corner belongs to.
    slot: Slot,
}

fn top_corners(cube: &Cube) -> Vec<TopCorner> {
    [Slot::BL, Slot::BR, Slot::FR, Slot::FL]
        .into_iter()
        .filter_map(|above| {
            let SlotInfo {
                left, right, up, ..
            } = above.info();
            let colors = [cube.get(Face::U, up), cube.get(right, 0), cube.get(left, 2)];
            Slot::of_white_corner(colors).map(|slot| TopCorner { above, slot })
        })
        .collect()
}

/// Tries every `algorithm` (each preceded by every `setup`) from the slot's
/// point of view and returns the first one that solves the slot.
fn solve_slot(
    cube: &Cube,
    slot: Slot,
    algorithms: &[Algorithm],
    setups: &[Option<Move>],
) -> Option<Vec<Move>> {
    for alg in algorithms {
        for setup in setups {
            let tokens: Vec<Token> = std::iter::once(Token::Y(slot.info().y))
                .chain(setup.map(Token::Turn))
                .chain(alg.iter().copied())
                .collect();
            let mut attempt = *cube;
            let moves = attempt.apply_tokens(&tokens);
            if slot.is_solved(&attempt) {
                return Some(moves);
            }
        }
    }
    None
}

const U_TURNS: [Move; 3] = [
    Move::new(Face::U, 1),
    Move::new(Face::U, 3),
    Move::new(Face::U, 2),
];
const U_SETUPS: [Option<Move>; 4] = [None, Some(U_TURNS[0]), Some(U_TURNS[1]), Some(U_TURNS[2])];

/// Corner and edge both on U: bring the corner above its slot and insert the pair.
fn pair_on_top(cube: &Cube) -> Vec<Move> {
    let mut cube = *cube;
    let mut result = Vec::new();
    loop {
        let edges = top_edges(&cube);
        let pairs: Vec<TopCorner> = top_corners(&cube)
            .into_iter()
            .filter(|corner| edges.contains(&corner.slot))
            .collect();
        if pairs.is_empty() {
            return result;
        }

        let mut moves = Vec::new();
        let corner = match pairs
            .iter()
            .rev()
            .find(|corner| corner.above == corner.slot)
        {
            Some(&corner) => corner,
            None => {
                let corner = pairs[0];
                if let Some(u) = align_corner(&cube, corner.slot) {
                    cube.apply(u);
                    moves.push(u);
                }
                corner
            }
        };

        let Some(insert) = solve_slot(&cube, corner.slot, &TOP_F2L, &[None]) else {
            return result;
        };
        cube.apply_all(&insert);
        moves.extend(insert);
        result.extend(moves);
    }
}

/// The U turn that puts the white corner of `slot` right above it.
fn align_corner(cube: &Cube, slot: Slot) -> Option<Move> {
    U_TURNS.into_iter().find(|&u| {
        let mut attempt = *cube;
        attempt.apply(u);
        top_corners(&attempt)
            .iter()
            .any(|corner| corner.slot == slot && corner.above == slot)
    })
}

/// Corner already in its slot, edge on U.
fn corner_in_slot(cube: &Cube) -> Vec<Move> {
    top_edges(cube)
        .into_iter()
        .filter(|&slot| slot.corner_inside(cube) == Some(slot))
        .find_map(|slot| solve_slot(cube, slot, &F2L_CORNER_IN_SLOT, &U_SETUPS))
        .unwrap_or_default()
}

/// Edge already in its slot, corner on U.
fn edge_in_slot(cube: &Cube) -> Vec<Move> {
    top_corners(cube)
        .into_iter()
        .map(|corner| corner.slot)
        .filter(|&slot| slot.edge_inside(cube) == Some(slot))
        .find_map(|slot| solve_slot(cube, slot, &F2L_EDGE_IN_SLOT, &U_SETUPS))
        .unwrap_or_default()
}

/// Solves one pair if the cube matches a known case, applying the moves to `cube`.
fn solve_known_case(cube: &mut Cube) -> Option<Vec<Move>> {
    let cases: [fn(&Cube) -> Vec<Move>; 3] = [corner_in_slot, edge_in_slot, pair_on_top];
    for case in cases {
        let moves = case(cube);
        if !moves.is_empty() {
            cube.apply_all(&moves);
            return Some(moves);
        }
    }
    None
}

fn unsolved_slots(cube: &Cube, order: [Slot; 4]) -> Vec<Slot> {
    order
        .into_iter()
        .filter(|slot| !slot.is_solved(cube))
        .collect()
}

fn from_slot(slot: Slot, alg: &str) -> Vec<Token> {
    let mut tokens = vec![Token::Y(slot.info().y)];
    tokens.extend(parse_tokens(alg).expect("valid algorithm"));
    tokens
}

/// Pulls a piece out of an unsolved slot so that a known case appears.
fn extract_pair(cube: &Cube) -> Option<Vec<Move>> {
    const EXTRACTIONS: [&str; 4] = ["R U R'", "R U' R'", "F' U F", "F' U' F"];
    for slot in unsolved_slots(cube, Slot::ALL) {
        for alg in EXTRACTIONS {
            let mut attempt = *cube;
            let moves = attempt.apply_tokens(&from_slot(slot, alg));
            if solve_known_case(&mut attempt).is_some() {
                return Some(moves);
            }
        }
    }
    None
}

/// Last resort: shake the unsolved slots until a known case appears.
fn shuffle_slots(cube: &Cube) -> Vec<Move> {
    let mut cube = *cube;
    let mut result = Vec::new();
    for slot in unsolved_slots(&cube, [Slot::FR, Slot::FL, Slot::BL, Slot::BR]) {
        result.extend(cube.apply_tokens(&from_slot(slot, "R U R'")));
        if solve_known_case(&mut cube).is_some() {
            break;
        }
    }
    result
}

pub fn solve(cube: &Cube) -> Vec<Move> {
    let mut cube = *cube;
    let mut result = Vec::new();
    loop {
        if let Some(moves) = solve_known_case(&mut cube) {
            result.extend(moves);
        } else if let Some(moves) = extract_pair(&cube) {
            cube.apply_all(&moves);
            result.extend(moves);
        } else if Slot::ALL.iter().all(|slot| slot.is_solved(&cube)) {
            return result;
        } else {
            let moves = shuffle_slots(&cube);
            cube.apply_all(&moves);
            result.extend(moves);
        }
    }
}
