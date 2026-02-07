import streamlit as st
from streamlit_option_menu import option_menu
from src.case_studies import (
    show_scenario_1, show_scenario_2, show_scenario_3, show_scenario_4,
    show_scenario_5, show_scenario_6, show_scenario_7, show_scenario_8, show_scenario_9
)

# Page Config
st.set_page_config(
    page_title="PhonePe Pulse Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    h1, h2, h3 {
        color: #008bf8; 
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    with st.sidebar:
        st.title("PhonePe Pulse")
        st.markdown("### Analysis Scenarios")
        st.info("Select a scenario to analyze:")
        
        scenario = st.radio(
            "Select Analysis:",
            [
                "1. Decoding Transaction Dynamics",
                "2. Device Dominance & Engagement",
                "3. Insurance Penetration & Growth",
                "4. Market Expansion Strategy",
                "5. User Engagement & Growth",
                "6. Insurance Engagement (Uptake)",
                "7. Top Transaction Performers",
                "8. Top User Registration",
                "9. Top Insurance Performers",
            ],
            index=0
        )
        
        st.divider()
        st.markdown("**About**: This dashboard provides deep insights into PhonePe's Pulse data across payments, users, and insurance.")

    # Routing
    if scenario == "1. Decoding Transaction Dynamics":
        show_scenario_1()
    elif scenario == "2. Device Dominance & Engagement":
        show_scenario_2()
    elif scenario == "3. Insurance Penetration & Growth":
        show_scenario_3()
    elif scenario == "4. Market Expansion Strategy":
        show_scenario_4()
    elif scenario == "5. User Engagement & Growth":
        show_scenario_5()
    elif scenario == "6. Insurance Engagement (Uptake)":
        show_scenario_6()
    elif scenario == "7. Top Transaction Performers":
        show_scenario_7()
    elif scenario == "8. Top User Registration":
        show_scenario_8()
    elif scenario == "9. Top Insurance Performers":
        show_scenario_9()

if __name__ == "__main__":
    main()
