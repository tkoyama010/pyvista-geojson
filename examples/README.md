# PyVista-GeoJSON Examples

This directory contains comprehensive examples demonstrating how to use the pyvista-geojson library for visualizing GeoJSON data with PyVista.

## Quick Start

To run these examples, you'll need to install the required dependencies:

```bash
pip install pyvista-geojson pyvista numpy scipy pandas ipywidgets
```

## Example Files

### 1. Basic Usage (`basic_usage.py`)
Demonstrates the fundamental usage of pyvista-geojson:
- Loading GeoJSON files
- Simple visualization
- Adding labels and basic styling

```bash
python basic_usage.py
```

### 2. Geometry Types (`geometry_types.py`)
Shows how to handle different GeoJSON geometry types:
- Point and MultiPoint geometries
- LineString and MultiLineString geometries
- Polygon and MultiPolygon geometries
- Comparative visualization of all types

```bash
python geometry_types.py
```

### 3. Filtering Examples (`filtering_example.py`)
Demonstrates various filtering techniques:
- Filter by attribute values
- Filter by ranges
- Filter by geometry types
- Dynamic filtering with interactive widgets

```bash
python filtering_example.py
```

### 4. 3D Visualization (`3d_visualization.py`)
Advanced 3D visualization techniques:
- Extruding polygons based on height attributes
- Elevation-based point visualization
- Terrain-like surface generation
- Animated and interactive 3D scenes

```bash
python 3d_visualization.py
```

### 5. Jupyter Notebook (`jupyter_example.ipynb`)
Interactive notebook demonstrating:
- Jupyter integration with PyVista
- Interactive widgets and controls
- Data analysis integration with pandas
- Export capabilities

Open with:
```bash
jupyter notebook jupyter_example.ipynb
```

## Sample Data

The `data/` directory contains sample GeoJSON files used in the examples:

- **`points.geojson`**: California cities with population and elevation data
- **`lines.geojson`**: Transportation networks (highways, interstates, transit)
- **`polygons.geojson`**: Building footprints with height and type information
- **`mixed_geometries.geojson`**: Combined dataset with points, lines, and polygons

## Example Workflows

### Beginner Workflow
1. Start with `basic_usage.py` to understand core concepts
2. Run `geometry_types.py` to see different geometry handling
3. Explore the Jupyter notebook for interactive features

### Advanced Workflow
1. Study `filtering_example.py` for data selection techniques
2. Experiment with `3d_visualization.py` for advanced 3D effects
3. Customize examples with your own GeoJSON data

## Key Features Demonstrated

### Data Loading and Visualization
- Loading GeoJSON files into PyVista meshes
- Preserving and accessing feature properties
- Basic and advanced visualization techniques

### Attribute-Based Styling
- Color coding by property values
- Size scaling based on attributes
- Categorical and continuous data visualization

### Interactive Features
- Dynamic filtering with sliders
- Multi-view layouts and subplots
- Camera controls and lighting effects

### 3D Capabilities
- Polygon extrusion based on height data
- Elevation visualization for point data
- Terrain generation from scattered data
- Animation and rotation effects

### Integration Features
- Jupyter notebook compatibility
- Pandas DataFrame integration
- Export capabilities (images, mesh data)
- Widget-based interactivity

## Customization Tips

### Using Your Own Data
Replace the sample GeoJSON files in the `data/` directory with your own:

```python
from pyvista_geojson import GeoJSONReader

# Load your GeoJSON file
reader = GeoJSONReader(\"path/to/your/file.geojson\")
mesh = reader.read()

# Visualize
mesh.plot()
```

### Filtering Your Data
Adapt the filtering examples to your data structure:

```python
# Filter by your property names
filtered_mesh = reader.read(
    filter_func=lambda props: props.get(\"your_property\") > threshold
)
```

### Styling Options
Customize colors, sizes, and visual properties:

```python
mesh.plot(
    scalars=\"your_attribute\",
    cmap=\"your_colormap\",
    point_size=20,
    line_width=5,
    opacity=0.8
)
```

## Performance Notes

- For large datasets, consider using filtering to reduce the number of features
- Use `off_screen=True` for batch processing and image generation
- Enable `show_scalar_bar=False` to improve performance for rapid updates

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Install all required packages
2. **File Not Found**: Ensure you're running from the examples directory
3. **Display Issues**: Set appropriate PyVista backend for your environment
4. **Memory Issues**: Use filtering for large datasets

### Getting Help

- Check the main pyvista-geojson documentation
- Review PyVista documentation for visualization options
- Examine the example source code for implementation details

## Contributing

Feel free to contribute additional examples or improvements:
1. Add new example scripts demonstrating specific use cases
2. Create sample data for different geographic regions or data types
3. Improve documentation and comments
4. Report issues or suggest enhancements

## License

These examples are provided under the same license as the pyvista-geojson project.