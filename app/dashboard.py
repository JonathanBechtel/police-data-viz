from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# load the dataframe
df = pd.read_csv('data/per_capita_crime.csv')

# function to get the data for the dashboard
app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Per Capita Crime By Race in Chicago', style={'textAlign':'center'}),
    dcc.Dropdown(df.year.unique().tolist() + ['Total'], 'Total', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def build_per_capita_crime_plot(year):
    """Takes an input for year to filter, then calculates plotly chart for 
    per capita crime rates"""

    if year == 'Total':
        grouping = df.groupby(['subject_race']).sum()

    else:
        year = int(year)

        temp_df = df.loc[df.year == year].copy()

        grouping = temp_df.groupby(['subject_race']).sum()

    fig = px.bar(grouping['crime'] / grouping['population'], 
                 title = f'Per Capita Crime By Race For Year: {year}')
    fig.update_layout({
        'yaxis': {'title': 'Per Capita Crime Rate'},
        'xaxis': {'title': 'Subject Race'}
    })

    return fig

if __name__ == '__main__':
    app.run(debug=True)
