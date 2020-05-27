import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.express as px
from tkinter.filedialog import askopenfilename

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# col_names = ["Task", "Group", "Participant", "Trial", "Saccade",
#              "Time", "Amplitude", "Peak Velocity", "Saccade-X", "Saccade-Y",
#              "Latency", "Pixel Distance", "Degree Distance", "Target-X", "Target-Y"]

csv_file_path = askopenfilename()
sacc_df = pd.read_csv(csv_file_path)

all_measures = ["Amplitude", "Peak Velocity","Latency", "Pixel Distance", "Degree Distance"]

plot_colors = {"GAP": 'blue',
               "MGS": 'orange',
               "VGS": 'green'}

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='yaxis-value',
            options=[{'label': i, 'value': i} for i in all_measures],
            value='Amplitude'
        )], style={'borderBottom': 'think lightgrey solid',
               'backgroundColor': 'rgb(250,250,250)',
               'padding': '10px 5px'}),

    html.Div([
        dcc.Graph(
            id='all-data-scatter',
            clickData={'points':[{'text': 'gapBL401ak',
                                  'customdata': 'GAP'}]}
        )], style={'display':'inline-block', 'width':'100%'}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='participant-scatter',
                clickData={'points': [{'customdata': 10}]}
            )]),
        html.Div([
            dcc.Graph(
                id='participant-histogram',
                # hoverData={'points': [{'pointNumbers': 0}, {'binNumber': 1}]},
                clear_on_unhover=True
            )]),

    ], style={'display': 'inline-block', 'width': '100%', 'columnCount': 2}),

    html.Div([
        html.Div([
            dcc.Graph(
                id='trial-scatter'
            )]),
        html.Div([
            dcc.Graph(
                id='pixel-space'
            )])
    ], style={'display': 'inline-block', 'width':'100%', 'columnCount':2})
])


@app.callback(
    dash.dependencies.Output('all-data-scatter', 'figure'),
    [dash.dependencies.Input('yaxis-value', 'value')])
def update_all_graph(plot_measure):
    # only participant means
    sacc_df_p = sacc_df[sacc_df['Level'] == "P"]

    traces = [(go.Scatter(
        x=sacc_df_p[sacc_df_p['Task'] == t]['Group'],
        y=sacc_df_p[sacc_df_p['Task'] == t][plot_measure],
        text=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        customdata=sacc_df_p[sacc_df_p['Task'] == t]['Task'],
        name=t,
        mode='markers',
        opacity=0.7,
        marker={
            'size':15
            # 'line':{'width':0.0, 'color':'white'}
        }
    )) for t in sacc_df_p.Task.unique()]

    return {
        'data': traces,
        'layout':
            go.Layout(
          title='Median across trials for each participant',
          xaxis_title = 'Group names',
          yaxis_title=plot_measure,
          hovermode = "closest"
            )
    }

@app.callback(
    dash.dependencies.Output('participant-histogram', 'figure'),
    [dash.dependencies.Input('all-data-scatter', 'clickData'),
     dash.dependencies.Input('yaxis-value', 'value')])
def update_participant_histogram(clickData_p, plot_measure):
    p_name = clickData_p['points'][0]['text']
    plot_col = plot_colors[clickData_p['points'][0]['customdata']]
    # only trial medians for given participant
    sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
    sacc_df_t = sacc_df_p[sacc_df_p['Level'] == "T"]

    counts, edges = np.histogram(sacc_df_t[plot_measure], bins=10)
    traces = (go.Histogram(
        x=sacc_df_t[plot_measure],
        hoverinfo='none',
        marker_color=plot_col,
        # text=["Bin count: " + str(c) for c in counts],
        # nbinsx=10
    ))
    return {
        'data': [traces],
        'layout':
            go.Layout(
          title='Histogram of trial data - (' + p_name + ')',
          xaxis_title = plot_measure,
          yaxis_title="Number of Trials",
          hovermode = "closest"
            )
    }



@app.callback(
    dash.dependencies.Output('participant-scatter', 'figure'),
    [dash.dependencies.Input('all-data-scatter', 'clickData'),
     dash.dependencies.Input('participant-histogram', 'hoverData'),
     dash.dependencies.Input('yaxis-value', 'value')])
