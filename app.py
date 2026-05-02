import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------- Page config ----------
st.set_page_config(page_title="HSC College Comparison", layout="wide")
st.markdown("""
<style>
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #1f77b4;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)
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
    "KARMAVEER BABURAO PATIL JUNIOR COLLEGE, PARINCHE": "KARMAVEER BABURAO PATIL Clg",
    "WAGHIRE COLLEGE OF ARTS,COME & SCIENCE, SASWAD": "WAGHIRE Clg, SASWAD",
    "KILACHAND JUNIOR COLLEGE, NIRA, TQ.PURANDAR, PUNE": "KILACHAND JR Clg, NIRA",
    "MAHARSHI WALMIKI JUINOR COLLEGE,WAHLE,TQ.PURANDAR": "MAHARSHI WALMIKI JR Clg, WAHLE",
    "PURANDAR JR.COLLEGE OF ARTS,SCIENCE,COMM, SASWAD": "PURANDAR JR Clg, SASWAD",
    "ABDULBHAI CHANDBHAI HUNDEKARI JR.COLLEGE, JEJURI": "ABDULBHAI HUNDEKARI Clg, JEJURI",
    "DR.SHANKARRAO KOLATE VIDYALAYA &JR.COLLEGE,PISARVE": "DR SHANKARRAO KOLATE Clg, PISARVE",
    "M.E.S.WAGHIRE HIGH SCHOOL & JR.COLLEGE, SASWAD": "MES WAGHIRE JR Clg, SASWAD",
    "SHRI.KEDARESHWAR VIDHYALAYA & JR.COLLEGE, KALDAREE": "SHRI KEDARESHWAR Clg, KALDAREE",
    "JIJAMATA VIDHYALAYA, JEJURI TAL-PURANDAR DT PUNE": "JIJAMATA VIDYALAYA, JEJURI",
    "RISE-PISE SEC.& HIGHER SEC. SCHOOL, RISE, PURANDAR": "RISE-PISE Clg, RISE",
    "SHREE SHIVAJI ENG.MEDIUM.SCHL.& JR COL.SASWAD,PUNE": "SHREE SHIVAJI ENGLISH MEDIUM Clg",
    "MJPV AND SMK JR COL A/P SHIVARI TAL PURANDHAR": "MJPV & SMK JR Clg, SHIVARI",
    "L R SHAHKANYA VIDYA MANDIR NIRA": "LR SHAHKANYA VIDYA MANDIR, NIRA",
    "WAGHIRE MAHAVIDY SASWAD": "WAGHIRE MAHAVIDYALAYA, SASWAD",
    "PURANDAR H SCH AND JR.COL": "PURANDAR HIGH SCHOOL & JR Clg",
    "PANCHKROSHI SHETKARI TECHNICAL VIDY AND VYAVS": "PANCHKROSHI SHETKARI TECH Clg"
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
    title=f'{stream} Stream – Top Colleges performance In Purandar Taluka ({year})',
    color='Pass Percent',
    color_continuous_scale='Blues',
    height=max(400, len(filtered) * 25)
)
fig.update_traces(textposition='outside', textfont=dict(size=16, family='Arial Black'))
fig.update_xaxes(range=[0, 105], showgrid=True, gridwidth=1, gridcolor='lightgray', 
                 title_font=dict(size=18, family='Arial Black'))
fig.update_layout(
    yaxis=dict(categoryorder='total ascending', tickfont=dict(size=16, family='Arial Black')),
    margin=dict(l=300, r=100, t=100, b=80),
    yaxis_title='',
    xaxis_title='Pass Percentage (%)',
    font=dict(size=16, family='Arial Black'),
    title_font=dict(size=20, family='Arial Black'),
    showlegend=False,
    hovermode='closest'
)
config = {
    'toImageButtonOptions': {
        'format': 'png',
        'filename': f'{stream}_{year}_colleges_comparison',
        'height': max(800, len(filtered) * 50),
        'width': 1920,
        'scale': 3
    }
}

st.plotly_chart(fig, use_container_width=True, config=config)

# ---------- Timeline: College Performance Over Years ----------
st.markdown("---")
st.markdown("<h2 style='color: #1f77b4;'>📈 College Performance Timeline</h2>", unsafe_allow_html=True)

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
        fig_timeline.update_xaxes(dtick=1, showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
        fig_timeline.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
        fig_timeline.update_layout(hovermode='closest',
                                   font=dict(size=14, family='Arial Black'),
                                   title_font=dict(size=18, family='Arial Black'),
                                   legend=dict(font=dict(size=14, family='Arial Black')))
        config_timeline = {
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'{college}_{stream}_timeline',
                'height': 800,
                'width': 1600,
                'scale': 3
            }
        }
        st.plotly_chart(fig_timeline, use_container_width=True, config=config_timeline)
    
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
            textfont=dict(size=16, family='Arial Black'),
            line_color='#1f77b4',
            marker_size=10,
            hovertemplate='Year: %{x}<br>Pass %: %{y:.1f}%<extra></extra>'
        )
        fig_pass_pct.update_xaxes(dtick=1, showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
        fig_pass_pct.update_yaxes(range=[0, 105], showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
        fig_pass_pct.update_layout(hovermode='closest',
                                   font=dict(size=14, family='Arial Black'),
                                   title_font=dict(size=18, family='Arial Black'))
        config_pass_pct = {
            'toImageButtonOptions': {
                'format': 'png',
                'filename': f'{college}_{stream}_pass_percentage_trend',
                'height': 800,
                'width': 1600,
                'scale': 3
            }
        }
        st.plotly_chart(fig_pass_pct, use_container_width=True, config=config_pass_pct)
    
    # Performance Table
    st.markdown("**📋 Performance Details:**")
    display_cols = ['Year', 'Candidates Appeared', 'Total Pass', 'Pass Percent', 'Distin-ction', 'Grade I', 'Grade II']
    styled_df = college_timeline[display_cols].style.format({
        'Pass Percent': '{:.1f}%',
        'Candidates Appeared': '{:.0f}',
        'Total Pass': '{:.0f}'
    }).background_gradient(subset=['Pass Percent'], cmap='Blues')
    st.dataframe(styled_df, use_container_width=True)
else:
    st.info(f"No timeline data available for {college}.")

# ---------- All Colleges Pass Percentage Trend ----------
st.markdown("---")
st.markdown("<h2 style='color: #1f77b4;'>📊 All Colleges Pass Percentage Trend</h2>", unsafe_allow_html=True)

all_colleges_trend = df[df['Stream'] == stream].sort_values('Year')

if not all_colleges_trend.empty:
    fig_all_colleges = px.line(
        all_colleges_trend,
        x='Year',
        y='Pass Percent',
        color='Name of the college',
        markers=True,
        title=f'{stream} Stream – All Colleges Pass Percentage Trend',
        labels={'Pass Percent': 'Pass %', 'Name of the college': 'College'},
        height=500
    )
    fig_all_colleges.update_xaxes(dtick=1, showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
    fig_all_colleges.update_yaxes(range=[0, 105], showgrid=True, gridwidth=1, gridcolor='lightgray',
                                  title_font=dict(size=16, family='Arial Black'),
                                  tickfont=dict(size=14, family='Arial Black'))
    fig_all_colleges.update_layout(yaxis=dict(tickfont=dict(size=14, family='Arial Black')), 
                                   hovermode='closest',
                                   font=dict(size=14, family='Arial Black'),
                                   title_font=dict(size=18, family='Arial Black'),
                                   legend=dict(font=dict(size=14, family='Arial Black')))
    fig_all_colleges.update_traces(hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Pass %: %{y:.1f}%<extra></extra>',
                                   marker_size=8)
    config_all_colleges = {
        'toImageButtonOptions': {
            'format': 'png',
            'filename': f'{stream}_all_colleges_trend',
            'height': 1000,
            'width': 1920,
            'scale': 3
        }
    }
    st.plotly_chart(fig_all_colleges, use_container_width=True, config=config_all_colleges)
else:
    st.info(f"No data available for {stream} stream")

# ---------- Top Colleges by Average Pass % (Last 5 Years) ----------
st.markdown("---")

# Calculate dynamic year range (last 5 years)
max_year = df['Year'].max()
min_year = max_year - 4
years_range = list(range(min_year, max_year + 1))
year_range_str = f"{min_year}-{max_year}"

st.markdown(f"<h2 style='color: #1f77b4;'>🏆 Top Colleges by Average Pass % ({year_range_str})</h2>", unsafe_allow_html=True)

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
        stream_data = avg_data[avg_data['Stream'] == stream_name]
        
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
                    yaxis=dict(tickfont=dict(size=16, family='Arial Black')),
                    yaxis_title='',
                    xaxis_title=f'Average Pass % ({year_range_str})',
                    margin=dict(l=250, r=50, t=80, b=60),
                    xaxis=dict(range=[0, 105], showgrid=True, gridwidth=1, gridcolor='lightgray',
                              title_font=dict(size=16, family='Arial Black'),
                              tickfont=dict(size=14, family='Arial Black')),
                    hovermode='closest',
                    font=dict(size=14, family='Arial Black'),
                    title_font=dict(size=18, family='Arial Black')
                )
                fig_top.update_traces(textposition='outside', texttemplate='%{x:.1f}%',
                                     textfont=dict(size=16, family='Arial Black'))
                config_top = {
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'{stream_name}_top_colleges_{year_range_str}',
                        'height': 800,
                        'width': 1920,
                        'scale': 3
                    }
                }
                st.plotly_chart(fig_top, use_container_width=True, config=config_top)
            
            with col2:
                st.markdown("**Summary:**")
                top_college = stream_data.iloc[0]
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                with col_metric1:
                    st.metric("🏆 Top College", top_college['College'][:25], delta=None)
                with col_metric2:
                    st.metric("📊 Avg Pass %", f"{top_college['Avg Pass %']:.1f}%", delta=None)
                with col_metric3:
                    st.metric("👥 Total Students", int(stream_data['Total Appeared'].sum()), delta=None)
        else:
            st.info(f"No data available for {stream_name} stream")

# ---------- Optional: raw data table ----------
st.markdown("---")
with st.expander("📋 Show raw data"):
    st.dataframe(filtered.drop(columns='Pass_Label'), use_container_width=True)
