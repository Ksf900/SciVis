import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import vtk
import os
from scipy.spatial import ConvexHull
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
# %matplotlib widget


plt.style.use('default')

np.random.seed(23765)

column_headers_pos = ['local id', 'pos x', 'pos y', 'pos z', 'area', 'type']

df_pos = pd.read_csv('rank_0_positions.txt', skiprows=8,
                     delimiter=' ', names=column_headers_pos)
areas = df_pos['area'].unique()

neurons = []
average_Ca = []
Average_pos_per_area = []
brain_area_boundaries = []

df_chosen_pos = pd.DataFrame()

for area in areas:
    df_area = df_pos[df_pos['area'] == area]
    local_neurons = df_area['local id'].unique()
    chosen_neurons = pd.DataFrame(np.random.choice(local_neurons, 5))
    neurons.append(chosen_neurons)

column_headers_monitors = ['step', 'calcium']
df_calcium = pd.DataFrame()
Ca_area = pd.DataFrame()
Area_pos = pd.DataFrame()

for neurons_per_area in neurons:
    for neuron in neurons_per_area.to_numpy():
        filepath = f'/Users/Kevin/Documents/Opleiding/Master/Computational_Science/Year_2/Semester_1/Period_2/Scientific_Visualisation_and_Virtual_Reality/Project/SciVisContest23/SciVisContest23/viz-stimulus/monitors/0_{neuron[0]}.csv'
        temp_df = pd.read_csv(filepath, skiprows=0, usecols=[
                              0, 5], delimiter=';', names=column_headers_monitors)
        # Add the neuron ID as a new column
        temp_df['neuron_id'] = neuron * \
            np.ones(len(temp_df['calcium']), dtype=int)
        df_calcium = pd.concat([df_calcium, temp_df], ignore_index=True)

for ix, i in enumerate(neurons):
    average_Ca = df_calcium[df_calcium['neuron_id'].isin(
        i.to_numpy())].groupby('step')['calcium'].mean()
    Average_pos_per_area_calc = df_pos[df_pos['local id'].isin(
        i[0])][['pos x', 'pos y', 'pos z']].mean(axis=0)
    Area_pos[areas[ix]] = Average_pos_per_area_calc
    Ca_area[areas[ix]] = average_Ca

# Create a VTK points object for the positions
points = vtk.vtkPoints()

# Create a VTK float array for calcium levels
calcium_levels = vtk.vtkFloatArray()
calcium_levels.SetName("Calcium Levels")

# Iterate through the areas
areas = Ca_area.columns
for area in areas:
    pos = Area_pos[area].values.reshape(3, -1)  # pos_x, pos_y, pos_z
    calcium = Ca_area[area].values  # Calcium levels

    for i in range(pos.shape[1]):
        # Add point to the points object
        points.InsertNextPoint(pos[0][i], pos[1][i], pos[2][i])

        # Add calcium value
        calcium_levels.InsertNextValue(calcium[i])

# Create a polydata object
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().SetScalars(calcium_levels)

# Create a sphere source (glyph shape)
sphere_source = vtk.vtkSphereSource()
sphere_source.SetRadius(1)  # Adjust the radius to make spheres larger

# Create a glyph filter to place spheres at each point
glyph = vtk.vtkGlyph3D()
glyph.SetSourceConnection(sphere_source.GetOutputPort())
glyph.SetInputData(polydata)
glyph.ScalingOff()  # Turn off scaling if you don't want the size to vary
glyph.Update()

# Create a mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(glyph.GetOutputPort())
mapper.SetScalarRange(calcium_levels.GetRange())  # Set range for color mapping

# Create an actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.1, 0.1)  # Dark background

# Create a render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Create a render window interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add color bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(mapper.GetLookupTable())
scalar_bar.SetTitle("Calcium Levels")
renderer.AddActor2D(scalar_bar)

# Start the visualization
render_window.Render()
interactor.Start()


# folder = "500neurons_vtp_files_stimulated"
# time_steps = np.arange(0, 30000, 100)

# for time_point in time_steps:
#     # Filter calcium data for the current time step
#     df_calcium_at_time = df_calcium[df_calcium['step'] == time_point]

#     # Merge with positions
#     df_merged = pd.merge(df_pos, df_calcium_at_time,
#                          left_on='local id', right_on='neuron_id')

#     # Export to VTP file
#     filename = f'neurons_timestep_{time_point}.vtp'
#     export_to_vtp(df_merged, folder, filename)

#     print(f"Saved: {os.path.join(folder, filename)}")
