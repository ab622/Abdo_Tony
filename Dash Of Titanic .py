import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the Titanic dataset
df = pd.read_csv('D:\\Vs Code\\Data Sets Projects\\Titanic Data set\\train.csv')

# Prepare data for figures
numeric_df = df.select_dtypes(include='number').dropna()

# Initialize the Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title='Titanic Dataset Dashboard')

# Define a function to create stats cards
def generate_stats_card(title, value, image_path):
    return html.Div(
        dbc.Card([
            dbc.CardImg(src=image_path, top=True, style={'width': '50px', 'alignSelf': 'center'}),
            dbc.CardBody([
                html.P(value, className="card-value", style={'margin': '0px', 'fontSize': '22px', 'fontWeight': 'bold'}),
                html.H4(title, className="card-title", style={'margin': '0px', 'fontSize': '18px', 'fontWeight': 'bold'})
            ], style={'textAlign': 'center'}),
        ], style={'paddingBlock': '10px', "backgroundColor": '#deb522', 'border': 'none', 'borderRadius': '10px'})
    )

# Layout of the dashboard with a Titanic-themed background image
app.layout = html.Div(style={
    'backgroundImage': 'url(./assets/titanic_background.jpg)',  # Replace with the path to your background image
    'backgroundSize': 'cover',
    'backgroundPosition': 'center',
    'minHeight': '100vh'
}, children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Titanic Dataset Dashboard", style={'textAlign': 'center', 'color': '#FFFFFF'}), width=15)
        ], style={'paddingTop': '20px'}),
        dbc.Row([
            dbc.Col(generate_stats_card("Total Passengers", len(df), "./assets/passenger-icon.png"), width=3),
            dbc.Col(generate_stats_card("Survived", df['Survived'].sum(), "./assets/survived-icon.png"), width=3),
            dbc.Col(generate_stats_card("Total Fare", f"${df['Fare'].sum():.2f}", "./assets/fare-icon.png"), width=3),
            dbc.Col(generate_stats_card("Average Age", f"{df['Age'].mean():.2f}", "./assets/age-icon.png"), width=3)
        ], style={'marginBlock': '10px'}),
        dbc.Row([
            dbc.Col(
                dcc.Tabs(id='graph-tabs', value='age-distribution', children=[
                    dcc.Tab(label='Age Distribution', value='age-distribution', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                    dcc.Tab(label='Fare Distribution', value='fare-distribution', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                    dcc.Tab(label='Survival by Class', value='survival-by-class', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                    dcc.Tab(label='Survival by Gender', value='survival-by-gender', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                    dcc.Tab(label='Correlation Heatmap', value='correlation-heatmap', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                    dcc.Tab(label='Scatter Matrix', value='scatter-matrix', style={'backgroundColor': '#000', 'color': '#deb522', 'borderRadius': '5px', 'margin': '5px'}, selected_style={'backgroundColor': '#deb522', 'color': '#000', 'borderRadius': '5px'}),
                ], style={'marginTop': '15px', 'height': '50px', 'display': 'flex', 'justifyContent': 'center'}), width=15)
        ], justify='center'),
        dbc.Row([
            dcc.Loading([
                html.Div(id='tabs-content')
            ], type='default', color='#deb522')
        ])
    ], style={'padding': '0px', 'backgroundColor': 'rgba(0, 0, 0, 0.5)'})  # Semi-transparent background for content container
])

# Callback to update the content of the selected tab
@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value')]
)
def update_tab(tab):
    if tab == 'age-distribution':
        fig = px.histogram(df, x='Age', nbins=30, title='Distribution of Passenger Ages')
    elif tab == 'fare-distribution':
        fig = px.histogram(df, x='Fare', nbins=30, title='Distribution of Passenger Fares')
    elif tab == 'survival-by-class':
        fig = px.histogram(df, x='Pclass', color='Survived', barmode='group', title='Survival Rates by Passenger Class')
    elif tab == 'survival-by-gender':
        fig = px.histogram(df, x='Sex', color='Survived', barmode='group', title='Survival Rates by Gender')
    elif tab == 'correlation-heatmap':
        fig = px.imshow(numeric_df.corr(), text_auto=True, aspect='auto', title='Correlation Heatmap')
    elif tab == 'scatter-matrix':
        fig = go.Figure(data=go.Splom(
            dimensions=[{'label': col, 'values': numeric_df[col]} for col in numeric_df.columns if col != 'Survived'],
            showupperhalf=False,
            text=numeric_df['Survived'],
            marker=dict(color=numeric_df['Survived'], colorscale='Viridis', size=5, showscale=False)
        )).update_layout(title='Scatter Matrix of Selected Features', dragmode='select')
    
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
