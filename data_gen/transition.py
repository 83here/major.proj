import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the two datasets
df_a = pd.read_csv('/Users/prasanna/Desktop/major.proj/data_gen/healthy.csv')
df_b = pd.read_csv('/Users/prasanna/Desktop/major.proj/data_gen/faulty.csv')

# Create the transition dataset
df_transition = df_a.copy()

# Define transition parameters
transition_start = 15   # Start transition after time step 5
transition_length = 20  # Transition over 10 time steps (steps 6-15)

# Calculate transition weights for each time step
for i in range(len(df_transition)):
    if i < transition_start:
        weight_b = 0  # Pure dataset A
    elif i >= transition_start + transition_length:
        weight_b = 1  # Pure dataset B
    else:
        # Linear interpolation between 0 and 1
        weight_b = (i - transition_start) / transition_length
    
    weight_a = 1 - weight_b
    
    if i >= transition_start:  # Only apply blending after time step 5
        # Apply weighted blend for each axis
        df_transition.loc[i, 'X-axis (g)'] = weight_a * df_a.loc[i, 'X-axis (g)'] + weight_b * df_b.loc[i, 'X-axis (g)']
        df_transition.loc[i, 'Y-axis (g)'] = weight_a * df_a.loc[i, 'Y-axis (g)'] + weight_b * df_b.loc[i, 'Y-axis (g)']
        df_transition.loc[i, 'Z-axis (g)'] = weight_a * df_a.loc[i, 'Z-axis (g)'] + weight_b * df_b.loc[i, 'Z-axis (g)']

# Save the transition dataset
df_transition.to_csv('/Users/prasanna/Desktop/major.proj/data_gen/transition.csv', index=False)