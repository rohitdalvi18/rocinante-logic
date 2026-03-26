# rocinante-logic

Determines the association between four characters aboard the Rocinante and four political systems using propositional logic.

## Characters & Systems

| Characters     | Political Systems       |
|----------------|------------------------|
| James Holden   | Belters                |
| Alex Kamal     | OPA                    |
| Joe Miller     | MCRN                   |
| Naomi Nagata   | United Nations         |

## Usage

```bash
python3 hero_villain.py
```

## How It Works

The solver encodes the puzzle as a propositional satisfiability problem:

- **16 boolean variables:** one for each (character, system) pair
- **Bijection constraints:** each character maps to exactly one system and vice versa
- **Knowledge base facts:** derived from the assignment 

All satisfying truth table assignments are enumerated and printed.

## Modules

| File              | Description                                      |
|-------------------|--------------------------------------------------|
| `hero_villain.py` | Main solver, encodes constraints, finds solutions |
| `logic.py`        | Propositional logic library |
