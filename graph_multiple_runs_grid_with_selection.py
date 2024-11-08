import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict


# Load the data from CSV into a pandas DataFrame
def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


# Load the CSV selection file and parse runs for each experiment and v_flow level
def load_selection_file(selection_filepath: str) -> Dict[str, Dict[int, List[str]]]:
    selection_df = pd.read_csv(selection_filepath, index_col=0)
    selection_dict = {}

    for experiment in selection_df.columns:
        selection_dict[experiment] = {}
        for v_flow in selection_df.index:
            # Parse the run IDs from the cell and store as a list of strings
            runs = selection_df.at[v_flow, experiment]
            selection_dict[experiment][int(v_flow)] = runs.split(';') if pd.notna(runs) else []

    return selection_dict


# Plot multiple static trajectories for the selected runs in a 3x3 grid
def plot_3x3_trajectories(df: pd.DataFrame, selection_dict: Dict[str, Dict[int, List[str]]]):
    experiments = ["Experiment_I", "Experiment_II", "Experiment_III"]
    v_flows = [15, 20, 25]

    fig, axs = plt.subplots(3, 3, figsize=(18, 18), sharex=True, sharey=True)

    # Loop over each subplot position
    for i, experiment in enumerate(experiments):
        for j, v_flow in enumerate(v_flows):
            ax = axs[j, i]  # Access the subplot at row j, column i

            # Retrieve runs from selection_dict for the current experiment and v_flow
            selected_runs = selection_dict.get(experiment, {}).get(v_flow, [])
            print("ex: ", experiment, "vf: ", v_flow, "selected_runs: ", selected_runs)

            # If no runs are selected, skip this plot
            if not selected_runs:
                ax.set_title(f"No Runs Selected for {experiment}, v_flow: {v_flow}")
                ax.axis('off')  # Hide axes if no runs are selected
                continue

            # Prefix 'Run_' to each selected run to match the format in df
            selected_runs = [f"Run_{run}" for run in selected_runs]

            # Filter the DataFrame for the current experiment, v_flow, and selected runs
            filtered_df = df[(df['section'] == experiment) & (df['v_flow'] == v_flow) & (df['run'].isin(selected_runs))]
            print("filtered_df: ", filtered_df)

            # Plot each run for the current experiment and v_flow level
            has_data = False  # Track if any data is actually plotted
            for run in selected_runs:
                run_df = filtered_df[filtered_df['run'] == run]
                if not run_df.empty:  # Only plot if data exists for the run
                    ax.plot(run_df['x'], run_df['y'], marker='o', linestyle='-', label=f"Run {run}")
                    has_data = True

            # Set title, labels, and legend for each subplot
            if has_data:
                ax.set_title(f"{experiment}, v_flow: {v_flow}", pad=15)
                ax.set_xlabel("X Position")
                ax.set_ylabel("Y Position")
                ax.legend(loc="upper right", fontsize="small")
                ax.grid(True)
            else:
                ax.set_title(f"No Data for {experiment}, v_flow: {v_flow}")
                ax.axis('off')  # Hide axes if no data is available for the plot

    # Adjust layout to prevent overlap
    plt.subplots_adjust(wspace=0.3, hspace=0.4)
    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    data_filepath = 'compiled_data.csv'  # Path to your main data CSV file
    selection_filepath = 'run_selection.csv'  # Path to your selection CSV file

    # Load data and run selection criteria
    df = load_data(data_filepath)
    selection_dict = load_selection_file(selection_filepath)

    # Plot the 3x3 grid of trajectories based on selection
    plot_3x3_trajectories(df, selection_dict)
