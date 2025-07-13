import streamlit as st
import pybaseball as pyb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import warnings
import sys
import os

# Add src directory to Python path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import live dashboard components
try:
    from dashboard.live_dashboard import render_live_dashboard, render_team_standings
    from utils.data_integration import IntegratedBaseballData
    LIVE_DATA_AVAILABLE = True
except ImportError as e:
    print(f"Live data components not available: {e}")
    LIVE_DATA_AVAILABLE = False

warnings.filterwarnings('ignore')

# Page config
st.set_page_config(
    page_title="⚾ Baseball Betting Data Dashboard",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable PyBaseball caching
pyb.cache.enable()

# Title and description
st.title("⚾ ParlayJaye Baseball Analytics Dashboard")
if LIVE_DATA_AVAILABLE:
    st.markdown("**🔴 LIVE: Enhanced with MLB-StatsAPI + PyBaseball** - Real-time games, standings, and 100+ betting analytics columns")
    st.success("✅ Live MLB Data Integration: ACTIVE")
else:
    st.markdown("**Powered by PyBaseball & Statcast Data** - The same data UmpScorecards uses, plus 80+ more columns")
    st.warning("⚠️ Live MLB Data Integration: Loading... (Will show 11 tabs when active)")

# Sidebar controls
st.sidebar.header("📊 Data Controls")

# Date selection
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=3),
        max_value=datetime.now()
    )
with col2:
    end_date = st.date_input(
        "End Date", 
        value=datetime.now(),
        max_value=datetime.now()
    )

# Team filter
teams = ['All Teams', 'LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL', 'STL', 'CHC', 'ARI', 'LAD', 'SF', 'CLE', 'SEA', 'MIA', 'NYM', 'WSH', 'BAL', 'SD', 'PHI', 'PIT', 'TEX', 'TB', 'BOS', 'CIN', 'COL', 'KC', 'DET', 'MIN', 'CWS', 'NYY']
selected_team = st.sidebar.selectbox("Select Team", teams)

# Player filter
@st.cache_data(ttl=86400)  # Cache for 24 hours
def get_player_list(df):
    """Get unique players from dataset"""
    if df.empty:
        return ['All Players']
    
    players = ['All Players']
    if 'player_name' in df.columns:
        unique_players = df['player_name'].dropna().unique()
        players.extend(sorted(unique_players))
    return players

selected_player = st.sidebar.selectbox("Select Player", ['All Players'])

# Data loading function
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_baseball_data(start_date, end_date):
    """Load Statcast data with caching"""
    try:
        with st.spinner(f"🔄 Loading baseball data from {start_date} to {end_date}..."):
            data = pyb.statcast(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load data
df = load_baseball_data(start_date, end_date)

if df.empty:
    st.warning("No data available for the selected date range. Try selecting dates during the MLB season (April-October).")
    st.stop()

# Filter by team if selected
if selected_team != 'All Teams':
    df = df[(df['home_team'] == selected_team) | (df['away_team'] == selected_team)]

# Update player dropdown with actual data
if not df.empty:
    player_options = get_player_list(df)
    if len(player_options) > 1:  # More than just 'All Players'
        selected_player = st.sidebar.selectbox("Select Player", player_options, key="player_select")
    
    # Filter by player if selected
    if selected_player != 'All Players' and 'player_name' in df.columns:
        df = df[df['player_name'] == selected_player]

# Main metrics
st.header("📈 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Pitches", f"{len(df):,}")
with col2:
    games = df['game_pk'].nunique() if 'game_pk' in df.columns else 0
    st.metric("Games", games)
with col3:
    avg_exit_velo = df['launch_speed'].mean() if 'launch_speed' in df.columns else 0
    st.metric("Avg Exit Velocity", f"{avg_exit_velo:.1f} mph")
with col4:
    home_runs = len(df[df['events'] == 'home_run']) if 'events' in df.columns else 0
    st.metric("Home Runs", home_runs)
with col5:
    total_columns = len(df.columns)
    st.metric("Data Columns", f"{total_columns} vs UmpScorecards' 5")

# Tabs for different visualizations
if LIVE_DATA_AVAILABLE:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
        "🔴 Live Games",
        "🏆 Standings", 
        "🎯 Strike Zone", 
        "🚀 Exit Velocity Analysis", 
        "🎯 Barrel Rate Trends", 
        "⚖️ Umpire Analysis", 
        "🌤️ Weather Impact", 
        "😴 Pitcher Fatigue", 
        "👤 Player Profile", 
        "📊 Original Analysis", 
        "🔍 Raw Data"
    ])
else:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "🎯 Strike Zone", 
        "🚀 Exit Velocity Analysis", 
        "🎯 Barrel Rate Trends", 
        "⚖️ Umpire Analysis", 
        "🌤️ Weather Impact", 
        "😴 Pitcher Fatigue", 
        "👤 Player Profile", 
        "📊 Original Analysis", 
        "🔍 Raw Data"
    ])

if LIVE_DATA_AVAILABLE:
    with tab1:
        try:
            render_live_dashboard()
        except Exception as e:
            st.error(f"Error loading live dashboard: {e}")
            st.info("Live MLB data integration is being set up. Please check back during MLB season for live games.")
    
    with tab2:
        try:
            render_team_standings()
        except Exception as e:
            st.error(f"Error loading standings: {e}")
            st.info("MLB standings will be available during the season.")
    
    # Shift existing tabs
    strike_zone_tab = tab3
    exit_velocity_tab = tab4
    barrel_rate_tab = tab5
    umpire_tab = tab6
    weather_tab = tab7
    fatigue_tab = tab8
    profile_tab = tab9
    original_tab = tab10
    raw_data_tab = tab11
else:
    # Original tab assignment when live data not available
    strike_zone_tab = tab1
    exit_velocity_tab = tab2
    barrel_rate_tab = tab3
    umpire_tab = tab4
    weather_tab = tab5
    fatigue_tab = tab6
    profile_tab = tab7
    original_tab = tab8
    raw_data_tab = tab9

