import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Page config ----------
st.set_page_config(page_title="HSC College Comparison", layout="wide")
st.title("🎓 College‑wise Pass Percentage Comparison")

# ---------- Load data (cached for speed) ----------
@st.cache_data
def load_data():
    df = pd.read_csv("combined_hsc_data.csv")
    df['Year'] = df['Year'].astype(int)
    
    return df

df = load_data()
# Define mapping dictionary
college_mapping = {
    "KARMAVEER BABURAO PATIL JUNIOR COLLEGE, PARINCHE": "KARMAVEER BABURAO PATIL COLLEGE",
    "WAGHIRE COLLEGE OF ARTS,COME & SCIENCE, SASWAD": "WAGHIRE COLLEGE, SASWAD",
    "KILACHAND JUNIOR COLLEGE, NIRA, TQ.PURANDAR, PUNE": "KILACHAND JR COLLEGE, NIRA",
    "MAHARSHI WALMIKI JUINOR COLLEGE,WAHLE,TQ.PURANDAR": "MAHARSHI WALMIKI JR COLLEGE, WAHLE",
    "PURANDAR JR.COLLEGE OF ARTS,SCIENCE,COMM, SASWAD": "PURANDAR JR COLLEGE, SASWAD",
    "ABDULBHAI CHANDBHAI HUNDEKARI JR.COLLEGE, JEJURI": "ABDULBHAI HUNDEKARI COLLEGE, JEJURI",
    "DR.SHANKARRAO KOLATE VIDYALAYA &JR.COLLEGE,PISARVE": "DR SHANKARRAO KOLATE COLLEGE, PISARVE",
    "M.E.S.WAGHIRE HIGH SCHOOL & JR.COLLEGE, SASWAD": "MES WAGHIRE JR COLLEGE, SASWAD",
    "SHRI.KEDARESHWAR VIDHYALAYA & JR.COLLEGE, KALDAREE": "SHRI KEDARESHWAR COLLEGE, KALDAREE",
    "JIJAMATA VIDHYALAYA, JEJURI TAL-PURANDAR DT PUNE": "JIJAMATA VIDYALAYA, JEJURI",
    "RISE-PISE SEC.& HIGHER SEC. SCHOOL, RISE, PURANDAR": "RISE-PISE COLLEGE, RISE",
    "SHREE SHIVAJI ENG.MEDIUM.SCHL.& JR COL.SASWAD,PUNE": "SHREE SHIVAJI ENGLISH MEDIUM COLLEGE, SASWAD",
    "MJPV AND SMK JR COL A/P SHIVARI TAL PURANDHAR": "MJPV & SMK JR COLLEGE, SHIVARI",
    "L R SHAHKANYA VIDYA MANDIR NIRA": "LR SHAHKANYA VIDYA MANDIR, NIRA",
    "WAGHIRE MAHAVIDY SASWAD": "WAGHIRE MAHAVIDYALAYA, SASWAD",
    "PURANDAR H SCH AND JR.COL": "PURANDAR HIGH SCHOOL & JR COLLEGE",
    "PANCHKROSHI SHETKARI TECHNICAL VIDY AND VYAVS": "PANCHKROSHI SHETKARI TECH COLLEGE"
}

df["Name of the college"] = df["Name of the college"].replace(college_mapping)

# ---------- Sidebar filters ----------
with st.sidebar:
    st.header("🔍 Filters")
    year = st.selectbox(
        "Select Year",
        sorted(df['Year'].unique()),
        index=len(df['Year'].unique()) - 1  # default = latest year
    )
    stream = st.selectbox(
        "Select Stream",
        sorted(df['Stream'].unique()),
        index=0  # or set to 1 for 'COMMERCE', etc.
    )

# ---------- Filter & prepare data ----------
filtered = df[(df['Year'] == year) & (df['Stream'] == stream)].copy()

if filtered.empty:
    st.warning(f"No data available for **{stream}** stream in **{year}**.")
    st.stop()

filtered['Pass_Label'] = filtered['Pass Percent'].apply(lambda x: f"{x:.1f}%")
filtered = filtered.sort_values('Pass Percent', ascending=False)

# ---------- Plotly chart ----------
fig = px.bar(
    filtered,
    x='Pass Percent',
    y='Name of the college',
    orientation='h',
    text='Pass_Label',
    title=f'{stream} Stream – Pass % ({year})',
    color='Pass Percent',
    color_continuous_scale='Blues',
    height=max(400, len(filtered) * 25)
)
fig.update_traces(textposition='outside', textfont_size=12)
fig.update_xaxes(range=[0, 105])
fig.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    margin=dict(l=300, r=100, t=100, b=80),
    yaxis_title='',
    xaxis_title='Pass Percentage (%)',
    font=dict(size=11),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ---------- Timeline: College Performance Over Years ----------
st.markdown("---")
st.subheader("📈 College Performance Timeline")

