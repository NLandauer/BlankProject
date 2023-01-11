# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:\Users\noell\PycharmProjects\Dash1\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site_dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                             value='ALL',
                                             placeholder='Select a launch site',
                                             searchable=True
                                             ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload_slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0', 100: '100'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_chart(entered_site):
    all_data = spacex_df
    filtered_data = spacex_df[spacex_df["Launch Site"] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(all_data,
                     values='class',
                     names='Launch Site',
                     title='Total Successful Launches Across All Sites')
        return fig
    else:
        fig = px.pie(filtered_data,
                     names='class',
                     title=('Total Successful Launches for Site ' + entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'),
              Input(component_id='payload_slider', component_property='value'))
def get_scatter_slider(entered_site, entered_payload):
    all_data = spacex_df
    filtered_data = spacex_df[spacex_df["Launch Site"] == entered_site]
    if entered_site == 'ALL':
        fig = px.scatter(all_data,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Correlation Between Payload Mass and Launch Success Across All Sites')
        return fig.update_xaxes(range=entered_payload)
    else:
        fig = px.scatter(filtered_data,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=('Correlation Between Payload Mass and Launch Success at Site ' + entered_site))
        return fig.update_xaxes(range=entered_payload)


# Run the app
if __name__ == '__main__':
    app.run_server()
