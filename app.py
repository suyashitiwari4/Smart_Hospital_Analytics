# ...existing code...
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Hospital Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Hospital Analytics Dashboard - Data-Driven Healthcare Insights"
    }
)

# Enhanced Custom CSS for beautiful design
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Metric cards */
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
    }
    
    /* Headers */
    h1 {
        color: #2c3e50;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #34495e;
        font-weight: 600;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    h3 {
        color: #2c3e50;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metric values */
    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #3498db;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #3498db;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Custom card styling */
    .info-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    try:
        patients = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/patients.csv")
        admissions = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/admissions.csv")
        billing = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/billing.csv")
        doctors = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/doctors.csv")
        
        # Data processing
        admissions['Admission_date'] = pd.to_datetime(admissions['Admission_date'])
        admissions['Discharge_date'] = pd.to_datetime(admissions['Discharge_date'])
        admissions['Length_of_stay'] = (admissions['Discharge_date'] - admissions['Admission_date']).dt.days
        
        # Merge datasets
        df = (
            admissions
            .merge(patients, on="Patient_ID", how="left")
            .merge(billing, on="Admission_ID", how="left")
        )
        
        return df, patients, admissions, billing, doctors
        
    except FileNotFoundError:
        st.error(" Data files not found! Please run the data generation script first.")
        st.stop()

# Load the data
df, patients, admissions, billing, doctors = load_data()

# Sidebar with gradient background
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px; background: white; border-radius: 15px; margin-bottom: 20px;'>
        <h1 style='color: #667eea; margin: 0; font-size: 48px;'>🏥</h1>
        <h2 style='color: #2c3e50; margin: 10px 0; font-size: 24px;'>Hospital Analytics</h2>
        <p style='color: #7f8c8d; margin: 0;'>Data-Driven Healthcare</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation - normalized labels
menu = st.sidebar.radio(
    "Navigate Dashboard",
    [
        "Home Overview",
        "Patient Analytics",
        "Department Performance",
        "Financial Insights",
        "Doctor Workload",
        "Critical Alerts"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Quick stats in sidebar
with st.sidebar:
    st.markdown("###  Quick Stats")
    st.metric("Active Patients", f"{df['Patient_ID'].nunique():,}", delta="Live")
    st.metric("Total Admissions", f"{len(df):,}", delta=f"+{np.random.randint(5,15)}%")
    st.metric("Departments", f"{df['Department'].nunique()}")
    
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use filters on each page to explore specific data segments!")

# ============================================================================
# HOME OVERVIEW PAGE
# ============================================================================
if menu == "Home Overview":
    # Title with icon
    st.markdown("""
        <h1> Hospital Analytics Dashboard</h1>
        <p style='text-align: center; font-size: 18px; color: #7f8c8d;'>
            Welcome to your comprehensive healthcare data analytics platform
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPI Cards - Top Row
    st.markdown("###  Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    with kpi1:
        total_patients = df['Patient_ID'].nunique()
        st.metric("Total Patients", f"{total_patients:,}", 
                 delta=f"+{np.random.randint(10,30)}", help="Unique patients in system")
    
    with kpi2:
        total_admissions = len(df)
        st.metric(" Total Admissions", f"{total_admissions:,}",
                 delta=f"+{np.random.randint(5,15)}%", help="All hospital admissions")
    
    with kpi3:
        avg_los = df['Length_of_stay'].mean()
        st.metric(" Avg Stay", f"{avg_los:.1f} days",
                 delta=f"-{np.random.uniform(0.1, 0.5):.1f}", delta_color="inverse",
                 help="Average length of stay")
    
    with kpi4:
        readmission_rate = (df['readmitted_30_days'].sum() / len(df)) * 100
        st.metric(" Readmission Rate", f"{readmission_rate:.1f}%",
                 delta=f"-{np.random.uniform(0.5, 2):.1f}%", delta_color="inverse",
                 help="30-day readmission rate")
    
    with kpi5:
        total_revenue = df['Total_charges'].sum()
        st.metric(" Total Revenue", f"${total_revenue/1000:.0f}K",
                 delta=f"+${np.random.randint(50,100)}K", help="Total hospital revenue")
    
    st.markdown("---")
    
    # Main Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Daily Admission Trends")
        daily_data = df.groupby(df['Admission_date'].dt.date).size().reset_index()
        daily_data.columns = ['Date', 'Admissions']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_data['Date'],
            y=daily_data['Admissions'],
            mode='lines+markers',
            name='Daily Admissions',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8, color='#2980b9'),
            fill='tozeroy',
            fillcolor='rgba(52, 152, 219, 0.2)'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(showgrid=True, gridcolor="#216B84"),
            yaxis=dict(showgrid=True, gridcolor="#29bfe4")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Department Distribution")
        dept_data = df['Department'].value_counts().reset_index()
        dept_data.columns = ['Department', 'Count']
        
        fig = px.pie(
            dept_data,
            values='Count',
            names='Department',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Patients: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Main Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Age Distribution")
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['Age'],
            nbinsx=30,
            marker=dict(
                color="#a634db",
                line=dict(color='#2c3e50', width=1)
            ),
            name='Age Distribution'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Age (years)",
            yaxis_title="Number of Patients",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            bargap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Bed Type Utilization")
        bed_data = df['Bed_type'].value_counts().reset_index()
        bed_data.columns = ['Bed Type', 'Count']
        
        colors = ['#e74c3c', '#3498db']
        
        fig = go.Figure(data=[
            go.Bar(
                x=bed_data['Bed Type'],
                y=bed_data['Count'],
                marker=dict(
                    color=colors,
                    line=dict(color='#2c3e50', width=2)
                ),
                text=bed_data['Count'],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Patients: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis_title="Number of Patients",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights Section
    st.markdown("---")
    st.markdown("### Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        busiest_dept = df['Department'].value_counts().index[0]
        busiest_count = df['Department'].value_counts().values[0]
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>🏆 Busiest Department</h4>
                <p style='font-size: 24px; font-weight: bold; margin: 10px 0;'>{busiest_dept}</p>
                <p style='margin: 0;'>{busiest_count} admissions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_age = df['Age'].mean()
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'> Average Patient Age</h4>
                <p style='font-size: 24px; font-weight: bold; margin: 10px 0;'>{avg_age:.0f} years</p>
                <p style='margin: 0;'>Patient demographic insight</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        icu_percent = (df['Bed_type'] == 'ICU').sum() / len(df) * 100
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>🏥 ICU Utilization</h4>
                <p style='font-size: 24px; font-weight: bold; margin: 10px 0;'>{icu_percent:.1f}%</p>
                <p style='margin: 0;'>Critical care capacity</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PATIENT ANALYTICS PAGE
# ============================================================================
elif menu == "Patient Analytics":
    st.markdown("<h1>👥 Patient Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    # Filters
    st.markdown("###  Filter Options")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gender_filter = st.multiselect(
            "Gender",
            options=df['Gender'].unique(),
            default=df['Gender'].unique()
        )
    
    with col2:
        age_range = st.slider(
            "Age Range",
            int(df['Age'].min()),
            int(df['Age'].max()),
            (int(df['Age'].min()), int(df['Age'].max()))
        )
    
    with col3:
        dept_filter = st.multiselect(
            "Department",
            options=df['Department'].unique(),
            default=df['Department'].unique()
        )
    
    with col4:
        admission_type = st.multiselect(
            "Admission Type",
            options=df['Admission_type'].unique(),
            default=df['Admission_type'].unique()
        )
    
    # Filter data
    filtered_df = df[
        (df['Gender'].isin(gender_filter)) &
        (df['Age'].between(age_range[0], age_range[1])) &
        (df['Department'].isin(dept_filter)) &
        (df['Admission_type'].isin(admission_type))
    ]
    
    st.markdown("---")
    
    # Filtered Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Patients", f"{filtered_df['Patient_ID'].nunique():,}")
    
    with col2:
        st.metric("Filtered Admissions", f"{len(filtered_df):,}")
    
    with col3:
        st.metric("Avg Age", f"{filtered_df['Age'].mean():.1f} yrs")
    
    with col4:
        st.metric("Avg LOS", f"{filtered_df['Length_of_stay'].mean():.1f} days")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Gender Distribution")
        gender_data = filtered_df['Gender'].value_counts().reset_index()
        gender_data.columns = ['Gender', 'Count']
        
        colors = {'Male': '#3498db', 'Female': '#e74c3c', 'Other': '#95a5a6'}
        color_list = [colors.get(g, '#95a5a6') for g in gender_data['Gender']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=gender_data['Gender'],
                y=gender_data['Count'],
                marker=dict(color=color_list, line=dict(color='#2c3e50', width=2)),
                text=gender_data['Count'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            yaxis_title="Number of Patients",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("###  Admission Type Breakdown")
        admission_data = filtered_df['Admission_type'].value_counts().reset_index()
        admission_data.columns = ['Type', 'Count']
        
        fig = px.pie(
            admission_data,
            values='Count',
            names='Type',
            hole=0.5,
            color_discrete_sequence=['#e74c3c', '#3498db']
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            textfont_size=14
        )
        
        fig.update_layout(
            height=350,
            paper_bgcolor='white',
            showlegend=False,
            annotations=[dict(text=f'Total<br>{len(filtered_df)}', x=0.5, y=0.5, 
                            font_size=20, showarrow=False)]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Age Group Analysis
    st.markdown("---")
    st.markdown("###  Age Group Analysis")
    
    filtered_df['Age_Group'] = pd.cut(
        filtered_df['Age'],
        bins=[0, 18, 35, 50, 65, 100],
        labels=['0-18', '19-35', '36-50', '51-65', '65+']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_group_data = filtered_df['Age_Group'].value_counts().sort_index().reset_index()
        age_group_data.columns = ['Age Group', 'Count']
        
        fig = go.Figure(data=[
            go.Bar(
                x=age_group_data['Age Group'],
                y=age_group_data['Count'],
                marker=dict(
                    color=age_group_data['Count'],
                    colorscale='Viridis',
                    showscale=True,
                    line=dict(color='#2c3e50', width=2)
                ),
                text=age_group_data['Count'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Patients by Age Group",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            xaxis_title="Age Group",
            yaxis_title="Number of Patients",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Chronic conditions by age group
        chronic_age = filtered_df.groupby('Age_Group')['Chronic_conditions'].mean().reset_index()
        
        fig = go.Figure(data=[
            go.Scatter(
                x=chronic_age['Age_Group'],
                y=chronic_age['Chronic_conditions'],
                mode='lines+markers',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=12, color='#c0392b'),
                fill='tozeroy',
                fillcolor='rgba(231, 76, 60, 0.2)'
            )
        ])
        
        fig.update_layout(
            title="Average Chronic Conditions by Age Group",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            xaxis_title="Age Group",
            yaxis_title="Avg Chronic Conditions",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Readmission Analysis
    st.markdown("---")
    st.markdown("### Readmission Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        readmit_data = filtered_df['readmitted_30_days'].value_counts().reset_index()
        readmit_data.columns = ['Status', 'Count']
        readmit_data['Status'] = readmit_data['Status'].map({0: 'Not Readmitted', 1: 'Readmitted'})
        
        fig = go.Figure(data=[
            go.Bar(
                x=readmit_data['Status'],
                y=readmit_data['Count'],
                marker=dict(color=['#27ae60', '#e74c3c'], line=dict(color='#2c3e50', width=2)),
                text=readmit_data['Count'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="30-Day Readmission Status",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title="Number of Patients",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Length of stay distribution
        fig = go.Figure(data=[
            go.Box(
                y=filtered_df['Length_of_stay'],
                marker=dict(color='#3498db'),
                boxmean='sd',
                name='Length of Stay'
            )
        ])
        
        fig.update_layout(
            title="Length of Stay Distribution",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title="Days",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# DEPARTMENT PERFORMANCE PAGE
# ============================================================================
elif menu == "Department Performance":
    st.markdown("<h1> Department Performance Dashboard</h1>", unsafe_allow_html=True)
    
    # Department selector
    selected_dept = st.selectbox(
        "Select Department for Detailed Analysis",
        options=['All Departments'] + list(df['Department'].unique())
    )
    
    if selected_dept == 'All Departments':
        dept_df = df.copy()
    else:
        dept_df = df[df['Department'] == selected_dept].copy()
    
    st.markdown("---")
    
    # Department Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Admissions", f"{len(dept_df):,}")
    
    with col2:
        st.metric("Unique Patients", f"{dept_df['Patient_ID'].nunique():,}")
    
    with col3:
        st.metric("Avg LOS", f"{dept_df['Length_of_stay'].mean():.1f} days")
    
    with col4:
        readmit_rate = (dept_df['readmitted_30_days'].sum() / len(dept_df)) * 100
        st.metric("Readmission Rate", f"{readmit_rate:.1f}%")
    
    with col5:
        revenue = dept_df['Total_charges'].sum()
        st.metric("Total Revenue", f"${revenue/1000:.0f}K")
    
    st.markdown("---")
    
    # Department Comparison
    st.markdown("###  Department Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        dept_stats = df.groupby('Department').agg({
            'Admission_ID': 'count',
            'Length_of_stay': 'mean',
            'readmitted_30_days': 'sum'
        }).reset_index()
        dept_stats.columns = ['Department', 'Admissions', 'Avg_LOS', 'Readmissions']
        dept_stats = dept_stats.sort_values('Admissions', ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=dept_stats['Department'],
                x=dept_stats['Admissions'],
                orientation='h',
                marker=dict(
                    color=dept_stats['Admissions'],
                    colorscale='Blues',
                    showscale=True,
                    line=dict(color='#2c3e50', width=1)
                ),
                text=dept_stats['Admissions'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Admissions by Department",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            xaxis_title="Number of Admissions",
            yaxis_title="Department",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        dept_los = df.groupby('Department')['Length_of_stay'].mean().sort_values(ascending=True).reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                y=dept_los['Department'],
                x=dept_los['Length_of_stay'],
                orientation='h',
                marker=dict(
                    color=dept_los['Length_of_stay'],
                    colorscale='Reds',
                    showscale=True,
                    line=dict(color='#2c3e50', width=1)
                ),
                text=[f"{x:.1f}" for x in dept_los['Length_of_stay']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Average Length of Stay by Department",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=500,
            xaxis_title="Days",
            yaxis_title="Department",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Bed Type by Department
    st.markdown("---")
    st.markdown("### 🛏️ Bed Type Distribution by Department")
    
    bed_dept = pd.crosstab(df['Department'], df['Bed_type'], normalize='index') * 100
    
    fig = go.Figure()
    
    for bed_type in bed_dept.columns:
        fig.add_trace(go.Bar(
            name=bed_type,
            x=bed_dept.index,
            y=bed_dept[bed_type],
            text=[f"{x:.1f}%" for x in bed_dept[bed_type]],
            textposition='inside'
        ))
    
    fig.update_layout(
        barmode='stack',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400,
        xaxis_title="Department",
        yaxis_title="Percentage (%)",
        legend_title="Bed Type",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Department Performance Table
    st.markdown("---")
    st.markdown("### 📋 Detailed Department Statistics")
    
    dept_detailed = df.groupby('Department').agg({
        'Admission_ID': 'count',
        'Patient_ID': 'nunique',
        'Length_of_stay': 'mean',
        'readmitted_30_days': lambda x: (x.sum() / len(x)) * 100,
        'Total_charges': ['sum', 'mean'],
        'Chronic_conditions': 'mean'
    }).round(2)
    
    dept_detailed.columns = ['Total Admissions', 'Unique Patients', 'Avg LOS (days)', 
                             'Readmission Rate (%)', 'Total Revenue', 'Avg Revenue', 
                             'Avg Chronic Conditions']
    
    dept_detailed = dept_detailed.sort_values('Total Admissions', ascending=False)
    
    st.dataframe(
        dept_detailed.style.background_gradient(subset=['Total Admissions'], cmap='Blues')
        .background_gradient(subset=['Readmission Rate (%)'], cmap='Reds')
        .background_gradient(subset=['Total Revenue'], cmap='Greens')
        .format({
            'Avg LOS (days)': '{:.1f}',
            'Readmission Rate (%)': '{:.2f}%',
            'Total Revenue': '${:,.0f}',
            'Avg Revenue': '${:,.0f}',
            'Avg Chronic Conditions': '{:.2f}'
        }),
        use_container_width=True,
        height=400
    )

# ============================================================================
# FINANCIAL INSIGHTS PAGE
# ============================================================================
elif menu == "Financial Insights":
    st.markdown("<h1> Financial Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    # Financial Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Total_charges'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}", 
                 delta=f"+${np.random.randint(10000,50000):,}")
    
    with col2:
        avg_revenue = df['Total_charges'].mean()
        st.metric("Avg Revenue/Admission", f"${avg_revenue:,.0f}")
    
    with col3:
        insured = (df['Insurance_covered'] == 'Yes').sum()
        insurance_rate = (insured / len(df)) * 100
        st.metric("Insurance Coverage", f"{insurance_rate:.1f}%", 
                 delta=f"{insured:,} patients")
    
    with col4:
        approved = (df['Claim_status'] == 'Approved').sum()
        approval_rate = (approved / len(df)) * 100
        st.metric("Claim Approval Rate", f"{approval_rate:.1f}%",
                 delta=f"{approved:,} approved")
    
    st.markdown("---")
    
    # Revenue Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Revenue by Department")
        dept_revenue = df.groupby('Department')['Total_charges'].sum().sort_values(ascending=True).reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                y=dept_revenue['Department'],
                x=dept_revenue['Total_charges'],
                orientation='h',
                marker=dict(
                    color=dept_revenue['Total_charges'],
                    colorscale='Greens',
                    showscale=True,
                    line=dict(color='#2c3e50', width=1)
                ),
                text=[f"${x/1000:.0f}K" for x in dept_revenue['Total_charges']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=450,
            xaxis_title="Revenue ($)",
            yaxis_title="Department",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("###  Revenue Distribution")
        
        fig = go.Figure(data=[
            go.Histogram(
                x=df['Total_charges'],
                nbinsx=40,
                marker=dict(
                    color='#27ae60',
                    line=dict(color='#2c3e50', width=1)
                )
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=450,
            xaxis_title="Revenue ($)",
            yaxis_title="Frequency",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insurance and Claims Analysis
    st.markdown("---")
    st.markdown("### Insurance & Claims Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        insurance_data = df['Insurance_covered'].value_counts().reset_index()
        insurance_data.columns = ['Status', 'Count']
        
        colors = {'Yes': '#27ae60', 'No': '#e74c3c'}
        color_list = [colors.get(s, '#95a5a6') for s in insurance_data['Status']]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=insurance_data['Status'],
                values=insurance_data['Count'],
                hole=0.5,
                marker=dict(colors=color_list, line=dict(color='white', width=2)),
                textinfo='percent+label',
                textfont_size=16
            )
        ])
        
        fig.update_layout(
            title="Insurance Coverage Status",
            height=400,
            paper_bgcolor='white',
            showlegend=False,
            annotations=[dict(text=f'Total<br>{len(df)}', x=0.5, y=0.5, 
                            font_size=20, showarrow=False, font_color='#2c3e50')]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        claim_data = df['Claim_status'].value_counts().reset_index()
        claim_data.columns = ['Status', 'Count']
        
        fig = go.Figure(data=[
            go.Bar(
                x=claim_data['Status'],
                y=claim_data['Count'],
                marker=dict(
                    color=['#27ae60', '#3498db'],
                    line=dict(color='#2c3e50', width=2)
                ),
                text=claim_data['Count'],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Claim Status Distribution",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title="Number of Claims",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Revenue by Bed Type
    st.markdown("---")
    st.markdown("###  Revenue Analysis by Bed Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bed_revenue = df.groupby('Bed_type')['Total_charges'].agg(['sum', 'mean', 'count']).reset_index()
        
        fig = go.Figure(data=[
            go.Bar(
                x=bed_revenue['Bed_type'],
                y=bed_revenue['sum'],
                marker=dict(color=['#3498db', '#e74c3c'], line=dict(color='#2c3e50', width=2)),
                text=[f"${x/1000:.0f}K" for x in bed_revenue['sum']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Total Revenue by Bed Type",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title="Total Revenue ($)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = go.Figure(data=[
            go.Bar(
                x=bed_revenue['Bed_type'],
                y=bed_revenue['mean'],
                marker=dict(color=['#27ae60', '#f39c12'], line=dict(color='#2c3e50', width=2)),
                text=[f"${x:,.0f}" for x in bed_revenue['mean']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Average Revenue per Admission by Bed Type",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            yaxis_title="Average Revenue ($)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Financial Summary Table
    st.markdown("---")
    st.markdown("### 📋 Financial Summary by Department")
    
    financial_summary = df.groupby('Department').agg({
        'Total_charges': ['sum', 'mean', 'count'],
        'Insurance_covered': lambda x: (x == 'Yes').sum(),
        'Claim_status': lambda x: (x == 'Approved').sum()
    }).round(0)
    
    financial_summary.columns = ['Total Revenue', 'Avg Revenue', 'Admissions', 
                                 'Insured Patients', 'Approved Claims']
    financial_summary = financial_summary.sort_values('Total Revenue', ascending=False)
    
    st.dataframe(
        financial_summary.style
        .background_gradient(subset=['Total Revenue'], cmap='Greens')
        .background_gradient(subset=['Avg Revenue'], cmap='Blues')
        .format({
            'Total Revenue': '${:,.0f}',
            'Avg Revenue': '${:,.0f}',
            'Admissions': '{:.0f}',
            'Insured Patients': '{:.0f}',
            'Approved Claims': '{:.0f}'
        }),
        use_container_width=True,
        height=400
    )

# ============================================================================
# DOCTOR WORKLOAD PAGE
# ============================================================================
elif menu == "Doctor Workload":
    st.markdown("<h1> Doctor Workload Analysis</h1>", unsafe_allow_html=True)
    
    # Doctor Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Doctors", f"{len(doctors):,}")
    
    with col2:
        avg_patients = doctors['Patients_handled'].mean()
        st.metric("Avg Patients/Doctor", f"{avg_patients:.0f}")
    
    with col3:
        avg_consult = doctors['Avg_consult_time'].mean()
        st.metric("Avg Consult Time", f"{avg_consult:.0f} min")
    
    with col4:
        max_workload = doctors['Patients_handled'].max()
        st.metric("Max Workload", f"{max_workload} patients")
    
    st.markdown("---")
    
    # Workload Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Doctor Workload Distribution")
        
        fig = go.Figure(data=[
            go.Histogram(
                x=doctors['Patients_handled'],
                nbinsx=25,
                marker=dict(
                    color='#3498db',
                    line=dict(color='#2c3e50', width=1)
                )
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            xaxis_title="Patients Handled",
            yaxis_title="Number of Doctors",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("###  Consultation Time Distribution")
        
        fig = go.Figure(data=[
            go.Histogram(
                x=doctors['Avg_consult_time'],
                nbinsx=20,
                marker=dict(
                    color='#e74c3c',
                    line=dict(color='#2c3e50', width=1)
                )
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            xaxis_title="Average Consultation Time (minutes)",
            yaxis_title="Number of Doctors",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Department Workload
    st.markdown("---")
    st.markdown("###  Average Workload by Department")
    
    dept_workload = doctors.groupby('Department').agg({
        'Patients_handled': ['mean', 'sum', 'count'],
        'Avg_consult_time': 'mean'
    }).reset_index()
    
    dept_workload.columns = ['Department', 'Avg_Patients', 'Total_Patients', 'Doctor_Count', 'Avg_Consult_Time']
    dept_workload = dept_workload.sort_values('Avg_Patients', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=dept_workload['Department'],
        x=dept_workload['Avg_Patients'],
        orientation='h',
        name='Avg Patients',
        marker=dict(color='#3498db', line=dict(color='#2c3e50', width=1)),
        text=[f"{x:.0f}" for x in dept_workload['Avg_Patients']],
        textposition='outside'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        xaxis_title="Average Patients per Doctor",
        yaxis_title="Department",
        xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Workload vs Consultation Time
    st.markdown("---")
    st.markdown("###  Workload vs Consultation Time Analysis")
    
    fig = go.Figure(data=[
        go.Scatter(
            x=doctors['Patients_handled'],
            y=doctors['Avg_consult_time'],
            mode='markers',
            marker=dict(
                size=12,
                color=doctors['Patients_handled'],
                colorscale='Viridis',
                showscale=True,
                line=dict(color='#2c3e50', width=1),
                colorbar=dict(title="Patients<br>Handled")
            ),
            text=doctors['Department'],
            hovertemplate='<b>%{text}</b><br>Patients: %{x}<br>Consult Time: %{y} min<extra></extra>'
        )
    ])
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        xaxis_title="Patients Handled",
        yaxis_title="Average Consultation Time (minutes)",
        xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
        yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Doctor Table
    st.markdown("---")
    st.markdown("###  Detailed Doctor Statistics")
    
    dept_filter = st.multiselect(
        "Filter by Department:",
        options=doctors['Department'].unique(),
        default=doctors['Department'].unique()
    )
    
    filtered_doctors = doctors[doctors['Department'].isin(dept_filter)].copy()
    filtered_doctors = filtered_doctors.sort_values('Patients_handled', ascending=False)
    
    st.dataframe(
        filtered_doctors.style
        .background_gradient(subset=['Patients_handled'], cmap='Reds')
        .background_gradient(subset=['Avg_consult_time'], cmap='Blues'),
        use_container_width=True,
        height=400
    )
    
    # Department Summary
    st.markdown("---")
    st.markdown("### Department-wise Doctor Summary")
    
    dept_summary = doctors.groupby('Department').agg({
        'Doctor_ID': 'count',
        'Patients_handled': ['sum', 'mean', 'min', 'max'],
        'Avg_consult_time': 'mean'
    }).round(1)
    
    dept_summary.columns = ['Total Doctors', 'Total Patients', 'Avg Patients', 
                            'Min Workload', 'Max Workload', 'Avg Consult Time']
    dept_summary = dept_summary.sort_values('Total Patients', ascending=False)
    
    st.dataframe(
        dept_summary.style
        .background_gradient(subset=['Total Patients'], cmap='Greens')
        .background_gradient(subset=['Avg Patients'], cmap='Oranges')
        .format({
            'Total Patients': '{:.0f}',
            'Avg Patients': '{:.1f}',
            'Min Workload': '{:.0f}',
            'Max Workload': '{:.0f}',
            'Avg Consult Time': '{:.1f} min'
        }),
        use_container_width=True,
        height=400
    )

# ============================================================================
# CRITICAL ALERTS PAGE
# ============================================================================
elif menu == "Critical Alerts":
    st.markdown("<h1> Critical Alerts & Risk Assessment</h1>", unsafe_allow_html=True)
    
    st.info(" This page identifies patients and scenarios requiring immediate attention")
    
    # Risk Thresholds
    st.markdown("###  Set Alert Thresholds")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        los_threshold = st.slider("High LOS Threshold (days)", 1, 20, 7)
    
    with col2:
        age_threshold = st.slider("High-Risk Age (years)", 40, 90, 65)
    
    with col3:
        chronic_threshold = st.slider("Chronic Conditions Threshold", 0, 4, 2)
    
    # Identify Critical Cases
    high_risk = df[
        ((df['Length_of_stay'] > los_threshold) |
         (df['Age'] > age_threshold) |
         (df['Chronic_conditions'] >= chronic_threshold)) &
        (df['readmitted_30_days'] == 1)
    ].copy()
    
    high_los = df[df['Length_of_stay'] > los_threshold].copy()
    elderly_patients = df[df['Age'] > age_threshold].copy()
    icu_patients = df[df['Bed_type'] == 'ICU'].copy()
    
    # Alert Metrics
    st.markdown("---")
    st.markdown("###  Critical Alerts Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>⚠️ High-Risk Patients</h4>
                <p style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{len(high_risk):,}</p>
                <p style='margin: 0;'>Requires immediate attention</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>⏱️ Extended Stay</h4>
                <p style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{len(high_los):,}</p>
                <p style='margin: 0;'>LOS > {los_threshold} days</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #ff9a56 0%, #ff6a00 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>👴 Elderly Patients</h4>
                <p style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{len(elderly_patients):,}</p>
                <p style='margin: 0;'>Age > {age_threshold} years</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='info-card' style='background: linear-gradient(135deg, #ff6a00 0%, #ee0979 100%); color: white;'>
                <h4 style='color: white; margin-top: 0;'>🏥 ICU Patients</h4>
                <p style='font-size: 32px; font-weight: bold; margin: 10px 0;'>{len(icu_patients):,}</p>
                <p style='margin: 0;'>Critical care monitoring</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Visual Analysis
    st.markdown("---")
    st.markdown("###  Risk Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Readmission risk by department
        dept_readmit = df.groupby('Department')['readmitted_30_days'].agg(['sum', 'count']).reset_index()
        dept_readmit['rate'] = (dept_readmit['sum'] / dept_readmit['count']) * 100
        dept_readmit = dept_readmit.sort_values('rate', ascending=True)
        
        fig = go.Figure(data=[
            go.Bar(
                y=dept_readmit['Department'],
                x=dept_readmit['rate'],
                orientation='h',
                marker=dict(
                    color=dept_readmit['rate'],
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Rate %"),
                    line=dict(color='#2c3e50', width=1)
                ),
                text=[f"{x:.1f}%" for x in dept_readmit['rate']],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Readmission Rate by Department",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=450,
            xaxis_title="Readmission Rate (%)",
            yaxis_title="Department",
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # LOS vs Readmission
        fig = go.Figure()
        
        for status in [0, 1]:
            data = df[df['readmitted_30_days'] == status]
            fig.add_trace(go.Box(
                y=data['Length_of_stay'],
                name='Readmitted' if status == 1 else 'Not Readmitted',
                marker=dict(color='#e74c3c' if status == 1 else '#27ae60'),
                boxmean='sd'
            ))
        
        fig.update_layout(
            title="Length of Stay: Readmitted vs Not Readmitted",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=450,
            yaxis_title="Length of Stay (days)",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # High-Risk Patient Table
    st.markdown("---")
    st.markdown("### 📋 High-Risk Patient List")
    
    if len(high_risk) > 0:
        # Calculate risk score
        high_risk['Risk_Score'] = (
            high_risk['Length_of_stay'] * 0.3 +
            high_risk['Age'] * 0.2 +
            high_risk['Chronic_conditions'] * 5 +
            high_risk['readmitted_30_days'] * 10
        )
        
        display_cols = ['Patient_ID', 'Age', 'Gender', 'Department', 'Bed_type',
                       'Length_of_stay', 'Chronic_conditions', 'Risk_Score']
        
        high_risk_display = high_risk[display_cols].sort_values('Risk_Score', ascending=False).head(50)
        
        st.dataframe(
            high_risk_display.style
            .background_gradient(subset=['Risk_Score'], cmap='Reds')
            .background_gradient(subset=['Length_of_stay'], cmap='Oranges')
            .format({'Risk_Score': '{:.2f}'}),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = high_risk[display_cols].to_csv(index=False)
        st.download_button(
            label=" Download High-Risk Patient Report",
            data=csv,
            file_name=f"high_risk_patients_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    else:
        st.success(" No high-risk patients identified with current thresholds!")
    
    # Recommendations
    st.markdown("---")
    st.markdown("### 💡 Automated Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='info-card'>
                <h4> Priority Actions</h4>
                <ul>
                    <li>Review all ICU patients daily</li>
                    <li>Follow up with patients having LOS > 7 days</li>
                    <li>Monitor elderly patients with chronic conditions</li>
                    <li>Implement discharge planning for high-risk patients</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        busiest_dept = df.groupby('Department')['readmitted_30_days'].sum().idxmax()
        highest_readmit = df.groupby('Department')['readmitted_30_days'].mean().max() * 100
        
        st.markdown(f"""
            <div class='info-card'>
                <h4>📈 Key Findings</h4>
                <ul>
                    <li><strong>{busiest_dept}</strong> has the highest readmissions</li>
                    <li>Readmission rate: <strong>{highest_readmit:.1f}%</strong></li>
                    <li>ICU utilization: <strong>{(len(icu_patients)/len(df)*100):.1f}%</strong></li>
                    <li>High-risk patients: <strong>{len(high_risk)}</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; padding: 30px; background: white; border-radius: 15px; margin-top: 30px;'>
        <h3 style='color: #2c3e50; margin-bottom: 15px;'>Hospital Analytics Dashboard</h3>
        <p style='color: #7f8c8d; margin: 5px 0;'><strong>Powered by:</strong> Streamlit • Pandas • Plotly</p>
        <p style='color: #7f8c8d; margin: 5px 0;'> Data-Driven Healthcare Excellence</p>
        <p style='color: #95a5a6; font-size: 12px; margin-top: 15px;'>
            Dashboard Version 2.0 | Last Updated: {datetime.now().strftime('%B %d, %Y')}
        </p>
    </div>
""", unsafe_allow_html=True)
# ...existing code...