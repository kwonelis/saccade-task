import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import pandas as pd
# import plotly.graph_objs as go

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # col_names = ["Task", "Group", "Participant", "Trial", "Saccade",
# #              "Time", "Amplitude", "Peak Velocity", "Saccade-X", "Saccade-Y",
# #              "Latency", "Pixel Distance", "Degree Distance", "Target-X", "Target-Y"]

# sacc_df = pd.read_csv('https://raw.githubusercontent.com/kwonelis/SaccadeData/master/all_single_saccade_data.csv')
# all_measures = ["Amplitude", "Peak Velocity","Latency", "Pixel Distance", "Degree Distance"]


# app.layout = html.Div([
#   html.Div([ 
#     html.Div([
#       dcc.Dropdown(
#         id='yaxis-value',
#         options=[{'label': i, 'value': i} for i in all_measures],
#         value='Latency'
#         )
#     ])
#   ], style={'borderBottom': 'think lightgrey solid', 
#                 'backgroundColor': 'rgb(250,250,250)',
#                 'padding': '10px 5px'}),
#   html.Div([
#     dcc.Graph(
#       id='all-data-scatter',
#       clickData={'points':[{'text': 'gapBL401ak'}]}
#     )
#   ], style={'display': 'inline-block', 'width': '49%', 'padding': '0 20'}),

#   html.Div([
#     dcc.Graph(id='participant-scatter', clickData={'points':[{'customdata': 1}]}),
#     dcc.Graph(id='trial-scatter'),
#     dcc.Graph(id='pixel-space')
#   ], style={'display': 'inline-block', 'width': '49%'})
# ])


# @app.callback(
#     dash.dependencies.Output('all-data-scatter', 'figure'),
#     [dash.dependencies.Input('yaxis-value', 'value')])
# def update_all_graph(plot_measure):
#     # only participant means
#     sacc_df_p = sacc_df[sacc_df['Level'] == "P"]
#     traces = [(go.Scatter(
#         x=sacc_df_p[sacc_df_p['Task'] == t]['Group'],
#         y=sacc_df_p[sacc_df_p['Task'] == t][plot_measure],
#         text=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
#         # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
#         name=t,
#         mode='markers',
#         opacity=0.7,
#         marker={
#             'size':15
#             # 'line':{'width':0.0, 'color':'white'}
#         }
#     )) for t in sacc_df_p.Task.unique()]

#     return {
#         'data': traces,
#         'layout':
#             go.Layout(
#           title='Median across trials for each participant',
#           xaxis_title = 'Group names',
#           yaxis_title=plot_measure,
#           hovermode = "closest"
#             )
#     }

# @app.callback(
#     dash.dependencies.Output('participant-scatter', 'figure'),
#     [dash.dependencies.Input('all-data-scatter', 'clickData'),     
#      dash.dependencies.Input('yaxis-value', 'value')])
# def update_participant_graph(clickData_p, plot_measure):
#     p_name = clickData_p['points'][0]['text']
#     # only trial means for given participant
#     sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
#     sacc_df_t = sacc_df_p[sacc_df_p['Level'] == "T"]
#     traces = (go.Scatter(
#         x=sacc_df_t['Trial'],
#         y=sacc_df_t[plot_measure],
#         text="Trial" + str(sacc_df_t['Trial']),
#         customdata=sacc_df_t['Trial'],
#         mode='markers',
#         opacity=0.7,
#         marker={
#             'size':15
#             # 'line':{'width':0.0, 'color':'white'}
#         }
#     ))

#     return {
#         'data': [traces],
#         'layout':
#             go.Layout(
#           title='Medians for each trial - (' + p_name + ')',
#           xaxis_title = 'Trial number',
#           yaxis_title=plot_measure,
#           hovermode = "closest"
#             )
#     }

# @app.callback(
#     dash.dependencies.Output('trial-scatter', 'figure'),
#     [dash.dependencies.Input('all-data-scatter', 'clickData'),     
#      dash.dependencies.Input('participant-scatter', 'clickData'),
#      dash.dependencies.Input('yaxis-value', 'value')])
# def update_trial_graph(clickData_p, clickData_t, plot_measure):
#     p_name = clickData_p['points'][0]['text']
#     trial_num = clickData_t['points'][0]['customdata']
#     # only trial means for given participant
#     sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
#     sacc_df_t = sacc_df_p[sacc_df_p['Trial'] == trial_num]
#     sacc_df_s = sacc_df_t[sacc_df_t['Level'] == "S"]
#     traces = (go.Scatter(
#         x=sacc_df_s['Saccade'],
#         y=sacc_df_s[plot_measure],
#         text="Saccade " + str(sacc_df_s['Saccade']),
#         # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
#         mode='markers',
#         opacity=0.7,
#         marker={
#             'size':15
#             # 'line':{'width':0.0, 'color':'white'}
#         }
#     ))

#     return {
#         'data': [traces],
#         'layout':
#             go.Layout(
#           title='Each saccade in Trial ' + str(trial_num) + ' - (' + p_name + ')',
#           xaxis_title = 'Saccade number',
#           yaxis_title=plot_measure,
#           hovermode = "closest"
#             )
#     }

# @app.callback(
#     dash.dependencies.Output('pixel-space', 'figure'),
#     [dash.dependencies.Input('all-data-scatter', 'clickData'),     
#      dash.dependencies.Input('participant-scatter', 'clickData')])
# def update_pixel_graph(clickData_p, clickData_t):
#     p_name = clickData_p['points'][0]['text']
#     trial_num = clickData_t['points'][0]['customdata']
#     # only trial means for given participant
#     sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
#     sacc_df_t = sacc_df_p[sacc_df_p['Trial'] == trial_num]
#     sacc_df_s = sacc_df_t[sacc_df_t['Level'] == "S"]
#     traces = []
#     traces.append(go.Scatter(
#         x=sacc_df_s['Saccade-X'],
#         y=sacc_df_s['Saccade-Y'],
#         text="Saccade " + str(sacc_df_s['Saccade']),
#         # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
#         mode='markers',
#         opacity=0.7,
#         name="Saccades",
#         marker={
#             'size':15
#             # 'line':{'width':0.0, 'color':'white'}
#         }
#     ))
#     traces.append(go.Scatter(
#         x=sacc_df_s[sacc_df_s["Saccade"] == 0]['Target-X'],
#         y=sacc_df_s[sacc_df_s["Saccade"] == 0]['Target-Y'],
#         text="Target",
#         # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
#         mode='markers',
#         opacity=0.7,
#         name="Target",
#         marker={
#             'size':15
#             # 'line':{'width':0.0, 'color':'white'}
#         }
#     ))

#     return {
#         'data': traces,
#         'layout':
#             go.Layout(
#           title='Saccade positions in Trial ' + str(trial_num) + ' - (' + p_name + ')',
#           xaxis_title = 'X',
#           yaxis_title= 'Y',
#           hovermode = "closest"
#             )
#     }

# if __name__ == '__main__':
#     app.run_server()
