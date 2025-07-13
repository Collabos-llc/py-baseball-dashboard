import pybaseball as pyb
import statsapi
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from .data_validator import PyBaseballDataValidator

class IntegratedBaseballData:
    """Combine PyBaseball historical data with MLB-StatsAPI live data"""
    
    def __init__(self):
        self.cache = {}
        self.validator = PyBaseballDataValidator()
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def get_player_complete_profile(_self, player_name, player_id=None):
        """Get complete player profile: historical Statcast + current stats"""
        
        # Get historical Statcast data from PyBaseball
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)  # Last year of data
        
        try:
            profile = {
                'name': player_name,
                'player_id': player_id,
                'statcast_data': None,
                'current_stats': None,
                'last_updated': datetime.now().isoformat()
            }
            
            # PyBaseball historical data (if player_id is available)
            if player_id:
                try:
                    statcast_data = pyb.statcast_batter(
                        start_dt=start_date.strftime('%Y-%m-%d'),
                        end_dt=end_date.strftime('%Y-%m-%d'),
                        player_id=player_id
                    )
                    # Validate and clean the statcast data
                    if statcast_data is not None and not statcast_data.empty:
                        validated_data = _self.validator.validate_batting_averages(statcast_data, player_id)
                        profile['statcast_data'] = validated_data
                    else:
                        profile['statcast_data'] = statcast_data
                except Exception as e:
                    print(f"Error getting Statcast data for {player_name}: {e}")
            
            # MLB-StatsAPI current season stats
            if player_id:
                try:
                    current_stats = statsapi.player_stat_data(player_id, group="hitting", type="season")
                    profile['current_stats'] = current_stats
                except Exception as e:
                    print(f"Error getting current stats for {player_name}: {e}")
            
            return profile
            
        except Exception as e:
            print(f"Error getting player profile: {e}")
            return {}
    
    @st.cache_data(ttl=1800)  # Cache for 30 minutes
    def get_game_context_analysis(_self, game_id, home_team, away_team):
        """Combine live game data with historical team performance"""
        
        try:
            analysis = {
                'game_id': game_id,
                'live_data': None,
                'home_team_historical': None,
                'away_team_historical': None,
                'betting_insights': []
            }
            
            # Live game data from MLB-StatsAPI
            try:
                live_data = statsapi.get('game', {'gamePk': game_id})
                analysis['live_data'] = live_data
            except Exception as e:
                print(f"Error getting live data: {e}")
            
            # Historical team data from PyBaseball
            try:
                current_year = datetime.now().year
                
                # Get team batting stats for context
                home_team_stats = pyb.team_batting(current_year, home_team)
                away_team_stats = pyb.team_batting(current_year, away_team)
                
                analysis['home_team_historical'] = home_team_stats
                analysis['away_team_historical'] = away_team_stats
                
                # Generate betting insights
                analysis['betting_insights'] = _self._generate_betting_insights(
                    live_data, home_team_stats, away_team_stats
                )
                
            except Exception as e:
                print(f"Error getting team historical data: {e}")
            
            return analysis
            
        except Exception as e:
            print(f"Error in game context analysis: {e}")
            return {}
    
    def _generate_betting_insights(self, live_data, home_stats, away_stats):
        """Generate betting insights from combined data"""
        insights = []
        
        try:
            # Weather-based insights
            if live_data and 'gameData' in live_data:
                weather = live_data.get('gameData', {}).get('weather', {})
                if weather.get('temp'):
                    temp = int(weather['temp'])
                    if temp > 80:
                        insights.append({
                            'type': 'weather',
                            'message': f"Hot weather ({temp}°F) favors hitters - consider OVER bets",
                            'confidence': 'medium'
                        })
                    elif temp < 55:
                        insights.append({
                            'type': 'weather',
                            'message': f"Cold weather ({temp}°F) hurts offense - consider UNDER bets",
                            'confidence': 'medium'
                        })
                
                # Wind insights
                wind = weather.get('wind', '')
                if wind:
                    if 'out' in wind.lower():
                        insights.append({
                            'type': 'weather',
                            'message': "Tailwind detected - favorable for home runs",
                            'confidence': 'high'
                        })
                    elif 'in' in wind.lower():
                        insights.append({
                            'type': 'weather',
                            'message': "Headwind detected - unfavorable for home runs",
                            'confidence': 'high'
                        })
            
            # Team performance insights with validated data
            if home_stats is not None and away_stats is not None and not home_stats.empty and not away_stats.empty:
                try:
                    # Validate team batting averages
                    home_avg = home_stats['AVG'].iloc[-1] if 'AVG' in home_stats.columns else 0
                    away_avg = away_stats['AVG'].iloc[-1] if 'AVG' in away_stats.columns else 0
                    
                    # Apply validation to team averages
                    validated_home_avg = home_avg if home_avg and 0 <= home_avg <= 1 else 0.244
                    validated_away_avg = away_avg if away_avg and 0 <= away_avg <= 1 else 0.244
                    
                    if abs(validated_home_avg - validated_away_avg) > 0.050:  # Significant difference
                        better_team = "home" if validated_home_avg > validated_away_avg else "away"
                        insights.append({
                            'type': 'team_performance',
                            'message': f"{better_team.title()} team has significant batting average advantage ({validated_home_avg:.3f} vs {validated_away_avg:.3f})",
                            'confidence': 'high'
                        })
                except Exception as e:
                    print(f"Error in team performance analysis: {e}")
            
        except Exception as e:
            print(f"Error generating betting insights: {e}")
        
        return insights
    
    def get_player_search_results(self, query):
        """Search for players by name"""
        try:
            # Use statsapi to search for players
            players = statsapi.lookup_player(query)
            
            results = []
            for player in players[:10]:  # Limit to 10 results
                results.append({
                    'id': player['id'],
                    'name': player['fullName'],
                    'position': player.get('primaryPosition', {}).get('name', 'Unknown'),
                    'team': player.get('currentTeam', {}).get('name', 'Free Agent')
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching for players: {e}")
            return []