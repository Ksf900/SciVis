import pandas as pd
import os
import vtk


def load_monitor_data(neurons, time_steps_set, monitor_variables, base_folder, area=None):
    """
    Load monitor data for neurons, optionally filtering by area.
    """
    column_headers_monitors = ['step', 'fired', 'fired_fraction', 'electric_activity', 'secondary_variable', 'calcium', 'target_calcium', 'synaptic_input', 'background_activity', 'grown_axons', 'connected_axons', 'grown_excitatory_dendrites', 'connected_excitatory_dendrites']

    indices_monitor_variables = [0]
    for monitor_variable in monitor_variables:
        indices_monitor_variables.append(column_headers_monitors.index(monitor_variable))

    df_monitor = pd.DataFrame()

    for neuron_id in neurons:
        if area:
            print(f"Loading data for neuron {neuron_id} in {area}...")
        else:
            print(f"Loading data for neuron {neuron_id}...")

        filename = f'monitors/0_{neuron_id}.csv'
        filepath = os.path.join(base_folder, filename)

        try:
            temp_df = pd.read_csv(filepath, skiprows=0, usecols=indices_monitor_variables, 
                                  delimiter=';', names=column_headers_monitors)
            temp_df = temp_df[temp_df['step'].isin(time_steps_set)]
            temp_df['neuron_id'] = neuron_id
            df_monitor = pd.concat([df_monitor, temp_df], ignore_index=True)
        except FileNotFoundError:
            print(f"Warning: File not found for neuron {neuron_id}. Skipping...")

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