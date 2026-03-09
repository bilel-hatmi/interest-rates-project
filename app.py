import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sub
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import base64
from plot_tree import plot_tree 
from hjm import build_forward_rates
from ho_lee import price_call_option


app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
app.title = "QuantCS: Pricing a Caplet"
server = app.server

logo_cs = 'projet-st-finance/img/logo_cs.png' # replace with your own image
encoded_image_cs = base64.b64encode(open(logo_cs, 'rb').read())

logo_univ = 'projet-st-finance/img/logo_univ.png' 
encoded_image_univ = base64.b64encode(open(logo_univ, 'rb').read())

logo = 'img/dall_e.png'
encoded_image_logo = base64.b64encode(open(logo, 'rb').read())



app.layout = dbc.Container(
    [
        dbc.Row(
            [dbc.Col([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_logo.decode()), style={'height':'60px', 'width':'90px'} ),
                ], width=1),
                dbc.Col(
                    [
                        html.H2("The Interest Rate Lab: Pricing a Caplet", className='text-center'),
                    ],
                    width=True,
                ),
                dbc.Col([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_cs.decode()), style={'height':'45px', 'width':'90px'} ),
                ], width=1), 
                dbc.Col([
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_univ.decode()), style={'height':'45px', 'width':'110px'} ),
                ], width=1),

            ],
            align="end",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H5('General Parameters of the Caplet'),
                                
                                html.P("Maturity (in years):"),
                                dcc.Input(id="T", value=1, type="number"),

                                html.P("Tenor (in months):"), 
                                dcc.Input(id="tenor", value=6, type="number"),

                                html.P("Number of Steps"),
                                dcc.Input(id='N', value=10, type='number'),

                                html.P("Zero-Coupon Rate (in %):"),
                                dcc.Slider(
                                    id="zc_rate", #to divide by 100 later on
                                    min=1.0,
                                    max=10,
                                    step=1,
                                    value=3,
                                    
                                ),


                                # dcc.Input(id='input', value='', type='text'),
                                html.Button('Show Current Rate', id='submit_cr', n_clicks=0),
                                html.Div(id='output_cr'),



                                html.P("Payoff"),
                                html.Div(children=[
                                dcc.Input(id="payoff_func", value="x-0.03 if x>=0.03 else 0", type="text"),
                                html.Div(id="output_pf")]),

                                html.H5('HJM Parameters'),

                                html.P('Volatility'), 
                                dcc.Input(id='sigma', value=0.2, type='number'),

                                html.P('Parameter pi'),
                                dcc.Input(id='pi', value=0.5, type='number'),

                                html.P('Parameter q'),
                                dcc.Input(id='q', value=0.5, type='number'),
                                html.P(''),

    
                                html.Button('Price with HJM !', id='submit_hjm', n_clicks=0),
                                html.Div(id='output_hjm'),

                                html.Button('Price with normalized Ho-Lee !', id='submit_hl', n_clicks=0),
                                html.Div(id='output_hl'),

                                html.Button('Generate Tree Plot !', id='submit_tree'),

                            ]
                        ),

                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                
                    dcc.Graph(id="tree_plot", style={"height": "100vh"}),
                
                        
                    ],
                    width=True,
                ),
            ]
        ),
        html.Hr(),
    ],
    fluid=True,
)
    




def plot_the_tree(pi, delta, rate, N, T, tenor, payoff_func):
    return plot_tree(pi, delta, rate, N, T, tenor, payoff_func)

@app.callback(
    Output('tree_plot', 'figure'),
    [Input('submit_tree', 'n_clicks'),
        Input('pi', 'value'),
        Input('q', 'value'),
        Input('zc_rate', 'value'),
        Input('N', 'value'),
        Input('T', 'value'),
        Input('tenor', 'value'),
        Input('payoff_func', 'value'),
        Input('sigma', 'value')
    ]
    
)


