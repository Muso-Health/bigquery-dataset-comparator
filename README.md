# BigQuery Dataset Comparator

This project provides a tool to compare two BigQuery datasets, checking for differences in tables, schemas, and data records. It's designed to help you ensure data consistency between different

 environments or versions of your data.

## Features

*   **Table Comparison:** Checks if all tables in one dataset exist in another.
*   **Schema Comparison:** Compares the schemas of tables with the same name, identifying differences in field names and types.
*   **Data Record Verification:** Verifies if all records from one dataset are present in another.
*   **Command-Line Interface:** Accepts project and dataset names as command-line arguments for flexibility

.
*   **Output to File:** Writes the comparison results to a specified output file.
* **Clear output** The output is clear and easy to understand.

## Prerequisites

*   **Python 3.8+:** This project is written in Python and requires Python 3.8 or a later version.
*   **Google Cloud SDK:** You need to have the Google Cloud SDK installed and configured with appropriate credentials to access BigQuery.
*   **Google Cloud Project:** You need to have a Google Cloud Project with BigQuery enabled.
*   **BigQuery Datasets:** You need to have two


## Usage

The script `main.py` is the entry point for the comparison. You can run it from the command line with the following arguments:


*   `--old_project`: The ID of the project containing the old dataset. (Required)
*   `--old_dataset`: The ID of the old dataset. (Required)
*   `--new_project`: The ID of the project containing the new dataset. (Required)
*   `--new_dataset`: The ID of the new dataset. (Required)
*   `--output_file`: The path to the output file where the results will be written. (Optional, defaults to `output.txt`)

**Example:**


This command will compare the `musoapp` dataset in the `musohealth` project with the `musoapp_old_instance` dataset in the `muso-health-cdi` project and write the results to `comparison_results.txt`.

## Output

The output file will contain a detailed report of the comparison, including:

* **Table Differences:**
    *   Tables present in the old dataset but not in the new dataset.
*   **Schema Differences:**
    *   For tables with the same name, weather all fields in the table of the old dataset are in the table of the same data set and have same data types.
*   **Data Record Verification:**
    *   Whether all records from the  old dataset are present in the new dataset.
    *   A sample of missing records (if any).
    *   Any errors encountered during the comparison.
* **Summary**
    * A summary of the comparison.

## Project Structure

*   `main.py`: The main script for running the comparison.
*   `dataset_comparator.py`: Contains the `DatasetComparator` class, which handles the comparison logic.
*   `requirements.txt`: Lists the required Python packages.
*   `README.md`: This file.

## Contributing

If you'd like to contribute to  this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

## License

 MIT License