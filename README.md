# Calculator

Calculator Pro — a modern, featureful desktop calculator built with Python and Tkinter. It provides a polished GUI, basic and some scientific operations, memory and history, keyboard support, and a compact, well-documented single-file implementation (calculator.py).

## Features

- Graphical desktop application (Tkinter) with a modern dark theme
- Basic arithmetic: +, -, ×, ÷, %
- Scientific helpers: square root (√), square (x²)
- Memory operations: MC, MR, M+, M-
- Calculation history (last 50 entries)
- Keyboard support (numbers, operators, Enter for =, Backspace, Escape/"c" for AC)
- Clipboard copy of result and a small animated startup

## Requirements

- Python 3.8 or newer
- Tkinter (usually included with standard Python distributions)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/nadimicherlareddykumar/calculator.git
cd calculator
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

## Running the app

Start the GUI by running:

```bash
python calculator.py
```

This opens the Calculator Pro window. Enter expressions using the on-screen buttons or your keyboard. Press Enter to evaluate, Backspace to delete, and Escape or the "c" key to clear.

## Programmatic usage

The project is primarily a GUI app, but the Calculator class can be instantiated from Python if you need to integrate or automate it. Example:

```python
import tkinter as tk
from calculator import Calculator

root = tk.Tk()
calc = Calculator(root)

# Set an expression programmatically
calc.expression = "2+3*4"
# Trigger evaluation (uses the same logic as the = button)
calc.on_button_click('=')

# Result is available in calc.expression
print(calc.expression)  # -> "14"

# Run the GUI loop if you want to show the window
# root.mainloop()
```

Note: The class exposes internal methods (e.g., on_button_click) rather than a dedicated evaluate() API. If you want a clean programmatic API, I can add a safe evaluate(expression:str) function that returns results without needing a Tk root.

## Safety note

calculator.py uses Python's eval() internally after replacing display symbols (× → *, ÷ → /). While input is constrained via the GUI buttons, if you import and use eval on untrusted input there is risk. I can replace eval with a safe expression parser (for example, using the ast module or a small shunting-yard parser) if you want the project hardened for untrusted inputs.

## Keyboard shortcuts

- Enter: evaluate (=)
- Backspace: delete (⌫)
- Escape or 'c': clear (AC)
- Ctrl+C: from the Edit menu copy result to clipboard

## Project structure

- calculator.py — main GUI implementation
- README.md — this file
- LICENSE — project license (MIT)

## Contributing

Contributions are welcome. Suggested next steps I can do and commit to a branch or main (your choice):

- Add a dedicated, safe evaluate() API for programmatic use
- Replace eval with a safe parser
- Add unit tests (pytest)
- Add GitHub Actions for CI

If you prefer, I can create a branch and open a PR with these changes instead of pushing straight to main.

## License

This repository is licensed under the MIT License. See LICENSE for details.
