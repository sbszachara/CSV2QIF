import csv
import argparse
from datetime import datetime


def print_row(rowNr, date, amount, description):
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<12} | "
        f"{str(amount):>10} | "
        f"{description:<50}"
    )


def csv2qif(input_file='input.csv', output_file='output.qif'):
    qif_data = ["!Type:Bank"]

    with open(input_file, 'r') as csv_file:
        rows = list(csv.reader(csv_file))
        
        # Skip the header row
        data_rows = rows[1:]
        
        print(f"Number of data rows in the CSV file: {len(data_rows)}")
        print("")
        print_row("Row", "Date", "Amount", "Description")
        print("-" * 80)

        rowNr = 1
        for row in data_rows:
            if not row[1]:  # Skip rows without a date
                continue
            
            # Extract relevant fields
            try:
                date = datetime.strptime(row[1], "%m/%d/%y")
                amount = row[4].replace("$", "").strip()
                if "-" in amount:
                    amount = f"-{amount.replace('-', '')}"  # Ensure correct formatting for negative amounts
                description = row[3].strip()

                # Print the row with the new date format
                print_row(rowNr, date.strftime("%m/%d/%Y"), amount, description)
                rowNr += 1

                # Create QIF data with MM/DD/YYYY format
                qif_data.extend([
                    f"D{date.strftime('%m/%d/%Y')}",
                    f"T{amount}",
                    f"P{description}",
                    "^"
                ])
            except Exception as e:
                print(f"Error processing row {rowNr}: {e}")
                continue

    # Write QIF file
    with open(output_file, 'w') as qif_file:
        qif_file.write('\n'.join(qif_data))
    print("\nQIF file created successfully")


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', default=['/Users/stevenszachara/CSVQIF/csv2qif-py/input/Citizen Sept and Oct 2024.csv', 'citizen_sept_oct_2024.qif'])
args = parser.parse_args()

if len(args.files) == 1:
    csv2qif(input_file=args.files[0])
else:
    csv2qif(*args.files)
