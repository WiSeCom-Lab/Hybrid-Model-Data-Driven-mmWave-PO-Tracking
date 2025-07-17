import pandas as pd
import numpy as np
import os

def create_combined_dataset_v2(ap_pos_file, ue_pos_file, info_selected_file):
    # Read AP position (remains the same)
    with open(ap_pos_file, 'r') as f:
        f.readline() # Skip header
        ap_line = f.readline().strip().split()
        ap_x, ap_y, ap_z = float(ap_line[0]), float(ap_line[1]), float(ap_line[2])

    # Read UE positions
    # Assuming UE_pos.txt has a header and then space-separated values
    ue_df = pd.read_csv(ue_pos_file, sep=' ', header=0, names=['UE_x', 'UE_y', 'UE_z'], skiprows=[0])

    # Read Info_selected data, carefully handling the '<ue>' separator
    # We'll read it line by line and filter out the separator
    channel_data = []
    with open(info_selected_file, 'r') as f:
        f.readline() # Skip initial header/comment if any (like "46.96580000 9.33329004E-08 ...")
        for line in f:
            line = line.strip()
            if line and line != '<ue>': # Skip empty lines and the '<ue>' separator
                parts = line.split()
                try:
                    # Convert parts to float, assuming all are numeric
                    channel_data.append([float(p) for p in parts])
                except ValueError:
                    # Handle cases where a line might not be purely numeric if unexpected data exists
                    print(f"Skipping non-numeric line in info_selected: {line}")
                    continue

    info_df = pd.DataFrame(channel_data, columns=[
        'Channel_Phase_deg', 'ToA_s', 'Channel_Gain_dBm',
        'DL_Azimuth_AoA_deg', 'DL_Elevation_AoA_deg',
        'Azimuth_AoD_deg', 'Elevation_AoD_deg'
    ])

    # --- Adjusting for 1 UE_pos row to 25 Info_selected rows ---
    # We expect info_df to have 25 times the number of rows as ue_df
    expected_info_rows = len(ue_df) * 25
    if len(info_df) != expected_info_rows:
        print(f"Warning: Mismatch in dataset lengths. Expected {expected_info_rows} channel rows, but got {len(info_df)}.")
        print("Please verify the correspondence between UE_pos and Info_selected.")
        return None

    # Expand ue_df to match the length of info_df
    # Each UE position needs to be repeated 25 times
    expanded_ue_data = []
    for index, row in ue_df.iterrows():
        for _ in range(25): # Repeat each UE row 25 times for the 25 channel parameters
            expanded_ue_data.append(row.to_dict())
    ue_df_expanded = pd.DataFrame(expanded_ue_data)

    # Add AP position columns (constant for all rows)
    ue_df_expanded['AP_x'] = ap_x
    ue_df_expanded['AP_y'] = ap_y
    ue_df_expanded['AP_z'] = ap_z

    # Combine the dataframes
    combined_df = pd.concat([ue_df_expanded.reset_index(drop=True), info_df.reset_index(drop=True)], axis=1)

    # Reorder columns for clarity
    final_columns = [
        'AP_x', 'AP_y', 'AP_z',
        'UE_x', 'UE_y', 'UE_z',
        'Channel_Phase_deg', 'ToA_s', 'Channel_Gain_dBm',
        'DL_Azimuth_AoA_deg', 'DL_Elevation_AoA_deg',
        'Azimuth_AoD_deg', 'Elevation_AoD_deg'
    ]
    combined_df = combined_df[final_columns]

    return combined_df

# # Example usage (using dummy files for demonstration as before):
# # Simulating file content (replace with actual file reading in tool code)
# ap_content = """AP positions (x y z)
# 120.0000 -21.0034 5.0000
# """
# ue_content = """UE positions (x y z)
# 124.3690 -1.9635 1.6000
# 119.3720 -2.1433 1.6000
# """ # Two UE positions for demonstration

# # For info_content, let's simulate 2 UE positions * 25 channel rows + 2 separator rows = 52 lines
# info_content = ""
# sample_channel_row = "46.96580000 9.33329004E-08 -101.8020 44.1254 12.0308 70.7191 -5.4555\n"
# for _ in range(2): # For each UE position
#     for _ in range(25): # 25 channel rows
#         info_content += sample_channel_row
#     info_content += "<ue>\n" # The separator

# # Create dummy files for demonstration
# with open('ap_pos_temp.txt', 'w') as f:
#     f.write(ap_content)
# with open('ue_pos_temp.txt', 'w') as f:
#     f.write(ue_content)
# with open('info_selected_temp.txt', 'w') as f:
#     f.write(info_content)

combined_df = create_combined_dataset_v2(f'{os.getcwd()}/../J3-OriPosTrack/data/ds1/AP_pos.txt', f'{os.getcwd()}/../J3-OriPosTrack/data/ds1/UE_pos.txt', f'{os.getcwd()}/../J3-OriPosTrack/data/ds1/Info_selected.txt')

if combined_df is not None:
    output_csv_path = 'mmWave_Vehicular_Dataset_v2.csv'
    combined_df.to_csv(output_csv_path, index=False)
    print(f"Dataset successfully created and saved to {output_csv_path}")
    print("\nFirst 5 rows of the combined dataset:")
    print(combined_df.head())
    print("\nLast 5 rows of the combined dataset:")
    print(combined_df.tail())
    print(f"\nTotal rows in combined dataset: {len(combined_df)}")