with strike_zone_tab:
    st.header("🎯 Strike Zone Analysis (UmpScorecards Style)")
    
    # Filter for pitches with location data
    zone_data = df.dropna(subset=['plate_x', 'plate_z', 'description']).copy()
    
    if not zone_data.empty:
        # Create strike zone plot
        fig = go.Figure()
        
        # Add strike zone rectangle
        fig.add_shape(
            type="rect",
            x0=-0.83, y0=1.5, x1=0.83, y1=3.5,
            line=dict(color="black", width=3),
            fillcolor="rgba(0,0,0,0.1)"
        )
        
        # Color by call type
        for call_type in zone_data['description'].unique():
            if pd.notna(call_type):
                subset = zone_data[zone_data['description'] == call_type]
                color = 'red' if 'ball' in call_type else 'blue' if 'strike' in call_type else 'green'
                
                fig.add_trace(go.Scatter(
                    x=subset['plate_x'],
                    y=subset['plate_z'],
                    mode='markers',
                    name=f"{call_type} ({len(subset)})",
                    marker=dict(color=color, size=6, opacity=0.6)
                ))
        
        fig.update_layout(
            title="Pitch Locations & Calls",
            xaxis_title="Horizontal Position (feet)",
            yaxis_title="Vertical Position (feet)",
            width=800,
            height=600,
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[0, 5])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No pitch location data available for selected period.")

