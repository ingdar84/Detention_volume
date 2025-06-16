# Detention volume estimation tool By Dario Di Nunzio https://www.linkedin.com/in/dariodinunzio/ 2025-06-16 This tool
# estimate the basic detention volume to provide in a new development, without considering the hydraulic structures.
# It is based by HEC-HMS pre vs post outflow results. The inputs are the CSV exported from time-series tables.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("HEC-HMS-results.csv")

# Extract Q_pre and Q_post from CSV
Q_pre = df["Q_pre"].values
Q_post = df["Q_post"].values

# Time step in seconds (5 minutes = 300 seconds)
delta_t_sec = 5 * 60

# Calculate excess flow where Q_post > Q_pre
excess_flow = np.maximum(Q_post - Q_pre, 0)

# Volume = sum of (excess_flow * time step)
# Convert cubic feet to acre-feet: 1 acre-foot = 43,560 cubic feet
volume_cuft = np.sum(excess_flow * delta_t_sec)
volume_acft = volume_cuft / 43560

print(f'The required detention basin is {volume_acft:.3f} ac-ft')