def update_participant_scatter(clickData_p, hoverData, plot_measure):
    p_name = clickData_p['points'][0]['text']
    plot_col = plot_colors[clickData_p['points'][0]['customdata']]
    # only trial medians for given participant
    sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
    sacc_df_t = sacc_df_p[sacc_df_p['Level'] == "T"]
    traces = []
    traces.append(go.Scatter(
        x= sacc_df_t['Trial'],
        y=sacc_df_t[plot_measure],
        text=[("Trial " + str(l)) for l in sacc_df_t['Trial']],
        name="Trials",
        customdata=sacc_df_t['Trial'],
        mode='markers',
        opacity=0.5,
        marker={
            'size':15,
            'color': plot_col
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))
    if hoverData:
        x_vals = []
        y_vals = []
        labels = []
        # name_bin = "Bin #: " + str(hoverData['points'][0]['binNumber'])
        for p in hoverData['points'][0]['pointNumbers']:
            x_vals.append(list(sacc_df_t['Trial'])[int(p)])
            y_vals.append(list(sacc_df_t[plot_measure])[int(p)])
            labels.append(list(sacc_df_t['Trial'])[int(p)])
        traces.append(go.Scatter(
            x=x_vals,
            y=y_vals,
            text=[("Trial " + str(l)) for l in labels],
            # name=name_bin,
            customdata=sacc_df_t['Trial'],
            mode='markers',
            opacity=1.0,
            marker={
                'size':15,
                'color': plot_col
                # 'line':{'width':0.0, 'color':'white'}
            }
        ))
    return {
        'data': traces,
        'layout':
            go.Layout(
          title='Saccade with max. amplitude for each trial - (' + p_name + ')',
          xaxis_title = 'Trial number',
          yaxis_title=plot_measure,
          hovermode = "closest",
                showlegend=False
            )
    }

@app.callback(
    dash.dependencies.Output('trial-scatter', 'figure'),
    [dash.dependencies.Input('all-data-scatter', 'clickData'),
     dash.dependencies.Input('participant-scatter', 'clickData'),
     dash.dependencies.Input('yaxis-value', 'value')])
def update_trial_graph(clickData_p, clickData_t, plot_measure):
    p_name = clickData_p['points'][0]['text']
    plot_col = plot_colors[clickData_p['points'][0]['customdata']]
    trial_num = clickData_t['points'][0]['customdata']
    # only trial means for given participant
    sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
    sacc_df_t = sacc_df_p[sacc_df_p['Trial'] == trial_num]
    sacc_df_s = sacc_df_t[sacc_df_t['Level'] == "S"]
    traces=[]

    # plot all saccades in trial
    traces.append(go.Scatter(
        x=sacc_df_s['Saccade'],
        y=sacc_df_s[plot_measure],
        text=["Sacc. amp: " + str(l) for l in sacc_df_s['Amplitude']],
        # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        mode='markers',
        name='Saccades',
        opacity=0.7,
        marker={
            'size':15,
            'color': plot_col
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))

    # plot sacc with max amplitude separately
    max_a = np.max(sacc_df_s["Amplitude"])
    traces.append(go.Scatter(
        x=sacc_df_s[sacc_df_s["Amplitude"] == max_a]['Saccade'],
        y=sacc_df_s[sacc_df_s["Amplitude"] == max_a][plot_measure],
        hovertext=["Sacc. amp: " + str(max_a)],
        text="Max Amp",
        textposition="top right",
        cliponaxis=False,
        # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        mode='markers+text',
        name='Max Amplitude',
        opacity=1.0,
        marker={
            'size': 15,
            'color': 'red'
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))

    return {
        'data': traces,
        'layout':
            go.Layout(
          title='Each saccade in Trial ' + str(trial_num) + ' - (' + p_name + ')',
          xaxis_title = 'Saccade number',
          yaxis_title=plot_measure,
          hovermode = "closest",
                showlegend=False
                # legend = {'orientation':'h',
                #           'x':0,
                #           'y':-0.5}
            )
    }

@app.callback(
    dash.dependencies.Output('pixel-space', 'figure'),
    [dash.dependencies.Input('all-data-scatter', 'clickData'),
     dash.dependencies.Input('participant-scatter', 'clickData')])
def update_pixel_graph(clickData_p, clickData_t):
    p_name = clickData_p['points'][0]['text']
    plot_col = plot_colors[clickData_p['points'][0]['customdata']]
    trial_num = clickData_t['points'][0]['customdata']
    # only trial means for given participant
    sacc_df_p = sacc_df[sacc_df['Participant'] == p_name]
    sacc_df_t = sacc_df_p[sacc_df_p['Trial'] == trial_num]
    sacc_df_s = sacc_df_t[sacc_df_t['Level'] == "S"]
    traces = []

    # plot all saccades in trial
    traces.append(go.Scatter(
        x=sacc_df_s['Saccade-X'],
        y=sacc_df_s['Saccade-Y'],
        text=sacc_df_s['Saccade'],
        # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        hovertext = ["Sacc. #: " + str(n) for n in  sacc_df_s['Saccade']],
        mode='markers+text',
        textposition="bottom center",
        cliponaxis=False,
        opacity=0.7,
        name="Saccades",
        marker={
            'size':15,
            'color': plot_col
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))

    # plot target value separately
    traces.append(go.Scatter(
        x=sacc_df_s[sacc_df_s["Saccade"] == 0]['Target-X'],
        y=sacc_df_s[sacc_df_s["Saccade"] == 0]['Target-Y'],
        text="Target",
        # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        mode='markers+text',
        textposition="top right",
        cliponaxis=False,
        opacity=0.7,
        name="Target",
        hovertext="Target Position",
        marker={
            'size':15,
            'color': 'black'
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))

    # plot saccade with max amplitude separately
    max_a = np.max(sacc_df_s["Amplitude"])
    traces.append(go.Scatter(
        x=sacc_df_s[sacc_df_s["Amplitude"] == max_a]['Saccade-X'],
        y=sacc_df_s[sacc_df_s["Amplitude"] == max_a]['Saccade-Y'],
        text="Max Amp",
        hovertext=["Sacc #: " + str(n) for n in sacc_df_s[sacc_df_s["Amplitude"] == max_a]['Saccade']],
        # customdata=sacc_df_p[sacc_df_p['Task'] == t]['Participant'],
        mode='markers+text',
        textposition="top right",
        cliponaxis=False,
        name='Max Amp',
        opacity=1.0,
        marker={
            'size': 15,
            'color': 'red'
            # 'line':{'width':0.0, 'color':'white'}
        }
    ))

    return {
        'data': traces,
        'layout':
            go.Layout(
          title='Saccade positions in Trial ' + str(trial_num) + ' - (' + p_name + ')',
          xaxis_title = 'X',
          yaxis_title= 'Y',
          hovermode = "closest",
                showlegend=False
                # legend={'orientation': 'h',
                #         'x': 0,
                #         'y': -0.25}
            )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
