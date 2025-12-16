"""
Tests for GIS Manager
"""

import unittest
from gis_manager import (
    GISManager, 
    GISDataManager, 
    GISLayerManager,
    GISCoordinateSystem,
    GISQuerySystem
)


class TestGISDataManager(unittest.TestCase):
    """Test Data Manager component"""
    
    def setUp(self):
        self.data_manager = GISDataManager()
    
    def test_add_feature(self):
        feature = {"type": "Feature", "geometry": {}}
        self.data_manager.add_feature(feature)
        self.assertEqual(len(self.data_manager.get_features()), 1)
    
    def test_clear_features(self):
        self.data_manager.add_feature({"test": "data"})
        self.data_manager.clear()
        self.assertEqual(len(self.data_manager.get_features()), 0)


class TestGISLayerManager(unittest.TestCase):
    """Test Layer Manager component"""
    
    def setUp(self):
        self.layer_manager = GISLayerManager()
    
    def test_add_layer(self):
        self.layer_manager.add_layer("test_layer")
        self.assertIn("test_layer", self.layer_manager.list_layers())
    
    def test_get_layer(self):
        self.layer_manager.add_layer("roads", "vector")
        layer = self.layer_manager.get_layer("roads")
        self.assertIsNotNone(layer)
        self.assertEqual(layer["type"], "vector")


class TestGISCoordinateSystem(unittest.TestCase):
    """Test Coordinate System component"""
    
    def setUp(self):
        self.coord_system = GISCoordinateSystem()
    
    def test_default_projection(self):
        info = self.coord_system.get_projection_info()
        self.assertEqual(info["epsg"], 4326)
    
    def test_transform_same_system(self):
        x, y = self.coord_system.transform(10.0, 20.0, 4326)
        self.assertEqual(x, 10.0)
        self.assertEqual(y, 20.0)


class TestGISQuerySystem(unittest.TestCase):
    """Test Query System component"""
    
    def setUp(self):
        self.data_manager = GISDataManager()
        self.query_system = GISQuerySystem(self.data_manager)
        
        # Add test features
        self.data_manager.add_feature({
            "geometry": {"coordinates": [10, 20]},
            "properties": {"name": "Feature1", "type": "point"}
        })
        self.data_manager.add_feature({
            "geometry": {"coordinates": [30, 40]},
            "properties": {"name": "Feature2", "type": "line"}
        })
    
    def test_query_by_bbox(self):
        results = self.query_system.query_by_bbox(5, 15, 15, 25)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["properties"]["name"], "Feature1")
    
    def test_query_by_attribute(self):
        results = self.query_system.query_by_attribute("type", "point")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["properties"]["name"], "Feature1")


class TestGISManager(unittest.TestCase):
    """Test main GIS Manager integration"""
    
    def setUp(self):
        self.gis = GISManager()
    
    def test_version(self):
        self.assertEqual(self.gis.version(), "1.1.1.1")
    
    def test_create_point_feature(self):
        feature = self.gis.create_point_feature(10.0, 20.0, {"name": "Test"})
        self.assertEqual(feature["geometry"]["type"], "Point")
        self.assertEqual(feature["geometry"]["coordinates"], [10.0, 20.0])
        self.assertEqual(feature["properties"]["name"], "Test")
    
    def test_get_info(self):
        self.gis.create_point_feature(10.0, 20.0)
        self.gis.layer_manager.add_layer("test")
        info = self.gis.get_info()
        
        self.assertEqual(info["version"], "1.1.1.1")
        self.assertEqual(info["features_count"], 1)
        self.assertEqual(info["layers_count"], 1)
        self.assertIn("projection", info)


if __name__ == "__main__":
    unittest.main()
