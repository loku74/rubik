# rubik

A Python-based Rubik's cube solver that can solve any valid cube configuration using the CFOP method (Cross, F2L, OLL, PLL).

## Installation

### Prerequisites
- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
cd rubik
uv sync
```

This creates a `.venv` and installs the locked dependencies from `uv.lock`.

## Usage

```
uv run main.py "<spin_sequence>" | --random [SPINS] [--display]
```


## Examples
### Solve a specific sequence
```bash
uv run main.py "R U2 F' D L2 B D' R' F2 U'"
```

### Generate and solve a random cube (20 random moves by default)
```bash
uv run main.py --random
```

### Generate and solve a random cube with specific number of moves
```bash
uv run main.py --random 42
```

### Valid Moves
Each face can be rotated clockwise (no suffix), counterclockwise ('), or 180° (2). Supported faces:
- **U** - Upper face
- **D** - Down face
- **F** - Front face
- **B** - Back face
- **L** - Left face
- **R** - Right face

## Benchmark

```bash
uv run benchmark.py
```

## Algorithm Ressources
- [F2L](https://www.cubeskills.com/uploads/pdf/tutorials/f2l.pdf)
- [OLL](https://speedcubedb.com/a/3x3/OLL)
- [PLL](https://speedcubedb.com/a/3x3/PLL)
