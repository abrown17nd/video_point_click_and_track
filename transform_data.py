import pandas as pd
import numpy as np
import os
import shutil
import stat

# Function to perform transformations on x, y data
def transform_data(df: pd.DataFrame,
                   flip_x: bool = False,
                   flip_y: bool = False,
                   shift_x_by: float = 0,
                   shift_y_by: float = 0,
                   rotate_deg: float = 0,
                   rotate_rad: float = 0,
                   video_flip_x: bool = False,
                   video_flip_y: bool = False,
                   video_width: float = None,
                   video_height: float = None,
                   adjust_run_timestamp_to_0: bool = False) -> pd.DataFrame:
    # Step 1: Video-based flipping (using video width and height)
    if video_flip_x and video_width is not None:
        df['x'] = video_width - df['x']
    if video_flip_y and video_height is not None:
        df['y'] = video_height - df['y']

    # Step 2: Flip x and/or y
    if flip_x:
        df['x'] = -df['x']
    if flip_y:
        df['y'] = -df['y']

    # Step 3: Shift x and y by specified amounts
    df['x'] += shift_x_by
    df['y'] += shift_y_by

    # Step 4: Adjust timestamps for each unique combination of experiment, v_flow, and run to start from zero if requested
    if adjust_run_timestamp_to_0:
        for (experiment, v_flow, run), group_df in df.groupby(['section', 'v_flow', 'run']):
            df.loc[group_df.index, 'timestamp'] -= group_df['timestamp'].iloc[0]

    # Step 5: Rotation (convert degrees to radians if needed)
    rotation_angle = rotate_rad if rotate_rad != 0 else np.deg2rad(rotate_deg)
    if rotation_angle != 0:
        # Create rotation matrix
        cos_theta = np.cos(rotation_angle)
        sin_theta = np.sin(rotation_angle)
        rotation_matrix = np.array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])

        # Apply rotation
        xy_rotated = np.dot(df[['x', 'y']], rotation_matrix)
        df['x'], df['y'] = xy_rotated[:, 0], xy_rotated[:, 1]

    return df

# Main function to handle file operations and transformations
def main():
    # File paths
    original_filepath = 'compiled_data.csv'
    backup_filepath = 'compiled_data_original.csv'
    transformed_filepath = 'compiled_data_transformed.csv'

    # Step 1: Check if backup file exists, if not create it
    if os.path.exists(backup_filepath):
        # Use existing backup as the input data
        input_filepath = backup_filepath
        print(f"Using existing backup file: '{backup_filepath}'")
    else:
        # Create backup from the original file and make it read-only
        shutil.copyfile(original_filepath, backup_filepath)
        os.chmod(backup_filepath, stat.S_IREAD)
        input_filepath = original_filepath
        print(f"Backup created: '{backup_filepath}' (set as read-only)")

    # Load the data from the chosen file (either backup or original)
    df = pd.read_csv(input_filepath)

    # Transformation parameters (adjust as needed)
    flip_x = True                  # Flip x axis
    flip_y = False                 # Flip y axis
    shift_x_by = -100              # Shift x by -100
    shift_y_by = 50                # Shift y by 50
    rotate_deg = 45                # Rotate by 45 degrees
    rotate_rad = 0                 # Rotate by an angle in radians (set to 0 if using degrees)
    video_flip_x = False           # Flip x axis based on video width
    video_flip_y = True            # Flip y axis based on video height
    video_width = 1920             # Width of the video (used if video_flip_x is True)
    video_height = 1080            # Height of the video (used if video_flip_y is True)
    adjust_run_timestamp_to_0 = True  # Adjust each run to start at timestamp 0



    # Step 2: Apply transformations
    df_transformed = transform_data(df,
                                    flip_x=flip_x,
                                    flip_y=flip_y,
                                    shift_x_by=shift_x_by,
                                    shift_y_by=shift_y_by,
                                    rotate_deg=rotate_deg,
                                    rotate_rad=rotate_rad,
                                    video_flip_x=video_flip_x,
                                    video_flip_y=video_flip_y,
                                    video_width=video_width,
                                    video_height=video_height,
                                    adjust_run_timestamp_to_0=adjust_run_timestamp_to_0)

    # Step 3: Save the transformed data to a new file and replace original file
    df_transformed.to_csv(transformed_filepath, index=False)
    shutil.move(transformed_filepath, original_filepath)

    print("Transformation complete. Original data saved as 'compiled_data_original.csv' (read-only), and transformed data saved as 'compiled_data.csv'.")

if __name__ == "__main__":
    main()
