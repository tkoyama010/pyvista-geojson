"""
3D visualization example for pyvista-geojson

This example demonstrates advanced 3D visualization techniques:
- Extruding polygons based on attributes
- Creating height-based visualizations
- Adding 3D effects and textures
"""

from pyvista_geojson import GeoJSONReader
import pyvista as pv
import numpy as np


def extrude_buildings():
    """Extrude polygon buildings based on height attribute"""
    reader = GeoJSONReader("data/polygons.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    plotter.add_text("3D Building Heights", position="upper_edge")
    
    # Extrude polygons based on height
    if "height" in mesh.array_names:
        extruded = mesh.extrude_along_normals(mesh["height"])
        plotter.add_mesh(
            extruded,
            scalars="height",
            show_edges=True,
            edge_color="white",
            cmap="plasma",
            opacity=0.9
        )
    else:
        # Fallback to simple visualization
        plotter.add_mesh(mesh, show_edges=True)
    
    plotter.add_scalar_bar(title="Building Height (m)")
    plotter.set_background("lightblue")
    
    # Add some lighting effects
    plotter.add_light(pv.Light(position=(10, 10, 10), focal_point=(0, 0, 0)))
    plotter.show_axes()
    plotter.show()


def elevation_visualization():
    """Create 3D visualization of points with elevation"""
    reader = GeoJSONReader("data/points.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    plotter.add_text("City Elevations in 3D", position="upper_edge")
    
    if "elevation" in mesh.array_names and len(mesh.points) > 0:
        # Create 3D points by using elevation as Z coordinate
        points_3d = mesh.points.copy()
        points_3d[:, 2] = mesh["elevation"] * 100  # Scale for visibility
        
        # Create new mesh with 3D coordinates
        elevated_mesh = pv.PolyData(points_3d)
        elevated_mesh.point_data.update(mesh.point_data)
        
        # Add spheres at each point
        spheres = elevated_mesh.glyph(scale="elevation", factor=500)
        plotter.add_mesh(
            spheres,
            scalars="elevation",
            cmap="terrain",
            opacity=0.8
        )
        
        # Add city labels
        if "name" in mesh.array_names:
            for i, name in enumerate(mesh["name"]):
                plotter.add_text(
                    name,
                    position=points_3d[i],
                    font_size=10,
                    color="black"
                )
        
        # Add vertical lines to ground
        for i, point in enumerate(points_3d):
            ground_point = point.copy()
            ground_point[2] = 0
            line = pv.Line(ground_point, point)
            plotter.add_mesh(line, color="gray", line_width=2, opacity=0.6)
    
    plotter.add_scalar_bar(title="Elevation (m)")
    plotter.set_background("skyblue")
    plotter.show_axes()
    plotter.show()


def terrain_like_visualization():
    """Create a terrain-like visualization from polygon data"""
    reader = GeoJSONReader("data/polygons.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    plotter.add_text("Terrain-like Visualization", position="upper_edge")
    
    if "height" in mesh.array_names:
        # Create a surface from the polygon centroids
        centroids = mesh.cell_centers()
        
        # Create a structured grid for interpolation
        bounds = mesh.bounds
        x = np.linspace(bounds[0], bounds[1], 50)
        y = np.linspace(bounds[2], bounds[3], 50)
        xx, yy = np.meshgrid(x, y)
        
        # Interpolate height values to create a smooth surface
        from scipy.spatial import distance_matrix
        
        # Simple inverse distance weighting
        grid_points = np.column_stack([xx.ravel(), yy.ravel()])
        centroid_points = centroids.points[:, :2]  # Only X, Y
        
        distances = distance_matrix(grid_points, centroid_points)
        # Avoid division by zero
        distances[distances == 0] = 1e-10
        weights = 1 / distances**2
        weights_sum = weights.sum(axis=1)
        
        interpolated_heights = np.sum(
            weights * centroids["height"][np.newaxis, :], axis=1
        ) / weights_sum
        
        # Create the terrain mesh
        zz = interpolated_heights.reshape(xx.shape)
        terrain = pv.StructuredGrid(xx, yy, zz * 0.01)  # Scale down for better visualization
        
        plotter.add_mesh(
            terrain,
            scalars=zz,
            cmap="terrain",
            show_edges=True,
            opacity=0.8
        )
        
        # Add the original polygons on top
        elevated_polygons = mesh.translate([0, 0, 0.1])
        plotter.add_mesh(
            elevated_polygons,
            scalars="height",
            cmap="viridis",
            opacity=0.9,
            edge_color="black"
        )
    
    plotter.add_scalar_bar(title="Height")
    plotter.set_background("lightgray")
    plotter.show_axes()
    plotter.show()


def animated_rotation():
    """Create an animated rotating visualization"""
    reader = GeoJSONReader("data/mixed_geometries.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    plotter.add_text("Rotating 3D View", position="upper_edge")
    
    # Add different visual styles for different geometry types
    if "category" in mesh.array_names:
        # Color by category
        categories = mesh["category"]
        category_colors = {
            "landmark": "red",
            "road": "blue", 
            "building": "green"
        }
        
        colors = [category_colors.get(cat, "gray") for cat in categories]
        plotter.add_mesh(
            mesh,
            scalars=colors,
            show_edges=True,
            line_width=3,
            opacity=0.8
        )
    else:
        plotter.add_mesh(mesh, show_edges=True)
    
    # Set camera for rotation
    plotter.camera.position = (10, 10, 10)
    plotter.camera.focal_point = (0, 0, 0)
    
    # Open and start rotation
    plotter.open_movie("rotation.mp4")  # Optional: save animation
    plotter.show(auto_close=False)
    
    # Rotate around Z-axis
    for angle in range(0, 360, 5):
        plotter.camera.azimuth = angle
        plotter.render()
        if hasattr(plotter, 'write_frame'):
            plotter.write_frame()  # Save frame for movie
    
    plotter.close()


def interactive_3d_scene():
    """Create an interactive 3D scene with multiple datasets"""
    plotter = pv.Plotter()
    plotter.add_text("Interactive 3D Scene", position="upper_edge")
    
    # Load and display points
    points_reader = GeoJSONReader("data/points.geojson")
    points_mesh = points_reader.read()
    
    if "elevation" in points_mesh.array_names:
        # Elevate points
        elevated_points = points_mesh.points.copy()
        elevated_points[:, 2] = points_mesh["elevation"] * 50
        points_3d = pv.PolyData(elevated_points)
        points_3d.point_data.update(points_mesh.point_data)
        
        spheres = points_3d.glyph(scale="population", factor=0.00001)
        plotter.add_mesh(
            spheres,
            scalars="population",
            cmap="Reds",
            name="cities"
        )
    
    # Add lines
    lines_reader = GeoJSONReader("data/lines.geojson")
    lines_mesh = lines_reader.read()
    plotter.add_mesh(
        lines_mesh,
        color="blue",
        line_width=5,
        name="roads"
    )
    
    # Add polygons
    polygons_reader = GeoJSONReader("data/polygons.geojson")
    polygons_mesh = polygons_reader.read()
    
    if "height" in polygons_mesh.array_names:
        extruded_buildings = polygons_mesh.extrude_along_normals(
            polygons_mesh["height"] * 0.1
        )
        plotter.add_mesh(
            extruded_buildings,
            scalars="height",
            cmap="viridis",
            opacity=0.7,
            name="buildings"
        )
    
    # Add interactive widgets
    plotter.add_checkbox_button_widget(
        lambda state: plotter.renderers[0].actors["cities"].SetVisibility(state),
        value=True,
        position=(10, 10),
        size=50,
        border_size=2,
        color_on="green",
        color_off="red"
    )
    
    # Add lighting and effects
    plotter.add_light(pv.Light(position=(20, 20, 20)))
    plotter.set_background("black")
    plotter.show_axes()
    plotter.show()


if __name__ == "__main__":
    print("1. Extruding buildings by height...")
    extrude_buildings()
    
    print("2. Elevation visualization...")
    elevation_visualization()
    
    print("3. Terrain-like visualization...")
    terrain_like_visualization()
    
    print("4. Animated rotation...")
    # animated_rotation()  # Uncomment to run animation
    
    print("5. Interactive 3D scene...")
    interactive_3d_scene()