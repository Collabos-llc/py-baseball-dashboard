import streamlit as st
import pandas as pd

st.title("🎯 Simple Baseball Dashboard Test")
st.write("If you can see this, Streamlit is working!")

# Test PyBaseball import
try:
    import pybaseball as pyb
    st.success("✅ PyBaseball imported successfully!")
    
    # Show some sample data without loading real data
    sample_data = {
        'pitch_type': ['FF', 'SL', 'CH', 'CU'],
        'release_speed': [95.2, 87.1, 83.5, 78.9],
        'launch_speed': [102.3, 89.5, 95.1, 78.2]
    }
    df = pd.DataFrame(sample_data)
    
    st.subheader("Sample Baseball Data")
    st.dataframe(df)
    
    st.info("✅ Dashboard setup is working! The main dashboard should work now.")
    
except ImportError as e:
    st.error(f"❌ PyBaseball import failed: {e}")

st.write("**Next Step**: Try the full dashboard at baseball_dashboard.py")