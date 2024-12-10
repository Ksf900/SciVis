import numpy as np
import vtk
import os

def export_to_vtp(df, folder, filename, monitor_variable):
    """
    Exports a variable from a DataFrame to a VTP file.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame with positional and variable data.
        folder (str): The folder to save the VTP file.
        filename (str): The name of the output VTP file.
        variable_name (str): The column name in the DataFrame to be exported as a scalar.
        vtk_name (str): The name for the scalar in the VTK file.
    """
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Full path to the file
    filepath = os.path.join(folder, filename)

    # Create a VTK points object
    points = vtk.vtkPoints()

    # Add points to the object
    for _, row in df.iterrows():
        points.InsertNextPoint(row['pos x'], row['pos y'], row['pos z'])

    # Create a polydata object
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)

    # Add variable data as a point scalar
    array = vtk.vtkFloatArray()
    array.SetName(monitor_variable)  # Set the name of the variable in the VTK file
    for _, row in df.iterrows():
        array.InsertNextValue(row[monitor_variable])

    polydata.GetPointData().SetScalars(array)

    # Write to a VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filepath)
    writer.SetInputData(polydata)

    # Ensure file is properly written
    writer.SetDataModeToAscii()  # Optional: Change to Binary for larger datasets
    writer.Write()
