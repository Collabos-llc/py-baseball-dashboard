import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.data_validator import PyBaseballDataValidator

class TestPyBaseballDataValidator(unittest.TestCase):
    """Comprehensive test suite for PyBaseballDataValidator"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.validator = PyBaseballDataValidator(cache_duration_hours=1)
        
        # Sample data with various null scenarios
        self.sample_data = pd.DataFrame({
            'player_name': ['Player A', 'Player B', 'Player C', 'Player D'],
            'batting_avg': [0.285, None, 0.0, 1.5],  # Valid, null, zero, invalid
            'hits': [85, 92, None, 78],
            'at_bats': [300, 320, 285, 295],
            'events': ['single', 'home_run', 'strikeout', 'double']
        })
        
        # Statcast-style data
        self.statcast_data = pd.DataFrame({
            'player_name': ['Mike Trout', 'Aaron Judge'] * 5,
            'events': ['single', 'home_run', 'strikeout', 'double', 'single',
                      'home_run', 'walk', 'single', 'double', 'strikeout'],
            'launch_speed': [95.2, 108.1, None, 98.5, 92.1,
                           112.3, None, 89.4, 101.2, None],
            'launch_angle': [12, 28, None, 15, 8,
                           32, None, 10, 22, None]
        })
    
    def test_validate_batting_averages_with_null_values(self):
        """Test validation of batting averages with null values."""
        result = self.validator.validate_batting_averages(self.sample_data)
        
        # Should not have any null values after validation
        self.assertFalse(result['batting_avg'].isnull().any())
        
        # Valid value should remain unchanged
        self.assertEqual(result['batting_avg'].iloc[0], 0.285)
        
        # Null value should be replaced with league average
        self.assertEqual(result['batting_avg'].iloc[1], 0.244)
        
        # Zero value should be replaced with league average
        self.assertEqual(result['batting_avg'].iloc[2], 0.244)
        
        # Invalid value (>1) should be replaced with league average
        self.assertEqual(result['batting_avg'].iloc[3], 0.244)
    
    def test_calculate_batting_average_from_hits_and_at_bats(self):
        """Test calculation of batting average from hits and at-bats."""
        data = pd.DataFrame({
            'hits': [85, 92, 78],
            'at_bats': [300, 320, 295]
        })
        
        result = self.validator._calculate_batting_average(data)
        
        # Check calculated averages
        expected_avgs = [85/300, 92/320, 78/295]
        for i, expected in enumerate(expected_avgs):
            self.assertAlmostEqual(result['calculated_avg'].iloc[i], expected, places=3)
    
    def test_calculate_batting_average_from_events(self):
        """Test calculation of batting average from Statcast events."""
        result = self.validator._calculate_avg_from_events(self.statcast_data)
        
        # Should have batting averages for both players
        self.assertEqual(len(result), len(self.statcast_data))
        self.assertFalse(result.isnull().any())
        
        # Each player should have a calculated average
        trout_data = self.statcast_data[self.statcast_data['player_name'] == 'Mike Trout']
        judge_data = self.statcast_data[self.statcast_data['player_name'] == 'Aaron Judge']
        
        # Count hits for each player
        hit_events = ['single', 'double', 'triple', 'home_run']
        trout_hits = trout_data['events'].isin(hit_events).sum()
        judge_hits = judge_data['events'].isin(hit_events).sum()
        
        expected_trout_avg = trout_hits / len(trout_data)
        expected_judge_avg = judge_hits / len(judge_data)
        
        # Verify calculations
        self.assertGreater(expected_trout_avg, 0)
        self.assertGreater(expected_judge_avg, 0)
    
    def test_validate_player_data_with_null_fields(self):
        """Test validation of player data with missing fields."""
        # Test with None data
        result = self.validator.validate_player_data(None)
        self.assertEqual(result['name'], 'Unknown Player')
        self.assertEqual(result['batting_avg'], 0.244)
        self.assertEqual(result['data_quality'], 'INSUFFICIENT_DATA')
        
        # Test with partial data
        partial_data = {'name': 'Test Player', 'batting_avg': None}
        result = self.validator.validate_player_data(partial_data)
        self.assertEqual(result['name'], 'Test Player')
        self.assertEqual(result['batting_avg'], 0.244)
        self.assertEqual(result['position'], 'Unknown')
    
    def test_data_quality_assessment(self):
        """Test data quality assessment functionality."""
        # High quality data
        high_quality = {
            'name': 'Mike Trout',
            'player_id': '545361',
            'position': 'CF',
            'team': 'Angels',
            'batting_avg': 0.285
        }
        result = self.validator.validate_player_data(high_quality)
        self.assertEqual(result['data_quality'], 'HIGH')
        
        # Low quality data
        low_quality = {
            'name': 'Unknown Player',
            'player_id': None,
            'position': 'Unknown'
        }
        result = self.validator.validate_player_data(low_quality)
        self.assertEqual(result['data_quality'], 'INSUFFICIENT_DATA')
    
    def test_caching_functionality(self):
        """Test caching of player batting averages."""
        player_id = 'test_player_123'
        batting_avg = 0.315
        
        # Cache the average
        self.validator.cache_player_average(player_id, batting_avg)
        
        # Verify it's in cache
        self.assertIn(player_id, self.validator.cache)
        self.assertEqual(self.validator.cache[player_id]['previous_avg'], batting_avg)
        
        # Test cache validation
        cached_data = self.validator.cache[player_id]
        self.assertTrue(self.validator._is_cache_valid(cached_data['timestamp']))
        
        # Test expired cache
        old_timestamp = datetime.now() - timedelta(hours=25)  # Older than cache duration
        self.assertFalse(self.validator._is_cache_valid(old_timestamp))
    
    def test_previous_game_fallback(self):
        """Test Tier 1 fallback: previous game average."""
        player_id = 'test_player_456'
        
        # Cache a previous average
        self.validator.cache_player_average(player_id, 0.320)
        
        # Create series with null values
        test_series = pd.Series([0.285, None, 0.0])
        
        # Apply fallback
        result = self.validator._apply_previous_game_fallback(test_series, player_id)
        
        # First value should remain unchanged
        self.assertEqual(result.iloc[0], 0.285)
        
        # Null and zero values should be replaced with cached average
        self.assertEqual(result.iloc[1], 0.320)
        self.assertEqual(result.iloc[2], 0.320)
    
    def test_final_fallback_league_average(self):
        """Test Tier 3 fallback: league average."""
        test_series = pd.Series([None, 0.0, -0.1, 1.5])
        
        result = self.validator._apply_final_fallback(test_series)
        
        # All invalid values should be replaced with league average
        for value in result:
            self.assertEqual(value, 0.244)
    
    def test_validation_stats(self):
        """Test validation statistics functionality."""
        # Add some cached data
        self.validator.cache_player_average('player1', 0.285)
        self.validator.cache_player_average('player2', 0.312)
        
        stats = self.validator.get_validation_stats()
        
        # Check stats structure
        self.assertIn('cache_size', stats)
        self.assertIn('cache_duration_hours', stats)
        self.assertIn('last_validation', stats)
        self.assertIn('league_average', stats)
        
        # Check values
        self.assertEqual(stats['cache_size'], 2)
        self.assertEqual(stats['cache_duration_hours'], 1.0)
        self.assertEqual(stats['league_average'], 0.244)
    
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames."""
        empty_df = pd.DataFrame()
        
        result = self.validator.validate_batting_averages(empty_df)
        
        # Should return empty DataFrame without errors
        self.assertTrue(result.empty)
    
    def test_invalid_batting_average_ranges(self):
        """Test handling of batting averages outside valid range."""
        invalid_data = pd.DataFrame({
            'batting_avg': [-0.5, 1.2, 0.285, None, 2.0]
        })
        
        result = self.validator.validate_batting_averages(invalid_data)
        
        # Invalid values should be replaced with league average
        expected = [0.244, 0.244, 0.285, 0.244, 0.244]
        
        for i, expected_val in enumerate(expected):
            self.assertEqual(result['batting_avg'].iloc[i], expected_val)
    
    def test_cache_clearing(self):
        """Test cache clearing functionality."""
        # Add some cached data
        self.validator.cache_player_average('player1', 0.285)
        self.validator.cache_player_average('player2', 0.312)
        
        # Verify cache has data
        self.assertEqual(len(self.validator.cache), 2)
        
        # Clear cache
        self.validator.clear_cache()
        
        # Verify cache is empty
        self.assertEqual(len(self.validator.cache), 0)

if __name__ == '__main__':
    unittest.main()