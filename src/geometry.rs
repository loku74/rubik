//! Integer 3D geometry used to describe the cube.
//!
//! Axes: `x` points to the right face, `y` to the up face and `z` to the front face.

use std::ops::Mul;

pub type Vec3 = [i32; 3];

pub fn dot(a: Vec3, b: Vec3) -> i32 {
    a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
}

/// A 3x3 integer matrix. Only rotations by multiples of 90° are ever built,
/// so every entry stays in `{-1, 0, 1}` and no rounding is involved.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Mat3(pub [[i32; 3]; 3]);

impl Mat3 {
    pub const IDENTITY: Mat3 = Mat3([[1, 0, 0], [0, 1, 0], [0, 0, 1]]);

    /// Quarter turn that is clockwise when looking at the plane from the tip of `axis`
    /// (i.e. a -90° rotation around `axis`, which must be a unit vector).
    ///
    /// Rodrigues' formula with θ = -90° reduces to `M = a·aᵀ - [a]×`.
    pub fn quarter_turn(axis: Vec3) -> Mat3 {
        let [x, y, z] = axis;
        let cross = [[0, -z, y], [z, 0, -x], [-y, x, 0]];
        let mut m = [[0; 3]; 3];
        for (i, row) in m.iter_mut().enumerate() {
            for (j, cell) in row.iter_mut().enumerate() {
                *cell = axis[i] * axis[j] - cross[i][j];
            }
        }
        Mat3(m)
    }

    pub fn pow(self, n: u8) -> Mat3 {
        (0..n).fold(Mat3::IDENTITY, |acc, _| acc * self)
    }

    /// For a rotation matrix the transpose is the inverse.
    pub fn transpose(self) -> Mat3 {
        let mut m = [[0; 3]; 3];
        for (i, row) in m.iter_mut().enumerate() {
            for (j, cell) in row.iter_mut().enumerate() {
                *cell = self.0[j][i];
            }
        }
        Mat3(m)
    }

    pub fn apply(self, v: Vec3) -> Vec3 {
        let m = self.0;
        [dot(m[0], v), dot(m[1], v), dot(m[2], v)]
    }
}

impl Mul for Mat3 {
    type Output = Mat3;

    fn mul(self, other: Mat3) -> Mat3 {
        let mut m = [[0; 3]; 3];
        for (i, row) in m.iter_mut().enumerate() {
            for (j, cell) in row.iter_mut().enumerate() {
                *cell = (0..3).map(|k| self.0[i][k] * other.0[k][j]).sum();
            }
        }
        Mat3(m)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn quarter_turn_around_up_moves_front_to_left() {
        let u = Mat3::quarter_turn([0, 1, 0]);
        assert_eq!(u.apply([0, 0, 1]), [-1, 0, 0]);
        assert_eq!(u.apply([1, 0, 0]), [0, 0, 1]);
    }

    #[test]
    fn four_quarter_turns_are_identity() {
        for axis in [[1, 0, 0], [0, -1, 0], [0, 0, 1]] {
            let m = Mat3::quarter_turn(axis);
            assert_eq!(m.pow(4), Mat3::IDENTITY);
            assert_eq!(m * m.transpose(), Mat3::IDENTITY);
        }
    }
}
