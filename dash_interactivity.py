import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app = dash.Dash(__name__)

app.title = "SpaceX Launch Records Dashboard"

app.layout = html.Div([html.H1("SpaceX Launch Records Dashboard",
                            style={'textAlign':'center','color':'#503D36','font=size':24}),
                        html.Div([
                            html.Label("Select Launch Site:"),
                                dcc.Dropdown(id='site-dropdown', 
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL Sites'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                            ],
                                        placeholder='Select Launch Site',
                                        searchable=True,
                                        style={'width': '80%', 'padding': '3px', 'text-align-last': 'center'})
                                ]),
                        html.Div([
                                html.Div(dcc.Graph(id='success-pie-chart'))]),
                        html.Div([
                            html.Label('Payload range (Kg)'),
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                    marks={0: '0.00',2500: '2500.00', 5000:'5000.00',7500:'7500.00',10000:'10000.00'}, 
                                    value=[0, 10000])
                              ]),
                        html.Div([
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))]) 
                        ])

# Define the callback function to update the input container based on the selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):

    if entered_site =='ALL Sites': 
        grouped_data= data.groupby('Launch Site')['class'].sum().reset_index()
        fig1 = px.pie(grouped_data, values='class',
        names='Launch Site',
        title='Total Success Launches By Site')
        return fig1
    else:
    # return the outcomes piechart for a selected site
        site_data = data[data['Launch Site'] == entered_site]
        count_data = site_data.groupby('class')['Launch Site'].count().reset_index()
        Title = 'Total Success Launches for site ' + str(entered_site)
        fig2 = px.pie(count_data,values='Launch Site',names='class',
                                title=Title)
        return fig2

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
     [Input(component_id='site-dropdown', component_property='value'), 
     Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(entered_site, value):

    if entered_site =='ALL Sites': 
        Title = 'Correlation between Payload and Success for all Sites'
        fig3 = px.scatter(data,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=Title)
        fig3.update_xaxes(range = value)
        return fig3
    else:
        Title = 'Correlation between Payload and Success for ' + str(entered_site)
        site_data = data[data['Launch Site'] == entered_site]
        fig4 = px.scatter(site_data,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=Title)
        fig4.update_xaxes(range = value)
        return fig4


# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)