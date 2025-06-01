# LOLCODE Interpreter and Compiler Project

## Overview

A Python-based interpreter and compiler for the **LOLCODE** esoteric programming language. This project aims to demonstrate the fundamental concepts of language processing, including lexical analysis, parsing, and execution generation.

## Features

* **Lexer:** Converts LOLCODE source code into a stream of tokens.
* **Parser:** Builds an Abstract Syntax Tree (AST) from the token stream.
* **Interpreter:** Executes the LOLCODE program directly from the AST.

### Design document with more information [here]()


##  Getting Started

### Prerequisites

Make sure you have **Python 3.x** installed on your system.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saveniukk/lolcode-interpreter
    cd lolcode-interpreter
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To execute a LOLCODE program, simply run the `main.py` script and provide the path to your `.lol` file:

```bash
python src/main.py examples/hello_world.lol
```
Example:

```python
# examples/hello_world.lol
HAI
VISIBLE "OHAI WORLD!"
KTHXBYE
```

Running the command above for hello_world.lol would output:
```bash
OHAI WORLD!
```

### Project Structure

```
lolcode-interpreter/
├── src/
│   ├── __init__.py           # Makes `src` a Python package
│   ├── lexer.py              # Defines `Token` and `Lexer` classes for tokenization
│   ├── parser.py             # Implements `Parser` class and grammar rules to build AST
│   ├── ast_nodes.py          # Contains definitions for all Abstract Syntax Tree node classes
│   ├── interpreter.py        # Core logic for executing the AST
│   ├── compiler.py           # (Future/Optional) Logic for code generation
│   └── main.py               # Entry point: handles file reading, orchestrates lexer, parser, and interpreter
├── tests/
│   ├── __init__.py           # Makes `tests` a Python package
│   ├── test_lexer.py         # Unit tests for the lexical analyzer
│   ├── test_parser.py        # Unit tests for the syntax analyzer
│   └── test_interpreter.py   # Unit and integration tests for the interpreter
├── examples/
│   ├── hello_world.lol       # Simple "Hello World" program
│   ├── variables.lol         # Demonstrates variable declaration and assignment
│   ├── loops.lol             # Example showing loop constructs
│   └── conditional.lol       # Illustrates conditional statements
├── requirements.txt          # Lists Python dependencies
└── README.md                 # Main README file
```

## Testing
We use pytest for our test suite. To run the tests:

```bash
pytest tests/
```