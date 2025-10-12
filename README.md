# rubik

A Python-based Rubik's cube solver that can solve any valid cube configuration using the CFOP method (Cross, F2L, OLL, PLL).

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository to your local machine

2. Navigate to the project directory:
   ```bash
   cd rubik
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv .
   ```

4. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source bin/activate
     ```
   - On Windows:
     ```powershell
     Scripts\activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```
python3 main.py "<spin_sequence>" | random | random:<spins>
```


## Examples
### Solve a specific sequence
```bash
python3 main.py "R U2 F' D L2 B D' R' F2 U'"
```

### Generate and solve a random cube (20 random moves by default)
```bash
python3 main.py random
```

### Generate and solve a random cube with specific number of moves
```bash
python3 main.py random:42
```

### Valid Moves
Each face can be rotated clockwise (no suffix), counterclockwise ('), or 180° (2). Supported faces:
- **U** - Upper face
- **D** - Down face
- **F** - Front face
- **B** - Back face
- **L** - Left face
- **R** - Right face

## Deactivating Virtual Environment

When you're done using the program, you can deactivate the virtual environment:
```bash
deactivate
```

## Algorithm Ressources
- [F2L](https://www.cubeskills.com/uploads/pdf/tutorials/f2l.pdf)
- [OLL](https://speedcubedb.com/a/3x3/OLL)
- [PLL](https://speedcubedb.com/a/3x3/PLL)
