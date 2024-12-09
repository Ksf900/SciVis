import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import vtk
import os
from functions import export_to_vtp

plt.style.use('default')

np.random.seed(23765)


column_headers_pos = ['local id', 'pos x', 'pos y', 'pos z', 'area', 'type']

df_pos = pd.read_csv('rank_0_positions.txt', skiprows=8,
                     delimiter=' ', names=column_headers_pos)
areas = df_pos['area'].unique()

neurons = []
average_Ca = []

for area in areas:
    df_area = df_pos[df_pos['area'] == area]
    local_neurons = df_area['local id'].unique()
    chosen_neurons = pd.DataFrame(np.random.choice(local_neurons, 5))

    neurons.append(chosen_neurons)


column_headers_monitors = ['step', 'calcium']
df_calcium = pd.DataFrame()
Ca_area = pd.DataFrame()

for i in neurons:
    for j in i.to_numpy():
        filepath = f'/Users/Kevin/Documents/Opleiding/Master/Computational_Science/Year_2/Semester_1/Period_2/Scientific_Visualisation_and_Virtual_Reality/Project/SciVisContest23/SciVisContest23/viz-stimulus/monitors/0_{j[0]}.csv'
        temp_df = pd.read_csv(filepath, skiprows=0, usecols=[
                              0, 5], delimiter=';', names=column_headers_monitors)
        # Add the neuron ID as a new column
        temp_df['neuron_id'] = j*np.ones(len(temp_df['calcium']), dtype=int)
        df_calcium = pd.concat([df_calcium, temp_df], ignore_index=True)

for ix, i in enumerate(neurons):
    average_Ca = df_calcium[df_calcium['neuron_id'].isin(
        i.to_numpy())].groupby('step')['calcium'].mean()

    Ca_area[areas[ix]] = average_Ca


folder = "500neurons_vtp_files_stimulated"
time_steps = np.arange(0, 30000, 100)

for time_point in time_steps:
    # Filter calcium data for the current time step
    df_calcium_at_time = df_calcium[df_calcium['step'] == time_point]

    # Merge with positions
    df_merged = pd.merge(df_pos, df_calcium_at_time,
                         left_on='local id', right_on='neuron_id')

    # Export to VTP file
    filename = f'neurons_timestep_{time_point}.vtp'
    export_to_vtp(df_merged, folder, filename)

    print(f"Saved: {os.path.join(folder, filename)}")
