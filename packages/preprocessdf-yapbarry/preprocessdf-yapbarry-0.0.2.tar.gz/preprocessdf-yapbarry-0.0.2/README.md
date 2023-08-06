# Hello World

This is an project that contains preprocessing techniques for numpy arrays and panda dataframes.

## Installation

Run the following to install:

```python
pip install preprocessdf-yapbarry
```

## Usage

```python
from preprocessdf import preprocess

# Pass your dataframe (aka df) into the preprocess class
p = preprocess(df)

# Do standard scaling on your dataframe values
p.standard_scale()
```

## For developers

```bash
pip install -e .[dev]
```
