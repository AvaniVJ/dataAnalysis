import pandas as pd
import ollama

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("pizza_sales.csv")

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_revenue = round(
    df['total_price'].sum(), 2
)

total_orders = df['order_id'].nunique()

total_pizzas = df['quantity'].sum()

avg_order_value = round(
    total_revenue / total_orders, 2
)

# ---------------------------------------------------
# TOP / LOWEST PIZZAS
# ---------------------------------------------------

top_pizzas = (
    df.groupby('pizza_name')['total_price']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

bottom_pizzas = (
    df.groupby('pizza_name')['total_price']
    .sum()
    .sort_values(ascending=True)
    .head(5)
)

top_pizza_text = top_pizzas.to_string()

bottom_pizza_text = bottom_pizzas.to_string()

# ---------------------------------------------------
# INGREDIENT ANALYSIS
# ---------------------------------------------------

all_ingredients = []

for ingredients in df['pizza_ingredients'].dropna():

    ingredient_list = ingredients.split(',')

    for ingredient in ingredient_list:

        all_ingredients.append(
            ingredient.strip()
        )

ingredient_series = pd.Series(all_ingredients)

top_ingredients = (
    ingredient_series.value_counts()
    .head(10)
)

top_ingredients_text = (
    top_ingredients.to_string()
)

# ---------------------------------------------------
# TOP INGREDIENTS IN TOP PIZZAS
# ---------------------------------------------------

best_pizza_names = (
    df.groupby('pizza_name')['total_price']
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

best_pizza_df = df[
    df['pizza_name'].isin(best_pizza_names)
]

best_ingredients = []

for ingredients in best_pizza_df['pizza_ingredients'].dropna():

    ingredient_list = ingredients.split(',')

    for ingredient in ingredient_list:

        best_ingredients.append(
            ingredient.strip()
        )

best_ingredient_series = pd.Series(best_ingredients)

best_ingredient_counts = (
    best_ingredient_series.value_counts()
    .head(10)
)

best_ingredient_text = (
    best_ingredient_counts.to_string()
)

# ---------------------------------------------------
# APP
# ---------------------------------------------------

app = Dash(__name__)

# ---------------------------------------------------
# BUTTON STYLE
# ---------------------------------------------------

question_style = {

    'padding': '12px 18px',

    'backgroundColor': '#007bff',

    'color': 'white',

    'border': 'none',

    'borderRadius': '10px',

    'cursor': 'pointer',

    'fontSize': '14px'
}

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

app.layout = html.Div([

    # ---------------------------------------------------
    # TITLE
    # ---------------------------------------------------

    html.H1(
        "🍕 AI Pizza Sales Intelligence Dashboard",
        style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'color': '#333'
        }
    ),

    # ---------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------

    html.Div([

        html.Div([

            html.H4("Revenue"),

            html.H2(f"${total_revenue}")

        ], style={
            'width': '23%',
            'padding': '20px',
            'textAlign': 'center',
            'backgroundColor': '#ffffff',
            'borderRadius': '12px',
            'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)'
        }),

        html.Div([

            html.H4("Orders"),

            html.H2(total_orders)

        ], style={
            'width': '23%',
            'padding': '20px',
            'textAlign': 'center',
            'backgroundColor': '#ffffff',
            'borderRadius': '12px',
            'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)'
        }),

        html.Div([

            html.H4("Pizzas Sold"),

            html.H2(total_pizzas)

        ], style={
            'width': '23%',
            'padding': '20px',
            'textAlign': 'center',
            'backgroundColor': '#ffffff',
            'borderRadius': '12px',
            'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)'
        }),

        html.Div([

            html.H4("Avg Order Value"),

            html.H2(f"${avg_order_value}")

        ], style={
            'width': '23%',
            'padding': '20px',
            'textAlign': 'center',
            'backgroundColor': '#ffffff',
            'borderRadius': '12px',
            'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)'
        })

    ], style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'marginBottom': '50px'
    }),

    # ---------------------------------------------------
    # CLICKABLE QUESTIONS
    # ---------------------------------------------------

    html.Div([

        html.H3("💡 Suggested Questions"),

        html.Div([

            html.Button(
                "Which pizzas underperform?",
                id='q1',
                n_clicks=0,
                style=question_style
            ),

            html.Button(
                "Which pizzas should receive more promotion?",
                id='q2',
                n_clicks=0,
                style=question_style
            ),

            html.Button(
                "Suggest strategies to improve revenue",
                id='q3',
                n_clicks=0,
                style=question_style
            ),

            html.Button(
                "Suggest a new pizza likely to perform well",
                id='q4',
                n_clicks=0,
                style=question_style
            ),

            html.Button(
                "Which ingredients are most popular?",
                id='q5',
                n_clicks=0,
                style=question_style
            ),

            html.Button(
                "Which ingredients appear in top pizzas?",
                id='q6',
                n_clicks=0,
                style=question_style
            )

        ], style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'gap': '10px'
        })

    ], style={
        'backgroundColor': '#ffffff',
        'padding': '20px',
        'borderRadius': '12px',
        'marginBottom': '30px',
        'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)'
    }),

    # ---------------------------------------------------
    # AI CHAT SECTION
    # ---------------------------------------------------

    html.Div([

        html.H2(
            "🤖 Ask AI About Pizza Sales",
            style={
                'marginBottom': '20px',
                'color': '#444'
            }
        ),

        dcc.Textarea(

            id='user_question',

            placeholder='''
Examples:
- Which pizzas underperform?
- Suggest strategies to improve revenue
- Which ingredients are most popular?
- Suggest a new pizza likely to perform well
            ''',

            style={
                'width': '100%',
                'height': '140px',
                'padding': '15px',
                'fontSize': '16px',
                'borderRadius': '10px',
                'border': '1px solid #ccc',
                'resize': 'none'
            }
        ),

        html.Br(),
        html.Br(),

        html.Button(

            'Ask AI',

            id='ask_ai',

            n_clicks=0,

            style={
                'padding': '15px 30px',
                'fontSize': '16px',
                'backgroundColor': '#28a745',
                'color': 'white',
                'border': 'none',
                'borderRadius': '10px',
                'cursor': 'pointer'
            }
        ),

        html.Br(),
        html.Br(),

        html.Div(

            id='ai_response',

            children="AI responses will appear here...",

            style={

                'backgroundColor': '#ffffff',

                'padding': '25px',

                'borderRadius': '12px',

                'boxShadow': '0px 2px 10px rgba(0,0,0,0.1)',

                'fontSize': '18px',

                'lineHeight': '1.8',

                'whiteSpace': 'pre-wrap',

                'minHeight': '250px'
            }
        )

    ], style={

        'backgroundColor': '#f8f9fa',

        'padding': '30px',

        'borderRadius': '15px'

    })

], style={

    'padding': '40px',

    'fontFamily': 'Arial',

    'backgroundColor': '#eeeeee',

    'minHeight': '100vh'

})

