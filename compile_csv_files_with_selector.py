import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

# Date format in the CSV filenames (matching the timestamp format in `Point Marking Program`)
DATE_FORMAT = "%Y%m%d_%H%M%S"


def compile_csv_files_with_selector(output_folder: str = 'compiled_data'):
    # Set up tkinter root for file dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Prompt user to select files
    file_paths = filedialog.askopenfilenames(
        title="Select CSV files to combine",
        filetypes=[("CSV files", "*.csv")],
        initialdir=os.getcwd()
    )

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List to store dataframes from selected files
    compiled_data = []
    first_date_in_range = None  # To determine output filename based on earliest date

    # Process each selected file
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        try:
            # Extract the date and time part from the filename
            # Assuming filename format: <section>_<v_flow>_Run_<run_number>_<timestamp>.csv
            parts = filename.split('_')
            timestamp_str = f"{parts[-2]}_{parts[-1].replace('.csv', '')}"  # Combine date and time

            # Parse the combined timestamp
            file_datetime = datetime.strptime(timestamp_str, DATE_FORMAT)

            # Read CSV and append to compiled data list
            df = pd.read_csv(file_path)
            compiled_data.append(df)

            # Track the earliest date for naming the output file
            if first_date_in_range is None or file_datetime < first_date_in_range:
                first_date_in_range = file_datetime
        except Exception as e:
            print(f"Skipping file {filename} due to error: {e}")

    # Concatenate all selected dataframes
    if compiled_data:
        compiled_df = pd.concat(compiled_data, ignore_index=True)
        # Create the output filename based on the earliest date
        output_filename = f'compiled_data_{first_date_in_range.strftime(DATE_FORMAT)}.csv'
        output_path = os.path.join(output_folder, output_filename)

        # Save the concatenated dataframe to the output file
        compiled_df.to_csv(output_path, index=False)
        print(f"Compiled data saved to {output_path}")
    else:
        print("No valid files were selected.")


# Example usage
compile_csv_files_with_selector()
