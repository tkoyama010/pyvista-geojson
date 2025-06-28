# pyvista-geojson

A Python library to read and visualize GeoJSON data using [PyVista](https://github.com/pyvista/pyvista).

![PyPI](https://img.shields.io/pypi/v/pyvista-geojson)
![License](https://img.shields.io/github/license/your-username/pyvista-geojson)

## Overview

`pyvista-geojson` is a lightweight Python library that allows you to easily load GeoJSON files and visualize them using PyVista. It supports basic geometry types such as `Point`, `LineString`, `Polygon`, and `MultiPolygon`, and maps their attributes to PyVista-compatible structures for interactive 3D rendering.

## Features

- 📍 Load GeoJSON files into PyVista meshes
- 🧭 Support for Point, LineString, Polygon, and MultiPolygon
- 🖼️ Attribute-based filtering and styling (e.g. color by property)
- 🌐 Interactive 3D visualization using PyVista's `Plotter`
- 🧪 Compatible with Jupyter Notebooks
- 🔧 Simple API with minimal dependencies

## Installation

```bash
pip install pyvista-geojson
````

## Usage

### Load and visualize a GeoJSON file

```python
from pyvista_geojson import GeoJSONReader
import pyvista as pv

# Load the GeoJSON file
reader = GeoJSONReader("example.geojson")

# Convert to PyVista mesh
mesh = reader.mesh  # or reader.to_pyvista()

# Plot
plotter = pv.Plotter()
plotter.add_mesh(mesh, show_edges=True)
plotter.show()
```

### Filter features by attribute

```python
# Filter only features where property 'type' == 'building'
buildings = reader.filter_by_property("type", "building")
pv.Plotter().add_mesh(buildings).show()
```

## Supported Geometry Types

* ✅ Point
* ✅ MultiPoint
* ✅ LineString
* ✅ MultiLineString
* ✅ Polygon
* ✅ MultiPolygon

## Development

```bash
git clone https://github.com/your-username/pyvista-geojson.git
cd pyvista-geojson
pip install -e .[dev]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

* [PyVista](https://github.com/pyvista/pyvista)
* [GeoJSON specification](https://datatracker.ietf.org/doc/html/rfc7946)
* [Shapely](https://github.com/shapely/shapely) for geometry handling
