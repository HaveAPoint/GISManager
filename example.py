"""
Example usage of GIS Manager

Demonstrates the four core components of the GIS system.
"""

from gis_manager import GISManager


def main():
    print("=" * 60)
    print("GIS Manager Example - Version 1.1.1.1")
    print("=" * 60)
    print()
    
    # Initialize GIS Manager
    gis = GISManager()
    print(f"✓ Initialized GIS Manager v{gis.version()}")
    print()
    
    # Component 1: Data Management
    print("1. DATA MANAGEMENT")
    print("-" * 60)
    gis.create_point_feature(10.0, 20.0, {"name": "City Hall", "type": "building"})
    gis.create_point_feature(12.0, 22.0, {"name": "Main Street", "type": "road"})
    gis.create_point_feature(15.0, 25.0, {"name": "Park", "type": "recreation"})
    print(f"✓ Added {len(gis.data_manager.get_features())} features")
    print()
    
    # Component 2: Layer Management
    print("2. LAYER MANAGEMENT")
    print("-" * 60)
    gis.layer_manager.add_layer("infrastructure", "vector")
    gis.layer_manager.add_layer("land_use", "vector")
    gis.layer_manager.add_layer("boundaries", "vector")
    print(f"✓ Created {len(gis.layer_manager.list_layers())} layers:")
    for layer_name in gis.layer_manager.list_layers():
        print(f"  - {layer_name}")
    print()
    
    # Component 3: Coordinate System
    print("3. COORDINATE SYSTEM")
    print("-" * 60)
    proj_info = gis.coordinate_system.get_projection_info()
    print(f"✓ Using projection: {proj_info['name']}")
    x, y = gis.coordinate_system.transform(10.0, 20.0, 4326)
    print(f"✓ Transform example: (10.0, 20.0) -> ({x}, {y})")
    print()
    
    # Component 4: Query System
    print("4. QUERY SYSTEM")
    print("-" * 60)
    
    # Spatial query
    bbox_results = gis.query_system.query_by_bbox(9, 19, 13, 23)
    print(f"✓ Bounding box query (9,19,13,23): {len(bbox_results)} features found")
    for feature in bbox_results:
        props = feature.get("properties", {})
        coords = feature["geometry"]["coordinates"]
        print(f"  - {props.get('name')} at ({coords[0]}, {coords[1]})")
    
    # Attribute query
    building_results = gis.query_system.query_by_attribute("type", "building")
    print(f"✓ Attribute query (type=building): {len(building_results)} features found")
    for feature in building_results:
        props = feature.get("properties", {})
        print(f"  - {props.get('name')}")
    print()
    
    # Summary
    print("=" * 60)
    print("SYSTEM SUMMARY")
    print("=" * 60)
    info = gis.get_info()
    print(f"Version:    {info['version']}")
    print(f"Features:   {info['features_count']}")
    print(f"Layers:     {info['layers_count']}")
    print(f"Projection: {info['projection']['name']}")
    print()


if __name__ == "__main__":
    main()
