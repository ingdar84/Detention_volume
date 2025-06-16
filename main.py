# Detention volume estimation tool By Dario Di Nunzio https://www.linkedin.com/in/dariodinunzio/ 2025-06-16 This tool
# estimate the basic detention volume to provide in a new development, without considering the hydraulic structures.
# It is based by HEC-HMS pre vs post outflow results. The inputs are the CSV exported from time-series tables.

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def load_file(file_type):
    """Allows user to select a file and returns the 'Outflow' column."""
    file_path = filedialog.askopenfilename(title=f"Select {file_type} CSV File", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return None  # If the user cancels, return None

    try:
        df = pd.read_csv(file_path)
        if "Outflow (CFS)" not in df.columns:
            messagebox.showerror("Error",
                                 f"'{file_type}' file does not contain an 'Outflow' column. "
                                 f"Please export the CSV file directly from Time-Series Table ")
            return None
        return df["Outflow (CFS)"].values  # Extract and return flow data

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load {file_type} file.\n{str(e)}")
        return None


def calculate_and_plot():
    """Processes data and plots hydrograph."""
    Qpre = load_file("Pre-Development")
    Qpost = load_file("Post-Development")

    if Qpre is None or Qpost is None:
        return

    # Time axis (assuming fixed intervals)
    time_minutes = np.arange(len(Qpre)) * 5  # Assuming 5-minute intervals

    # Time step in seconds
    delta_t_sec = 5 * 60

    # Excess flow calculation
    excess_flow = np.maximum(Qpost - Qpre, 0)
    volume_cuft = np.sum(excess_flow * delta_t_sec)
    volume_acft = volume_cuft / 43560

    result_label.config(text=f'The required detention basin is {volume_acft:.3f} ac-ft')

    # Plot Hydrograph
    plt.figure(figsize=(8, 4))
    plt.plot(time_minutes, Qpre, label="Pre-Development", linestyle="--")
    plt.plot(time_minutes, Qpost, label="Post-Development", alpha=0.8)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Flow (cfs)")
    plt.title("Hydrograph Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


root = tk.Tk()
root.title("Detention volume estimation")
root.geometry("400x200")  # Adjust window size

# Label to help the user to generate the input correctly
info_label = tk.Label(root, text="Export the pre and post CSV files from HEC-HMS --> Time Series Tables.\n "
                                 "Include column labels", fg="red")
info_label.pack(pady=10)

# Label to display results inside the window
result_label = tk.Label(root, text="Select CSV files to start", fg="blue")
result_label.pack(pady=30)

select_file_button = tk.Button(root, text="Select CSV Files & Calculate", command=calculate_and_plot)
select_file_button.pack(pady=10)

root.mainloop()
