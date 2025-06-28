"""
Geometry types example for pyvista-geojson

This example demonstrates how to handle different GeoJSON geometry types:
- Point and MultiPoint
- LineString and MultiLineString  
- Polygon and MultiPolygon
"""

from pyvista_geojson import GeoJSONReader
import pyvista as pv


def visualize_points():
    """Visualize Point geometries"""
    reader = GeoJSONReader("data/points.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    
    # Scale point size by population
    if "population" in mesh.array_names:
        plotter.add_mesh(
            mesh,
            scalars="population",
            point_size=20,
            render_points_as_spheres=True,
            cmap="viridis"
        )
    else:
        plotter.add_mesh(mesh, color="red", point_size=20)
    
    plotter.add_scalar_bar(title="Population")
    plotter.show_axes()
    plotter.show()


def visualize_lines():
    """Visualize LineString and MultiLineString geometries"""
    reader = GeoJSONReader("data/lines.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    
    # Color lines by number of lanes
    if "lanes" in mesh.array_names:
        plotter.add_mesh(
            mesh,
            scalars="lanes",
            line_width=5,
            cmap="coolwarm"
        )
    else:
        plotter.add_mesh(mesh, color="blue", line_width=3)
    
    plotter.add_scalar_bar(title="Number of Lanes")
    plotter.show_axes()
    plotter.show()


def visualize_polygons():
    """Visualize Polygon and MultiPolygon geometries"""
    reader = GeoJSONReader("data/polygons.geojson")
    mesh = reader.read()
    
    plotter = pv.Plotter()
    
    # Color polygons by type
    if "type" in mesh.array_names:
        # Create a mapping for categorical data
        unique_types = mesh.get_array("type").unique()
        type_to_color = {
            "park": "green",
            "commercial": "blue", 
            "residential": "orange"
        }
        
        colors = [type_to_color.get(t, "gray") for t in mesh["type"]]
        plotter.add_mesh(
            mesh,
            scalars=colors,
            show_edges=True,
            edge_color="black",
            opacity=0.8
        )
    else:
        plotter.add_mesh(mesh, color="lightblue", show_edges=True)
    
    plotter.show_axes()
    plotter.show()


def visualize_all_types():
    """Visualize all geometry types in a single plot"""
    plotter = pv.Plotter(shape=(2, 2))
    
    # Points (top-left)
    plotter.subplot(0, 0)
    plotter.add_text("Point Geometries", position="upper_edge")
    reader = GeoJSONReader("data/points.geojson")
    points_mesh = reader.read()
    plotter.add_mesh(
        points_mesh,
        scalars="elevation",
        point_size=20,
        render_points_as_spheres=True
    )
    
    # Lines (top-right)
    plotter.subplot(0, 1)
    plotter.add_text("LineString Geometries", position="upper_edge")
    reader = GeoJSONReader("data/lines.geojson")
    lines_mesh = reader.read()
    plotter.add_mesh(lines_mesh, scalars="lanes", line_width=5)
    
    # Polygons (bottom-left)
    plotter.subplot(1, 0)
    plotter.add_text("Polygon Geometries", position="upper_edge")
    reader = GeoJSONReader("data/polygons.geojson")
    polygons_mesh = reader.read()
    plotter.add_mesh(
        polygons_mesh,
        scalars="height",
        show_edges=True,
        cmap="plasma"
    )
    
    # Mixed (bottom-right)
    plotter.subplot(1, 1)
    plotter.add_text("Mixed Geometries", position="upper_edge")
    reader = GeoJSONReader("data/mixed_geometries.geojson")
    mixed_mesh = reader.read()
    plotter.add_mesh(
        mixed_mesh,
        scalars="importance",
        show_edges=True,
        cmap="turbo"
    )
    
    plotter.link_views()
    plotter.show()


if __name__ == "__main__":
    print("1. Visualizing Points...")
    visualize_points()
    
    print("2. Visualizing Lines...")
    visualize_lines()
    
    print("3. Visualizing Polygons...")
    visualize_polygons()
    
    print("4. Visualizing All Types Together...")
    visualize_all_types()