import plotly.graph_objs as go
import pandas as pd

def plot_spending_by_category(filtered_df, selected_year='Overall', selected_month='Overall'):
    if selected_year != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Year'] == int(selected_year)]
    if selected_month != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Month'] == selected_month]

    category_spending = filtered_df.groupby('Product Category')['Price for Customer'].sum().reset_index()
    category_spending = category_spending.sort_values(by='Price for Customer', ascending=False)
    
    trace = go.Bar(
        x=category_spending['Price for Customer'],
        y=category_spending['Product Category'],
        orientation='h',
        marker=dict(color='rgba(50, 171, 96, 1)'),
        text=category_spending['Price for Customer'].apply(lambda x: f"₹{x:,.2f}"),
        textposition='auto'
    )
    
    layout = go.Layout(
        title='Spending by Category',
        xaxis=dict(title='Total Spending'),
        yaxis=dict(title='Category', automargin=True),
        margin=dict(l=150, r=20, t=50, b=50),
        showlegend=False
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    return fig

def plot_savings_by_category(filtered_df, selected_year='Overall', selected_month='Overall'):
    if selected_year != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Year'] == int(selected_year)]
    if selected_month != 'Overall':
        filtered_df = filtered_df[filtered_df['Order Month'] == selected_month]
    
    category_savings = filtered_df.groupby('Product Category')['Savings'].sum().reset_index()
    category_savings = category_savings.sort_values(by='Savings', ascending=False)
    
    trace = go.Bar(
        x=category_savings['Savings'],
        y=category_savings['Product Category'],
        orientation='h',
        marker=dict(color='rgba(219, 64, 82, 1)'),
        text=category_savings['Savings'].apply(lambda x: f"₹{x:,.2f}"),
        textposition='auto'
    )
    
    layout = go.Layout(
        title='Savings by Category',
        xaxis=dict(title='Total Savings'),
        yaxis=dict(title='Category', automargin=True),
        margin=dict(l=150, r=20, t=50, b=50),
        showlegend=False
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    return fig

def plot_spending_over_months(filtered_df, selected_year='Overall'):
    if selected_year != 'Overall':
        filtered_df = filtered_df[pd.to_datetime(filtered_df['Order Date']).dt.year == int(selected_year)]

    monthly_spending = filtered_df.groupby(pd.to_datetime(filtered_df['Order Date']).dt.to_period('M'))['Price for Customer'].sum().reset_index()
    monthly_spending['Date'] = monthly_spending['Order Date'].dt.strftime('%Y-%m')  # Convert to YYYY-MM format
    monthly_spending = monthly_spending.sort_values('Date')

    trace = go.Scatter(
        x=monthly_spending['Date'],
        y=monthly_spending['Price for Customer'],
        mode='lines+markers',
        name='Spending',
        line=dict(color='rgb(50, 171, 96)'),
        marker=dict(symbol='circle', size=8),
        text=monthly_spending['Price for Customer'].apply(lambda x: f"₹{x:,.2f}")
    )

    layout = go.Layout(
        title='Monthly Spending',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Total Spending'),
        margin=dict(l=150, r=20, t=50, b=50),
        showlegend=True
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig

def plot_savings_over_months(filtered_df, selected_year='Overall'):
    if selected_year != 'Overall':
        filtered_df = filtered_df[pd.to_datetime(filtered_df['Order Date']).dt.year == int(selected_year)]

    monthly_savings = filtered_df.groupby(pd.to_datetime(filtered_df['Order Date']).dt.to_period('M'))['Savings'].sum().reset_index()
    monthly_savings['Date'] = monthly_savings['Order Date'].dt.strftime('%Y-%m')  # Convert to YYYY-MM format
    monthly_savings = monthly_savings.sort_values('Date')

    trace = go.Scatter(
        x=monthly_savings['Date'],
        y=monthly_savings['Savings'],
        mode='lines+markers',
        name='Savings',
        line=dict(color='rgb(219, 64, 82)'),
        marker=dict(symbol='circle', size=8),
        text=monthly_savings['Savings'].apply(lambda x: f"₹{x:,.2f}")
    )

    layout = go.Layout(
        title='Monthly Savings',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Total Savings'),
        margin=dict(l=150, r=20, t=50, b=50),
        showlegend=True
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig
