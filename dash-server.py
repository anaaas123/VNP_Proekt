import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv('lc-processed.csv')
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['Month'] = df['DateTime'].dt.to_period('M').astype(str)
grouped_by_month = df.groupby(['Month', 'sentiment']).size().reset_index(name='Count')
grouped_by_country = df.groupby(['country', 'sentiment']).size().reset_index(name='Count')
color_map = {'positive': 'green', 'neutral': 'gray', 'negative': 'red'}

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout for the different pages
# Define the layout for the different pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav(className='navbar navbar-expand-lg navbar-light bg-light', children=[
        html.Div(className='container', children=[
            html.A(className='navbar-brand', href='/', children='Long COVID Data Visualization'),
            dcc.Link('Overview', className='nav-link', href='/'),
            dcc.Link('Timelapse', className='nav-link', href='/by-month'),
            dcc.Link('By Country', className='nav-link', href='/by-country'),
        ])
    ]),
    html.Div(id='page-content')
])

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <title>{%title%}</title>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# Define the callback to update the page content
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return create_figure1()
    elif pathname == '/by-month':
        return create_figure2()
    elif pathname == '/by-country':
        return create_figure3()
    else:
        return '404 - Page not found'

def create_figure1():
    fig1 = px.bar(grouped_by_month, x='Month', y='Count', color='sentiment',
                 color_discrete_map=color_map,
                 title='Sentiment of Tweets Over Time',
                 labels={'Month': 'Month', 'Count': 'Tweet Count', 'sentiment': 'Sentiment'},
                 category_orders={'sentiment': ['positive', 'neutral', 'negative']})
    return dcc.Graph(figure=fig1)

def create_figure2():
    fig2 = px.bar(grouped_by_month, x='sentiment', y='Count', color='sentiment',
                 color_discrete_map=color_map,
                 title='Sentiment of Tweets By Month',
                 labels={'Count': 'Tweet Count', 'sentiment': 'Sentiment'},
                 animation_frame='Month',
                 category_orders={'sentiment': ['positive', 'neutral', 'negative']})
    fig2.update_xaxes(title='Sentiment')
    fig2.update_layout(barmode='relative', xaxis={'type': 'category'})
    fig2.update_yaxes(range=[0, 2500])
    return dcc.Graph(figure=fig2)

def create_figure3():
    fig3 = px.bar(grouped_by_country, x='country', y='Count', color='sentiment',
                 color_discrete_map=color_map,
                 title='Sentiment of Tweets by Country',
                 labels={'country': 'Country', 'Count': 'Tweet Count', 'sentiment': 'Sentiment'})
    return dcc.Graph(figure=fig3)


if __name__ == '__main__':
    app.run_server(debug=False)
#%%

#%%
