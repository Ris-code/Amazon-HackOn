import streamlit as st
from streamlit_option_menu import option_menu
import os
from datetime import datetime, timedelta
import plotly.graph_objs as go
import pandas as pd
import pages.plot as pt
import plotly.express as px

image = os.path.join(os.path.dirname(__file__), '..', 'Images')

st.set_page_config(
    page_title="Amazon",
    page_icon=os.path.join(image, 'logo.png'),
    initial_sidebar_state="expanded",
    layout="wide",
)

data_path = os.path.join(os.path.dirname(__file__), '..', 'Automated Budgeting Solution', 'customer_orders.csv')
df = pd.read_csv(data_path)

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.strftime('%Y-%m')

def spend_plot(filtered_df):
    fig1 = pt.plot_spending_by_category(filtered_df)
    fig2 = pt.plot_spending_over_months(filtered_df)

    return fig1, fig2

def save_plot(filtered_df):
    fig1 = pt.plot_savings_by_category(filtered_df)
    fig2 = pt.plot_savings_over_months(filtered_df)

    return fig1, fig2
# Function to display order details with filters
def display_orders():
    st.title("Order Details")

    # Filters
    categories = df['Product Category'].unique()
    selected_category = st.selectbox("Select Product Category", options=["All"] + list(categories))

    min_price, max_price = st.slider("Select Price Range (Price for Customer)", 
                                     min_value=float(df['Price for Customer'].min()), 
                                     max_value=float(df['Price for Customer'].max()), 
                                     value=(float(df['Price for Customer'].min()), float(df['Price for Customer'].max())))

    start_date, end_date = st.date_input("Select Order Date Range", 
                                         value=(df['Order Date'].min(), df['Order Date'].max()), 
                                         min_value=df['Order Date'].min(), 
                                         max_value=df['Order Date'].max())

    # Filter dataframe based on selections
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Product Category'] == selected_category]
    
    filtered_df = filtered_df[(filtered_df['Price for Customer'] >= min_price) & (filtered_df['Price for Customer'] <= max_price)]
    filtered_df = filtered_df[(filtered_df['Order Date'] >= pd.Timestamp(start_date)) & (filtered_df['Order Date'] <= pd.Timestamp(end_date))]

    # Display filtered orders
    st.markdown("### Filtered Orders")
    st.write(filtered_df[['Order ID', 'Product Name', 'MRP', 'Price for Customer', 'Order Date']])

# Function to display order details with filters
def display_orders_and_savings():
    st.title("Order Details and Savings")

    # Filters
    categories = df['Product Category'].unique()
    selected_category = st.selectbox("Select Product Category", options=["All"] + list(categories))

    min_savings, max_savings = st.slider("Select Savings Range", 
                                         min_value=float(df['Savings'].min()), 
                                         max_value=float(df['Savings'].max()), 
                                         value=(float(df['Savings'].min()), float(df['Savings'].max())))

    start_date, end_date = st.date_input("Select Order Date Range", 
                                         value=(df['Order Date'].min(), df['Order Date'].max()), 
                                         min_value=df['Order Date'].min(), 
                                         max_value=df['Order Date'].max())

    # Filter dataframe based on selections
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Product Category'] == selected_category]
    
    filtered_df = filtered_df[(filtered_df['Savings'] >= min_savings) & (filtered_df['Savings'] <= max_savings)]
    filtered_df = filtered_df[(filtered_df['Order Date'] >= pd.Timestamp(start_date)) & (filtered_df['Order Date'] <= pd.Timestamp(end_date))]

    # Calculate total savings
    total_savings = round(filtered_df['Savings'].sum(), 2)

    # Display total savings
    st.markdown(f"""<div style='border: 1px solid red; display: flex; align-items: center; justify-content: center; padding: 10px; border-radius: 5px;'>
                    <span style='font-weight: bold; margin-right: 10px;'>Total Savings:</span>
                    <span>{total_savings}</span>
                </div>""", unsafe_allow_html=True)

    # Display filtered orders
    st.markdown("### Filtered Orders")
    st.write(filtered_df[['Order ID', 'Product Name', 'MRP', 'Price for Customer', 'Savings', 'Order Date']])

