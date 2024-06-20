import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv(r"C:\Users\91860\OneDrive\Desktop\hackon\Amazon-HackOn\Automated Budgeting Solution\user_orders.csv")

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Category Spending and Savings Analysis"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in df['Order Year'].unique()] + [{'label': 'Overall', 'value': 'Overall'}],
        value='Overall',
        clearable=False,
        style={'width': '50%'}
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in df['Order Month'].unique()] + [{'label': 'Overall', 'value': 'Overall'}],
        value='Overall',
        clearable=False,
        style={'width': '50%'}
    ),
    html.Div(id='cards', style={'display': 'flex', 'justify-content': 'space-around'}),
    html.Div([
        dcc.Graph(id='category-spending-bar', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='category-savings-bar', style={'display': 'inline-block', 'width': '48%'})
    ])
])

@app.callback(
    [Output('category-spending-bar', 'figure'),
     Output('category-savings-bar', 'figure'),
     Output('cards', 'children')],
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_charts_and_cards(selected_year, selected_month):
    filtered_df = df.copy()
    if selected_year != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Year'] == selected_year]
    if selected_month != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Month'] == selected_month]
    
    # Spending by category
    category_spending = filtered_df.groupby('Product Category')['Price for Customer'].sum().reset_index()
    spending_figure = {
        'data': [
            {'y': category_spending['Product Category'], 'x': category_spending['Price for Customer'], 'type': 'bar', 'orientation': 'h', 'name': 'Spending'}
        ],
        'layout': {
            'title': 'Spending by Category',
            'yaxis': {'title': 'Category'},
            'xaxis': {'title': 'Total Spending'}
        }
    }
    
    # Savings by category
    category_savings = filtered_df.groupby('Product Category')['Savings'].sum().reset_index()
    savings_figure = {
        'data': [
            {'y': category_savings['Product Category'], 'x': category_savings['Savings'], 'type': 'bar', 'orientation': 'h', 'name': 'Savings'}
        ],
        'layout': {
            'title': 'Savings by Category',
            'yaxis': {'title': 'Category'},
            'xaxis': {'title': 'Total Savings'}
        }
    }
    
    # Total spending and savings
    total_spending = filtered_df['Price for Customer'].sum()
    total_savings = filtered_df['Savings'].sum()
    
    cards = [
        html.Div([
            html.H3('Total Spending'),
            html.P(f'₹{total_spending:,.2f}')
        ], style={'border': '1px solid black', 'padding': '10px', 'width': '45%', 'text-align': 'center'}),
        html.Div([
            html.H3('Total Savings'),
            html.P(f'₹{total_savings:,.2f}')
        ], style={'border': '1px solid black', 'padding': '10px', 'width': '45%', 'text-align': 'center'})
    ]
    
    return spending_figure, savings_figure, cards

if __name__ == '__main__':
    app.run_server(debug=True)
