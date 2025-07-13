import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
import pybaseball as pyb

logger = logging.getLogger(__name__)

class PyBaseballDataValidator:
    """
    Data validation and fallback strategies for PyBaseball data collection.
    Handles null values, missing data, and provides robust fallback mechanisms.
    
    Implements three-tier fallback strategy:
    1. Previous game average (cached)
    2. Season average from PyBaseball API
    3. MLB league average (0.244)
    """
    
    def __init__(self, cache_duration_hours: int = 24):
        self.cache = {}
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.logger = logger
        self.league_average = 0.244  # 2024 MLB league batting average
    
    def validate_batting_averages(self, data: pd.DataFrame, player_id: Optional[str] = None) -> pd.DataFrame:
        """
        Validate and clean batting average data with comprehensive fallback strategy.
        
        Args:
            data: DataFrame containing player batting data
            player_id: Optional player ID for targeted validation
            
        Returns:
            DataFrame with validated and cleaned batting averages
        """
        if data is None or data.empty:
            self.logger.warning("Empty or None data provided for batting average validation")
            return pd.DataFrame()
        
        validated_data = data.copy()
        
        # Check for batting average columns
        avg_columns = [col for col in validated_data.columns if 'avg' in col.lower() or 'average' in col.lower()]
        
        if not avg_columns:
            self.logger.info("No batting average columns found, checking for calculable stats")
            validated_data = self._calculate_batting_average(validated_data)
            avg_columns = ['calculated_avg']
        
        for col in avg_columns:
            if col in validated_data.columns:
                validated_data[col] = self._apply_batting_average_fallback(
                    validated_data[col], 
                    player_id, 
                    col
                )
        
        return validated_data
    
    def _apply_batting_average_fallback(self, avg_series: pd.Series, player_id: Optional[str], column_name: str) -> pd.Series:
        """
        Apply three-tier fallback strategy for null batting averages.
        
        Tier 1: Use previous game average for same player
        Tier 2: Use season average for same player  
        Tier 3: Use league average or mark as INSUFFICIENT_DATA
        """
        validated_series = avg_series.copy()
        
        # Create mask for invalid values: null, zero, negative, or >1.0
        invalid_mask = (validated_series.isnull() | 
                       (validated_series == 0) | 
                       (validated_series < 0) | 
                       (validated_series > 1.0))
        
        if not invalid_mask.any():
            return validated_series
        
        self.logger.info(f"Found {invalid_mask.sum()} invalid values in {column_name}, applying fallback strategy")
        
        # Tier 1: Previous game average
        validated_series = self._apply_previous_game_fallback(validated_series, player_id)
        
        # Tier 2: Season average
        validated_series = self._apply_season_average_fallback(validated_series, player_id)
        
        # Tier 3: League average or mark insufficient
        validated_series = self._apply_final_fallback(validated_series)
        
        remaining_invalid = (validated_series.isnull() | 
                            (validated_series < 0) | 
                            (validated_series > 1.0)).sum()
        if remaining_invalid > 0:
            self.logger.warning(f"Still have {remaining_invalid} invalid values after all fallback strategies")
        
        return validated_series
    
    def _apply_previous_game_fallback(self, series: pd.Series, player_id: Optional[str]) -> pd.Series:
        """Tier 1: Use previous valid game average for the same player."""
        if player_id and player_id in self.cache:
            cached_data = self.cache[player_id]
            if 'previous_avg' in cached_data and self._is_cache_valid(cached_data['timestamp']):
                previous_avg = cached_data['previous_avg']
                invalid_mask = (series.isnull() | (series == 0) | (series < 0) | (series > 1.0))
                series.loc[invalid_mask] = previous_avg
                self.logger.info(f"Applied previous game fallback: {previous_avg:.3f} for {invalid_mask.sum()} values")
        
        return series
    
    def _apply_season_average_fallback(self, series: pd.Series, player_id: Optional[str]) -> pd.Series:
        """Tier 2: Calculate and use season average for the player."""
        if player_id:
            try:
                season_avg = self._get_player_season_average(player_id)
                if season_avg is not None:
                    invalid_mask = (series.isnull() | (series == 0) | (series < 0) | (series > 1.0))
                    if invalid_mask.any():
                        series.loc[invalid_mask] = season_avg
                        self.logger.info(f"Applied season average fallback: {season_avg:.3f} for {invalid_mask.sum()} values")
            except Exception as e:
                self.logger.error(f"Error getting season average for player {player_id}: {e}")
        
        return series
    
    def _apply_final_fallback(self, series: pd.Series) -> pd.Series:
        """Tier 3: Use league average as final fallback."""
        invalid_mask = (series.isnull() | (series == 0) | (series < 0) | (series > 1.0))
        
        if invalid_mask.any():
            series.loc[invalid_mask] = self.league_average
            self.logger.warning(f"Applied league average fallback ({self.league_average}) for {invalid_mask.sum()} values")
        
        return series
    
    def _calculate_batting_average(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate batting average from available data if not present."""
        result_data = data.copy()
        
        if 'hits' in data.columns and 'at_bats' in data.columns:
            # Standard calculation: hits / at_bats
            at_bats_nonzero = data['at_bats'].replace(0, np.nan)
            result_data['calculated_avg'] = data['hits'] / at_bats_nonzero
            result_data['calculated_avg'] = result_data['calculated_avg'].fillna(self.league_average)
            self.logger.info("Calculated batting average from hits and at_bats")
        elif 'events' in data.columns:
            # Calculate from Statcast events data
            result_data['calculated_avg'] = self._calculate_avg_from_events(data)
            self.logger.info("Calculated batting average from Statcast events")
        else:
            # No calculable data available
            result_data['calculated_avg'] = self.league_average
            self.logger.warning("No batting average data available, using league average")
        
        return result_data
    
    def _calculate_avg_from_events(self, data: pd.DataFrame) -> pd.Series:
        """Calculate batting average from Statcast events data."""
        if 'events' not in data.columns:
            return pd.Series([self.league_average] * len(data))
        
        hit_events = ['single', 'double', 'triple', 'home_run']
        
        # Group by player if player column exists
        if 'player_name' in data.columns:
            player_stats = data.groupby('player_name').apply(
                lambda x: self._calc_player_avg_from_events(x, hit_events)
            )
            # Map back to original dataframe
            return data['player_name'].map(player_stats).fillna(self.league_average)
        else:
            # Calculate overall average
            return pd.Series([self._calc_overall_avg_from_events(data, hit_events)] * len(data))
    
    def _calc_player_avg_from_events(self, player_data: pd.DataFrame, hit_events: List[str]) -> float:
        """Calculate batting average for a single player from events."""
        if player_data.empty:
            return self.league_average
        
        total_abs = len(player_data)
        hits = player_data['events'].isin(hit_events).sum()
        
        return hits / total_abs if total_abs > 0 else self.league_average
    
    def _calc_overall_avg_from_events(self, data: pd.DataFrame, hit_events: List[str]) -> float:
        """Calculate overall batting average from events data."""
        if data.empty:
            return self.league_average
        
        total_abs = len(data)
        hits = data['events'].isin(hit_events).sum()
        
        return hits / total_abs if total_abs > 0 else self.league_average
    
    def _get_player_season_average(self, player_id: str) -> Optional[float]:
        """Get player's season batting average with caching."""
        cache_key = f"season_avg_{player_id}"
        
        if cache_key in self.cache:
            cached_entry = self.cache[cache_key]
            if self._is_cache_valid(cached_entry['timestamp']):
                return cached_entry['value']
        
        try:
            # Get current season data
            current_year = datetime.now().year
            start_date = f"{current_year}-03-01"
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            season_data = pyb.statcast_batter(start_date, end_date, player_id)
            
            if season_data is not None and not season_data.empty:
                season_avg = self._calc_overall_avg_from_events(
                    season_data, 
                    ['single', 'double', 'triple', 'home_run']
                )
                
                # Cache the result
                self.cache[cache_key] = {
                    'value': season_avg,
                    'timestamp': datetime.now()
                }
                
                return season_avg
            
        except Exception as e:
            self.logger.error(f"Error fetching season data for player {player_id}: {e}")
        
        return None
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cached data is still valid."""
        return datetime.now() - timestamp < self.cache_duration
    
    def validate_player_data(self, player_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation for player data with null checking.
        
        Args:
            player_data: Dictionary containing player information
            
        Returns:
            Validated player data with fallback values
        """
        if not player_data:
            return self._get_default_player_data()
        
        validated_data = player_data.copy()
        
        # Validate required fields
        required_fields = {
            'name': 'Unknown Player',
            'player_id': None,
            'position': 'Unknown',
            'team': 'Free Agent',
            'batting_avg': self.league_average
        }
        
        for field, default_value in required_fields.items():
            if field not in validated_data or validated_data[field] is None:
                validated_data[field] = default_value
                self.logger.info(f"Applied default value for {field}: {default_value}")
        
        # Validate batting average specifically
        if 'batting_avg' in validated_data:
            avg = validated_data['batting_avg']
            if avg is None or avg < 0 or avg > 1:
                validated_data['batting_avg'] = self.league_average
                self.logger.warning(f"Invalid batting average {avg}, using league average")
        
        # Add data quality flag
        validated_data['data_quality'] = self._assess_data_quality(validated_data)
        
        return validated_data
    
    def _get_default_player_data(self) -> Dict[str, Any]:
        """Return default player data structure."""
        return {
            'name': 'Unknown Player',
            'player_id': None,
            'position': 'Unknown',
            'team': 'Free Agent',
            'batting_avg': self.league_average,
            'data_quality': 'INSUFFICIENT_DATA'
        }
    
    def _assess_data_quality(self, player_data: Dict[str, Any]) -> str:
        """Assess the quality of player data."""
        quality_score = 0
        total_fields = 5
        
        if player_data.get('name') and player_data['name'] != 'Unknown Player':
            quality_score += 1
        if player_data.get('player_id'):
            quality_score += 1
        if player_data.get('position') and player_data['position'] != 'Unknown':
            quality_score += 1
        if player_data.get('team') and player_data['team'] != 'Free Agent':
            quality_score += 1
        if player_data.get('batting_avg') and player_data['batting_avg'] != self.league_average:
            quality_score += 1
        
        quality_percentage = quality_score / total_fields
        
        if quality_percentage >= 0.8:
            return 'HIGH'
        elif quality_percentage >= 0.6:
            return 'MEDIUM'
        elif quality_percentage >= 0.4:
            return 'LOW'
        else:
            return 'INSUFFICIENT_DATA'
    
    def cache_player_average(self, player_id: str, batting_avg: float):
        """Cache a player's batting average for future fallback use."""
        if player_id and batting_avg is not None and 0 <= batting_avg <= 1:
            self.cache[player_id] = {
                'previous_avg': batting_avg,
                'timestamp': datetime.now()
            }
            self.logger.debug(f"Cached batting average {batting_avg:.3f} for player {player_id}")
    
    def clear_cache(self):
        """Clear the validation cache."""
        self.cache.clear()
        self.logger.info("Validation cache cleared")
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Get statistics about validation operations."""
        return {
            'cache_size': len(self.cache),
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600,
            'last_validation': datetime.now().isoformat(),
            'league_average': self.league_average
        }