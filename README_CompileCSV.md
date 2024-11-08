# CSV Compilation Program with File Selector

## Overview
The **CSV Compilation Program** is a Python script that combines data from multiple CSV files, selected manually by the user through a dialog box. The resulting compiled CSV file is saved with a name based on the earliest timestamp in the selected files.

## Usage
1. Run the program, which will open a file selection dialog.
2. Select the CSV files to compile.
3. The program saves the combined CSV file in the `compiled_data` folder.

## Output
The combined CSV file is named using the earliest timestamp from the selected files, with the format:

compiled_data_<earliest_date>.csv


## Dependencies
- Python 3
- Pandas
- Tkinter (typically installed with Python)

## File Format Requirements
Files should be named in the format:

<section>_<v_flow>_Run_<run_number>_<timestamp>.csv ```
where timestamp follows the format YYYYMMDD_HHMMSS.