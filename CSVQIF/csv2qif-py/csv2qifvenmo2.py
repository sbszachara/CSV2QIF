import csv

# Define the QIF file header
QIF_HEADER = "!Type:Bank"

# Function to create a QIF entry for a transaction
def create_qif_entry(row):
    entry = []
    # Format date from "2024-10-01T16:55:24" to "MM/DD/YYYY"
    if row["Datetime"]:
        date_parts = row["Datetime"].split("T")[0].split("-")
        entry.append(f"D{date_parts[1]}/{date_parts[2]}/{date_parts[0]}")
    # Amount (remove parentheses for negatives)
    if row["Amount (total)"]:
        amount = row["Amount (total)"].replace("(", "-").replace(")", "").replace(",", "")
        entry.append(f"T{amount}")
    # Payee (use "To" or "From" as appropriate)
    if row["To"]:
        entry.append(f"P{row['To']}")
    elif row["From"]:
        entry.append(f"P{row['From']}")
    # Memo
    if row["Note"]:
        entry.append(f"M{row['Note']}")
    # End of transaction
    entry.append("^")
    return "\n".join(entry)

# Convert CSV to QIF
def convert_csv_to_qif(input_csv, output_qif):
    with open(input_csv, "r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(output_qif, "w", newline="", encoding="utf-8") as qif_file:
            # Write QIF header
            qif_file.write(QIF_HEADER + "\n")
            # Process each row in the CSV
            for row in csv_reader:
                if row["Datetime"]:  # Skip summary or empty rows
                    qif_entry = create_qif_entry(row)
                    qif_file.write(qif_entry + "\n")
    print(f"QIF file created: {output_qif}")

# File paths
input_csv_file = "/Users/stevenszachara/CSVQIF/csv2qif-py/input/VenmoStatement_Oct_2024.csv"  # Replace with your input CSV file
output_qif_file = "venmo_data.qif"  # Replace with your desired QIF output file

# Run the conversion
convert_csv_to_qif(input_csv_file, output_qif_file)
