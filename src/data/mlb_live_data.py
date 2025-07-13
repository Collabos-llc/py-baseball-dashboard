import statsapi
import pandas as pd
from datetime import datetime, timedelta
import redis
import json
import logging
import os

class MLBLiveData:
    def __init__(self, redis_host='redis', redis_port=6379):
        """Initialize MLB Live Data collector with caching"""
        try:
            self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
            # Test connection
            self.redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.redis_client = None
            
        self.logger = logging.getLogger(__name__)
        
    def get_todays_games(self):
        """Get all games for today"""
        cache_key = f"games_{datetime.now().strftime('%Y-%m-%d')}"
        
        # Check cache first
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")
        
        try:
            # Get today's schedule
            schedule = statsapi.schedule()
            games_data = []
            
            for game in schedule:
                game_info = {
                    'game_id': game['game_id'],
                    'away_team': game['away_name'],
                    'home_team': game['home_name'],
                    'game_time': game['game_datetime'],
                    'status': game['status'],
                    'away_score': game.get('away_score', 0),
                    'home_score': game.get('home_score', 0),
                    'inning': game.get('current_inning', 0),
                    'venue': game.get('venue_name', '')
                }
                games_data.append(game_info)
            
            # Cache for 5 minutes
            if self.redis_client:
                try:
                    self.redis_client.setex(cache_key, 300, json.dumps(games_data))
                except Exception as e:
                    print(f"Cache write error: {e}")
                    
            return games_data
            
        except Exception as e:
            self.logger.error(f"Error fetching today's games: {e}")
            return []
    
    def get_live_game_data(self, game_id):
        """Get detailed live data for a specific game"""
        cache_key = f"live_game_{game_id}"
        
        # Check cache (30 second cache for live data)
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")
        
        try:
            # Get live game data
            game_data = statsapi.get('game', {'gamePk': game_id})
            
            processed_data = {
                'game_id': game_id,
                'status': game_data['gameData']['status']['abstractGameState'],
                'inning': game_data['liveData']['linescore'].get('currentInning', 0),
                'inning_state': game_data['liveData']['linescore'].get('inningState', ''),
                'away_team': game_data['gameData']['teams']['away']['name'],
                'home_team': game_data['gameData']['teams']['home']['name'],
                'away_score': game_data['liveData']['linescore']['teams']['away'].get('runs', 0),
                'home_score': game_data['liveData']['linescore']['teams']['home'].get('runs', 0),
                'weather': game_data['gameData'].get('weather', {}),
                'venue': game_data['gameData']['venue']['name'],
                'attendance': game_data['gameData'].get('attendance', 0)
            }
            
            # Cache for 30 seconds during live games
            if self.redis_client:
                try:
                    self.redis_client.setex(cache_key, 30, json.dumps(processed_data))
                except Exception as e:
                    print(f"Cache write error: {e}")
                    
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Error fetching live game {game_id}: {e}")
            return {}
    
    def get_player_season_stats(self, player_id):
        """Get current season stats for a player"""
        cache_key = f"player_stats_{player_id}_{datetime.now().strftime('%Y')}"
        
        # Check cache (cache for 1 hour)
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")
        
        try:
            player_data = statsapi.get('person', {'personId': player_id})
            stats = statsapi.player_stat_data(player_id, group="hitting", type="season")
            
            processed_stats = {
                'player_id': player_id,
                'name': player_data['people'][0]['fullName'],
                'position': player_data['people'][0]['primaryPosition']['name'],
                'team': player_data['people'][0]['currentTeam']['name'],
                'stats': stats
            }
            
            # Cache for 1 hour
            if self.redis_client:
                try:
                    self.redis_client.setex(cache_key, 3600, json.dumps(processed_stats))
                except Exception as e:
                    print(f"Cache write error: {e}")
                    
            return processed_stats
            
        except Exception as e:
            self.logger.error(f"Error fetching player stats {player_id}: {e}")
            return {}
    
    def get_team_standings(self):
        """Get current MLB standings"""
        cache_key = f"standings_{datetime.now().strftime('%Y-%m-%d')}"
        
        if self.redis_client:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    return json.loads(cached_data)
            except Exception as e:
                print(f"Cache read error: {e}")
        
        try:
            standings_data = statsapi.standings_data()
            
            # Cache for 4 hours
            if self.redis_client:
                try:
                    self.redis_client.setex(cache_key, 14400, json.dumps(standings_data))
                except Exception as e:
                    print(f"Cache write error: {e}")
                    
            return standings_data
            
        except Exception as e:
            self.logger.error(f"Error fetching standings: {e}")
            return {}