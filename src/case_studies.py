import streamlit as st
import pandas as pd
import plotly.express as px
from src.db import execute_query

def calculate_growth_metrics(df):
    """
    Calculates Year-over-Year growth for state-wise transaction data.
    """
    # Group by State, Year, Category
    grouped = df.groupby(['state', 'year', 'transaction_type'])['transaction_amount'].sum().reset_index()
    
    # Sort to ensure shift works correctly
    grouped = grouped.sort_values(['state', 'transaction_type', 'year'])
    
    # Calculate Previous Year Amount
    grouped['prev_year_amount'] = grouped.groupby(['state', 'transaction_type'])['transaction_amount'].shift(1)
    
    # Calculate Growth Rate
    # Handle division by zero or NaN
    grouped['growth_rate'] = ((grouped['transaction_amount'] - grouped['prev_year_amount']) / grouped['prev_year_amount']) * 100
    
    return grouped

def show_scenario_1():
    st.title("Scenario 1: Decoding Transaction Dynamics")
    st.markdown("""
    **Business Problem**: Identify which regions and categories are growing vs. declining.
    **Goal**: Drive targeted interventions for stagnating areas.
    """)
    
    # 1. Fetch Data
    query = "SELECT * FROM aggregated_transaction"
    df = execute_query(query)
    
    if df.empty:
        st.error("No data found!")
        return

    # Data Prep
    df['state'] = df['state'].str.title().str.replace("-", " ")
    
    # 2. Filters
    years = sorted(df['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    
    # 3. Calculate Growth
    growth_df = calculate_growth_metrics(df)
    current_year_growth = growth_df[growth_df['year'] == selected_year]
    
    # 4. Visualization: Growth Matrix (Heatmap)
    st.subheader(f"Growth Matrix: States vs Categories ({selected_year})")
    st.write("**Red** = Decline (Needs Attention) | **Blue/Green** = Growth (Healthy)")
    
    if not current_year_growth.empty:
        pivot_growth = current_year_growth.pivot(index='state', columns='transaction_type', values='growth_rate')
        
        fig_heat = px.imshow(
            pivot_growth,
            labels=dict(x="Category", y="State", color="Growth %"),
            x=pivot_growth.columns,
            y=pivot_growth.index,
            color_continuous_scale="RdBu",
            range_color=[-50, 50], # Cap to focus on typical variance
            aspect="auto",
            height=800
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
        # 5. Top 3 Growing vs Declining
        st.subheader("Regional Performance Highlights")
        
        # Aggregate total growth per state (weighted average approximation or total value growth)
        state_totals = df.groupby(['state', 'year'])['transaction_amount'].sum().reset_index()
        state_totals['prev'] = state_totals.groupby('state')['transaction_amount'].shift(1)
        state_totals['growth'] = ((state_totals['transaction_amount'] - state_totals['prev']) / state_totals['prev']) * 100
        
        curr_state_growth = state_totals[state_totals['year'] == selected_year]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("Top 3 Fastest Growing States")
            top_3 = curr_state_growth.nlargest(3, 'growth')
            for _, row in top_3.iterrows():
                st.metric(label=row['state'], value=f"₹{row['transaction_amount']/1e9:.2f}B", delta=f"{row['growth']:.1f}%")
                
        with col2:
            st.error("Top 3 Declining / Slowest States")
            bot_3 = curr_state_growth.nsmallest(3, 'growth')
            for _, row in bot_3.iterrows():
                st.metric(label=row['state'], value=f"₹{row['transaction_amount']/1e9:.2f}B", delta=f"{row['growth']:.1f}%")
                
        # 6. Trend Analysis (Deep Dive)
        st.divider()
        st.subheader("Deep Dive: Category Trends")
        selected_state = st.selectbox("Select State to Investigate", df['state'].unique())
        
        state_data = df[df['state'] == selected_state]
        state_data['period'] = state_data['year'].astype(str) + "-Q" + state_data['quarter'].astype(str)
        
        fig_trend = px.line(state_data, x='period', y='transaction_amount', color='transaction_type',
                            title=f"Transaction Trend for {selected_state}",
                            markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    else:
        st.warning("Not enough data to calculate growth for the selected year (Need previous year data).")

def show_scenario_2():
    st.title("Scenario 2: Device Dominance & User Engagement")
    st.markdown("""
    **Business Problem**: Trends in device usage vary, and some devices might be underutilized despite high registrations.
    **Goal**: Identify if 'Budget' devices correlate with lower App Engagement.
    """)
    
    # 1. Fetch Data
    try:
        df_dev = execute_query("SELECT * FROM aggregated_user_device")
        df_user = execute_query("SELECT * FROM aggregated_user")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    if df_dev.empty or df_user.empty:
        st.error("Missing data tables.")
        return
        
    # Data Prep
    df_dev['state'] = df_dev['state'].str.title().str.replace("-", " ")
    df_user['state'] = df_user['state'].str.title().str.replace("-", " ")
    
    # 2. Filters
    years = sorted(df_dev['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    
    # Filter for selected year
    dev_curr = df_dev[df_dev['year'] == selected_year]
    user_curr = df_user[df_user['year'] == selected_year]
    
    # --- Visualization 1: Brand Market Share Trends ---
    st.subheader("1. Device Brand Trends (National)")
    
    national_trends = df_dev.groupby(['year', 'brand'])['count'].sum().reset_index()
    fig_trend = px.line(national_trends, x='year', y='count', color='brand', 
                        title="Growth of Device Brands Over Time", markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # --- Visualization 2: Correlation Analysis ---
    st.subheader(f"2. Engagement vs Device Dominance ({selected_year})")
    st.write("Does the dominant device brand in a state impact how much users engage with the app?")
    
    # 1. Find dominant brand per state
    state_brand = dev_curr.groupby(['state', 'brand'])['count'].sum().reset_index()
    idx = state_brand.groupby(['state'])['count'].transform(max) == state_brand['count']
    dominant_brands = state_brand[idx].rename(columns={'brand': 'dominant_brand', 'count': 'brand_count'})
    
    # 2. Get Engagement Stats
    df_trans = execute_query(f"SELECT state, SUM(transaction_count) as total_trans FROM aggregated_transaction WHERE year={selected_year} GROUP BY state")
    df_trans['state'] = df_trans['state'].str.title().str.replace("-", " ")
    
    state_users = user_curr.groupby(['state'])['registered_users'].sum().reset_index()
    
    # Merge all
    merged = pd.merge(dominant_brands, state_users, on='state')
    merged = pd.merge(merged, df_trans, on='state')
    
    merged['engagement_score'] = merged['total_trans'] / merged['registered_users']
    merged['dominance_pct'] = (merged['brand_count'] / merged['registered_users']) * 100
    
    fig_scatter = px.scatter(
        merged, 
        x='dominance_pct', 
        y='engagement_score',
        color='dominant_brand',
        size='registered_users',
        hover_name='state',
        title="Correlation: Brand Dominance % vs Transactions/User",
        labels={'dominance_pct': 'Dominant Brand Market Share (%)', 'engagement_score': 'Transactions per User'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.info("""
    **Hypothesis Check**: 
    - If 'Budget' brand dominated states (e.g., Xiaomi/Vivo) cluster at the bottom, it suggests lower engagement.
    - If 'Premium' brand states (e.g. Apple/Samsung) are higher, it confirms the 'Affluence = Activity' theory.
    """)
    
    # --- Visualization 3: Regional Bar Chart ---
    st.subheader(f"3. Regional Brand Dominance Map ({selected_year})")
    
    fig_bar = px.bar(dominant_brands, x='state', y='brand_count', color='dominant_brand',
                     title="Dominant Device Brand by State",
                     labels={'brand_count': 'User Count', 'dominant_brand': 'Top Brand'})
    st.plotly_chart(fig_bar, use_container_width=True)

def show_scenario_3():
    st.title("Scenario 3: Insurance Penetration & Growth Potential")
    st.markdown("""
    **Business Problem**: Identifying untapped opportunities where transaction volume is high but insurance adoption is low.
    **Goal**: Prioritize regions for insurance marketing.
    """)
    
    # 1. Fetch Data
    try:
        df_ins = execute_query("SELECT * FROM aggregated_insurance")
        df_trans = execute_query("SELECT state, year, quarter, SUM(transaction_count) as total_trans FROM aggregated_transaction GROUP BY state, year, quarter")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return

    if df_ins.empty:
        st.error("No insurance data found.")
        return
        
    # Data Prep
    df_ins['state'] = df_ins['state'].str.title().str.replace("-", " ")
    df_trans['state'] = df_trans['state'].str.title().str.replace("-", " ")
    
    # 2. Filters
    years = sorted(df_ins['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    
    # --- Visualization 1: Growth Trajectory ---
    st.subheader("1. Insurance Growth Trajectory")
    
    national_growth = df_ins.groupby(['year', 'quarter'])['insurance_count'].sum().reset_index()
    national_growth['period'] = national_growth['year'].astype(str) + "-Q" + national_growth['quarter'].astype(str)
    
    fig_line = px.line(national_growth, x='period', y='insurance_count', markers=True,
                       title="Total Insurance Policies Sold Over Time")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # --- Visualization 2: Opportunity Matrix ---
    st.subheader(f"2. Opportunity Matrix: Transactions vs Insurance ({selected_year})")
    
    ins_curr = df_ins[df_ins['year'] == selected_year].groupby('state')['insurance_count'].sum().reset_index()
    trans_curr = df_trans[df_trans['year'] == selected_year].groupby('state')['total_trans'].sum().reset_index()
    
    opp_df = pd.merge(ins_curr, trans_curr, on='state')
    opp_df['penetration_per_1k_trans'] = (opp_df['insurance_count'] / opp_df['total_trans']) * 1000
    
    fig_scatter = px.scatter(
        opp_df,
        x='total_trans',
        y='insurance_count',
        size='penetration_per_1k_trans',
        color='penetration_per_1k_trans',
        hover_name='state',
        text='state',
        log_x=True, log_y=True,
        title="Opportunity Matrix (Log Scale)",
        labels={'total_trans': 'Total Transactions (Potential)', 'insurance_count': 'Insurance Policies Sold'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.info("""
    **Interpretation**:
    - **Bottom-Right**: High Transactions, Low Insurance -> **High Opportunity (Target Here)**.
    - **Top-Right**: High Transactions, High Insurance -> **Mature Markets**.
    """)
    
    # --- Visualization 3: Top Adoption Markets ---
    st.subheader(f"3. Top 10 States by Insurance Adoption ({selected_year})")
    
    top_states = ins_curr.nlargest(10, 'insurance_count')
    fig_bar = px.bar(top_states, x='state', y='insurance_count', color='insurance_count',
                     title="Top States for Insurance Sales")
    st.plotly_chart(fig_bar, use_container_width=True)


def show_scenario_4():
    st.title("Scenario 4: Market Expansion Strategy")
    st.markdown("""
    **Business Problem**: Identifying Emerging Markets (High Growth, Low Volume) to capture early.
    **Goal**: Classify states into Stars, Cash Cows, and Opportunity Zones.
    """)
    
    try:
        query = """
            SELECT state, year, quarter, SUM(transaction_amount) as total_val, SUM(transaction_count) as total_vol 
            FROM aggregated_transaction 
            GROUP BY state, year, quarter
        """
        df = execute_query(query)
        df_cat = execute_query("SELECT state, year, transaction_type, SUM(transaction_amount) as amount FROM aggregated_transaction GROUP BY state, year, transaction_type")
        df_dist = execute_query("SELECT state, district, year, SUM(total_transactions) as total_vol FROM map_map GROUP BY state, district, year")
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return
    
    if df.empty:
        st.error("No transaction data found.")
        return

    df['state'] = df['state'].str.title().str.replace("-", " ")
    if not df_cat.empty:
        df_cat['state'] = df_cat['state'].str.title().str.replace("-", " ")
    if not df_dist.empty:
        df_dist['state'] = df_dist['state'].str.title().str.replace("-", " ")
        df_dist['district'] = df_dist['district'].str.title()
    
    years = sorted(df['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    df_curr = df[df['year'] == selected_year]
    
    st.subheader(f"1. Market Maturity Matrix ({selected_year})")
    market_size = df_curr.groupby('state')['total_vol'].sum().reset_index()
    df = df.sort_values(['state', 'year', 'quarter'])
    df['prev_vol'] = df.groupby('state')['total_vol'].shift(1)
    df['qoq_growth'] = ((df['total_vol'] - df['prev_vol']) / df['prev_vol']) * 100
    avg_growth = df[df['year'] == selected_year].groupby('state')['qoq_growth'].mean().reset_index()
    matrix_df = pd.merge(market_size, avg_growth, on='state')
    
    median_vol = matrix_df['total_vol'].median()
    median_growth = matrix_df['qoq_growth'].median()
    
    def classify(row):
        if row['total_vol'] >= median_vol and row['qoq_growth'] >= median_growth:
            return "Star (High Vol, High Growth)"
        elif row['total_vol'] >= median_vol and row['qoq_growth'] < median_growth:
            return "Cash Cow (High Vol, Low Growth)"
        elif row['total_vol'] < median_vol and row['qoq_growth'] >= median_growth:
            return "Emerging (Low Vol, High Growth)"
        else:
            return "Slow (Low Vol, Low Growth)"
            
    matrix_df['Category'] = matrix_df.apply(classify, axis=1)
    fig_scatter = px.scatter(matrix_df, x='total_vol', y='qoq_growth', color='Category', size='total_vol', text='state', hover_name='state', log_x=True,
                             title="Maturity Matrix: Market Size vs Momentum",
                             labels={'total_vol': 'Transaction Volume (Log)', 'qoq_growth': 'Avg QoQ Growth (%)'})
    fig_scatter.add_vline(x=median_vol, line_dash="dash", line_color="grey", annotation_text="Median Vol")
    fig_scatter.add_hline(y=median_growth, line_dash="dash", line_color="grey", annotation_text="Median Growth")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.subheader("2. Category Gap Analysis")
    cat_curr = df_cat[df_cat['year'] == selected_year] if not df_cat.empty else pd.DataFrame()
    if not cat_curr.empty:
        state_sums = cat_curr.groupby('state')['amount'].transform('sum')
        cat_curr['percent'] = (cat_curr['amount'] / state_sums) * 100
        fig_norm = px.bar(cat_curr, x='state', y='percent', color='transaction_type', title="Payment Mix % by State", labels={'percent': 'Share of Total Value (%)'})
        st.plotly_chart(fig_norm, use_container_width=True)
    else:
        st.info("Category breakdown data unavailable for this year.")
    
    st.subheader(f"3. Hidden Gems: Top Emerging Districts ({selected_year})")
    emerging_states = matrix_df[matrix_df['Category'].str.contains("Emerging")]['state'].tolist()
    if emerging_states and not df_dist.empty:
        dist_emerging = df_dist[(df_dist['year'] == selected_year) & (df_dist['state'].isin(emerging_states))]
        if not dist_emerging.empty:
            top_districts = dist_emerging.nlargest(10, 'total_vol')
            fig_dist = px.bar(top_districts, x='total_vol', y='district', color='state', orientation='h', title="Top Districts in Emerging Markets")
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("No district-level data for emerging states.")
    elif not emerging_states:
        st.info("No states classified as 'Emerging' this year based on median thresholds.")
    else:
        st.info("District-level data unavailable.")

def show_scenario_5():
    st.title("Scenario 5: User Engagement & Growth Strategy")
    st.markdown("""
    **Business Problem**: Understanding user retention and deeper engagement beyond just registration.
    **Goal**: Analyze App Opens vs Registered Users.
    """)
    
    try:
        df_user = execute_query("SELECT * FROM aggregated_user")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return
        
    if df_user.empty:
        st.error("No user data found.")
        return

    df_user['state'] = df_user['state'].str.title().str.replace("-", " ")
    years = sorted(df_user['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    user_curr = df_user[df_user['year'] == selected_year]
    
    st.subheader("1. User Registration Growth")
    growth_trend = df_user.groupby(['year', 'quarter'])['registered_users'].sum().reset_index()
    growth_trend['period'] = growth_trend['year'].astype(str) + "-Q" + growth_trend['quarter'].astype(str)
    fig_line = px.line(growth_trend, x='period', y='registered_users', markers=True, title="Total Registered Users Over Time")
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.subheader(f"2. Engagement Rate: App Opens vs Registrations ({selected_year})")
    state_eng = user_curr.groupby('state')[['registered_users', 'app_opens']].sum().reset_index()
    if state_eng['app_opens'].sum() == 0:
        st.warning("App Opens data might be missing for this year.")
    state_eng['engagement_rate'] = state_eng['app_opens'] / state_eng['registered_users']
    state_eng = state_eng.sort_values('engagement_rate', ascending=False)
    fig_bar = px.bar(state_eng, x='state', y='engagement_rate', color='engagement_rate', title="Avg App Opens per User by State", color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("3. Top Districts by Registered Users")
    try:
        df_dist_user = execute_query(f"SELECT state, district, SUM(registered_users) as users FROM map_user WHERE year={selected_year} GROUP BY state, district")
        df_dist_user['district'] = df_dist_user['district'].str.title()
        top_districts = df_dist_user.nlargest(10, 'users')
        if not top_districts.empty:
            fig_dist = px.bar(top_districts, x='users', y='district', color='state', orientation='h', title="Top 10 Districts by Registered Users")
            st.plotly_chart(fig_dist, use_container_width=True)
    except:
        st.info("District level user data not available.")

def show_scenario_6():
    st.title("Scenario 6: Insurance Engagement Analysis")
    st.markdown("""
    **Business Problem**: Determining the 'quality' of insurance adoption (Premium Sizing).
    **Goal**: Analyze Average Premium Size and Policy Density.
    """)
    
    try:
        df_ins = execute_query("SELECT * FROM aggregated_insurance")
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return
        
    if df_ins.empty:
        st.error("No insurance data found.")
        return

    df_ins['state'] = df_ins['state'].str.title().str.replace("-", " ")
    years = sorted(df_ins['year'].unique())
    selected_year = st.sidebar.selectbox("Select Analysis Year", years, index=len(years)-1)
    ins_curr = df_ins[df_ins['year'] == selected_year]
    
    st.subheader(f"1. Average Premium Size by State ({selected_year})")
    state_prem = ins_curr.groupby('state')[['insurance_count', 'insurance_amount']].sum().reset_index()
    state_prem['avg_premium'] = state_prem['insurance_amount'] / state_prem['insurance_count']
    state_prem = state_prem.sort_values('avg_premium', ascending=False)
    fig_bar = px.bar(state_prem, x='state', y='avg_premium', color='avg_premium', title="Average Premium Value (₹) by State", labels={'avg_premium': 'Avg Premium (₹)'})
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.subheader("2. Volume vs Value Matrix")
    fig_scatter = px.scatter(state_prem, x='insurance_count', y='avg_premium', size='insurance_amount', color='state', hover_name='state', log_x=True, title="Policy Volume vs Premium Value", labels={'insurance_count': 'Total Policies Sold', 'avg_premium': 'Avg Policy Value'})
    st.plotly_chart(fig_scatter, use_container_width=True)

def show_scenario_7():
    st.title("Scenario 7: Top Transaction Performers")
    st.markdown("**Goal**: Identify Top States, Districts, and Pincodes by Transaction Volume for a specific Year & Quarter.")
    
    try:
        years = execute_query("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year DESC")['year'].tolist()
        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])
    except:
        st.error("Error fetching years.")
        return

    st.subheader(f"1. Top 10 States (Transactions) - Q{selected_quarter} {selected_year}")
    q_state = f"SELECT state, SUM(transaction_count) as count, SUM(transaction_amount) as amount FROM aggregated_transaction WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY state ORDER BY count DESC LIMIT 10"
    df_state = execute_query(q_state)
    if not df_state.empty:
        df_state['state'] = df_state['state'].str.title().str.replace("-", " ")
        fig_s = px.bar(df_state, x='count', y='state', orientation='h', title="Top States by Volume", color='amount')
        st.plotly_chart(fig_s, use_container_width=True)
        
    st.subheader("2. Top 10 Districts (Transactions)")
    try:
        q_dist = f"SELECT district, state, SUM(total_transactions) as count FROM map_map WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY district, state ORDER BY count DESC LIMIT 10"
        df_dist = execute_query(q_dist)
        if not df_dist.empty:
            df_dist['district'] = df_dist['district'].str.title()
            fig_d = px.bar(df_dist, x='count', y='district', color='state', orientation='h', title="Top Districts by Volume")
            st.plotly_chart(fig_d, use_container_width=True)
    except:
        st.warning("District data unavailable.")
        
    st.subheader("3. Top 10 Pincodes (Transactions)")
    try:
        q_pin = f"SELECT pincode, state, SUM(transaction_count) as count FROM top_map WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY pincode, state ORDER BY count DESC LIMIT 10"
        df_pin = execute_query(q_pin)
        if not df_pin.empty: st.table(df_pin)
    except:
        st.warning("Pincode data unavailable.")

def show_scenario_8():
    st.title("Scenario 8: User Registration Leaderboard")
    st.markdown("**Goal**: Identify Top Regions for New User Registrations.")
    
    try:
        years = execute_query("SELECT DISTINCT year FROM aggregated_user ORDER BY year DESC")['year'].tolist()
        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])
    except: return

    st.subheader(f"1. Top 10 States (Registrations) - Q{selected_quarter} {selected_year}")
    q_state = f"SELECT state, SUM(registered_users) as users FROM aggregated_user WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY state ORDER BY users DESC LIMIT 10"
    df_state = execute_query(q_state)
    if not df_state.empty:
        df_state['state'] = df_state['state'].str.title().str.replace("-", " ")
        fig_s = px.bar(df_state, x='users', y='state', orientation='h', title="Top States by Registered Users")
        st.plotly_chart(fig_s, use_container_width=True)
        
    st.subheader("2. Top 10 Districts (Registrations)")
    try:
        q_dist = f"SELECT district, state, SUM(registered_users) as users FROM map_user WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY district, state ORDER BY users DESC LIMIT 10"
        df_dist = execute_query(q_dist)
        if not df_dist.empty:
            df_dist['district'] = df_dist['district'].str.title()
            fig_d = px.bar(df_dist, x='users', y='district', color='state', orientation='h', title="Top Districts by Registered Users")
            st.plotly_chart(fig_d, use_container_width=True)
    except:
        st.warning("District data not found.")
        
    st.subheader("3. Top 10 Pincodes (Registrations)")
    try:
        q_pin = f"SELECT pincode, state, SUM(registered_users) as users FROM top_user WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY pincode, state ORDER BY users DESC LIMIT 10"
        df_pin = execute_query(q_pin)
        if not df_pin.empty: st.table(df_pin)
    except:
        st.warning("Pincode data not found.")

def show_scenario_9():
    st.title("Scenario 9: Insurance Leaderboard")
    st.markdown("**Goal**: Identify Top Regions for Insurance Sales.")
    
    try:
        years = execute_query("SELECT DISTINCT year FROM aggregated_insurance ORDER BY year DESC")['year'].tolist()
        selected_year = st.sidebar.selectbox("Select Year", years)
        selected_quarter = st.sidebar.selectbox("Select Quarter", [1, 2, 3, 4])
    except:
        st.error("Error fetching years.")
        return

    st.subheader(f"1. Top 10 States (Policies Sold) - Q{selected_quarter} {selected_year}")
    q_state = f"SELECT state, SUM(insurance_count) as count FROM aggregated_insurance WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY state ORDER BY count DESC LIMIT 10"
    df_state = execute_query(q_state)
    if not df_state.empty:
        df_state['state'] = df_state['state'].str.title().str.replace("-", " ")
        fig_s = px.bar(df_state, x='count', y='state', orientation='h', title="Top States by Policies Sold")
        st.plotly_chart(fig_s, use_container_width=True)
        
    st.subheader("2. Top 10 Districts (Policies Sold)")
    try:
        q_dist = f"SELECT district, state, SUM(insurance_count) as count FROM map_insurance WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY district, state ORDER BY count DESC LIMIT 10"
        df_dist = execute_query(q_dist)
        if not df_dist.empty:
            df_dist['district'] = df_dist['district'].str.title()
            fig_d = px.bar(df_dist, x='count', y='district', color='state', orientation='h', title="Top Districts by Policies Sold")
            st.plotly_chart(fig_d, use_container_width=True)
    except:
        st.warning("District data unavailable.")
        
    st.subheader("3. Top 10 Pincodes (Policies Sold)")
    try:
        q_pin = f"SELECT pincode, state, SUM(insurance_count) as count FROM top_insurance WHERE year={selected_year} AND quarter={selected_quarter} GROUP BY pincode, state ORDER BY count DESC LIMIT 10"
        df_pin = execute_query(q_pin)
        if not df_pin.empty: st.table(df_pin)
    except:
        st.warning("Pincode data unavailable.")