college = st.selectbox(
    "Select College for Timeline View",
    sorted(df[df['Stream'] == stream]['Name of the college'].unique()),
    key="college_selector"
)

college_timeline = df[(df['Name of the college'] == college) & (df['Stream'] == stream)].sort_values('Year')

if not college_timeline.empty:
    college_timeline = college_timeline.copy()
    college_timeline['Pass_Label'] = college_timeline['Pass Percent'].apply(lambda x: f"{x:.1f}%")
    col1, col2 = st.columns(2)
    
    with col1:
        # Timeline: Candidates Appeared vs Passed
        fig_timeline = px.line(
            college_timeline,
            x='Year',
            y=['Candidates Appeared', 'Total Pass'],
            markers=True,
            title=f'{college} ({stream}) – Appeared vs Passed Over Time',
            labels={'value': 'Count', 'variable': 'Category'},
            height=400
        )
        fig_timeline.update_traces(mode='lines+markers', hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Count: %{y}<extra></extra>')
        fig_timeline.update_xaxes(dtick=1)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Timeline: Pass Percentage Trend
        fig_pass_pct = px.line(
            college_timeline,
            x='Year',
            y='Pass Percent',
            text='Pass_Label',
            markers=True,
            title=f'{college} ({stream}) – Pass Percentage Trend',
            labels={'Pass Percent': 'Pass %'},
            height=400,
            line_shape='spline'
        )
        fig_pass_pct.update_traces(
            mode='lines+markers+text',
            textposition='top center',
            textfont_size=12,
            line_color='#1f77b4',
            marker_size=8,
            hovertemplate='Year: %{x}<br>Pass %: %{y:.1f}%<extra></extra>'
        )
        fig_pass_pct.update_xaxes(dtick=1)
        fig_pass_pct.update_yaxes(range=[0, 105])
        st.plotly_chart(fig_pass_pct, use_container_width=True)
    
    # Performance Table
    st.markdown("**Performance Details:**")
    display_cols = ['Year', 'Candidates Appeared', 'Total Pass', 'Pass Percent', 'Distin-ction', 'Grade I', 'Grade II']
    st.dataframe(college_timeline[display_cols].style.format({
        'Pass Percent': '{:.1f}%',
        'Candidates Appeared': '{:.0f}',
        'Total Pass': '{:.0f}'
    }), use_container_width=True)
else:
    st.info(f"No timeline data available for {college}.")

# ---------- Top Colleges by Average Pass % (Last 5 Years) ----------
st.markdown("---")

# Calculate dynamic year range (last 5 years)
max_year = df['Year'].max()
min_year = max_year - 4
years_range = list(range(min_year, max_year + 1))
year_range_str = f"{min_year}-{max_year}"

st.subheader(f"🏆 Top Colleges by Average Pass % ({year_range_str})")

# Filter data for last 5 years
avg_data = df[df['Year'].isin(years_range)].groupby(['Name of the college', 'Stream']).agg({
    'Pass Percent': 'mean',
    'Candidates Appeared': 'sum',
    'Total Pass': 'sum'
}).reset_index()
avg_data.columns = ['College', 'Stream', 'Avg Pass %', 'Total Appeared', 'Total Passed']
avg_data = avg_data.sort_values(['Stream', 'Avg Pass %'], ascending=[True, True])

# Display by stream in tabs
streams = sorted(avg_data['Stream'].unique())
tabs = st.tabs(streams)

for tab, stream_name in zip(tabs, streams):
    with tab:
        stream_data = avg_data[avg_data['Stream'] == stream_name].head(10)
        
        if not stream_data.empty:
            # Create visualization
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig_top = px.bar(
                    stream_data,
                    x='Avg Pass %',
                    y='College',
                    orientation='h',
                    title=f'Top Colleges – {stream_name} Stream',
                    color='Avg Pass %',
                    color_continuous_scale='blues',
                    height=400
                )
                fig_top.update_layout(
                    yaxis_title='',
                    xaxis_title=f'Average Pass % ({year_range_str})',
                    margin=dict(l=250, r=50, t=80, b=60),
                    xaxis=dict(range=[0, 105])
                )
                fig_top.update_traces(textposition='outside', texttemplate='%{x:.1f}%')
                st.plotly_chart(fig_top, use_container_width=True)
            
            with col2:
                st.markdown("**Summary:**")
                st.metric("Top College", stream_data.iloc[0]['College'][:30])
                st.metric("Avg Pass %", f"{stream_data.iloc[0]['Avg Pass %']:.1f}%")
                st.metric("Total Students", int(stream_data['Total Appeared'].sum()))
        else:
            st.info(f"No data available for {stream_name} stream")

# ---------- Optional: raw data table ----------
with st.expander("📋 Show raw data"):
    st.dataframe(filtered.drop(columns='Pass_Label'))
