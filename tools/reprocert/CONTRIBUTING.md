# Contributing

ReproCert welcomes narrowly scoped, test-backed contributions.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
python -m build
```

## Contribution rules

- preserve the distinction between claim failure, inconclusive evidence, and execution error;
- do not add secret/environment-value capture;
- do not introduce shell execution for claim commands;
- include tests for parser, path-boundary, and verdict changes;
- describe trust-boundary changes explicitly;
- do not claim scientific validation or producer authenticity from local certificate verification.
