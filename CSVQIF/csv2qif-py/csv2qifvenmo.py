import csv
import argparse
from datetime import datetime


def print_row(rowNr, date, amount, payee, memo):
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<19} | "
        f"{str(amount):>10} | "
        f"{payee:<20} | "
        f"{memo:<30}"
    )


def csv2qif(input_file='input.csv', output_file='output.qif'):
    qif_data = ["!Type:Bank"]

    with open(input_file, 'r') as csv_file:
        rows = list(csv.reader(csv_file, delimiter=','))
        
        # Skip the header lines and find actual data start
        data_start_index = next(i for i, row in enumerate(rows) if row[1].strip().lower() == "id")
        data_rows = rows[data_start_index + 1:]
        
        print(f"Number of data rows in the CSV file: {len(data_rows)}")
        print("")
        print_row("Row", "Date", "Amount", "Payee", "Memo")
        print("-" * 80)

        rowNr = 1
        for row in data_rows:
            if not row[1]:  # Skip empty rows
                continue
            
            # Extract relevant fields
            try:
                date = datetime.strptime(row[2], "%Y-%m-%dT%H:%M:%S")
                amount = row[8].replace("+", "").replace("$", "").strip()
                if "-" in amount:
                    amount = f"-{amount.replace('-', '')}"  # Ensure correct formatting for negative amounts
                payee = row[6].strip() if row[6] else row[7].strip()
                memo = row[5].strip() if row[5] else ""

                # Print the row with the new date format
                print_row(rowNr, date.strftime("%m/%d/%Y"), amount, payee, memo)
                rowNr += 1

                # Create QIF data with MM/DD/YYYY format
                qif_data.extend([
                    f"D{date.strftime('%m/%d/%Y')}",
                    f"T{amount}",
                    f"P{payee}",
                    f"M{memo}",
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
parser.add_argument('files', nargs='*', default=['/Users/stevenszachara/CSVQIF/csv2qif-py/input/VenmoStatement_Sep_2024.csv', 'venmo_sep_2024.qif'])
args = parser.parse_args()

if len(args.files) == 1:
    csv2qif(input_file=args.files[0])
else:
    csv2qif(*args.files)