# Function to display budget and spending analysis
def display_budget_and_spendings():
    st.title("Budget and Spending Analysis")
    st.header("Set Budget Limits")
    col1, col2 = st.columns(2)
    with col1:
    # Inputs for budget limits
        monthly_budget = st.number_input("Monthly Budget Limit", min_value=0, value=10000, step=100)
    
    with col2:
        yearly_budget = st.number_input("Yearly Budget Limit", min_value=0, value=120000, step=1000)

    # Calculate monthly and yearly spendings
    monthly_spendings = df.groupby('Order Month')['Price for Customer'].sum().reset_index()
    yearly_spendings = df.groupby('Order Year')['Price for Customer'].sum().reset_index()


    # Compare spendings with budget limits
    monthly_spendings['Status'] = monthly_spendings['Price for Customer'].apply(lambda x: 'Over Budget' if x > monthly_budget else 'Within Budget')
    yearly_spendings['Status'] = yearly_spendings['Price for Customer'].apply(lambda x: 'Over Budget' if x > yearly_budget else 'Within Budget')

    main_choice = option_menu(
        menu_title="",
        options=["Monthly Spendings", "Yearly Spendings"],
        icons=["calendar-month", "calendar"],
        menu_icon="cast",
        default_index=0,
        orientation = "horizontal",
        styles={
            "container": {"background-color": "#141920"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px",
                "color": "white"
            },
            "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
        }
    )

    if main_choice == "Monthly Spendings":
        if (monthly_spendings['Price for Customer'] > monthly_budget).any():
            st.warning("Monthly budget limit exceeded!")
        # Display spendings and limits
        st.header("Monthly Spendings")
        fig_monthly = px.bar(monthly_spendings, x='Order Month', y='Price for Customer', color='Status', title="Monthly Spendings")
        fig_monthly.add_hline(y=monthly_budget, line_dash="dot", annotation_text="Monthly Budget Limit", line_color="red")
        st.plotly_chart(fig_monthly)

    elif main_choice == "Yearly Spendings":
        if (yearly_spendings['Price for Customer'] > yearly_budget).any():
            st.warning("Yearly budget limit exceeded!")

        st.header("Yearly Spendings")
        fig_yearly = px.bar(yearly_spendings, x='Order Year', y='Price for Customer', color='Status', title="Yearly Spendings")
        fig_yearly.add_hline(y=yearly_budget, line_dash="dot", annotation_text="Yearly Budget Limit", line_color="red")
        st.plotly_chart(fig_yearly)

# Function to display EMI analysis
def display_emi_analysis():
    st.title("EMI Analysis")

    # Filter EMI orders
    emi_df = df[df['Payment Method'] == 'EMI'].copy()

    if emi_df.empty:
        st.info("No EMI orders found.")
        return

    # Calculate EMI details
    current_date = datetime.now()
    emi_df['Duration (months)'] = emi_df['Duration (months)'].fillna(0).astype(int)
    emi_df['Monthly Payment'] = emi_df['Monthly Payment'].fillna(0).astype(float)
    emi_df['Order Date'] = pd.to_datetime(emi_df['Order Date'])
    emi_df['Months Passed'] = emi_df['Order Date'].apply(lambda x: (current_date.year - x.year) * 12 + current_date.month - x.month)

    emi_df['Amount Paid'] = emi_df.apply(lambda row: min(row['Months Passed'], row['Duration (months)']) * row['Monthly Payment'], axis=1)
    emi_df['Amount Left'] = emi_df['Price for Customer'] - emi_df['Amount Paid']
    emi_df['Interest Paid'] = emi_df['Amount Paid'] * 0.1  # Assuming 10% interest rate on amount paid
    emi_df['Interest Left'] = emi_df['Amount Left'] * 0.1  # Assuming 10% interest rate on amount left

    # Display EMI details
    st.write(emi_df[['Order ID', 'Product Name', 'Product Category', 'Price for Customer', 'Order Date', 'Amount Paid', 'Amount Left', 'Interest Paid', 'Interest Left']])

    # Visualizations
    st.header("EMI Analysis Visualizations")

    emi_df['Full Name'] = emi_df['Order ID'].astype(str) + ' ' + emi_df['Product Name']

    options = st.selectbox(
        "Select order",
        emi_df['Full Name'].tolist(),
        index = 0,
    )

    selected_order_id = options.split()[0]

    if selected_order_id in emi_df['Order ID'].astype(str).tolist():
        emi = emi_df[emi_df['Order ID'].astype(str) == selected_order_id].iloc[0]

        # Grouped bar chart for Amount Paid, Amount Left, Interest Paid, Interest Left
        fig_grouped_bar = go.Figure(data=[
            go.Bar(name='Amount Paid', x=['Amount'], y=[emi['Amount Paid']], marker_color='orange'),
            go.Bar(name='Amount Left', x=['Amount'], y=[emi['Amount Left']], marker_color='white'),
            go.Bar(name='Interest Paid', x=['Interest'], y=[emi['Interest Paid']], marker_color='lightgreen'),
            go.Bar(name='Interest Left', x=['Interest'], y=[emi['Interest Left']], marker_color='lightcoral')
        ])
        fig_grouped_bar.update_layout(barmode='group', title_text="EMI Amount and Interest Analysis")
        st.plotly_chart(fig_grouped_bar)


