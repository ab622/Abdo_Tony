import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the Titanic dataset
df = pd.read_csv('D:\\Vs Code\\Data Sets Projects\\Titanic Data set\\train.csv')

# Prepare data for figures
numeric_df = df.select_dtypes(include='number').dropna()

# Set up the Streamlit app layout
st.title("Titanic Dataset Dashboard")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Age Distribution", "Fare Distribution", "Survival by Class", "Survival by Gender", "Correlation Heatmap", "Scatter Matrix"])

# Age Distribution
if page == "Age Distribution":
    st.header("Distribution of Passenger Ages")
    fig = px.histogram(df, x='Age', nbins=30, title='Distribution of Passenger Ages')
    st.plotly_chart(fig)

# Fare Distribution
elif page == "Fare Distribution":
    st.header("Distribution of Passenger Fares")
    fig = px.histogram(df, x='Fare', nbins=30, title='Distribution of Passenger Fares')
    st.plotly_chart(fig)

# Survival by Class
elif page == "Survival by Class":
    st.header("Survival Rates by Passenger Class")
    fig = px.histogram(df, x='Pclass', color='Survived', barmode='group', title='Survival Rates by Passenger Class')
    st.plotly_chart(fig)

# Survival by Gender
elif page == "Survival by Gender":
    st.header("Survival Rates by Gender")
    fig = px.histogram(df, x='Sex', color='Survived', barmode='group', title='Survival Rates by Gender')
    st.plotly_chart(fig)

# Correlation Heatmap
elif page == "Correlation Heatmap":
    st.header("Correlation Heatmap")
    corr_matrix = numeric_df.corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect='auto', title='Correlation Heatmap')
    st.plotly_chart(fig)

# Scatter Matrix
elif page == "Scatter Matrix":
    st.header("Scatter Matrix of Selected Features")
    fig = go.Figure(data=go.Splom(
        dimensions=[{'label': col, 'values': numeric_df[col]} for col in numeric_df.columns if col != 'Survived'],
        showupperhalf=False,
        text=numeric_df['Survived'],
        marker=dict(color=numeric_df['Survived'], colorscale='Viridis', size=5, showscale=False)
    ))
    fig.update_layout(title='Scatter Matrix of Selected Features', dragmode='select')
    st.plotly_chart(fig)
