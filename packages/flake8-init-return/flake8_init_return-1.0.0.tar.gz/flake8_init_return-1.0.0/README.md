flake8-init-return
================

flake8 plugin which forbids not having a return type on a class' `__init__` function

## installation

`pip install flake8-init-return`

## flake8 codes

| Code   | Description                         |
|--------|-------------------------------------|
| FIR100 | missing return value for initalizer |

## rationale

As [PEP-484](https://peps.python.org/pep-0484/) says, a class' `__init__`
functions ought to be annotated with `-> None`. This plugin makes sure
that they are annotated, but it leaves up the type checking for another
tool.

This might be useful when a type checker is not yet integrated
into a project's development flow.


## as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions

Sample `.pre-commit-config.yaml`:

```yaml
-   repo: https://github.com/pycqa/flake8
    rev: 3.8.1
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-init-return==1.0.0]
```
