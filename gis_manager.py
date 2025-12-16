"""
GIS Manager - A simple Geographic Information System Manager
Version: 1.1.1.1

This module provides four core GIS components:
1. Data Management
2. Layer Management
3. Coordinate System
4. Query System
"""

from typing import List, Dict, Tuple, Optional, Any
import json


class GISDataManager:
    """Component 1: Manages geographic data storage and retrieval"""
    
    def __init__(self):
        self.features = []
    
    def add_feature(self, feature: Dict) -> None:
        """Add a geographic feature to the data store"""
        self.features.append(feature)
    
    def get_features(self) -> List[Dict]:
        """Retrieve all features"""
        return self.features
    
    def clear(self) -> None:
        """Clear all features"""
        self.features = []


class GISLayerManager:
    """Component 2: Manages spatial layers and their organization"""
    
    def __init__(self):
        self.layers = {}
    
    def add_layer(self, name: str, layer_type: str = "vector") -> None:
        """Add a new layer"""
        self.layers[name] = {
            "type": layer_type,
            "features": [],
            "visible": True
        }
    
    def get_layer(self, name: str) -> Optional[Dict]:
        """Get a specific layer"""
        return self.layers.get(name)
    
    def list_layers(self) -> List[str]:
        """List all layer names"""
        return list(self.layers.keys())


class GISCoordinateSystem:
    """Component 3: Handles coordinate transformations and projections"""
    
    def __init__(self, epsg_code: int = 4326):
        self.epsg_code = epsg_code  # Default to WGS84
    
    def transform(self, x: float, y: float, target_epsg: int) -> Tuple[float, float]:
        """Transform coordinates from one system to another"""
        # Simplified transformation (in real implementation, use pyproj)
        if self.epsg_code == target_epsg:
            return (x, y)
        # Placeholder transformation
        return (x, y)
    
    def get_projection_info(self) -> Dict:
        """Get information about current projection"""
        return {
            "epsg": self.epsg_code,
            "name": f"EPSG:{self.epsg_code}"
        }


class GISQuerySystem:
    """Component 4: Performs spatial queries and analysis"""
    
    def __init__(self, data_manager: GISDataManager):
        self.data_manager = data_manager
    
    def query_by_bbox(self, min_x: float, min_y: float, 
                      max_x: float, max_y: float) -> List[Dict]:
        """Query features within a bounding box"""
        results = []
        for feature in self.data_manager.get_features():
            if "geometry" in feature:
                coords = feature["geometry"].get("coordinates", [])
                if coords and len(coords) >= 2:
                    x, y = coords[0], coords[1]
                    if min_x <= x <= max_x and min_y <= y <= max_y:
                        results.append(feature)
        return results
    
    def query_by_attribute(self, key: str, value: Any) -> List[Dict]:
        """Query features by attribute value"""
        results = []
        for feature in self.data_manager.get_features():
            if "properties" in feature:
                if feature["properties"].get(key) == value:
                    results.append(feature)
        return results


class GISManager:
    """Main GIS Manager integrating all four components"""
    
    def __init__(self):
        self.data_manager = GISDataManager()
        self.layer_manager = GISLayerManager()
        self.coordinate_system = GISCoordinateSystem()
        self.query_system = GISQuerySystem(self.data_manager)
    
    def version(self) -> str:
        """Return version number"""
        return "1.1.1.1"
    
    def create_point_feature(self, x: float, y: float, properties: Dict = None) -> Dict:
        """Create a point feature"""
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [x, y]
            },
            "properties": properties or {}
        }
        self.data_manager.add_feature(feature)
        return feature
    
    def get_info(self) -> Dict:
        """Get system information"""
        return {
            "version": self.version(),
            "features_count": len(self.data_manager.get_features()),
            "layers_count": len(self.layer_manager.list_layers()),
            "projection": self.coordinate_system.get_projection_info()
        }


if __name__ == "__main__":
    # Example usage
    gis = GISManager()
    print(f"GIS Manager v{gis.version()}")
    
    # Create some sample features
    gis.create_point_feature(10.0, 20.0, {"name": "Point 1"})
    gis.create_point_feature(15.0, 25.0, {"name": "Point 2"})
    
    # Create layers
    gis.layer_manager.add_layer("roads", "vector")
    gis.layer_manager.add_layer("buildings", "vector")
    
    # Display info
    info = gis.get_info()
    print(json.dumps(info, indent=2))
