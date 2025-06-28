# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # PyVista-GeoJSON Jupyter Notebook Example
#
# This notebook demonstrates how to use pyvista-geojson in a Jupyter environment for interactive geospatial data visualization.

# %%
# Import required libraries
from pyvista_geojson import GeoJSONReader
import pyvista as pv
import numpy as np

# Enable notebook integration
pv.set_jupyter_backend('trame')
pv.global_theme.notebook = True

# %% [markdown]
# ## Basic GeoJSON Loading and Visualization

# %%
# Load a simple GeoJSON file
reader = GeoJSONReader("data/points.geojson")
mesh = reader.read()

# Quick visualization
mesh.plot(
    scalars="population",
    point_size=20,
    render_points_as_spheres=True,
    cmap="viridis",
    show_scalar_bar=True,
    title="California Cities by Population"
)

# %% [markdown]
# ## Interactive Filtering

# %%
# Create an interactive plot with slider for filtering
reader = GeoJSONReader("data/points.geojson")
all_data = reader.read()

# Get population range
min_pop = all_data["population"].min()
max_pop = all_data["population"].max()

print(f"Population range: {min_pop:,} to {max_pop:,}")

# Function to create filtered visualization
def visualize_filtered_cities(min_population=500000):
    """Visualize cities above a population threshold"""
    filtered_mesh = reader.read(
        filter_func=lambda props: props.get("population", 0) >= min_population
    )
    
    if filtered_mesh.n_points > 0:
        plotter = pv.Plotter(notebook=True)
        plotter.add_mesh(
            filtered_mesh,
            scalars="population",
            point_size=25,
            render_points_as_spheres=True,
            cmap="plasma"
        )
        
        # Add city labels
        for i, name in enumerate(filtered_mesh["name"]):
            plotter.add_text(
                f"{name}\n{filtered_mesh['population'][i]:,}",
                position=filtered_mesh.points[i],
                font_size=10
            )
        
        plotter.add_scalar_bar(title="Population")
        plotter.show()
        
        print(f"Showing {filtered_mesh.n_points} cities with population >= {min_population:,}")
    else:
        print(f"No cities found with population >= {min_population:,}")

# Demonstrate with different thresholds
visualize_filtered_cities(1000000)  # Cities over 1 million

# %% [markdown]
# ## Multiple Geometry Types

# %%
# Create a subplot showing different geometry types
plotter = pv.Plotter(shape=(1, 3), notebook=True)

# Points
plotter.subplot(0, 0)
points_reader = GeoJSONReader("data/points.geojson")
points_mesh = points_reader.read()
plotter.add_text("Points", position="upper_edge")
plotter.add_mesh(
    points_mesh,
    scalars="elevation",
    point_size=20,
    render_points_as_spheres=True
)

# Lines
plotter.subplot(0, 1)
lines_reader = GeoJSONReader("data/lines.geojson")
lines_mesh = lines_reader.read()
plotter.add_text("Lines", position="upper_edge")
plotter.add_mesh(
    lines_mesh,
    scalars="lanes",
    line_width=5
)

# Polygons
plotter.subplot(0, 2)
polygons_reader = GeoJSONReader("data/polygons.geojson")
polygons_mesh = polygons_reader.read()
plotter.add_text("Polygons", position="upper_edge")
plotter.add_mesh(
    polygons_mesh,
    scalars="height",
    show_edges=True
)

plotter.link_views()
plotter.show()

# %% [markdown]
# ## 3D Extrusion Example

# %%
# Extrude polygons based on height attribute
reader = GeoJSONReader("data/polygons.geojson")
mesh = reader.read()

# Create 3D buildings
if "height" in mesh.array_names:
    # Extrude polygons
    extruded = mesh.extrude_along_normals(mesh["height"] * 0.001)  # Scale for visualization
    
    # Create the visualization
    plotter = pv.Plotter(notebook=True)
    plotter.add_mesh(
        extruded,
        scalars="height",
        show_edges=True,
        edge_color="white",
        cmap="plasma",
        opacity=0.9
    )
    
    # Add building labels
    centroids = mesh.cell_centers()
    for i, name in enumerate(mesh["name"]):
        height = mesh["height"][i]
        position = centroids.points[i]
        position[2] = height * 0.001  # Position at top of building
        
        plotter.add_text(
            f"{name}\n{height}m",
            position=position,
            font_size=8
        )
    
    plotter.add_scalar_bar(title="Building Height (m)")
    plotter.set_background("lightblue")
    plotter.show_axes()
    plotter.show()
