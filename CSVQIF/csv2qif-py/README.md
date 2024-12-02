# CSV to QIF Converter in Python

This is a utility for converting CSV files into QIF (Quicken Interchange Format) files. It's implemented in Python and runs as a Python script.

The utility reads data from a specified CSV file and writes it to a new QIF file. It prints to the console details about the process, including the number of rows in the CSV file, the data in each row, and whether the file was written successfully.

## Prerequisites

- Python 3.x

This uses the following built-in Python modules, so no external installations are required:

- `csv` to read the CSV file, so no external libraries are required,
- `argparse` to parse command-line arguments,
- `datetime` to parse the date in the CSV file

## Installation

1. Clone this repository to your local machine.
2. Navigate to the directory where the repository was cloned.

## Usage

To convert a CSV file to QIF, run:

```
python csv2qif.py [input] [output]
```

Replace `[input]` with the path/filename of your CSV file, and `[output]` with the path/filename of the QIF file to be written.

Arguments:

- if no arguments are provided, the utility will look for a file named `input.csv` in the current directory, and write the output to a file named `output.qif` in the current directory.
- if one argument is provided, the utility will look for a file with that name in the current directory, and write the output to a file named `output.qif` in the current directory.
- if two arguments are provided, the utility will look for a file with the first name in the current directory, and write the output to a file with the second name in the current directory.

Example with 2 arguments:

```
python csv2qif.py .\input\input001.csv .\output\ouput001.qif
```

## CSV Format

The CSV file should be formatted as follows:

```
Date;Amount;Payee;Memo
22/06/21;-14.90;some payee name;some memo
```

- `Date`: the date of the transaction in `DD/MM/YY` format.
- `Amount`: the amount of the transaction, negative for expenses and positive for income. the amount must be in the format `###0.00` (no separators for thousands, and a dot for the decimal separator).
- `Payee`: the name of the payee or payor.
- `Memo`: a memo or note about the transaction (optional)

All fields should be separated by semicolons (`;`).

If that is not the format you want, then change the code in `csv2qif.py` to match your format.

## QIF Format

The resulting QIF file will be formatted like this:

```
!Type:Bank
D22/06/21
T-14.90
Psome payee name
Msome memo
^
```

- `D`: date of the transaction.
- `T`: amount of the transaction.
- `P`: payee of the transaction.
- `M`: memo about the transaction.
- `^`: end of the transaction record.

Each field begins with a single-letter code, followed by the data for that field. Transaction records are separated by caret (`^`) characters.

## Prefer using TypeScript?

If you prefer using TypeScript, check out [csv2qif-ts](https://github.com/fabrizionastri/csv2qif-ts)
