# GISManager

A simple Geographic Information System (GIS) Manager with four core components.

## Version: 1.1.1.1

## Features

The GIS Manager provides **four** essential GIS components:

1. **Data Management** - Store and retrieve geographic features
2. **Layer Management** - Organize spatial data into layers
3. **Coordinate System** - Handle coordinate transformations and projections
4. **Query System** - Perform spatial and attribute queries

## Installation

```bash
# Clone the repository
git clone https://github.com/HaveAPoint/GISManager.git
cd GISManager
```

## Usage

```python
from gis_manager import GISManager

# Initialize the GIS Manager
gis = GISManager()

# Create point features
gis.create_point_feature(10.0, 20.0, {"name": "Location 1", "type": "poi"})
gis.create_point_feature(15.0, 25.0, {"name": "Location 2", "type": "poi"})

# Create layers
gis.layer_manager.add_layer("roads", "vector")
gis.layer_manager.add_layer("buildings", "vector")

# Query features by bounding box
results = gis.query_system.query_by_bbox(5, 15, 20, 30)

# Query features by attribute
poi_results = gis.query_system.query_by_attribute("type", "poi")

# Get system information
info = gis.get_info()
print(f"Version: {info['version']}")
print(f"Features: {info['features_count']}")
print(f"Layers: {info['layers_count']}")
```

## Running Tests

```bash
python test_gis_manager.py
```

## Components

### 1. GISDataManager
Manages the storage and retrieval of geographic features.

### 2. GISLayerManager
Organizes features into logical layers with different types (vector, raster).

### 3. GISCoordinateSystem
Handles coordinate reference systems and transformations (default: WGS84/EPSG:4326).

### 4. GISQuerySystem
Performs spatial queries (bounding box) and attribute-based queries.

## License

MIT