else:
    print("No height data available for extrusion")

# %% [markdown]
# ## Interactive Widgets

# %%
# Create an interactive plot with widgets
from ipywidgets import interact, IntSlider, Dropdown

# Load all data types
points_reader = GeoJSONReader("data/points.geojson")
lines_reader = GeoJSONReader("data/lines.geojson")
polygons_reader = GeoJSONReader("data/polygons.geojson")

def create_interactive_plot(geometry_type="points", color_by="population", point_size=15):
    """Create interactive plot based on widget selections"""
    
    plotter = pv.Plotter(notebook=True)
    
    if geometry_type == "points":
        mesh = points_reader.read()
        if color_by in mesh.array_names:
            plotter.add_mesh(
                mesh,
                scalars=color_by,
                point_size=point_size,
                render_points_as_spheres=True
            )
        else:
            plotter.add_mesh(mesh, point_size=point_size)
            
    elif geometry_type == "lines":
        mesh = lines_reader.read()
        if color_by in mesh.array_names:
            plotter.add_mesh(mesh, scalars=color_by, line_width=5)
        else:
            plotter.add_mesh(mesh, line_width=5)
            
    elif geometry_type == "polygons":
        mesh = polygons_reader.read()
        if color_by in mesh.array_names:
            plotter.add_mesh(mesh, scalars=color_by, show_edges=True)
        else:
            plotter.add_mesh(mesh, show_edges=True)
    
    plotter.add_scalar_bar(title=color_by.title())
    plotter.show()

# Create interactive widgets
interact(
    create_interactive_plot,
    geometry_type=Dropdown(
        options=["points", "lines", "polygons"],
        value="points",
        description="Geometry:"
    ),
    color_by=Dropdown(
        options=["population", "elevation", "height", "lanes"],
        value="population",
        description="Color by:"
    ),
    point_size=IntSlider(
        min=5,
        max=30,
        step=5,
        value=15,
        description="Point size:"
    )
)

# %% [markdown]
# ## Data Analysis Integration

# %%
# Demonstrate integration with pandas and data analysis
import pandas as pd

# Convert mesh data to pandas DataFrame for analysis
reader = GeoJSONReader("data/points.geojson")
mesh = reader.read()

# Extract data to DataFrame
data = {
    'name': mesh['name'],
    'population': mesh['population'],
    'elevation': mesh['elevation'],
    'longitude': mesh.points[:, 0],
    'latitude': mesh.points[:, 1]
}

df = pd.DataFrame(data)
print("City data summary:")
print(df.describe())
print("\nCity details:")
print(df)

# Create correlation analysis
correlation = df[['population', 'elevation']].corr()
print(f"\nCorrelation between population and elevation: {correlation.iloc[0, 1]:.3f}")

# Visualize the analysis results
mesh.plot(
    scalars="population",
    point_size=25,
    render_points_as_spheres=True,
    cmap="coolwarm",
    title="Population Analysis Results"
)

# %% [markdown]
# ## Export and Save Options

# %%
# Demonstrate export capabilities
reader = GeoJSONReader("data/mixed_geometries.geojson")
mesh = reader.read()

# Create a nice visualization
plotter = pv.Plotter(notebook=True, off_screen=True)  # off_screen for export
plotter.add_mesh(
    mesh,
    scalars="importance",
    show_edges=True,
    cmap="viridis"
)
plotter.add_scalar_bar(title="Importance")
plotter.set_background("white")

# Save as image
plotter.screenshot("mixed_geometries_visualization.png")
print("Visualization saved as 'mixed_geometries_visualization.png'")

# Save mesh data in various formats
mesh.save("mixed_geometries.vtk")  # VTK format
mesh.save("mixed_geometries.ply")  # PLY format
print("Mesh data saved in VTK and PLY formats")

# Show the plot
plotter.show()

# %% [markdown]
# ## Summary
#
# This notebook demonstrated:
#
# 1. **Basic GeoJSON loading and visualization** with pyvista-geojson
# 2. **Interactive filtering** based on feature properties
# 3. **Multiple geometry types** (points, lines, polygons) in subplots
# 4. **3D extrusion** of polygons based on attributes
# 5. **Interactive widgets** for dynamic exploration
# 6. **Data analysis integration** with pandas
# 7. **Export capabilities** for images and mesh data
#
# The pyvista-geojson library provides a powerful bridge between GeoJSON geographic data and PyVista's 3D visualization capabilities, making it easy to create interactive and informative geospatial visualizations in Jupyter notebooks.
