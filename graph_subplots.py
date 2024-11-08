import pandas as pd
import matplotlib.pyplot as plt
from typing import List


# Load the data from CSV into a pandas DataFrame
def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


# Filter DataFrame based on selected experiments, v_flows, and runs
def filter_multiple_runs(df: pd.DataFrame, experiment: str, v_flow: int, runs: List[str]) -> pd.DataFrame:
    return df[(df['section'] == experiment) & (df['v_flow'] == v_flow) & (df['run'].isin(runs))]


# Plot multiple static trajectories for the selected runs in a 3x3 grid
def plot_3x3_trajectories(df: pd.DataFrame):
    experiments = ["Experiment_I", "Experiment_II", "Experiment_III"]
    v_flows = [15, 20, 25]
    runs = df['run'].unique()  # Get all unique runs

    fig, axs = plt.subplots(3, 3, figsize=(18, 18), sharex=True, sharey=True)

    # Loop over each subplot position
    for i, experiment in enumerate(experiments):
        for j, v_flow in enumerate(v_flows):
            ax = axs[j, i]  # Access the subplot at row j, column i
            filtered_df = df[(df['section'] == experiment) & (df['v_flow'] == v_flow)]

            # Plot each run for the current experiment and v_flow level
            for run in filtered_df['run'].unique():
                run_df = filtered_df[filtered_df['run'] == run]
                ax.plot(run_df['x'], run_df['y'], marker='o', linestyle='-', label=f"{run}")

            # Set title, labels, and legend for each subplot
            ax.set_title(f"{experiment}, v_flow: {v_flow}")
            ax.set_xlabel("X Position")
            ax.set_ylabel("Y Position")
            ax.legend(loc="upper right", fontsize="small")
            ax.grid(True)

    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    filepath = 'compiled_data/compiled_data.csv'  # Path to your CSV file
    df = load_data(filepath)

    # Plot the 3x3 grid of trajectories
    plot_3x3_trajectories(df)
