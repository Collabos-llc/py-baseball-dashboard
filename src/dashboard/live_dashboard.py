import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data.mlb_live_data import MLBLiveData
import pandas as pd
from datetime import datetime

def render_live_dashboard():
    """Render the live MLB dashboard tab"""
    st.header("🔴 Live MLB Games & Data")
    
    # Initialize live data connector
    try:
        mlb_live = MLBLiveData()
    except Exception as e:
        st.error(f"Failed to connect to MLB data service: {e}")
        st.info("💡 Make sure Redis is running via Docker: `docker-compose up -d redis`")
        return
    
    # Get today's games
    with st.spinner("Loading today's games..."):
        games = mlb_live.get_todays_games()
    
    if not games:
        st.warning("No games found for today or API error")
        st.info("💡 **Tip**: This works best during MLB season (April-October)")
        return
    
    # Display games in columns
    st.subheader("Today's Games")
    
    # Create columns for games
    cols_per_row = 3
    for i in range(0, len(games), cols_per_row):
        cols = st.columns(cols_per_row)
        
        for j, game in enumerate(games[i:i+cols_per_row]):
            with cols[j]:
                # Game card
                status_color = {
                    'Live': '🔴',
                    'Final': '✅', 
                    'Scheduled': '⏰',
                    'Postponed': '⏸️'
                }.get(game['status'], '⚪')
                
                st.metric(
                    label=f"{status_color} {game['away_team']} @ {game['home_team']}",
                    value=f"{game['away_score']} - {game['home_score']}",
                    delta=f"Inning {game['inning']}" if game['inning'] > 0 else game['game_time'][:5]
                )
                
                # Button to view detailed game data
                if st.button(f"View Details", key=f"game_{game['game_id']}"):
                    st.session_state.selected_game = game['game_id']
    
    # Detailed game view
    if 'selected_game' in st.session_state:
        st.subheader("🔍 Game Details")
        
        with st.spinner("Loading game details..."):
            game_details = mlb_live.get_live_game_data(st.session_state.selected_game)
        
        if game_details:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Away Team", game_details['away_team'], game_details['away_score'])
            
            with col2:
                st.metric("Home Team", game_details['home_team'], game_details['home_score'])
            
            with col3:
                st.metric("Status", game_details['status'], f"Inning {game_details['inning']}")
            
            # Weather info if available
            if game_details.get('weather'):
                st.subheader("🌤️ Weather Conditions")
                weather = game_details['weather']
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    temp = weather.get('temp', 'N/A')
                    st.metric("Temperature", f"{temp}°F" if temp != 'N/A' else temp)
                with col2:
                    wind = weather.get('wind', 'N/A')
                    st.metric("Wind", wind)
                with col3:
                    condition = weather.get('condition', 'N/A')
                    st.metric("Condition", condition)
                
                # Betting insights based on weather
                if temp != 'N/A' and isinstance(temp, (int, float)):
                    if temp > 80:
                        st.success(f"🔥 **HOT WEATHER ALERT**: {temp}°F - Ball carries farther! Consider OVER bets on HR props")
                    elif temp < 55:
                        st.info(f"❄️ **COLD WEATHER**: {temp}°F - Ball doesn't carry as well. Consider UNDER bets")
                    
                if wind != 'N/A' and isinstance(wind, str):
                    if 'out' in wind.lower():
                        st.warning("💨 **TAILWIND**: Wind helping hitters - great for HR props!")
                    elif 'in' in wind.lower():
                        st.info("🌪️ **HEADWIND**: Wind hurting hitters - avoid HR props")

def render_team_standings():
    """Render team standings tab"""
    st.header("🏆 MLB Standings")
    
    try:
        mlb_live = MLBLiveData()
    except Exception as e:
        st.error(f"Failed to connect to MLB data service: {e}")
        return
    
    with st.spinner("Loading standings..."):
        standings = mlb_live.get_team_standings()
    
    if not standings:
        st.warning("No standings data available")
        st.info("💡 **Note**: Standings are only available during MLB season")
        return
    
    # Convert to DataFrames for better display
    def safe_dataframe(division_data):
        if division_data and len(division_data) > 0:
            df = pd.DataFrame(division_data)
            # Ensure we have the required columns
            required_cols = ['name', 'w', 'l', 'pct', 'gb']
            available_cols = [col for col in required_cols if col in df.columns]
            if available_cols:
                return df[available_cols]
        return pd.DataFrame()
    
    al_east = safe_dataframe(standings.get('American League East', []))
    al_central = safe_dataframe(standings.get('American League Central', []))
    al_west = safe_dataframe(standings.get('American League West', []))
    
    nl_east = safe_dataframe(standings.get('National League East', []))
    nl_central = safe_dataframe(standings.get('National League Central', []))
    nl_west = safe_dataframe(standings.get('National League West', []))
    
    # Display in tabs
    al_tab, nl_tab = st.tabs(["American League", "National League"])
    
    with al_tab:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("AL East")
            if not al_east.empty:
                st.dataframe(al_east, hide_index=True)
            else:
                st.info("No AL East data available")
        
        with col2:
            st.subheader("AL Central") 
            if not al_central.empty:
                st.dataframe(al_central, hide_index=True)
            else:
                st.info("No AL Central data available")
        
        with col3:
            st.subheader("AL West")
            if not al_west.empty:
                st.dataframe(al_west, hide_index=True)
            else:
                st.info("No AL West data available")
    
    with nl_tab:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("NL East")
            if not nl_east.empty:
                st.dataframe(nl_east, hide_index=True)
            else:
                st.info("No NL East data available")
        
        with col2:
            st.subheader("NL Central")
            if not nl_central.empty:
                st.dataframe(nl_central, hide_index=True)
            else:
                st.info("No NL Central data available")
        
        with col3:
            st.subheader("NL West")
            if not nl_west.empty:
                st.dataframe(nl_west, hide_index=True)
            else:
                st.info("No NL West data available")
    
    # Add refresh button
    if st.button("🔄 Refresh Standings"):
        st.rerun()