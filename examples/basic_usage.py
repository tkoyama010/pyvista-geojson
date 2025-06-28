"""
Basic usage example for pyvista-geojson

This example demonstrates how to load and visualize a simple GeoJSON file
using the pyvista-geojson library.
"""

from pyvista_geojson import GeoJSONReader
import pyvista as pv


def main():
    # Load a GeoJSON file containing various geometries
    reader = GeoJSONReader("data/mixed_geometries.geojson")
    mesh = reader.read()

    # Create a plotter and add the mesh (off-screen)
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh, show_edges=True, line_width=2)
    
    # Add labels for features if they have names
    if "name" in mesh.array_names:
        labels = mesh["name"]
        points = mesh.points
        for i, label in enumerate(labels):
            if label:  # Only add label if it exists
                plotter.add_text(label, position=points[i], font_size=10)
    
    # Set a nice camera angle
    plotter.camera_position = "xy"
    plotter.show_axes()
    
    # Save the plot as an image
    plotter.screenshot("basic_usage_output.png")
    print("Saved plot to basic_usage_output.png")


def simple_visualization():
    """Even simpler example - minimal code to visualize GeoJSON"""
    # Load and display in just a few lines
    reader = GeoJSONReader("data/points.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh, show_edges=True, point_size=10)
    plotter.screenshot("simple_visualization_output.png")
    print("Saved plot to simple_visualization_output.png")


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to run the simple visualization instead
    # simple_visualization()