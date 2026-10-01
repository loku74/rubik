use crate::cube::{Color, Cube};
use crate::moves::{Face, Move, random_move};

const EDGES: [usize; 4] = [1, 3, 5, 7];

/// Every white edge sits on U or D with its white sticker facing up or down.
fn edges_oriented(cube: &Cube) -> bool {
    let white_on = |face| {
        EDGES
            .iter()
            .filter(|&&i| cube.get(face, i) == Color::White)
            .count()
    };
    white_on(Face::D) + white_on(Face::U) == 4
}

/// The white cross is built and every edge matches its side center.
fn cross_solved(cube: &Cube) -> bool {
    EDGES.iter().all(|&i| cube.get(Face::D, i) == Color::White)
        && [Face::F, Face::R, Face::B, Face::L]
            .into_iter()
            .all(|face| cube.get(face, 7) == cube.get(face, 4))
}

/// Random walks of at most `limit` moves until one reaches `goal`.
fn random_search(cube: &Cube, goal: fn(&Cube) -> bool, limit: usize, cross: bool) -> Vec<Move> {
    if goal(cube) {
        return Vec::new();
    }

    let mut rng = rand::rng();
    loop {
        let mut attempt = *cube;
        let mut moves = Vec::with_capacity(limit);
        let mut previous = None;
        for _ in 0..limit {
            let m = random_move(&mut rng, previous, cross);
            previous = Some(m.face);
            attempt.apply(m);
            moves.push(m);
            if goal(&attempt) {
                return moves;
            }
        }
    }
}

/// Drops every move the cross does not actually need.
fn prune(cube: &Cube, mut moves: Vec<Move>) -> Vec<Move> {
    let mut i = 0;
    while i < moves.len() {
        let mut attempt = *cube;
        attempt.apply_all(&moves[..i]);
        attempt.apply_all(&moves[i + 1..]);
        if cross_solved(&attempt) {
            moves.remove(i);
        } else {
            i += 1;
        }
    }
    moves
}

pub fn solve(cube: &Cube) -> Vec<Move> {
    let mut moves = random_search(cube, edges_oriented, 6, false);

    let mut oriented = *cube;
    oriented.apply_all(&moves);
    moves.extend(random_search(&oriented, cross_solved, 6, true));

    prune(cube, moves)
}