with exit_velocity_tab:
    st.header("🚀 Exit Velocity Analysis - The Sweet Spot")
    
    # Exit velocity data
    exit_data = df.dropna(subset=['launch_speed', 'launch_angle']).copy()
    
    if not exit_data.empty:
        # Calculate home run probability zones
        exit_data['hr_zone'] = 'Low Probability'
        exit_data.loc[(exit_data['launch_speed'] >= 95) & 
                     (exit_data['launch_angle'] >= 25) & 
                     (exit_data['launch_angle'] <= 35), 'hr_zone'] = 'Sweet Spot (80%+ HR)'
        exit_data.loc[(exit_data['launch_speed'] >= 100) & 
                     (exit_data['launch_angle'] >= 20) & 
                     (exit_data['launch_angle'] <= 40), 'hr_zone'] = 'High Probability'
        
        # Betting insights
        sweet_spot_hits = len(exit_data[exit_data['hr_zone'] == 'Sweet Spot (80%+ HR)'])
        actual_hrs = len(exit_data[exit_data['events'] == 'home_run']) if 'events' in exit_data.columns else 0
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Sweet Spot Hits", sweet_spot_hits)
        with col2:
            st.metric("Actual Home Runs", actual_hrs)
        with col3:
            avg_exit_velo = exit_data['launch_speed'].mean()
            st.metric("Avg Exit Velocity", f"{avg_exit_velo:.1f} mph")
        with col4:
            optimal_angle_pct = len(exit_data[(exit_data['launch_angle'] >= 25) & 
                                            (exit_data['launch_angle'] <= 35)]) / len(exit_data) * 100
            st.metric("Optimal Angle %", f"{optimal_angle_pct:.1f}%")
        
        # Main scatter plot
        fig = px.scatter(
            exit_data,
            x='launch_speed',
            y='launch_angle',
            color='hr_zone',
            color_discrete_map={
                'Sweet Spot (80%+ HR)': '#22c55e',
                'High Probability': '#eab308',
                'Low Probability': '#ef4444'
            },
            title="Exit Velocity vs Launch Angle - Home Run Sweet Spot Analysis",
            labels={
                'launch_speed': 'Exit Velocity (mph)',
                'launch_angle': 'Launch Angle (degrees)'
            },
            hover_data=['events'] if 'events' in exit_data.columns else None
        )
        
        # Add sweet spot rectangle
        fig.add_shape(
            type="rect",
            x0=95, y0=25, x1=120, y1=35,
            line=dict(color="green", width=2, dash="dash"),
            fillcolor="rgba(34, 197, 94, 0.1)"
        )
        
        fig.add_annotation(
            x=107.5, y=30,
            text="Sweet Spot Zone<br>95+ mph, 25-35°",
            showarrow=True,
            arrowhead=2,
            bgcolor="white",
            bordercolor="green"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Betting insights
        if sweet_spot_hits > 0:
            st.subheader("🎯 Betting Edge Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**Sweet Spot Performance**: {sweet_spot_hits} hits in optimal zone")
                if actual_hrs > 0:
                    conversion_rate = (actual_hrs / sweet_spot_hits) * 100 if sweet_spot_hits > 0 else 0
                    st.info(f"**Conversion Rate**: {conversion_rate:.1f}% of sweet spot hits became HRs")
                
                if avg_exit_velo >= 108:
                    st.warning("🔥 **High Exit Velocity Alert**: Player consistently hitting 108+ mph - bet HR props even with low odds!")
            
            with col2:
                # Recent trend analysis
                if len(exit_data) >= 10:
                    recent_sweet_spots = exit_data.tail(10)['hr_zone'].value_counts().get('Sweet Spot (80%+ HR)', 0)
                    if recent_sweet_spots >= 3:
                        st.error("⚡ **Hot Streak Alert**: 3+ sweet spot hits in last 10 ABs - player is locked in!")
                    elif recent_sweet_spots == 0:
                        st.info("📉 **Value Opportunity**: No recent sweet spots but player has history - potential bounce-back candidate")
    else:
        st.warning("No exit velocity data available for selected period.")

with barrel_rate_tab:
    st.header("🎯 Barrel Rate Trends - Expected vs Actual Performance")
    
    # Calculate barrel rate and expected stats
    barrel_data = df.dropna(subset=['launch_speed', 'launch_angle']).copy()
    
    if not barrel_data.empty and 'game_date' in barrel_data.columns:
        # Define barrel criteria (Statcast definition)
        barrel_data['is_barrel'] = (
            ((barrel_data['launch_speed'] >= 98) & (barrel_data['launch_angle'] >= 26) & (barrel_data['launch_angle'] <= 30)) |
            ((barrel_data['launch_speed'] >= 99) & (barrel_data['launch_angle'] >= 25) & (barrel_data['launch_angle'] <= 31)) |
            ((barrel_data['launch_speed'] >= 100) & (barrel_data['launch_angle'] >= 24) & (barrel_data['launch_angle'] <= 33)) |
            ((barrel_data['launch_speed'] >= 101) & (barrel_data['launch_angle'] >= 23) & (barrel_data['launch_angle'] <= 34)) |
            ((barrel_data['launch_speed'] >= 102) & (barrel_data['launch_angle'] >= 22) & (barrel_data['launch_angle'] <= 35)) |
            ((barrel_data['launch_speed'] >= 103) & (barrel_data['launch_angle'] >= 21) & (barrel_data['launch_angle'] <= 36)) |
            ((barrel_data['launch_speed'] >= 104) & (barrel_data['launch_angle'] >= 20) & (barrel_data['launch_angle'] <= 37)) |
            ((barrel_data['launch_speed'] >= 105) & (barrel_data['launch_angle'] >= 19) & (barrel_data['launch_angle'] <= 38)) |
            ((barrel_data['launch_speed'] >= 106) & (barrel_data['launch_angle'] >= 18) & (barrel_data['launch_angle'] <= 39)) |
            ((barrel_data['launch_speed'] >= 107) & (barrel_data['launch_angle'] >= 17) & (barrel_data['launch_angle'] <= 40)) |
            ((barrel_data['launch_speed'] >= 108) & (barrel_data['launch_angle'] >= 16) & (barrel_data['launch_angle'] <= 41)) |
            ((barrel_data['launch_speed'] >= 109) & (barrel_data['launch_angle'] >= 15) & (barrel_data['launch_angle'] <= 42)) |
            ((barrel_data['launch_speed'] >= 110) & (barrel_data['launch_angle'] >= 14) & (barrel_data['launch_angle'] <= 43)) |
            ((barrel_data['launch_speed'] >= 111) & (barrel_data['launch_angle'] >= 13) & (barrel_data['launch_angle'] <= 44)) |
            ((barrel_data['launch_speed'] >= 112) & (barrel_data['launch_angle'] >= 12) & (barrel_data['launch_angle'] <= 45)) |
            ((barrel_data['launch_speed'] >= 113) & (barrel_data['launch_angle'] >= 11) & (barrel_data['launch_angle'] <= 46)) |
            ((barrel_data['launch_speed'] >= 114) & (barrel_data['launch_angle'] >= 10) & (barrel_data['launch_angle'] <= 47)) |
            ((barrel_data['launch_speed'] >= 115) & (barrel_data['launch_angle'] >= 9) & (barrel_data['launch_angle'] <= 48)) |
            ((barrel_data['launch_speed'] >= 116) & (barrel_data['launch_angle'] >= 8) & (barrel_data['launch_angle'] <= 50))
        )
        
        # Convert game_date to datetime if it's not already
        barrel_data['game_date'] = pd.to_datetime(barrel_data['game_date'])
        
        # Group by week to show trends
        barrel_data['week'] = barrel_data['game_date'].dt.to_period('W').dt.start_time
        
        weekly_stats = barrel_data.groupby('week').agg({
            'is_barrel': ['sum', 'count'],
            'events': lambda x: (x == 'home_run').sum(),
            'estimated_woba_using_speedangle': 'mean'
        }).round(3)
        
        # Flatten column names
        weekly_stats.columns = ['barrels', 'batted_balls', 'actual_hr', 'avg_xwoba']
        weekly_stats['barrel_rate'] = (weekly_stats['barrels'] / weekly_stats['batted_balls'] * 100).round(1)
        
        # Calculate expected home runs (simplified: barrel rate * 0.5 + other factors)
        weekly_stats['expected_hr'] = (weekly_stats['barrels'] * 0.6 + 
                                     weekly_stats['avg_xwoba'] * weekly_stats['batted_balls'] * 0.3).round(1)
        
        weekly_stats['value_gap'] = weekly_stats['expected_hr'] - weekly_stats['actual_hr']
        weekly_stats.reset_index(inplace=True)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_barrels = weekly_stats['barrels'].sum()
            st.metric("Total Barrels", int(total_barrels))
        with col2:
            avg_barrel_rate = weekly_stats['barrel_rate'].mean()
            st.metric("Avg Barrel Rate", f"{avg_barrel_rate:.1f}%")
        with col3:
            total_expected = weekly_stats['expected_hr'].sum()
            total_actual = weekly_stats['actual_hr'].sum()
            st.metric("Expected HR", f"{total_expected:.1f}")
        with col4:
            value_gap = total_expected - total_actual
            st.metric("Value Gap", f"{value_gap:+.1f}", delta=f"{'Under' if value_gap > 0 else 'Over'}performing")
        
        if len(weekly_stats) > 1:
            # Main trend chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=weekly_stats['week'],
                y=weekly_stats['actual_hr'],
                mode='lines+markers',
                name='Actual Home Runs',
                line=dict(color='#ef4444', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=weekly_stats['week'],
                y=weekly_stats['expected_hr'],
                mode='lines+markers',
                name='Expected Home Runs',
                line=dict(color='#22c55e', width=3, dash='dash'),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Expected vs Actual Home Runs Over Time",
                xaxis_title="Week",
                yaxis_title="Home Runs",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Betting insights
            st.subheader("💰 Value Betting Opportunities")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Find underperforming weeks
                underperforming_weeks = weekly_stats[weekly_stats['value_gap'] > 1.0]
                if not underperforming_weeks.empty:
                    st.error("🔻 **Underperforming Periods** (Due for Bounce-Back)")
                    for _, week in underperforming_weeks.iterrows():
                        st.write(f"Week of {week['week'].strftime('%m/%d')}: {week['value_gap']:+.1f} HR gap")
                    st.info("💡 **Betting Strategy**: Target OVER on HR props - player is due for regression to mean")
                else:
                    st.success("✅ No significant underperformance detected")
            
            with col2:
                # Find overperforming weeks
                overperforming_weeks = weekly_stats[weekly_stats['value_gap'] < -1.0]
                if not overperforming_weeks.empty:
                    st.warning("🔺 **Overperforming Periods** (Regression Risk)")
                    for _, week in overperforming_weeks.iterrows():
                        st.write(f"Week of {week['week'].strftime('%m/%d')}: {week['value_gap']:+.1f} HR gap")
                    st.info("⚠️ **Betting Strategy**: Consider UNDER on HR props - potential regression coming")
                else:
                    st.success("✅ No significant overperformance detected")
            
            # Recent trend analysis
            if len(weekly_stats) >= 3:
                recent_weeks = weekly_stats.tail(3)
                recent_gap = recent_weeks['value_gap'].mean()
                
                st.subheader("📈 Recent Trend Analysis")
                if recent_gap > 0.5:
                    st.error(f"🚨 **Strong Buy Signal**: {recent_gap:+.1f} HR gap over last 3 weeks - player significantly underperforming expected metrics")
                elif recent_gap < -0.5:
                    st.warning(f"⚠️ **Caution Signal**: {recent_gap:+.1f} HR gap over last 3 weeks - player may be overdue for regression")
                else:
                    st.success(f"✅ **Balanced Performance**: {recent_gap:+.1f} HR gap - player performing close to expectations")
        else:
            st.info("Need more data points to show trends. Try expanding your date range.")
    else:
        st.warning("No sufficient data available for barrel rate analysis.")
    
with umpire_tab:
    st.header("⚖️ Umpire Strike Zone Analysis - Hidden Betting Edges")
    
    # Filter for pitches with umpire and location data
    ump_data = df.dropna(subset=['plate_x', 'plate_z', 'description']).copy()
    
    if not ump_data.empty and 'umpire' in ump_data.columns:
        # Umpire selection
        umpires = ['All Umpires'] + sorted(ump_data['umpire'].unique().tolist())
        selected_umpire = st.selectbox("Select Umpire for Analysis", umpires)
        
        if selected_umpire != 'All Umpires':
            ump_analysis = ump_data[ump_data['umpire'] == selected_umpire].copy()
        else:
            ump_analysis = ump_data.copy()
        
        # Define rule book strike zone
        def in_strike_zone(row):
            return (-0.83 <= row['plate_x'] <= 0.83) and (row['sz_bot'] <= row['plate_z'] <= row['sz_top'])
        
        ump_analysis['in_rule_zone'] = ump_analysis.apply(in_strike_zone, axis=1)
        ump_analysis['called_strike'] = ump_analysis['description'].str.contains('strike|Strike', na=False)
        
        # Calculate accuracy by zone
        def get_zone(row):
            x, z = row['plate_x'], row['plate_z']
            if -0.83 <= x <= 0.83 and row['sz_bot'] <= z <= row['sz_top']:
                if x < -0.28:
                    return "Inside" if row['stand'] == 'L' else "Outside"
                elif x > 0.28:
                    return "Outside" if row['stand'] == 'L' else "Inside"
                else:
                    return "Middle"
            elif z < row['sz_bot']:
                return "Low"
            elif z > row['sz_top']:
                return "High"
            elif x < -0.83:
                return "Wide Left"
            else:
                return "Wide Right"
        
        if 'stand' in ump_analysis.columns:
            ump_analysis['zone'] = ump_analysis.apply(get_zone, axis=1)
        else:
            ump_analysis['zone'] = 'Unknown'
        
        # Zone accuracy analysis
        zone_stats = ump_analysis.groupby('zone').agg({
            'in_rule_zone': ['sum', 'count'],
            'called_strike': ['sum', 'count']
        }).round(3)
        
        zone_stats.columns = ['strikes_in_zone', 'pitches_in_zone', 'called_strikes', 'total_pitches']
        zone_stats['accuracy'] = ((zone_stats['strikes_in_zone'] + 
                                 (zone_stats['total_pitches'] - zone_stats['pitches_in_zone'] - 
                                  zone_stats['called_strikes'] + zone_stats['strikes_in_zone'])) / 
                                zone_stats['total_pitches'] * 100).round(1)
        
        zone_stats['call_rate'] = (zone_stats['called_strikes'] / zone_stats['total_pitches'] * 100).round(1)
        zone_stats.reset_index(inplace=True)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_pitches = len(ump_analysis)
            st.metric("Total Pitches", total_pitches)
        with col2:
            overall_accuracy = zone_stats['accuracy'].mean()
            st.metric("Overall Accuracy", f"{overall_accuracy:.1f}%")
        with col3:
            strike_rate = ump_analysis['called_strike'].mean() * 100
            st.metric("Strike Call Rate", f"{strike_rate:.1f}%")
        with col4:
            if selected_umpire != 'All Umpires':
                st.metric("Umpire", selected_umpire)
            else:
                st.metric("Umpires", f"{ump_data['umpire'].nunique()} different")
        
        # Strike zone heatmap
        if not ump_analysis.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Actual calls scatter plot
                fig = go.Figure()
                
                # Add strike zone rectangle
                fig.add_shape(
                    type="rect",
                    x0=-0.83, y0=ump_analysis['sz_bot'].mean(), 
                    x1=0.83, y1=ump_analysis['sz_top'].mean(),
                    line=dict(color="black", width=3),
                    fillcolor="rgba(0,0,0,0.1)"
                )
                
                # Plot calls
                strikes = ump_analysis[ump_analysis['called_strike'] == True]
                balls = ump_analysis[ump_analysis['called_strike'] == False]
                
                if not strikes.empty:
                    fig.add_trace(go.Scatter(
                        x=strikes['plate_x'],
                        y=strikes['plate_z'],
                        mode='markers',
                        name=f"Called Strikes ({len(strikes)})",
                        marker=dict(color='red', size=4, opacity=0.6)
                    ))
                
                if not balls.empty:
                    fig.add_trace(go.Scatter(
                        x=balls['plate_x'],
                        y=balls['plate_z'],
                        mode='markers',
                        name=f"Called Balls ({len(balls)})",
                        marker=dict(color='blue', size=4, opacity=0.6)
                    ))
                
                fig.update_layout(
                    title="Umpire Strike Zone Map",
                    xaxis_title="Horizontal Position (feet)",
                    yaxis_title="Vertical Position (feet)",
                    xaxis=dict(range=[-2, 2]),
                    yaxis=dict(range=[0, 5]),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Zone accuracy chart
                if not zone_stats.empty:
                    fig = px.bar(
                        zone_stats,
                        x='zone',
                        y='accuracy',
                        title="Accuracy by Zone",
                        labels={'accuracy': 'Accuracy (%)', 'zone': 'Zone'},
                        color='accuracy',
                        color_continuous_scale='RdYlGn'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Betting insights
        st.subheader("💰 Umpire Betting Edges")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Zone Tendencies**")
            
            # Find most biased zones
            if not zone_stats.empty:
                lowest_accuracy = zone_stats.loc[zone_stats['accuracy'].idxmin()]
                highest_accuracy = zone_stats.loc[zone_stats['accuracy'].idxmax()]
                
                st.error(f"**Weakest Zone**: {lowest_accuracy['zone']} ({lowest_accuracy['accuracy']:.1f}% accuracy)")
                st.success(f"**Strongest Zone**: {highest_accuracy['zone']} ({highest_accuracy['accuracy']:.1f}% accuracy)")
                
                # Strike rate insights
                tight_zones = zone_stats[zone_stats['call_rate'] < 40]
                loose_zones = zone_stats[zone_stats['call_rate'] > 60]
                
                if not tight_zones.empty:
                    st.info(f"**Tight Zones**: {', '.join(tight_zones['zone'].tolist())}")
                    st.write("→ More hitter-friendly counts → More home runs")
                
                if not loose_zones.empty:
                    st.warning(f"**Loose Zones**: {', '.join(loose_zones['zone'].tolist())}")
                    st.write("→ More pitcher-friendly counts → Fewer home runs")
        
        with col2:
            st.write("**⚡ Live Betting Strategy**")
            
            if selected_umpire != 'All Umpires':
                # Specific umpire recommendations
                avg_acc = zone_stats['accuracy'].mean()
                
                if avg_acc < 85:
                    st.error("🚨 **HIGH VALUE OPPORTUNITY**")
                    st.write("This umpire has poor accuracy - expect:")
                    st.write("• More favorable hitter counts")
                    st.write("• Increased home run rates")
                    st.write("• **BET: OVER on HR props**")
                elif avg_acc > 95:
                    st.success("⚠️ **TIGHT STRIKE ZONE**")
                    st.write("This umpire is very accurate - expect:")
                    st.write("• More consistent calls")
                    st.write("• Pitcher-friendly environment")
                    st.write("• **BET: UNDER on HR props**")
                else:
                    st.info("📊 **NEUTRAL UMPIRE**")
                    st.write("Standard strike zone - look for other edges")
            else:
                st.info("💡 **General Strategy**")
                st.write("• Track specific umpires before games")
                st.write("• Target hitters vs loose umpires")
                st.write("• Avoid HR props with tight umps")
                st.write("• Use live betting when bias becomes clear")
    
    elif not ump_data.empty:
        st.warning("Umpire data not available in this dataset. Try expanding your date range or check data source.")
        
        # Still show basic strike zone analysis
        st.subheader("📊 Basic Strike Zone Analysis")
        
        # Show pitch location patterns
        fig = go.Figure()
        
        # Add strike zone rectangle  
        avg_sz_top = ump_data['sz_top'].mean() if 'sz_top' in ump_data.columns else 3.5
        avg_sz_bot = ump_data['sz_bot'].mean() if 'sz_bot' in ump_data.columns else 1.5
        
        fig.add_shape(
            type="rect",
            x0=-0.83, y0=avg_sz_bot, x1=0.83, y1=avg_sz_top,
            line=dict(color="black", width=3),
            fillcolor="rgba(0,0,0,0.1)"
        )
        
        # Color by call type
        for call_type in ump_data['description'].unique():
            if pd.notna(call_type):
                subset = ump_data[ump_data['description'] == call_type]
                color = 'red' if 'ball' in call_type else 'blue' if 'strike' in call_type else 'green'
                
                fig.add_trace(go.Scatter(
                    x=subset['plate_x'],
                    y=subset['plate_z'],
                    mode='markers',
                    name=f"{call_type} ({len(subset)})",
                    marker=dict(color=color, size=4, opacity=0.6)
                ))
        
        fig.update_layout(
            title="Pitch Locations & Calls (No Umpire Data)",
            xaxis_title="Horizontal Position (feet)",
            yaxis_title="Vertical Position (feet)",
            width=800,
            height=600,
            xaxis=dict(range=[-2, 2]),
            yaxis=dict(range=[0, 5])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No pitch location data available for umpire analysis.")

with weather_tab:
    st.header("🌤️ Weather Impact Analysis - Environmental Betting Edge")
    
    # Weather data analysis
    weather_cols = ['wind_speed', 'wind_direction', 'temperature', 'hit_distance_sc']
    available_weather_cols = [col for col in weather_cols if col in df.columns]
    
    if len(available_weather_cols) >= 2:
        weather_data = df.dropna(subset=available_weather_cols).copy()
        
        if not weather_data.empty:
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if 'temperature' in weather_data.columns:
                    avg_temp = weather_data['temperature'].mean()
                    st.metric("Avg Temperature", f"{avg_temp:.1f}°F")
                else:
                    st.metric("Temperature", "N/A")
            
            with col2:
                if 'wind_speed' in weather_data.columns:
                    avg_wind = weather_data['wind_speed'].mean()
                    st.metric("Avg Wind Speed", f"{avg_wind:.1f} mph")
                else:
                    st.metric("Wind Speed", "N/A")
            
            with col3:
                home_runs = len(weather_data[weather_data['events'] == 'home_run']) if 'events' in weather_data.columns else 0
                st.metric("Home Runs", home_runs)
            
            with col4:
                if 'hit_distance_sc' in weather_data.columns:
                    avg_distance = weather_data['hit_distance_sc'].mean()
                    st.metric("Avg Hit Distance", f"{avg_distance:.0f} ft")
                else:
                    st.metric("Hit Distance", "N/A")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Temperature vs Home Run Distance
                if 'temperature' in weather_data.columns and 'hit_distance_sc' in weather_data.columns:
                    hr_data = weather_data[weather_data['events'] == 'home_run'].copy() if 'events' in weather_data.columns else weather_data.copy()
                    
                    if not hr_data.empty:
                        fig = px.scatter(
                            hr_data,
                            x='temperature',
                            y='hit_distance_sc',
                            title="Temperature vs Home Run Distance",
                            labels={
                                'temperature': 'Temperature (°F)',
                                'hit_distance_sc': 'Distance (feet)'
                            },
                            trendline="ols"
                        )
                        fig.update_traces(marker=dict(color='red', size=8))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Temperature insights
                        hot_games = hr_data[hr_data['temperature'] > 80]
                        cold_games = hr_data[hr_data['temperature'] < 60]
                        
                        if not hot_games.empty and not cold_games.empty:
                            hot_avg = hot_games['hit_distance_sc'].mean()
                            cold_avg = cold_games['hit_distance_sc'].mean()
                            temp_diff = hot_avg - cold_avg
                            
                            if temp_diff > 10:
                                st.success(f"🔥 **Hot Weather Boost**: +{temp_diff:.0f} ft on 80°F+ days")
                            elif temp_diff < -10:
                                st.info(f"❄️ **Cold Weather Impact**: {temp_diff:.0f} ft on <60°F days")
                else:
                    st.info("Temperature or distance data not available")
            
            with col2:
                # Wind Impact Analysis
                if 'wind_speed' in weather_data.columns and 'wind_direction' in weather_data.columns:
                    wind_data = weather_data.dropna(subset=['wind_speed', 'wind_direction']).copy()
                    
                    if not wind_data.empty:
                        # Categorize wind direction impact
                        def categorize_wind_impact(direction):
                            if pd.isna(direction):
                                return 'Unknown'
                            direction = str(direction).lower()
                            if any(word in direction for word in ['out', 'blow', 'help']):
                                return 'Favorable'
                            elif any(word in direction for word in ['in', 'against', 'hurt']):
                                return 'Against'
                            else:
                                return 'Neutral'
                        
                        wind_data['wind_impact'] = wind_data['wind_direction'].apply(categorize_wind_impact)
                        
                        # Wind speed vs home runs
                        wind_summary = wind_data.groupby(['wind_impact']).agg({
                            'wind_speed': 'mean',
                            'events': lambda x: (x == 'home_run').sum() if 'events' in wind_data.columns else 0,
                            'hit_distance_sc': 'mean' if 'hit_distance_sc' in wind_data.columns else lambda x: 0
                        }).round(1)
                        
                        wind_summary.reset_index(inplace=True)
                        
                        if not wind_summary.empty:
                            fig = px.bar(
                                wind_summary,
                                x='wind_impact',
                                y='events',
                                title="Home Runs by Wind Direction",
                                labels={'events': 'Home Runs', 'wind_impact': 'Wind Impact'},
                                color='events',
                                color_continuous_scale='Reds'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Wind data not available")
            
            # Weather betting insights
            st.subheader("🌪️ Weather Betting Strategy")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**🌡️ Temperature Effects**")
                if 'temperature' in weather_data.columns:
                    current_temp = weather_data['temperature'].iloc[-1] if not weather_data.empty else 70
                    
                    if current_temp > 85:
                        st.error("🔥 **HIGH HEAT ALERT**")
                        st.write("• Ball carries 15+ feet further")
                        st.write("• **BET: OVER on HR props**")
                        st.write("• Target power hitters")
                    elif current_temp < 55:
                        st.info("❄️ **COLD WEATHER**")
                        st.write("• Ball dies in the air")
                        st.write("• **BET: UNDER on HR props**")
                        st.write("• Favor pitchers")
                    else:
                        st.success("🌤️ **NEUTRAL TEMP**")
                        st.write("• Standard ball flight")
                        st.write("• Look for other edges")
                else:
                    st.info("Temperature data not available")
            
            with col2:
                st.write("**💨 Wind Conditions**")
                if 'wind_speed' in weather_data.columns and 'wind_direction' in weather_data.columns:
                    latest_wind = weather_data[['wind_speed', 'wind_direction']].iloc[-1] if not weather_data.empty else {'wind_speed': 5, 'wind_direction': 'Unknown'}
                    
                    wind_speed = latest_wind['wind_speed']
                    wind_dir = str(latest_wind['wind_direction']).lower()
                    
                    if wind_speed > 15 and 'out' in wind_dir:
                        st.error("🌪️ **STRONG TAILWIND**")
                        st.write(f"• {wind_speed:.0f} mph helping")
                        st.write("• +20-30 feet on fly balls")
                        st.write("• **BET: OVER on HR props**")
                    elif wind_speed > 15 and 'in' in wind_dir:
                        st.warning("💨 **STRONG HEADWIND**")
                        st.write(f"• {wind_speed:.0f} mph against")
                        st.write("• Kills 20+ fly balls")
                        st.write("• **BET: UNDER on HR props**")
                    else:
                        st.info("🍃 **MANAGEABLE WIND**")
                        st.write("• Minimal impact expected")
                        st.write("• Focus on other factors")
                else:
                    st.info("Wind data not available")
            
            with col3:
                st.write("**⚡ Live Betting Tips**")
                st.write("🎯 **Best Opportunities:**")
                st.write("• Hot days (85°F+) + tailwind")
                st.write("• Target pull hitters")
                st.write("• Bet early innings")
                st.write("")
                st.write("⚠️ **Avoid When:**")
                st.write("• Cold + strong headwind")
                st.write("• High humidity (ball heavy)")
                st.write("• Pitcher-friendly conditions")
        else:
            st.warning("No weather data available for the selected period.")
    else:
        st.info("Weather data columns not found in dataset. Available columns might include wind_speed, wind_direction, temperature, hit_distance_sc.")
        
        # Show available columns for debugging
        weather_related_cols = [col for col in df.columns if any(term in col.lower() for term in ['wind', 'temp', 'weather', 'humid'])]
        if weather_related_cols:
            st.write("**Weather-related columns found:**", weather_related_cols)

with fatigue_tab:
    st.header("😴 Pitcher Fatigue Analysis - Times Through Order")
    
    # Pitcher fatigue analysis
    if 'pitcher' in df.columns and 'at_bat_number' in df.columns:
        fatigue_data = df.dropna(subset=['pitcher', 'at_bat_number']).copy()
        
        # Calculate times through order (simplified)
        fatigue_data['times_through'] = ((fatigue_data['at_bat_number'] - 1) // 9) + 1
        fatigue_data['times_through'] = fatigue_data['times_through'].clip(1, 4)  # Cap at 4
        
        if not fatigue_data.empty:
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_pitchers = fatigue_data['pitcher'].nunique()
                st.metric("Pitchers Analyzed", total_pitchers)
            
            with col2:
                avg_exit_velo = fatigue_data['launch_speed'].mean() if 'launch_speed' in fatigue_data.columns else 0
                st.metric("Avg Exit Velocity", f"{avg_exit_velo:.1f} mph")
            
            with col3:
                total_hrs = len(fatigue_data[fatigue_data['events'] == 'home_run']) if 'events' in fatigue_data.columns else 0
                st.metric("Total Home Runs", total_hrs)
            
            with col4:
                third_time_data = fatigue_data[fatigue_data['times_through'] >= 3]
                third_time_hrs = len(third_time_data[third_time_data['events'] == 'home_run']) if 'events' in third_time_data.columns else 0
                st.metric("3rd+ Time Through HRs", third_time_hrs)
            
            # Fatigue analysis by times through order
            fatigue_stats = fatigue_data.groupby('times_through').agg({
                'launch_speed': 'mean',
                'launch_angle': 'mean',
                'events': lambda x: (x == 'home_run').sum() if len(x) > 0 else 0,
                'pitcher': 'count'
            }).round(2)
            
            fatigue_stats.columns = ['avg_exit_velo', 'avg_launch_angle', 'home_runs', 'total_pitches']
            fatigue_stats['hr_rate'] = (fatigue_stats['home_runs'] / fatigue_stats['total_pitches'] * 100).round(2)
            fatigue_stats.reset_index(inplace=True)
            
            if len(fatigue_stats) > 1:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Exit velocity trend
                    fig = px.line(
                        fatigue_stats,
                        x='times_through',
                        y='avg_exit_velo',
                        title="Exit Velocity by Times Through Order",
                        labels={
                            'times_through': 'Times Through Order',
                            'avg_exit_velo': 'Average Exit Velocity (mph)'
                        },
                        markers=True
                    )
                    fig.update_traces(line=dict(color='blue', width=3), marker=dict(size=10))
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Home run rate trend
                    fig = px.line(
                        fatigue_stats,
                        x='times_through',
                        y='hr_rate',
                        title="Home Run Rate by Times Through Order",
                        labels={
                            'times_through': 'Times Through Order',
                            'hr_rate': 'Home Run Rate (%)'
                        },
                        markers=True
                    )
                    fig.update_traces(line=dict(color='red', width=3), marker=dict(size=10))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Fatigue insights table
                st.subheader("📊 Fatigue Progression Analysis")
                
                # Calculate progression from 1st to 3rd time through
                first_time = fatigue_stats[fatigue_stats['times_through'] == 1]
                third_time = fatigue_stats[fatigue_stats['times_through'] == 3]
                
                if not first_time.empty and not third_time.empty:
                    exit_velo_increase = third_time['avg_exit_velo'].iloc[0] - first_time['avg_exit_velo'].iloc[0]
                    hr_rate_increase = third_time['hr_rate'].iloc[0] - first_time['hr_rate'].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            "Exit Velocity Change (1st → 3rd)", 
                            f"{exit_velo_increase:+.1f} mph",
                            delta=f"{'Increase' if exit_velo_increase > 0 else 'Decrease'}"
                        )
                    
                    with col2:
                        st.metric(
                            "HR Rate Change (1st → 3rd)",
                            f"{hr_rate_increase:+.1f}%",
                            delta=f"{'Higher' if hr_rate_increase > 0 else 'Lower'}"
                        )
                
                # Display fatigue stats table
                st.dataframe(fatigue_stats, use_container_width=True)
                
                # Betting insights
                st.subheader("💰 Pitcher Fatigue Betting Strategy")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🚨 The Third Time Through Alert**")
                    
                    if len(fatigue_stats) >= 3:
                        third_time_stats = fatigue_stats[fatigue_stats['times_through'] == 3]
                        if not third_time_stats.empty:
                            third_hr_rate = third_time_stats['hr_rate'].iloc[0]
                            third_exit_velo = third_time_stats['avg_exit_velo'].iloc[0]
                            
                            if third_hr_rate > fatigue_stats['hr_rate'].iloc[0] * 1.5:
                                st.error("🔥 **MAJOR FATIGUE DETECTED**")
                                st.write(f"• HR rate jumps to {third_hr_rate:.1f}%")
                                st.write(f"• Exit velo: {third_exit_velo:.1f} mph")
                                st.write("• **BET: OVER on next batter HR prop**")
                            else:
                                st.success("✅ **PITCHER HOLDING UP**")
                                st.write("• Consistent performance")
                                st.write("• No major fatigue signs")
                
                with col2:
                    st.write("**⚡ Live Betting Triggers**")
                    st.write("🎯 **Bet OVER when:**")
                    st.write("• Starter faces lineup 3rd time")
                    st.write("• Exit velocity trending up")
                    st.write("• Power hitter due up")
                    st.write("")
                    st.write("⚠️ **Watch for:**")
                    st.write("• Manager warm-up signals")
                    st.write("• Pitch count over 90")
                    st.write("• Previous hard contact")
                    st.write("")
                    st.write("🔄 **Relief Pitcher Notes:**")
                    st.write("• Fresh arm advantage")
                    st.write("• First batter often struggles")
                    st.write("• Bet UNDER on reliever debut")
            else:
                st.info("Need more data to show fatigue trends. Try expanding your date range.")
        else:
            st.warning("No pitcher fatigue data available.")
    else:
        st.info("Pitcher fatigue analysis requires 'pitcher' and 'at_bat_number' columns.")
        
        # Show what columns are available
        pitcher_cols = [col for col in df.columns if 'pitch' in col.lower()]
        if pitcher_cols:
            st.write("**Pitcher-related columns found:**", pitcher_cols)

with profile_tab:
    st.header("👤 Player Profile Analysis - Complete Scouting Report")
    
    if selected_player != 'All Players' and 'player_name' in df.columns:
        player_data = df[df['player_name'] == selected_player].copy()
        
        if not player_data.empty:
            # Player metrics calculation
            metrics_data = player_data.dropna(subset=['launch_speed', 'launch_angle']).copy()
            
            if not metrics_data.empty:
                # Calculate key metrics
                avg_exit_velo = metrics_data['launch_speed'].mean()
                avg_launch_angle = metrics_data['launch_angle'].mean()
                
                # Barrel rate calculation
                barrel_criteria = (
                    (metrics_data['launch_speed'] >= 98) & 
                    (metrics_data['launch_angle'] >= 8) & 
                    (metrics_data['launch_angle'] <= 50)
                )
                barrel_rate = barrel_criteria.sum() / len(metrics_data) * 100
                
                # Hard hit rate (95+ mph)
                hard_hit_rate = (metrics_data['launch_speed'] >= 95).sum() / len(metrics_data) * 100
                
                # Sweet spot rate (8-32 degrees)
                sweet_spot_rate = ((metrics_data['launch_angle'] >= 8) & 
                                 (metrics_data['launch_angle'] <= 32)).sum() / len(metrics_data) * 100
                
                # Expected stats
                avg_xwoba = metrics_data['estimated_woba_using_speedangle'].mean() if 'estimated_woba_using_speedangle' in metrics_data.columns else 0.300
                
                # Pull rate calculation (negative plate_x for righties, positive for lefties)
                if 'stand' in metrics_data.columns and 'plate_x' in metrics_data.columns:
                    righties = metrics_data[metrics_data['stand'] == 'R']
                    lefties = metrics_data[metrics_data['stand'] == 'L']
                    
                    pull_hits = 0
                    total_hits = 0
                    
                    if not righties.empty:
                        pull_hits += (righties['plate_x'] < -0.5).sum()  # Right-handed pull to left
                        total_hits += len(righties)
                    
                    if not lefties.empty:
                        pull_hits += (lefties['plate_x'] > 0.5).sum()   # Left-handed pull to right
                        total_hits += len(lefties)
                    
                    pull_rate = (pull_hits / total_hits * 100) if total_hits > 0 else 50
                else:
                    pull_rate = 50  # Default neutral
                
                # Create radar chart data
                radar_data = {
                    'metric': ['Exit Velocity', 'Launch Angle', 'Barrel Rate', 'Hard Hit %', 'Sweet Spot %', 'Expected wOBA', 'Pull Rate'],
                    'value': [
                        min(avg_exit_velo / 115 * 100, 100),  # Scale to 100
                        min(abs(avg_launch_angle - 15) / 15 * 100, 100),  # Optimal around 15-25 degrees
                        min(barrel_rate * 2, 100),  # Scale barrel rate
                        min(hard_hit_rate, 100),
                        min(sweet_spot_rate, 100),
                        min(avg_xwoba / 0.500 * 100, 100),  # Scale xwOBA
                        min(pull_rate, 100)
                    ]
                }
                
                radar_df = pd.DataFrame(radar_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Radar chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=radar_df['value'],
                        theta=radar_df['metric'],
                        fill='toself',
                        name=selected_player,
                        line=dict(color='blue', width=2),
                        fillcolor='rgba(0, 100, 255, 0.2)'
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 100]
                            )
                        ),
                        showlegend=True,
                        title=f"{selected_player} - Power Profile Radar",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Launch angle distribution
                    angle_bins = [-90, -10, 10, 25, 35, 50, 90]
                    angle_labels = ['Ground Ball', 'Line Drive', 'Fly Ball', 'Sweet Spot', 'Pop Up', 'High Pop']
                    
                    metrics_data['angle_category'] = pd.cut(
                        metrics_data['launch_angle'], 
                        bins=angle_bins, 
                        labels=angle_labels,
                        include_lowest=True
                    )
                    
                    angle_dist = metrics_data['angle_category'].value_counts()
                    
                    colors = ['#ff4444', '#ffa500', '#ffff00', '#00ff00', '#0080ff', '#8000ff']
                    
                    fig = go.Figure(data=[go.Pie(
                        labels=angle_dist.index,
                        values=angle_dist.values,
                        hole=0.4,
                        marker=dict(colors=colors[:len(angle_dist)])
                    )])
                    
                    fig.update_layout(
                        title=f"{selected_player} - Launch Angle Distribution",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Player summary metrics
                st.subheader("📊 Key Performance Indicators")
                
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    st.metric("Exit Velocity", f"{avg_exit_velo:.1f} mph")
                with col2:
                    st.metric("Barrel Rate", f"{barrel_rate:.1f}%")
                with col3:
                    st.metric("Hard Hit %", f"{hard_hit_rate:.1f}%")
                with col4:
                    st.metric("Sweet Spot %", f"{sweet_spot_rate:.1f}%")
                with col5:
                    st.metric("Expected wOBA", f"{avg_xwoba:.3f}")
                
                # Betting assessment
                st.subheader("💰 Betting Profile Assessment")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**🎯 Strengths**")
                    strengths = []
                    
                    if avg_exit_velo >= 108:
                        strengths.append("Elite exit velocity")
                    if barrel_rate >= 15:
                        strengths.append("High barrel rate")
                    if hard_hit_rate >= 45:
                        strengths.append("Consistent hard contact")
                    if 20 <= avg_launch_angle <= 30:
                        strengths.append("Optimal launch angle")
                    
                    if strengths:
                        for strength in strengths:
                            st.success(f"✅ {strength}")
                    else:
                        st.info("Developing power profile")
                
                with col2:
                    st.write("**⚠️ Concerns**")
                    concerns = []
                    
                    if avg_exit_velo < 95:
                        concerns.append("Below-average exit velocity")
                    if barrel_rate < 8:
                        concerns.append("Low barrel rate")
                    if hard_hit_rate < 35:
                        concerns.append("Inconsistent hard contact")
                    if avg_launch_angle < 5 or avg_launch_angle > 40:
                        concerns.append("Suboptimal launch angle")
                    
                    if concerns:
                        for concern in concerns:
                            st.warning(f"⚠️ {concern}")
                    else:
                        st.success("Well-rounded profile")
                
                with col3:
                    st.write("**🎲 Betting Recommendations**")
                    
                    # Overall assessment
                    power_score = (avg_exit_velo/115 + barrel_rate/20 + hard_hit_rate/50) / 3 * 100
                    
                    if power_score >= 75:
                        st.error("🔥 **ELITE POWER**")
                        st.write("• Bet OVER on HR props")
                        st.write("• Target vs weak pitching")
                        st.write("• Hot weather advantage")
                    elif power_score >= 60:
                        st.warning("⚡ **ABOVE AVERAGE**")
                        st.write("• Situational HR betting")
                        st.write("• Favorable matchups only")
                        st.write("• Consider park factors")
                    else:
                        st.info("📊 **DEVELOPING**")
                        st.write("• Avoid HR props")
                        st.write("• Focus on contact stats")
                        st.write("• Look for value elsewhere")
            else:
                st.warning(f"No sufficient statistical data available for {selected_player}")
        else:
            st.warning(f"No data found for player: {selected_player}")
    else:
        st.info("Select a specific player from the sidebar to view detailed profile analysis.")
        
        # Show player selection hint
        if 'player_name' in df.columns:
            top_players = df['player_name'].value_counts().head(10)
            st.write("**Most Active Players in Dataset:**")
            for player, count in top_players.items():
                st.write(f"• {player} ({count} plate appearances)")

with original_tab:
    st.header("📊 Original Pitch Type Analysis")
    
    if 'pitch_name' in df.columns:
        pitch_counts = df['pitch_name'].value_counts().head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pitch type pie chart
            fig = px.pie(
                values=pitch_counts.values,
                names=pitch_counts.index,
                title="Pitch Type Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Pitch speed by type
            speed_data = df.dropna(subset=['pitch_name', 'release_speed'])
            if not speed_data.empty:
                fig = px.box(
                    speed_data,
                    x='pitch_name',
                    y='release_speed',
                    title="Pitch Speed by Type"
                )
                fig.update_layout(xaxis={'tickangle': 45})
                st.plotly_chart(fig, use_container_width=True)

with raw_data_tab:
    st.header("🔍 Raw Data Explorer")
    
    st.subheader("Available Columns")
    
    # Show all columns with descriptions
    important_cols = {
        'plate_x': 'Horizontal position at plate (UmpScorecards uses this)',
        'plate_z': 'Vertical position at plate (UmpScorecards uses this)',
        'sz_top': 'Top of strike zone (UmpScorecards uses this)',
        'sz_bot': 'Bottom of strike zone (UmpScorecards uses this)',
        'description': 'Pitch call (UmpScorecards uses this)',
        'launch_speed': 'Exit velocity (mph)',
        'launch_angle': 'Launch angle (degrees)',
        'estimated_woba_using_speedangle': 'Expected wOBA based on exit velo/angle',
        'release_speed': 'Pitch velocity',
        'pitch_name': 'Type of pitch thrown',
        'events': 'Result of at-bat',
        'home_score': 'Home team score',
        'away_score': 'Away team score'
    }
    
    for col, desc in important_cols.items():
        if col in df.columns:
            st.write(f"✅ **{col}**: {desc}")
        else:
            st.write(f"❌ **{col}**: {desc} (not available)")
    
    st.subheader("Sample Data")
    
    # Show sample of actual data
    display_cols = [col for col in important_cols.keys() if col in df.columns]
    if display_cols:
        st.dataframe(df[display_cols].head(20))
    
    st.subheader("Data Summary")
    st.write(f"**Total Rows**: {len(df):,}")
    st.write(f"**Total Columns**: {len(df.columns)}")
    st.write(f"**Date Range**: {df['game_date'].min() if 'game_date' in df.columns else 'N/A'} to {df['game_date'].max() if 'game_date' in df.columns else 'N/A'}")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Data Advantage**: You have access to 100+ data points vs. UmpScorecards' 5 basic columns. "
    "This gives you a massive edge for betting analysis!"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**🚀 Next Steps:**")
st.sidebar.markdown("1. Explore different date ranges")
st.sidebar.markdown("2. Focus on specific teams/players")
st.sidebar.markdown("3. Build betting models with this data")
st.sidebar.markdown("4. Create automated content generation")