def sidebar_spend_analysis():
    filtered_df = df.copy()

    main_choice = option_menu(
        menu_title="",
        options=["Graphical Analysis", "Order Details"],
        icons=["bar-chart-line-fill", "clipboard-data-fill"],
        menu_icon="cast",
        default_index=0,
        orientation = "horizontal",
        styles={
            "container": {"background-color": "#141920"},
            "icon": {"color": "rgba(50, 171, 96, 1)", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px",
                "color": "white"
            },
            "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
        }
    )

    if main_choice == "Graphical Analysis":
        option = st.selectbox(
            "Choose the required analysis",
            ["Spending Analysis according to item category", "Spending Analysis according to montly spending"],
            index = 0
        )
        fig1, fig2 = spend_plot(filtered_df)
        if option == "Spending Analysis according to item category":
            st.plotly_chart(fig1)
        elif option == "Spending Analysis according to montly spending":
            st.plotly_chart(fig2)
    
    elif main_choice == "Order Details":
        display_orders()

def sidebar_save_analysis():
    filtered_df = df.copy()

    main_choice = option_menu(
        menu_title="",
        options=["Graphical Analysis", "Order Details"],
        icons=["bar-chart-line-fill", "clipboard-data-fill"],
        menu_icon="cast",
        default_index=0,
        orientation = "horizontal",
        styles={
            "container": {"background-color": "#141920"},
            "icon": {"color": "red", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px",
                "color": "white"
            },
            "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
        }
    )

    if main_choice == "Graphical Analysis":
        option = st.selectbox(
            "Choose the required analysis",
            ["Spending Analysis according to item category", "Spending Analysis according to montly spending"],
            index = 0
        )
        fig1, fig2 = save_plot(filtered_df)
        if option == "Spending Analysis according to item category":
            st.plotly_chart(fig1)
        elif option == "Spending Analysis according to montly spending":
            st.plotly_chart(fig2)
    
    elif main_choice == "Order Details":
        display_orders_and_savings()

def spending_analysis():
    filtered_df = df.copy()  
    summation = round(sum(filtered_df["Price for Customer"].tolist()), 2)
    st.markdown("""
        <div style='border: 2px solid rgba(50, 171, 96, 1); padding: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='font-size: 20px; font-weight: bold;'>Total Spending</span>
            <span style='font-size: 20px; font-weight: bold; color: white;'>Rs {}</span>
        </div>
        """.format(summation), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    fig1, fig2 = spend_plot(filtered_df)
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.plotly_chart(fig2)

def savings_analysis():
    filtered_df = df.copy()  
    summation = round(sum(filtered_df["Savings"].tolist()), 2)
    st.markdown("""
        <div style='border: 2px solid red; padding: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
            <span style='font-size: 20px; font-weight: bold;'>Total Savings</span>
            <span style='font-size: 20px; font-weight: bold; color: white;'>Rs {}</span>
        </div>
        """.format(summation), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    fig1, fig2 = save_plot(filtered_df)
    with col1:
        st.plotly_chart(fig1)
    with col2:
        st.plotly_chart(fig2)

def dashboard():
    main_choice = option_menu(
        menu_title="",
        options=["Spending Analysis", "Saving Analysis", "EMI"],
        icons=["bar-chart-line", "bar-chart-line", "bank"],
        menu_icon="cast",
        default_index=0,
        orientation = "horizontal",
        styles={
            "container": {"background-color": "#141920"},
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px",
                "color": "white"
            },
            "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
        }
    )

    if main_choice == "Spending Analysis":
        spending_analysis()
    elif main_choice == "Saving Analysis":
        savings_analysis()
    elif main_choice == "EMI":
        display_emi_analysis()

def finance():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; background-color: transparent; color: white; border-radius: 10px; border: 1px solid orange; font-weight: 300px; font-size: 35px;'>FINALYTICS</h1>", unsafe_allow_html=True)
        main_choice = option_menu(
            menu_title="",
            options=["Dashboard", "Spending Analysis", "Saving Analysis", "Budget Management"],
            icons=["file-bar-graph-fill", "bar-chart-line", "bar-chart-line", "wallet-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"background-color": "#141920"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                    "color": "white"
                },
                "nav-link-selected": {"background-color": "rgba(192,192,192, 0.2)", "color": "#ffffff"},
            }
        )
    if main_choice == "Dashboard":
        dashboard()
    elif main_choice == "Spending Analysis":
        sidebar_spend_analysis()
    elif main_choice == "Saving Analysis":
        sidebar_save_analysis()
    elif main_choice == "Budget Management":
        display_budget_and_spendings()


finance()