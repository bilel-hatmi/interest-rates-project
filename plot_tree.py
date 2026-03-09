import numpy as np 
import plotly.graph_objects as go
from ho_lee import price_call_option



def y_n(T):
    y_n = [0]
    for i in range(1, T+1):
        y_n.extend([j for j in range(-i, i+1, 2)])
    return y_n

def y_n_app(T):
    y_n = [[0]]
    for i in range(1, T+1):
        y_n.append([j for j in range(-i, i+1, 2)])
    return y_n
    
def build_nodes(T):
    Xn_app = [[i for _ in range(i+1)] for i in range(T+1)]
    Xn = [item for sublist in Xn_app for item in sublist]
    Yn = y_n(T)

    Xe, Ye = [], []
    y_app = y_n_app(T)
    for i in range(T):
        for j in range(len(Xn_app[i])):
            Xe += [i, i+1, None]
            Xe += [i, i+1, None]
            Ye += [y_app[i][j], y_app[i][j]+1, None]
            Ye += [y_app[i][j], y_app[i][j]-1, None]
    return Xn, Yn, Xe, Ye            
                



def plot_tree(pi, delta, rate, N, T, tenor, payoff_func):

    pricing = price_call_option(pi, delta, rate, N, T, tenor, payoff_func)
    pricing = np.round(pricing, 4)
    Xn, Yn, Xe, Ye = build_nodes(N*T)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Xe,
                    y=Ye,
                    mode='lines',
                    line=dict(color='rgb(210,210,210)', width=1),
                    hoverinfo='none'
                    ))
    fig.add_trace(go.Scatter(x=Xn,
                    y=Yn,
                    mode='markers',
                    marker=dict(symbol='circle-dot',
                                    size=37,
                                    color='#6175c1',    #'#DB4551',
                                    line=dict(color='rgb(50,50,50)', width=1)
                                    ),
                    text='',
                    hoverinfo='text',
                    opacity=0.8
                    ))

    def make_annotations(prices, font_size=10, font_color='rgb(250,250,250)'):
        m, _ = np.shape(prices)
        T = m-1
        Xn_app = [[i for _ in range(i+1)] for i in range(T+1)]
        Yn_app = y_n_app(T)

        annotations = []
        
        for j in range(m):
            for i in range(j+1):
                annotations.append(
                    dict(
                        text=str(prices[i][j]), # or replace labels with a different list for the text within the circle
                        x=Xn_app[j][i], y=Yn_app[j][i],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
        return annotations

    axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=True,
                showticklabels=False,
                )

    fig.update_layout(title= 'Pricing Contingent Claims with Ho-Lee Model',
                annotations=make_annotations(pricing),
                font_size=12,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(l=40, r=40, b=85, t=100),
                hovermode='closest',
                plot_bgcolor='rgb(248,248,248)'
                )



    return fig 


## example of use:

# rate = 0.03
# T=1
# N=10
# tenor=6
# pi = 0.5
# delta = 0.999
# def payoff_func(x):
#     return x-0.03
# X = np.zeros((N*T+1, N*T+1))


# fig = plot_tree(pi, delta, rate, N, T, tenor, payoff_func)
# fig.show()

