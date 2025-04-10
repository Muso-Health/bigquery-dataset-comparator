import argparse
from dataset_comparator import DatasetComparator
from google.cloud import bigquery


def main():
    # Instantiate the argument parser
    parser = argparse.ArgumentParser(
        description="Compare two BigQuery datasets."
    )

    # Add the arguments
    parser.add_argument(
        "--old_project", required=True, help="The old project ID."
    )
    parser.add_argument(
        "--old_dataset", required=True, help="The old dataset ID."
    )
    parser.add_argument(
        "--new_project", required=True, help="The new project ID."
    )
    parser.add_argument(
        "--new_dataset", required=True, help="The new dataset ID."
    )
    parser.add_argument(
        "--output_file", required=False, help="The output file path.", default="output.txt"
    )
    # Parse the arguments
    args = parser.parse_args()

    # Instantiate the BigQuery client
    client = bigquery.Client(project=args.old_project)

    # Instantiate the DatasetComparator
    comparator = DatasetComparator(
        client,
        args.old_project,
        args.old_dataset,
        args.new_project,
        args.new_dataset,
    )

    # Call the compare_tables method
    comparison_result = comparator.compare_tables()

    # Print the difference if any
    has_same_tables = True
    output_string = ""
    for table_id, result in comparison_result.items():
        if not result["are_equal"]:
            output_string += result["differences"] + "\n"
            has_same_tables = False

    strong_comparison_result = comparator.compare_common_tables()
    has_same_fields = True
    for table_id, result in strong_comparison_result.items():
        if not result["are_equal"]:
            output_string += result["differences"] + "\n"
            has_same_fields = False

    if has_same_tables:
        output_string += f"All tables in {args.old_project}.{args.old_dataset} are in {args.new_project}.{args.new_dataset}\n"
    if has_same_fields:
        output_string += f"All fields in tables in {args.old_project}.{args.old_dataset} are contained in the same table of {args.new_project}.{args.new_dataset}\n"

    verification_result = comparator.verify_old_data_record_are_in_new_table()
    result = DatasetComparator.format_results('verify_all_present', verification_result)
    output_string += result

    with open(args.output_file, "w") as f:
        f.write(output_string)
    print(f"Results written to {args.output_file}")

if __name__ == "__main__":
    main()