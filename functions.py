import numpy as np
import vtk
import os


def export_to_vtp(df, folder, filename):
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

    # Add calcium data as a point scalar
    calcium_array = vtk.vtkFloatArray()
    calcium_array.SetName("Calcium Concentration")
    for _, row in df.iterrows():
        calcium_array.InsertNextValue(row['calcium'])

    polydata.GetPointData().SetScalars(calcium_array)

    # Write to a VTP file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(filepath)
    writer.SetInputData(polydata)

    # Ensure file is properly written
    writer.SetDataModeToAscii()  # Optional: Change to Binary for larger datasets
    writer.Write()
