#!/usr/bin/env python3
"""
PyBaseball Data Exploration Script
This script demonstrates how to access MLB Statcast data and shows available columns.
"""

import pybaseball as pyb
import pandas as pd
from datetime import datetime, timedelta

def main():
    print("🚀 PyBaseball Data Exploration")
    print("=" * 50)
    
    # Enable caching for faster subsequent runs
    pyb.cache.enable()
    
    # Get recent data (last 3 days to ensure we have games)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    
    print(f"📅 Fetching Statcast data from {start_date} to {end_date}")
    print("⏳ This may take a moment on first run (caching data)...")
    
    try:
        # Fetch Statcast data
        data = pyb.statcast(start_date, end_date)
        
        if data.empty:
            print("❌ No data found for these dates. Trying a broader range...")
            # Try last week if no recent games
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            data = pyb.statcast(start_date, end_date)
        
        if data.empty:
            print("❌ Still no data. MLB season might be off or try different dates.")
            return
        
        print(f"✅ Successfully loaded {len(data)} pitch records!")
        print()
        
        # Show all available columns
        print("📊 ALL AVAILABLE COLUMNS:")
        print("=" * 30)
        columns = data.columns.tolist()
        for i, col in enumerate(columns, 1):
            print(f"{i:2d}. {col}")
        
        print(f"\n🔢 Total columns available: {len(columns)}")
        print()
        
        # Highlight UmpScorecards columns
        ump_columns = ['balls', 'strikes', 'outs_when_up', 'inning', 'inning_topbot']
        print("⚾ UmpScorecards Uses These 5 Columns:")
        print("=" * 40)
        for col in ump_columns:
            if col in columns:
                print(f"✅ {col}")
            else:
                print(f"❌ {col} (not found)")
        
        print()
        
        # Show betting-relevant columns
        betting_columns = [
            'launch_speed', 'launch_angle', 'estimated_woba_using_speedangle',
            'hit_distance_sc', 'spin_axis', 'release_speed', 'effective_speed',
            'woba_value', 'babip_value', 'iso_value', 'plate_x', 'plate_z'
        ]
        
        print("💰 KEY BETTING-RELEVANT COLUMNS:")
        print("=" * 35)
        available_betting = [col for col in betting_columns if col in columns]
        for col in available_betting:
            print(f"✅ {col}")
        
        print(f"\n🎯 You have {len(available_betting)} advanced metrics for betting analysis!")
        print()
        
        # Show sample data
        print("📝 SAMPLE DATA (First 3 Records):")
        print("=" * 35)
        sample_cols = ['game_date', 'player_name', 'events', 'launch_speed', 'launch_angle', 'estimated_woba_using_speedangle']
        available_sample_cols = [col for col in sample_cols if col in columns]
        
        if available_sample_cols:
            print(data[available_sample_cols].head(3).to_string())
        else:
            print("Sample columns not available in current dataset")
        
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! PyBaseball is working and you have access to:")
        print(f"   • {len(data)} recent pitch records")
        print(f"   • {len(columns)} total data columns")
        print(f"   • {len(available_betting)} advanced betting metrics")
        print("   • WAY MORE data than UmpScorecards!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure you have internet connection")
        print("   2. Try: pip install --upgrade pybaseball")
        print("   3. MLB season runs April-October")

if __name__ == "__main__":
    main()