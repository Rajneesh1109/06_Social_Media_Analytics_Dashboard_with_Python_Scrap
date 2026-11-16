"""
Project: 06_Social_Media_Analytics_Dashboard_with_Python_Scrap
Module: app.py
Author: Rajneesh Chaubey (ABES Engineering College)
GitHub: https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap
Description: Streamlit interactive analytics dashboard providing real-time multi-platform
             visualizations, KPI scorecards, sentiment analysis, and data filtering.
"""

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Social Media Analytics Dashboard | Python Scraping",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-lbl {
        color: #64748B;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- DATA LOADER -----------------
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "dataset.csv")
    if not os.path.exists(file_path):
        file_path = "dataset.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['post_timestamp'] = pd.to_datetime(df['post_timestamp'])
        return df
    else:
        st.error(f"Dataset file not found at {file_path}. Please run scraper.py first.")
        return pd.DataFrame()

df = load_data()

# ----------------- HEADER -----------------
st.markdown('<div class="main-header">📈 Social Media Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">'
    '<b>Project:</b> 06_Social_Media_Analytics_Dashboard_with_Python_Scrap | '
    '<b>Candidate:</b> Rajneesh Chaubey (ABES Engineering College) | '
    '<a href="https://github.com/Rajneesh1109/06_Social_Media_Analytics_Dashboard_with_Python_Scrap" target="_blank">'
    '🔗 GitHub Repository</a>'
    '</div>',
    unsafe_allow_html=True
)

if df.empty:
    st.warning("No data available to display.")
    st.stop()

# ----------------- SIDEBAR FILTERS -----------------
st.sidebar.header("🔍 Filters & Controls")

# Platform Filter
platforms = ["All Platforms"] + sorted(list(df['platform'].unique()))
selected_platform = st.sidebar.selectbox("Select Social Platform", platforms)

# Sentiment Filter
sentiments = ["All Sentiments"] + sorted(list(df['sentiment_category'].unique()))
selected_sentiment = st.sidebar.selectbox("Filter by Sentiment", sentiments)

# Content Type Filter
content_types = ["All Types"] + sorted(list(df['content_type'].unique()))
selected_type = st.sidebar.selectbox("Content Media Type", content_types)

# Date Filter
min_date = df['post_timestamp'].min().date()
max_date = df['post_timestamp'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Apply Filters
filtered_df = df.copy()
if selected_platform != "All Platforms":
    filtered_df = filtered_df[filtered_df['platform'] == selected_platform]
if selected_sentiment != "All Sentiments":
    filtered_df = filtered_df[filtered_df['sentiment_category'] == selected_sentiment]
if selected_type != "All Types":
    filtered_df = filtered_df[filtered_df['content_type'] == selected_type]
if len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df['post_timestamp'].dt.date >= start_d) & 
        (filtered_df['post_timestamp'].dt.date <= end_d)
    ]

# ----------------- KPI METRICS ROW -----------------
col1, col2, col3, col4, col5 = st.columns(5)

total_posts = len(filtered_df)
total_views = filtered_df['views_count'].sum() if total_posts > 0 else 0
total_likes = filtered_df['likes_count'].sum() if total_posts > 0 else 0
avg_eng_rate = filtered_df['engagement_rate'].mean() if total_posts > 0 else 0.0
pos_percent = (len(filtered_df[filtered_df['sentiment_category'] == 'Positive']) / total_posts * 100) if total_posts > 0 else 0.0

with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-lbl">Total Posts</div><div class="metric-val">{total_posts:,}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-lbl">Total Impressions</div><div class="metric-val">{total_views:,}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-lbl">Total Likes</div><div class="metric-val">{total_likes:,}</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-lbl">Avg Engagement</div><div class="metric-val">{avg_eng_rate:.2f}%</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><div class="metric-lbl">Positive Sentiment</div><div class="metric-val">{pos_percent:.1f}%</div></div>', unsafe_allow_html=True)

st.write("")

# ----------------- CHARTS ROW 1 -----------------
ch_col1, ch_col2 = st.columns(2)

with ch_col1:
    st.subheader("🎯 Sentiment Distribution")
    sentiment_counts = filtered_df['sentiment_category'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentiment', 'Count']
    color_map = {'Positive': '#10B981', 'Neutral': '#64748B', 'Negative': '#EF4444'}
    fig_sent = px.pie(
        sentiment_counts, 
        names='Sentiment', 
        values='Count', 
        hole=0.45,
        color='Sentiment',
        color_discrete_map=color_map
    )
    fig_sent.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_sent, use_container_width=True)

with ch_col2:
    st.subheader("📊 Average Engagement Rate by Platform")
    platform_eng = filtered_df.groupby('platform')['engagement_rate'].mean().reset_index().sort_values(by='engagement_rate', ascending=False)
    fig_eng = px.bar(
        platform_eng, 
        x='platform', 
        y='engagement_rate', 
        labels={'platform': 'Social Platform', 'engagement_rate': 'Avg Engagement Rate (%)'},
        color='engagement_rate',
        color_continuous_scale='Blues'
    )
    fig_eng.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_eng, use_container_width=True)

# ----------------- CHARTS ROW 2 -----------------
ch_col3, ch_col4 = st.columns(2)

with ch_col3:
    st.subheader("📅 Engagement Trends Over Time")
    daily_trend = filtered_df.groupby(filtered_df['post_timestamp'].dt.date).agg({
        'likes_count': 'sum',
        'comments_count': 'sum',
        'shares_count': 'sum'
    }).reset_index()
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=daily_trend['post_timestamp'], y=daily_trend['likes_count'], name='Likes', mode='lines+markers', line=dict(color='#3B82F6', width=2)))
    fig_trend.add_trace(go.Scatter(x=daily_trend['post_timestamp'], y=daily_trend['comments_count'], name='Comments', mode='lines+markers', line=dict(color='#10B981', width=2)))
    fig_trend.add_trace(go.Scatter(x=daily_trend['post_timestamp'], y=daily_trend['shares_count'], name='Shares', mode='lines+markers', line=dict(color='#F59E0B', width=2)))
    fig_trend.update_layout(margin=dict(t=20, b=20, l=20, r=20), xaxis_title="Post Date", yaxis_title="Total Interactions")
    st.plotly_chart(fig_trend, use_container_width=True)

with ch_col4:
    st.subheader("🏷️ Top Hashtag Frequencies")
    all_tags = []
    for tags in filtered_df['hashtags'].dropna():
        for t in tags.split(','):
            cleaned_tag = t.strip()
            if cleaned_tag and cleaned_tag != 'None':
                all_tags.append(cleaned_tag)
    tag_df = pd.Series(all_tags).value_counts().head(8).reset_index()
    tag_df.columns = ['Hashtag', 'Frequency']
    fig_tags = px.bar(
        tag_df,
        x='Frequency',
        y='Hashtag',
        orientation='h',
        color='Frequency',
        color_continuous_scale='Tealgrn'
    )
    fig_tags.update_layout(margin=dict(t=20, b=20, l=20, r=20), yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_tags, use_container_width=True)

# ----------------- DATA TABLE -----------------
st.subheader("📋 Scraped Records Data Explorer")
display_cols = ['post_id', 'platform', 'author_username', 'post_text', 'engagement_rate', 'sentiment_category', 'likes_count', 'views_count']
st.dataframe(filtered_df[display_cols].head(50), use_container_width=True)

# CSV Download Button
csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Dataset (CSV)",
    data=csv_data,
    file_name="filtered_social_media_analytics.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Developed by Rajneesh Chaubey | Defense & Full-Stack Engineering | ABES Engineering College")
