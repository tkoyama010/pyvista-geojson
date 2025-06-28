"""
Filtering example for pyvista-geojson

This example demonstrates how to filter GeoJSON features based on their properties.
"""

from pyvista_geojson import GeoJSONReader
import pyvista as pv


def filter_by_attribute():
    """Filter features by a specific attribute value"""
    reader = GeoJSONReader("data/points.geojson")
    
    # Filter cities with population > 1 million
    mesh = reader.read(filter_func=lambda props: props.get("population", 0) > 1000000)
    
    plotter = pv.Plotter()
    plotter.add_text("Cities with Population > 1 Million", position="upper_edge")
    plotter.add_mesh(
        mesh,
        scalars="population",
        point_size=30,
        render_points_as_spheres=True,
        cmap="Reds"
    )
    
    # Add city labels
    if "name" in mesh.array_names and len(mesh.points) > 0:
        for i, name in enumerate(mesh["name"]):
            plotter.add_text(
                name,
                position=mesh.points[i],
                font_size=12,
                color="black"
            )
    
    plotter.add_scalar_bar(title="Population")
    plotter.show_axes()
    plotter.show()


def filter_by_range():
    """Filter features within a specific range"""
    reader = GeoJSONReader("data/points.geojson")
    
    # Filter cities with elevation between 20 and 100 meters
    mesh = reader.read(
        filter_func=lambda props: 20 <= props.get("elevation", 0) <= 100
    )
    
    plotter = pv.Plotter()
    plotter.add_text("Cities with Elevation 20-100m", position="upper_edge")
    plotter.add_mesh(
        mesh,
        scalars="elevation",
        point_size=25,
        render_points_as_spheres=True,
        cmap="terrain"
    )
    
    plotter.add_scalar_bar(title="Elevation (m)")
    plotter.show_axes()
    plotter.show()


def filter_by_type():
    """Filter features by geometry or property type"""
    reader = GeoJSONReader("data/lines.geojson")
    
    # Filter only highways
    mesh = reader.read(
        filter_func=lambda props: props.get("type") in ["highway", "interstate"]
    )
    
    plotter = pv.Plotter()
    plotter.add_text("Highways and Interstates Only", position="upper_edge")
    
    # Color by road type
    road_colors = {"highway": "red", "interstate": "blue"}
    for road_type, color in road_colors.items():
        # Filter for each type
        type_mesh = reader.read(
            filter_func=lambda props: props.get("type") == road_type
        )
        if type_mesh.n_points > 0:
            plotter.add_mesh(
                type_mesh,
                color=color,
                line_width=5,
                label=road_type.capitalize()
            )
    
    plotter.add_legend()
    plotter.show_axes()
    plotter.show()


def filter_multiple_criteria():
    """Filter using multiple criteria"""
    reader = GeoJSONReader("data/mixed_geometries.geojson")
    
    # Filter features with importance >= 8 OR category == "building"
    def complex_filter(props):
        return (props.get("importance", 0) >= 8 or 
                props.get("category") == "building")
    
    mesh = reader.read(filter_func=complex_filter)
    
    plotter = pv.Plotter()
    plotter.add_text("High Importance or Buildings", position="upper_edge")
    plotter.add_mesh(
        mesh,
        scalars="importance",
        show_edges=True,
        cmap="viridis",
        edge_color="black"
    )
    
    # Add labels
    if "name" in mesh.array_names:
        for i, name in enumerate(mesh["name"]):
            if name:
                plotter.add_text(
                    name,
                    position=mesh.points[i],
                    font_size=10
                )
    
    plotter.add_scalar_bar(title="Importance")
    plotter.show_axes()
    plotter.show()


def dynamic_filtering():
    """Example of dynamic filtering with interactive updates"""
    import numpy as np
    
    reader = GeoJSONReader("data/points.geojson")
    all_features = reader.read()
    
    plotter = pv.Plotter()
    plotter.add_text("Dynamic Population Filter", position="upper_edge")
    
    # Get population range
    populations = all_features["population"]
    min_pop, max_pop = populations.min(), populations.max()
    
    # Create initial mesh with all features
    mesh_actor = plotter.add_mesh(
        all_features,
        scalars="population",
        point_size=20,
        render_points_as_spheres=True,
        cmap="YlOrRd"
    )
    
    # Add slider for filtering
    def update_filter(value):
        # Filter based on slider value
        filtered = reader.read(
            filter_func=lambda props: props.get("population", 0) >= value
        )
        
        # Update the mesh
        plotter.remove_actor(mesh_actor)
        if filtered.n_points > 0:
            plotter.add_mesh(
                filtered,
                scalars="population",
                point_size=20,
                render_points_as_spheres=True,
                cmap="YlOrRd",
                name="filtered_mesh"
            )
    
    plotter.add_slider_widget(
        update_filter,
        [min_pop, max_pop],
        value=min_pop,
        title="Min Population",
        fmt="%.0f",
        style="modern"
    )
    
    plotter.add_scalar_bar(title="Population")
    plotter.show_axes()
    plotter.show()


if __name__ == "__main__":
    print("1. Filter by attribute value...")
    filter_by_attribute()
    
    print("2. Filter by range...")
    filter_by_range()
    
    print("3. Filter by type...")
    filter_by_type()
    
    print("4. Filter with multiple criteria...")
    filter_multiple_criteria()
    
    print("5. Dynamic filtering with slider...")
    dynamic_filtering()