import csv
import os
from datetime import datetime

def convert_all_csv_files(output_suffix='_output.csv'):
    """
    Converts all CSV files in the current directory to the desired format.
    Each output file is named by appending '_output.csv' to the original filename (e.g., 'NVDA.csv' -> 'NVDA_output.csv').

    The output CSV files do not contain a header row.
    """
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List all files in the directory
    for filename in os.listdir(script_dir):
        # Process only .csv files and exclude output files to prevent re-processing
        if filename.lower().endswith('.csv') and not filename.endswith(output_suffix):
            input_file = os.path.join(script_dir, filename)
            symbol = os.path.splitext(filename)[0]
            output_filename = f"{symbol}{output_suffix}"
            output_file = os.path.join(script_dir, output_filename)

            print(f"Processing '{filename}' -> '{output_filename}'")

            with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
                 open(output_file, 'w', newline='', encoding='utf-8') as outfile:

                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                # Skip the header row in the input CSV
                header = next(reader, None)
                if header is None:
                    print(f"Warning: '{filename}' is empty. Skipping.")
                    continue

                for row_number, row in enumerate(reader, start=2):  # Start at 2 to account for header
                    if not row:
                        print(f"Skipping empty row {row_number} in '{filename}'.")
                        continue  # Skip empty rows

                    try:
                        # Unpack the input row
                        date_str, close_last, volume, open_price, high, low = row

                        # Convert date from mm/dd/yyyy to yyyymmdd
                        date_obj = datetime.strptime(date_str.strip(), '%m/%d/%Y')
                        formatted_date = date_obj.strftime('%Y%m%d')

                        # Remove '$' and ',' from numeric fields
                        close_last = close_last.replace('$', '').replace(',', '').strip()
                        open_price = open_price.replace('$', '').replace(',', '').strip()
                        high = high.replace('$', '').replace(',', '').strip()
                        low = low.replace('$', '').replace(',', '').strip()
                        volume = volume.replace('$', '').replace(',', '').strip()

                        # Create the output row in the required order
                        output_row = [
                            symbol,
                            formatted_date,
                            open_price,
                            high,
                            low,
                            close_last,
                            volume
                        ]

                        writer.writerow(output_row)

                    except ValueError as ve:
                        print(f"Error processing row {row_number} in '{filename}': {ve}. Skipping row.")
                    except IndexError:
                        print(f"Error: Row {row_number} in '{filename}' does not have enough columns. Skipping row.")

            print(f"Finished processing '{filename}'. Output saved to '{output_filename}'.\n")

    print("All CSV files have been processed.")

# Example usage
if __name__ == "__main__":
    convert_all_csv_files()