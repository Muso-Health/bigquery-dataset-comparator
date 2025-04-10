class DatasetComparator:
    def __init__(self, client, old_project, old_dataset, new_project, new_dataset):
        self.client = client
        self.old_project = old_project
        self.old_dataset = old_dataset
        self.new_project = new_project
        self.new_dataset = new_dataset
        self.old_tables = self.get_old_tables()
        self.new_tables = self.get_new_tables()

    def get_tables(self, project, dataset_id):
        print(f"Getting tables for {project}.{dataset_id}")
        dataset_ref = self.client.dataset(dataset_id, project=project)
        try:
            dataset = self.client.get_dataset(dataset_ref)
        except Exception as e:
            print(f"Error getting dataset {project}.{dataset_id}: {e}")
            return {}
        tables = {}
        for table_item in self.client.list_tables(dataset):
            print(f"Getting table {project}.{dataset_id}.{table_item.table_id}")
            table_ref = dataset_ref.table(table_item.table_id)
            try:
                table = self.client.get_table(table_ref)
                tables[table.table_id] = table
                print(f"Table {project}.{dataset_id}.{table_item.table_id} retrieved successfully")
            except Exception as e:
                print(f"Error getting table {project}.{dataset_id}.{table_item.table_id}: {e}")
        return tables

    def get_old_tables(self):
        return self.get_tables(self.old_project, self.old_dataset)

    def  get_new_tables(self):
        return self.get_tables(self.new_project, self.new_dataset)

    def common_tables(self):
        return set( self.old_tables.keys()) & set(self.new_tables.keys())

    def compare_common_tables(self):
        comparison_results = {}
        common_tables = self.common_tables()
        for table_id in common_tables:
            old_table = self.old_tables[table_id]
            new_table = self.new_tables[table_id]

            old_schema = {field.name: field.field_type for field in old_table.schema}
            new_schema = {field.name: field.field_type for field in new_table.schema}

            are_equal = True
            differences = []

            for field_name, old_field_type in old_schema.items():
                if field_name not in new_schema:
                    are_equal = False
                    differences.append(
                        f"Field '{field_name}' is present in {self.old_project}.{old_table}.{table_id} but not in {self.new_project}.{self.new_dataset}.{table_id}"
                    )
                elif old_field_type != new_schema[field_name]:
                    are_equal = False
                    differences.append(
                        f"Field '{field_name}' has type '{old_field_type}' in {self.old_project}.{old_table}.{table_id} but type '{new_schema[field_name]}' in {self.new_project}.{self.new_dataset}.{table_id}"
                    )
            if are_equal:
                comparison_results[table_id] = {'are_equal': True, 'differences': None}
            else:
                comparison_results[table_id] = {'are_equal': False, 'differences': differences}

        return comparison_results

    def compare_tables(self):
        comparison_results = {}
        for table_id in self.old_tables:
            if table_id in self.new_tables:
                comparison_results[table_id] = {'are_equal': True, 'differences': None}
            else:
                comparison_results[table_id] = {'are_equal': False, 'differences': f"Table '{table_id}' is present in {self.old_project}.{self.old_dataset} but not in {self.new_project}.{self.new_dataset} "}
        return comparison_results

    def verify_old_data_record_are_in_new_table(self):
        verification_results = {}
        common_tables = self.common_tables()
        for table_name in common_tables:
            old_table_id = f"`{self.old_project}.{self.old_dataset}.{table_name}`"
            new_table_id = f"`{self.new_project}.{self.new_dataset}.{table_name}`"

            verification_results[table_name] = {'all_present': True, 'missing_records_sample': None, 'error': None}

            try:
                # Construct a query to find records in old_table that are NOT in new_table
                # This assumes that the order of columns might be different, so we select all
                # columns and compare row by row. For large tables, this can be slow.
                # Consider adding a unique key column to the WHERE clause for better performance
                # if one exists.

                # Note: The EXCEPT DISTINCT operator is used to find the difference in rows.
                query = f"""
                           SELECT * FROM {old_table_id}
                           EXCEPT DISTINCT
                           SELECT * FROM {new_table_id}
                           LIMIT 5
                       """
                query_job = self.client.query(query)
                missing_records = list(query_job.result())

                if missing_records:
                    verification_results[table_name]['all_present'] = False
                    verification_results[table_name]['missing_records_sample'] = [dict(row) for row in missing_records]

            except Exception as e:
                verification_results[table_name]['error'] = f"Error comparing records for {table_name}: {e}"

        return verification_results

    @staticmethod
    def format_results(result_type: str, record_verification: dict) -> str:
        output = ""
        if result_type == "verify_all_present":
            if record_verification:
                output += "Record Verification Results:\n"
                for table_name, result in record_verification.items():
                    output += f"\nTable: {table_name}\n"
                    if result['error']:
                        output += f"  Error: {result['error']}\n"
                    elif result['all_present']:
                        output += "  All records from dataset_1 are present in dataset_2.\n"
                    else:
                        output += "  Not all records from dataset_1 are present in dataset_2.\n"
                        if result['missing_records_sample']:
                            output += "  Sample of missing records from dataset_1:\n"
                            for record in result['missing_records_sample']:
                                output += f"    - {record}\n"
                        else:
                            output += "  Could not retrieve a sample of missing records.\n"
            else:
                output += "Record verification failed or no common tables found.\n"
        return output