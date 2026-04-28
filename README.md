# HSC Result Analysis

This project analyzes Higher Secondary Certificate (HSC) college results from 2021 to 2025 and provides an interactive Streamlit dashboard for comparing college-wise performance by year and stream.

## Project Overview

The repository contains raw yearly HSC result files, a combined CSV dataset, an exploratory notebook, and a Streamlit application.

Main capabilities:

- Compare college-wise pass percentages for a selected year and stream.
- View appeared vs passed student counts for a selected college over time.
- Track pass percentage trends for a selected college.
- Review average pass percentage performance across the latest five-year range.
- Inspect filtered raw data directly from the dashboard.

## Project Structure

```text
HSC/
|-- app.py
|-- EDA&FE.ipynb
|-- combined_hsc_data.csv
|-- README.md
`-- Data/
    |-- HSC2021.pdf
    |-- HSC2021.xlsx
    |-- HSC2022.pdf
    |-- HSC2022.xlsx
    |-- HSC2023.pdf
    |-- HSC2023.xlsx
    |-- HSC2024.pdf
    |-- HSC2024.xlsx
    |-- HSC2025.pdf
    `-- HSC2025.xlsx
```

## Files

### `app.py`

The main Streamlit dashboard.

It loads `combined_hsc_data.csv`, applies sidebar filters for year and stream, and renders:

- A horizontal Plotly bar chart of college pass percentages.
- A college performance timeline showing candidates appeared and total pass counts.
- A pass percentage trend chart for the selected college.
- A detailed performance table with yearly counts and grade categories.
- Stream-wise tabs for average pass percentage across the latest five-year range.
- An expandable raw data table for the currently selected year and stream.

### `EDA&FE.ipynb`

The exploratory data analysis and feature engineering notebook.

It includes code for:

- Reading Excel files from the `Data/` folder.
- Extracting the year from each file name.
- Combining yearly Excel datasets into `combined_hsc_data.csv`.
- Standardizing selected college names.
- Checking year-wise candidate totals.
- Creating Plotly charts for college comparison, stream registrations, and pass percentage trends.

### `combined_hsc_data.csv`

The processed dataset used by the Streamlit app.

Current dataset summary:

- Rows: 168
- Years: 2021, 2022, 2023, 2024, 2025
- Streams: `ARTS`, `COMMERCE`, `HSC.VOC`, `SCIENCE`, `TECH.SCI`
- Unique colleges: 20

### `Data/`

Contains the original HSC result source files in PDF and Excel format for each year from 2021 to 2025.

## Dataset Columns

`combined_hsc_data.csv` contains the following columns:

| Column | Description |
| --- | --- |
| `Name of the college` | College or junior college name |
| `Stream` | Academic stream |
| `Candidates Registerd` | Number of registered candidates |
| `Candidates Appeared` | Number of candidates who appeared |
| `Distin-ction` | Number of students with distinction |
| `Grade I` | Number of students with Grade I |
| `Grade II` | Number of students with Grade II |
| `Pass Grade` | Number of students with pass grade |
| `Total Pass` | Total number of passed students |
| `Pass Percent` | Pass percentage |
| `Year` | Result year |

## Requirements

Recommended Python packages:

```bash
pip install streamlit pandas plotly openpyxl notebook ipywidgets
```

Core dashboard dependencies:

- `streamlit`
- `pandas`
- `plotly`

Notebook/data preparation dependencies:

- `openpyxl`
- `notebook` or `jupyter`
- `ipywidgets`

## How to Run the Dashboard

From the project folder, run:

```bash
streamlit run app.py
```

The dashboard will open in a browser. Use the sidebar to select:

- Year
- Stream

Then select a college in the timeline section to view historical performance.

## How to Regenerate the Combined CSV

Open `EDA&FE.ipynb` and run the data loading cells that read:

```python
files = [
    "Data/HSC2021.xlsx",
    "Data/HSC2022.xlsx",
    "Data/HSC2023.xlsx",
    "Data/HSC2024.xlsx",
    "Data/HSC2025.xlsx"
]
```

The notebook reads each Excel file, adds a `Year` column based on the file name, concatenates all yearly data, and writes:

```text
combined_hsc_data.csv
```

After regenerating the CSV, restart the Streamlit app so it reloads the updated data.

## Dashboard Sections

### College-wise Pass Percentage

Shows a ranked horizontal bar chart for the selected year and stream.

### College Performance Timeline

Shows historical performance for one selected college in the selected stream:

- Candidates appeared vs total passed
- Pass percentage trend
- Year-wise performance details

### Average Pass Percentage

Calculates average pass percentage by college and stream for the latest five-year range in the data.

### Raw Data

Displays the filtered dataset for the selected year and stream.

## Notes

- The app expects `combined_hsc_data.csv` to be present in the same folder as `app.py`.
- The `Year` column is converted to integer before filtering and charting.
- Some source column names contain spelling or formatting issues from the original data, such as `Candidates Registerd` and `Distin-ction`; the app uses these names as-is.
- The notebook contains a college-name mapping step for standardization. If you regenerate the CSV and want standardized names reflected in the dashboard, ensure the mapping is applied before saving the CSV.
