# rubik

A Rust Rubik's cube solver that can solve any valid cube configuration using the CFOP method (Cross, F2L, OLL, PLL).

## Installation

### Prerequisites
- [Rust](https://www.rust-lang.org/tools/install) (edition 2024, Rust 1.85 or higher)

### Build

```bash
cargo build --release
```

The binary is written to `target/release/rubik`.

## Usage

```
rubik "<spin_sequence>" | --random [SPINS] [--display] [--copy] [--visual]
```

## Examples
### Solve a specific sequence
```bash
cargo run --release -- "R U2 F' D L2 B D' R' F2 U'"
```

### Generate and solve a random cube (20 random moves by default)
```bash
cargo run --release -- --random
```

### Generate and solve a random cube with specific number of moves
```bash
cargo run --release -- -r 42
```

### Display the cube before and after solving
```bash
cargo run --release -- -r -d
```

### Copy the solution to the clipboard
```bash
cargo run --release -- -r -c
```
Uses `pbcopy` on macOS, `clip` on Windows and `wl-copy`, `xclip` or `xsel` on Linux.

### Watch the cube in 3D
```bash
cargo run --release -- -r -v
```
Opens a window that plays the scramble on a solved cube, then the solution, animating every turn. The current move is highlighted in the move list.

| Control | Action |
| --- | --- |
| `Space` | Play / pause (restarts once solved) |
| `←` / `→` | Step one move back / forward |
| `↑` / `↓` | Faster / slower |
| `S` | Skip the scramble |
| `R` | Restart |
| Mouse drag / wheel | Orbit / zoom |
| `Esc` / `Q` | Quit |

The renderer uses [macroquad](https://github.com/not-fl3/macroquad), which loads OpenGL at runtime, so no system libraries are needed to build.

### Valid Moves
Each face can be rotated clockwise (no suffix), counterclockwise ('), or 180° (2). Supported faces:
- **U** - Upper face
- **D** - Down face
- **F** - Front face
- **B** - Back face
- **L** - Left face
- **R** - Right face

## How moves work

Each sticker is described by the position of its cubie (`x`, `y`, `z` in `{-1, 0, 1}`) and the normal of the face it is glued on. A face turn is the 90° rotation matrix around that face's normal (`src/geometry.rs`), applied to every sticker of the layer. These rotations are turned into sticker permutation tables once at startup, so applying a move is a single table lookup per sticker.

Whole-cube `y` rotations used in the algorithm files are resolved the same way: the inverse rotation matrix maps each face turn back to the face it actually affects.

## Tests and benchmark

```bash
cargo test --release
cargo run --release --bin benchmark -- 1000
```

The tests include reference states produced by the original Python implementation (`tests/fixtures/python_states.txt`).

## Algorithm Ressources
- [F2L](https://www.cubeskills.com/uploads/pdf/tutorials/f2l.pdf)
- [OLL](https://speedcubedb.com/a/3x3/OLL)
- [PLL](https://speedcubedb.com/a/3x3/PLL)