# ---------------------------------------------------
# AI CALLBACK
# ---------------------------------------------------

@app.callback(

    Output('ai_response', 'children'),

    Input('ask_ai', 'n_clicks'),
    Input('q1', 'n_clicks'),
    Input('q2', 'n_clicks'),
    Input('q3', 'n_clicks'),
    Input('q4', 'n_clicks'),
    Input('q5', 'n_clicks'),
    Input('q6', 'n_clicks'),

    State('user_question', 'value')

)

def ai_assistant(
    ask_btn,
    q1,
    q2,
    q3,
    q4,
    q5,
    q6,
    question
):

    from dash import callback_context

    ctx = callback_context

    if not ctx.triggered:

        return "Ask a question about pizza sales."

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # ---------------------------------------------------
    # CLICKABLE QUESTIONS
    # ---------------------------------------------------

    if button_id == 'q1':

        question = "Which pizzas underperform?"

    elif button_id == 'q2':

        question = "Which pizzas should receive more promotion?"

    elif button_id == 'q3':

        question = "Suggest strategies to improve revenue"

    elif button_id == 'q4':

        question = "Suggest a new pizza likely to perform well"

    elif button_id == 'q5':

        question = "Which ingredients are most popular?"

    elif button_id == 'q6':

        question = "Which ingredients appear in top pizzas?"

    if not question:

        return "Please enter a question."

    # ---------------------------------------------------
    # PROMPT
    # ---------------------------------------------------

    prompt = f"""
    Pizza Sales Dataset

    Revenue:
    {total_revenue}

    Orders:
    {total_orders}

    Top Performing Pizzas:
    {top_pizza_text}

    Lowest Performing Pizzas:
    {bottom_pizza_text}

    Most Popular Ingredients:
    {top_ingredients_text}

    Ingredients Used In Top Pizzas:
    {best_ingredient_text}

    User Question:
    {question}

    Instructions:
    - Use only dataset context
    - Give business insight
    - Give recommendation
    - Keep concise
    """

    # ---------------------------------------------------
    # OLLAMA RESPONSE
    # ---------------------------------------------------

    response = ollama.chat(

        model='mistral',

        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],

        options={
            'num_predict': 220,
            'temperature': 0.1
            
        }
    )

    return response['message']['content']

# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
