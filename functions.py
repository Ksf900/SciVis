import numpy as np
import vtk
import os
import pandas as pd

def load_monitor_data(neurons, time_steps_set, monitor_variables, base_folder):
    """Load monitor data for all neurons."""
    column_headers_monitors = ['step', 'fired', 'fired_fraction', 'electric_activity', 'secondary_variable', 'calcium', 'target_calcium', 'synaptic_input', 'background_activity', 'grown_axons', 'connected_axons', 'grown_excitatory_dendrites', 'connected_excitatory_dendrites']

    indices_monitor_variables = [0]
    for monitor_variable in monitor_variables:
        indices_monitor_variables.append(column_headers_monitors.index(monitor_variable))

    df_monitor = pd.DataFrame()

    for i in neurons:
        print(f"Loading data for neuron {i}")
        filename = f'monitors/0_{i}.csv'
        filepath = os.path.join(base_folder, filename)
        
        temp_df = pd.read_csv(filepath, skiprows=0, usecols=indices_monitor_variables, 
                            delimiter=';', names=column_headers_monitors)
        
        temp_df = temp_df[temp_df['step'].isin(time_steps_set)]
        
        temp_df['neuron_id'] = i
        
        df_monitor = pd.concat([df_monitor, temp_df], ignore_index=True)

    return df_monitor


def load_monitor_data_for_area(area, neurons_in_area, time_steps_set, monitor_variables, base_folder):
    """
    Load monitor data for all neurons in a specific area.
    """
    column_headers_monitors = ['step', 'fired', 'fired_fraction', 'electric_activity', 'secondary_variable', 
                               'calcium', 'target_calcium', 'synaptic_input', 'background_activity', 
                               'grown_axons', 'connected_axons', 'grown_excitatory_dendrites', 
                               'connected_excitatory_dendrites']

    indices_monitor_variables = [0]
    for monitor_variable in monitor_variables:
        indices_monitor_variables.append(column_headers_monitors.index(monitor_variable))

    df_monitor = pd.DataFrame()

    for neuron_id in neurons_in_area:
        print(f"Loading data for neuron {neuron_id} in {area}...")
        filename = f'monitors/0_{neuron_id}.csv'
        filepath = os.path.join(base_folder, filename)

        temp_df = pd.read_csv(filepath, skiprows=0, usecols=indices_monitor_variables, delimiter=';', names=column_headers_monitors)
        temp_df = temp_df[temp_df['step'].isin(time_steps_set)]
        temp_df['neuron_id'] = neuron_id

        df_monitor = pd.concat([df_monitor, temp_df], ignore_index=True)

    return df_monitor

def export_to_vtp(data, folder, filename, monitor_variables):
    """
    Exports the given data to a VTP file.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

    filepath = os.path.join(folder, filename)

    points = vtk.vtkPoints()

    polydata = vtk.vtkPolyData()
    scalar_arrays = {var: vtk.vtkFloatArray() for var in monitor_variables}
    for var, array in scalar_arrays.items():
        array.SetName(var)

    area_array = vtk.vtkStringArray()
    area_array.SetName("area")

    for point_data in data:
        points.InsertNextPoint(point_data['pos x'], point_data['pos y'], point_data['pos z'])
        for var in monitor_variables:
            scalar_arrays[var].InsertNextValue(point_data[var])
        area_array.InsertNextValue(point_data['area'])

    polydata.SetPoints(points)
    for array in scalar_arrays.values():
        polydata.GetPointData().AddArray(array)
    polydata.GetPointData().AddArray(area_array)

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filepath)
    writer.SetInputData(polydata)
    writer.Write()

def write_vtp_files_for_area(df_merged, output_folder, simulation, area, monitor_variables, time_steps):
    """
    Write VTP files for each timestep in the area.
    """
    os.makedirs(output_folder, exist_ok=True)

    for time_point in time_steps:
        print(f"Writing VTP for area {area} at timestep {time_point}...")
        df_timestep = df_merged[df_merged['step'] == time_point]

        filename = f"{simulation}_{area}_timestep_{time_point}.vtp"
        export_to_vtp(df_timestep.to_dict('records'), output_folder, filename=filename, monitor_variables=monitor_variables)
        print(f"Saved: {os.path.join(output_folder, filename)}")