def update_tree_plot(n_clicks, pi, q, zc_rate, N, T, tenor, payoff_func, sigma):

    if n_clicks is None:
        # The button has not been clicked yet
        return {}
    else:

        def payoff_f(x):
            return eval(payoff_func, {"__builtins__": None}, {"x": x, **globals()})
        
        def q_to_delta_time(q_param, delta_time):
            return np.exp((-sigma*delta_time**(3/2))/np.sqrt((q_param*(1-q_param))))
        
        delta = q_to_delta_time(q, 1/N)

        fig = plot_the_tree(pi, delta, zc_rate/100, N, T, tenor, payoff_f)

        return fig









def compute_current_rate(N, tenor, zc_rate):
    delta_time = 1/N
    tau = tenor/12
    n = tau/delta_time 
    n = round(n)
    price = np.exp(-zc_rate*(n/N))
    current_rate=(1-price)/(tau*price)
    return current_rate

@app.callback(
    Output('output_cr', 'children'),
    [Input('submit_cr', 'n_clicks'),
        Input('N', 'value'),
        Input('tenor', 'value'),
        Input('zc_rate', 'value')
     ]
    )

def update_output_cr(n_clicks, N, tenor, zc_rate):
    if n_clicks > 0:
        current_rate = compute_current_rate(N, tenor, zc_rate/100)
        return f'The current rate is {current_rate}.'



@app.callback(
    dash.dependencies.Output("output_pf", "children"),
    [dash.dependencies.Input("payoff_func", "value")])


def update_output_pf(input_value):
    try:

        # Transform the input string into a function
        def f(x):
            return eval(input_value, {"__builtins__": None}, {"x": x, **globals()})
        
        return html.Div([
            html.P(f"The function is f(x) = {input_value}"),
        ])
    except Exception as e:
        return html.Div([
            html.P(f"Invalid input: {e}")
        ])




def pricing_hjm(sigma, pi, q, f0, T, N, tenor, payoff_func):
    price = build_forward_rates(sigma, pi, q, f0, T, N, tenor, payoff_func)[-1]
    return price

@app.callback(
    Output('output_hjm', 'children'),
    [Input('submit_hjm', 'n_clicks'),
     Input('zc_rate', 'value'),
        Input('sigma', 'value'),
        Input('pi', 'value'),
        Input('q', 'value'),
        Input('T', 'value'),
        Input('N', 'value'),
        Input('tenor', 'value'),
        Input('payoff_func', 'value')
        ]
        
)

def update_output_hjm(n_clicks, zc_rate, sigma, pi, q, T, N, tenor, payoff_func):
    if n_clicks>0:

        def payoff_f(x):
            return eval(payoff_func, {"__builtins__": None}, {"x": x, **globals()})
        
        delta_time = 1/N
        tau = tenor/12
        n = tau/delta_time 
        n = round(n)
        p0 = [np.exp(-(zc_rate/100)*delta_time*i) for i in range(N*T+n+1)]
        f0 = []

        for i in range(N*T+n):
            f0.append(-np.log(p0[i+1]/p0[i])/delta_time)
        
        price = pricing_hjm(sigma, pi, q, f0, T, N, tenor, payoff_f)
        return f'The HJM price is {price}.'





def pricing_hl(pi, delta, rate, N, T, tenor, payoff_func):
    return price_call_option(pi, delta, rate, N, T, tenor, payoff_func)[0,0]
    
@app.callback(
    Output('output_hl', 'children'),
    [Input('submit_hl', 'n_clicks'),
        Input('pi', 'value'),
        Input('zc_rate', 'value'),
        Input('N', 'value'),
        Input('T', 'value'),
        Input('tenor', 'value'),
        Input('payoff_func', 'value'),
        Input('sigma', 'value'),
        Input('q', 'value')
    ]
)

def update_output_hl(n_clicks, pi, zc_rate, N, T, tenor, payoff_func, sigma, q):

    if n_clicks>0:

        def payoff_f(x):
            return eval(payoff_func, {"__builtins__": None}, {"x": x, **globals()})
        
        def q_to_delta_time(q_param, delta_time):
            return np.exp((-sigma*delta_time**(3/2))/np.sqrt((q_param*(1-q_param))))
        
        delta = q_to_delta_time(q, 1/N)
        
        price = pricing_hl(1-pi, delta, zc_rate/100, N, T, tenor, payoff_f)

        return f'The Ho-Lee price is {price}.'





if __name__ == "__main__":
    app.run_server(debug=False)
