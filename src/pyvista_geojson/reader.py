"""
GeoJSON Reader for PyVista
"""

import json
import numpy as np
import pyvista as pv
from typing import Optional, Callable, Dict, Any, List, Tuple


class GeoJSONReader:
    """
    A reader class for converting GeoJSON files to PyVista meshes.
    
    This class can handle various GeoJSON geometry types including Points,
    LineStrings, and Polygons, and converts them to appropriate PyVista
    data structures for 3D visualization.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize the GeoJSON reader.
        
        Parameters
        ----------
        file_path : str
            Path to the GeoJSON file to read
        """
        self.file_path = file_path
        self._data = None
        
    def _load_data(self):
        """Load GeoJSON data from file."""
        if self._data is None:
            with open(self.file_path, 'r') as f:
                self._data = json.load(f)
        return self._data
    
    def read(self, filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None) -> pv.PolyData:
        """
        Read the GeoJSON file and convert to PyVista mesh.
        
        Parameters
        ----------
        filter_func : callable, optional
            Function to filter features based on their properties.
            Should return True to include the feature, False to exclude.
            
        Returns
        -------
        pv.PolyData
            PyVista mesh containing the GeoJSON geometry and attributes
        """
        data = self._load_data()
        
        if data['type'] != 'FeatureCollection':
            raise ValueError("Only FeatureCollection GeoJSON files are supported")
        
        features = data['features']
        
        # Apply filter if provided
        if filter_func:
            features = [f for f in features if filter_func(f.get('properties', {}))]
        
        if not features:
            # Return empty mesh if no features
            return pv.PolyData()
        
        # Separate features by geometry type
        points = []
        lines = []
        polygons = []
        point_data = {}
        line_data = {}
        polygon_data = {}
        
        for feature in features:
            geom = feature['geometry']
            props = feature.get('properties', {})
            geom_type = geom['type']
            
            if geom_type == 'Point':
                coords = geom['coordinates']
                # Add Z coordinate if not present
                if len(coords) == 2:
                    coords.append(0.0)
                points.append(coords)
                
                # Store properties for this point
                for key, value in props.items():
                    if key not in point_data:
                        point_data[key] = []
                    point_data[key].append(value)
                    
            elif geom_type == 'LineString':
                coords = geom['coordinates']
                # Convert to 3D if needed
                line_points = []
                for coord in coords:
                    if len(coord) == 2:
                        coord.append(0.0)
                    line_points.append(coord)
                lines.append(line_points)
                
                # Store properties for this line
                for key, value in props.items():
                    if key not in line_data:
                        line_data[key] = []
                    line_data[key].append(value)
                    
            elif geom_type == 'Polygon':
                # Handle exterior ring (first ring)
                exterior_ring = geom['coordinates'][0]
                poly_points = []
                for coord in exterior_ring:
                    if len(coord) == 2:
                        coord.append(0.0)
                    poly_points.append(coord)
                polygons.append(poly_points)
                
                # Store properties for this polygon
                for key, value in props.items():
                    if key not in polygon_data:
                        polygon_data[key] = []
                    polygon_data[key].append(value)
        
        # Create combined mesh
        mesh = self._create_combined_mesh(
            points, lines, polygons,
            point_data, line_data, polygon_data
        )
        
        return mesh
    
    def _create_combined_mesh(self, points: List, lines: List, polygons: List,
                            point_data: Dict, line_data: Dict, polygon_data: Dict) -> pv.PolyData:
        """Create a combined PyVista mesh from all geometry types."""
        
        all_points = []
        all_cells = []
        cell_types = []
        combined_data = {}
        
        point_offset = 0
        
        # Add points
        if points:
            all_points.extend(points)
            for i in range(len(points)):
                all_cells.extend([1, point_offset + i])  # VTK_VERTEX
                cell_types.append(1)  # VTK_VERTEX
            
            # Add point data
            for key, values in point_data.items():
                if key not in combined_data:
                    combined_data[key] = []
                combined_data[key].extend(values)
                
            point_offset = len(points)
        
        # Add lines
        for line, line_props_idx in zip(lines, range(len(lines))):
            line_start = point_offset
            all_points.extend(line)
            
            # Create line cell
            n_points = len(line)
            cell = [n_points] + list(range(line_start, line_start + n_points))
            all_cells.extend(cell)
            cell_types.append(4)  # VTK_POLY_LINE
            
            # Add line data (replicate for each point in the line)
            for key, values in line_data.items():
                if key not in combined_data:
                    combined_data[key] = [None] * point_offset
                # Extend with None for points not in this line, then add line value
                combined_data[key].extend([values[line_props_idx]] * n_points)
            
            # Fill None for point data keys not in line data
            for key in point_data.keys():
                if key not in line_data:
                    if key not in combined_data:
                        combined_data[key] = [None] * point_offset
                    combined_data[key].extend([None] * n_points)
                    
            point_offset += n_points
        
        # Add polygons
        for polygon, poly_props_idx in zip(polygons, range(len(polygons))):
            poly_start = point_offset
            all_points.extend(polygon)
            
            # Create polygon cell
            n_points = len(polygon)
            cell = [n_points] + list(range(poly_start, poly_start + n_points))
            all_cells.extend(cell)
            cell_types.append(7)  # VTK_POLYGON
            
            # Add polygon data
            for key, values in polygon_data.items():
                if key not in combined_data:
                    combined_data[key] = [None] * point_offset
                combined_data[key].extend([values[poly_props_idx]] * n_points)
            
            # Fill None for other data keys
            for key in list(point_data.keys()) + list(line_data.keys()):
                if key not in polygon_data:
                    if key not in combined_data:
                        combined_data[key] = [None] * point_offset
                    combined_data[key].extend([None] * n_points)
                    
            point_offset += n_points
        
        if not all_points:
            return pv.PolyData()
        
        # Create PyVista mesh
        points_array = np.array(all_points, dtype=float)
        mesh = pv.PolyData(points_array)
        
        # Add cells
        if all_cells:
            cells_array = np.array(all_cells, dtype=int)
            cell_types_array = np.array(cell_types, dtype=np.uint8)
            mesh = pv.UnstructuredGrid(cells_array, cell_types_array, points_array)
            # Convert to PolyData for better compatibility
            mesh = mesh.extract_surface()
        
        # Add point data
        for key, values in combined_data.items():
            if len(values) == len(points_array):
                # Convert to appropriate numpy array
                try:
                    # Try numeric conversion first
                    numeric_values = []
                    for v in values:
                        if v is None:
                            numeric_values.append(0.0)  # Default for None
                        else:
                            numeric_values.append(float(v))
                    mesh.point_data[key] = np.array(numeric_values)
                except (ValueError, TypeError):
                    # If not numeric, store as string array
                    string_values = [str(v) if v is not None else "" for v in values]
                    mesh.point_data[key] = np.array(string_values)
        
        return mesh