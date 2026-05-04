import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("pizza_sales.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')

df['day'] = df['order_date'].dt.day_name()
df['month'] = df['order_date'].dt.month_name()

# -----------------------------
# KPI CALCULATIONS
# -----------------------------

total_revenue = df['total_price'].sum()
total_orders = df['order_id'].nunique()
total_pizzas = df['quantity'].sum()

avg_order_value = total_revenue / total_orders
avg_pizzas_order = total_pizzas / total_orders

# -----------------------------
# APP
# -----------------------------

app = Dash(__name__)

# -----------------------------
# LAYOUT
# -----------------------------

app.layout = html.Div([

html.H1("🍕 Pizza Sales Interactive Dashboard",
style={'textAlign':'center'}),

# KPI CARDS
html.Div([

html.Div([
html.H4("Revenue"),
html.H2(f"${total_revenue:,.2f}")
],style={'width':'24%','textAlign':'center'}),

html.Div([
html.H4("Orders"),
html.H2(total_orders)
],style={'width':'24%','textAlign':'center'}),

html.Div([
html.H4("Pizzas Sold"),
html.H2(total_pizzas)
],style={'width':'24%','textAlign':'center'}),

html.Div([
html.H4("Avg Order Value"),
html.H2(f"${avg_order_value:.2f}")
],style={'width':'24%','textAlign':'center'})

],style={'display':'flex'}),

# ROW 1
html.Div([
dcc.Graph(id='daily_chart'),
dcc.Graph(id='monthly_chart')
],style={'display':'flex'}),

# ROW 2
html.Div([
dcc.Graph(id='category_chart'),
dcc.Graph(id='size_chart')
],style={'display':'flex'}),

# ROW 3
html.Div([
dcc.Graph(id='top_revenue'),
dcc.Graph(id='top_quantity'),
dcc.Graph(id='top_orders')
],style={'display':'flex'}),

# ROW 4
html.Div([
dcc.Graph(id='bottom_revenue'),
dcc.Graph(id='bottom_quantity'),
dcc.Graph(id='bottom_orders')
],style={'display':'flex'})

])

# -----------------------------
# CALLBACK
# -----------------------------

@app.callback(

Output('daily_chart','figure'),
Output('monthly_chart','figure'),
Output('category_chart','figure'),
Output('size_chart','figure'),
Output('top_revenue','figure'),
Output('top_quantity','figure'),
Output('top_orders','figure'),
Output('bottom_revenue','figure'),
Output('bottom_quantity','figure'),
Output('bottom_orders','figure'),

Input('category_chart','clickData')

)

def update_dashboard(category_click):

    filtered_df = df

    if category_click:

        category = category_click['points'][0]['label']
        filtered_df = df[df['pizza_category']==category]

    # DAILY TREND
    daily = filtered_df.groupby('day')['order_id'].nunique().reset_index()

    fig1 = px.bar(
        daily,
        x='day',
        y='order_id',
        title="Daily Orders Trend"
    )

    # MONTHLY TREND
    monthly = filtered_df.groupby('month')['order_id'].nunique().reset_index()

    fig2 = px.line(
        monthly,
        x='month',
        y='order_id',
        title="Monthly Orders Trend"
    )

    # CATEGORY SALES
    category_sales = filtered_df.groupby('pizza_category')['total_price'].sum().reset_index()

    fig3 = px.pie(
        category_sales,
        names='pizza_category',
        values='total_price',
        title="Sales by Category"
    )

    # SIZE SALES
    size_sales = filtered_df.groupby('pizza_size')['total_price'].sum().reset_index()

    fig4 = px.pie(
        size_sales,
        names='pizza_size',
        values='total_price',
        title="Sales by Size"
    )

    # TOP 5 REVENUE
    top_rev = filtered_df.groupby('pizza_name')['total_price'].sum().nlargest(5).reset_index()

    fig5 = px.bar(
        top_rev,
        x='total_price',
        y='pizza_name',
        orientation='h',
        title="Top 5 by Revenue"
    )

    # TOP 5 QUANTITY
    top_qty = filtered_df.groupby('pizza_name')['quantity'].sum().nlargest(5).reset_index()

    fig6 = px.bar(
        top_qty,
        x='quantity',
        y='pizza_name',
        orientation='h',
        title="Top 5 by Quantity"
    )

    # TOP 5 ORDERS
    top_orders = filtered_df.groupby('pizza_name')['order_id'].nunique().nlargest(5).reset_index()

    fig7 = px.bar(
        top_orders,
        x='order_id',
        y='pizza_name',
        orientation='h',
        title="Top 5 by Orders"
    )

    # BOTTOM 5 REVENUE
    bottom_rev = filtered_df.groupby('pizza_name')['total_price'].sum().nsmallest(5).reset_index()

    fig8 = px.bar(
        bottom_rev,
        x='total_price',
        y='pizza_name',
        orientation='h',
        title="Bottom 5 by Revenue"
    )

    # BOTTOM 5 QUANTITY
    bottom_qty = filtered_df.groupby('pizza_name')['quantity'].sum().nsmallest(5).reset_index()

    fig9 = px.bar(
        bottom_qty,
        x='quantity',
        y='pizza_name',
        orientation='h',
        title="Bottom 5 by Quantity"
    )

    # BOTTOM 5 ORDERS
    bottom_orders = filtered_df.groupby('pizza_name')['order_id'].nunique().nsmallest(5).reset_index()

    fig10 = px.bar(
        bottom_orders,
        x='order_id',
        y='pizza_name',
        orientation='h',
        title="Bottom 5 by Orders"
    )

    return fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig10


# -----------------------------
# RUN
# -----------------------------

app.run(debug=True)