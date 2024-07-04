import pandas as pd

# Load the entire CSV file into a DataFrame
file_path = 'output_handover_scenario_training3_cleaned.csv'
my_data = pd.read_csv(file_path)

# Define the required cell_ids range (0 to 6, assuming there are 7 cell_ids in total)
required_cell_ids = set(range(7))

# Create an empty DataFrame to store processed data
processed_data = pd.DataFrame()
last_known_radius = {cell_id: 0 for cell_id in required_cell_ids}
# Group by 't' and process each group
for t_value, group in my_data.groupby('t'):
    # Find existing cell_ids in the group
    existing_cell_ids = set(group['cell_id'])
    # Find missing cell_ids
    missing_cell_ids = required_cell_ids - existing_cell_ids

    # Create rows for missing cell_ids
    missing_rows = []
    for missing_cell_id in missing_cell_ids:
        new_row = {
            't': t_value,
            'cell_id': missing_cell_id,
            'cell_load': 0,
            'cell_barring': 0,
            'traffic_steering': 0,
            'cell_radius': last_known_radius[missing_cell_id],
        }
        missing_rows.append(new_row)

    for cell_id in existing_cell_ids:
        last_known_radius[cell_id] = group.loc[group['cell_id'] == cell_id, 'cell_radius'].values[0]
    # Convert missing rows to DataFrame and concatenate with the group
    missing_rows_df = pd.DataFrame(missing_rows)
    group = pd.concat([group, missing_rows_df], ignore_index=True)
    group = group.sort_values(by='cell_id')

    # Append processed group to processed_data DataFrame
    processed_data = pd.concat([processed_data, group], ignore_index=True)

# Save the processed data to a new CSV file
# processed_data.to_csv('output_handover_scenario_training_processed.csv', index=False)
processed_data.to_csv('output_handover_scenario_training3_processed.csv', index=False)

print("Processed data has been saved to 'output_handover_scenario_training3_processed.csv'")
