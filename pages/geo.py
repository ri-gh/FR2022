from __future__ import annotations
import dash
from dash import html, dash_table, callback
from dash import dcc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


df = pd.read_csv('last_df.csv')

city_list = df['Libellé de la commune'].unique().tolist()
dept_list = df['Libellé du département'].unique().tolist()
abst = round(df.groupby('Libellé du département')['% Abs/Ins'].mean(),2)


table_abst_per_dept = pd.DataFrame(abst)
table_abst_per_dept = table_abst_per_dept.rename(columns={'% Abs/Ins':'Abstention score'})
table_abst_per_dept['Departement'] = table_abst_per_dept.index
table_abst_per_dept = table_abst_per_dept.sort_values('Abstention score',ascending= False)
table_abst_per_dept = table_abst_per_dept[['Departement','Abstention score']].reset_index(drop=True)

for i in range(0,len(table_abst_per_dept)):
        table_abst_per_dept['Abstention score'][i] = (str(table_abst_per_dept['Abstention score'][i])) +str(' %')



#we have to create columns first for DataTable
columns_table = [{'name': 'Departement', 'id': 'Departement'}, 
 {'name': 'Vote abstention', 'id': 'Vote abstention'},
 {'name': 'Blanc voted', 'id': 'Blanc voted'},
 {'name': 'Null voted', 'id': 'Null voted'}]

columns_table_results_city = [{'name': 'Candidate', 'id': 'Candidate'}, 
 {'name': 'Score', 'id': 'Voix'}]

columns_table_city = [{'name': 'City', 'id': 'City'}, 
{'name': 'Vote abstention', 'id': 'Vote abstention'},
{'name': 'Blanc voted', 'id': 'Blanc voted'},
{'name': 'Null voted', 'id': 'Null voted'}]


logo = 'https://avatars0.githubusercontent.com/u/5997976?s=400&v=4'

app = dash.Dash(__name__,suppress_callback_exceptions=True)
server= app.server,

app.scripts.config.serve_locally = True

dash.register_page(__name__)


layout = html.Div(children=[    html.Div(                
            dbc.Row(
                [   #logo
                    dbc.Col(html.Img(src=logo, height="40px", style={'padding-left': '20px'})),
                ])),
    html.Div([
        html.Div(children=html.H5(children="Let's see some statistics by departement:",
    style={'textAlign' : 'center'}),id='title-page'),
    html.Div(children=html.P(children="Select a departement:")),
    dcc.Dropdown(id="select-departement",
    options=sorted([{"label": dept, "value":dept} for dept in dept_list], key = lambda x: x['label']),
    value="Hauts-de-Seine",
    placeholder='Select a departement...'),

    html.Div(children=html.H3(children=" ")),
    dcc.Graph(id="result-per-dept",className='notest'),
    html.Div(children=html.H3(children=" ")),
    dash_table.DataTable(id="abst-cities-table",
    data=[],
    fill_width=False,
        style_cell={'textAlign': 'center'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)'
    },
    style_header={
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'
    },
    style_table={'margin-left': '40vw', 'margin-top': '3vw'})]),

    dcc.Graph(id="abst-dept",className='test'),
    html.Div(children=html.H3(children=" "),),

    html.Div(children=html.H5(children="Let's analyze the results by city for the selected departement:",
    style={'textAlign' : 'center'})),
    html.Div(children=html.H3(children=" "),),
    html.Div(id="dep-city-results-div"),
    dbc.NavLink("If you don't know in which departement a city is located, no worries, just click here",href="#city_straight",external_link=True),
    #to create a link to navigate in another section of the same page
    dcc.Dropdown(id='select-dep-city',
    value="",
    placeholder='Choose a city from the selected departement...',),
    dcc.Graph(id="dep-city-results",className='test'),

    html.Div(children=html.H3(children=" ")),
    dash_table.DataTable(id="result-cities-table-city",
    data=[],
    fill_width=False,
    style_cell={'textAlign': 'center',
                    'font_size': '15px'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)',
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'color': 'rgb(159, 241, 253)',
            'backgroundColor': 'black',
        }
    ],
    style_header={'textAlign': 'center',
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'},
    style_table={'margin-left': '40vw', 'margin-top': '3vw'}),

    dcc.Graph(id= "stats-dep-per-city",className='test'),
    
    html.Div(children=html.H3(children=" ")),
    dash_table.DataTable(id="abst-cities-table-city",
    data=[],
    fill_width=False,
        style_cell={'textAlign': 'center',
                        'font_size': '15px'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)'
    },
    style_header={'textAlign': 'center',
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'
    },
    style_table={'margin-left': '40vw', 'margin-top': '3vw'}),
    html.Br(),

    html.Div(children=html.P(children="Choose the city you are looking for in the list below:"),id= "city_straight",),
    dcc.Dropdown(id="select-city",
    options=sorted([{"label": city, "value":city} for city in city_list], key = lambda x: x['label']),
    value="",
    placeholder='Select a city...',),
    html.Div(id="city-div"),
    dcc.Graph(id="result-per-city",className='test'),
        html.Div(children=html.H3(children=" ")),
    dash_table.DataTable(id="abst-cities-table-dunno-dept",
    data=[],
    fill_width=False,
        style_cell={'textAlign': 'center',
                        'font_size': '15px'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'color': 'rgb(159, 241, 253)',
            'backgroundColor': 'black',
        }],
    style_header={'textAlign': 'center',
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'
    },
    style_table={'margin-left': '40vw', 'margin-top': '3vw'}),
    dcc.Graph(id="stats-per-city",className='test'),

    html.Div(children=html.H3(children=" ")),
    dash_table.DataTable(id="abst-table-city",
    data=[],
    fill_width=False,
        style_cell={'textAlign': 'center',
                        'font_size': '15px'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)'
    },
    style_header={'textAlign': 'center',
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'
    },
    style_table={'margin-left': '40vw', 'margin-top': '3vw'}),
    html.Br(),
    dbc.NavLink("Let's go higher",href="#title-page",external_link=True),
    html.Br()

    ])


@callback(
    dash.dependencies.Output("result-per-dept", "figure"),
    dash.dependencies.Output("result-per-dept", "className"),
    dash.dependencies.Input("select-departement", "value"))

def resultcitypie(deptmt: str in dept_list):
    
    dfdep = df[df['Libellé du département'] == deptmt]
    test = pd.DataFrame(round(dfdep.groupby('Nom')['Voix'].sum()/(dfdep['Voix'].sum())*100,2))

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.5],
        specs=[[{"type": "pie"}, {"type": "bar"}]])

    fig.add_trace(go.Pie(labels=test.index,
                                values=test['Voix'],
                            legendgroup="group",
                            name='Results',
        textinfo='percent+label',
        textfont={'color':"rgb(159, 241, 253)","size":12},
        hovertemplate="<br>".join(["Department: {}".format(deptmt),
    "Candidate: %{label}",
    "Score : %{percent}"])),
        row=1, col=1)
    fig.update_traces(hole=.5)
   
    fig.add_trace(go.Bar(x=test.index, y=test['Voix'],marker_color=test['Voix'],legendgroup="group",
    name='Bar chart',
    hovertemplate="<br>".join(["Department: {}".format(deptmt),
    "Candidate: %{label}",
    "Score : %{y}%"])),row=1, col=2)

    fig.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
    fig.update_yaxes(color="rgb(159, 241, 253)") #change color of yaxes labels
    fig.update_layout(
    xaxis={'categoryorder':'total descending'},
    yaxis_title="Score (%)",
    legend_title_font_color="rgb(159, 241, 253)",
    legend=dict(font=dict(color="rgb(159, 241, 253)")), #to change color of the legend 
    title = "2022 french presidential elections first round final results in {}".format(deptmt),
    title_font_color="rgb(159, 241, 253)",#to change the color of the figure title
    showlegend=True,
    plot_bgcolor="black",#to change the background of the plot
    paper_bgcolor="black")

    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("abst-cities-table", "data"),
    dash.dependencies.Output("abst-cities-table", "columns"),
    dash.dependencies.Input("select-departement", "value"))

def tab_stats(deptmt: str in dept_list):
    dfdep = df[df['Libellé du département'] == deptmt].reset_index(drop=True)

    stats_figures = pd.DataFrame(round(dfdep.groupby('Libellé du département')['% Abs/Ins'].mean(),2))
    stats_figures['Departement'] = stats_figures.index
    stats_figures['Blanc voted'] = (round(dfdep.groupby('Libellé du département')['% Blancs/Vot'].mean(),2))
    stats_figures['Null voted'] = (round(dfdep.groupby('Libellé du département')['% Nuls/Vot'].mean(),2))
    stats_figures= stats_figures.rename(columns={'% Abs/Ins':'Vote abstention'})
    stats_figures= stats_figures[['Departement','Vote abstention','Blanc voted','Null voted']].reset_index(drop=True)
    for i in range(0,len(stats_figures)):
        stats_figures['Vote abstention'][i] = str(stats_figures['Vote abstention'][i])
        stats_figures['Vote abstention'][i] = (stats_figures['Vote abstention'][i])+ str(' %')
        stats_figures['Blanc voted'][i] = str(stats_figures['Blanc voted'][i])
        stats_figures['Blanc voted'][i] = (stats_figures['Blanc voted'][i])+ str(' %')
        stats_figures['Null voted'][i] = str(stats_figures['Null voted'][i])
        stats_figures['Null voted'][i] = (stats_figures['Null voted'][i])+ str(' %')

    return stats_figures.to_dict(orient='records'),columns_table


@callback(
    dash.dependencies.Output("abst-dept", "figure"),
    dash.dependencies.Output("abst-dept", "className"),
    dash.dependencies.Input("select-departement", "value"))

def resultdeptabst(deptmt: str in dept_list):

    dfabs = df[df['Libellé du département'] == deptmt]
    test2 = pd.DataFrame(round(dfabs.groupby('Libellé de la commune')['% Abs/Ins'].mean(),2))

    fig = px.bar(test2,x=test2.index, y=test2['% Abs/Ins'],
    color='% Abs/Ins',
    title ="Vote abstention (%) by city for departement of {} ({})".format(deptmt,dfabs['Code du département'].unique()[0]))

    fig.update_layout(legend = dict(bgcolor = 'rgb(159, 241, 253)'),   
        xaxis={'categoryorder':'total descending'},
    title_font_color="rgb(159, 241, 253)",
    legend_title_font_color="rgb(159, 241, 253)",
    yaxis_title = 'Abstention score (%)',
    xaxis_title = 'Cities of {}'.format(deptmt),
    plot_bgcolor="black",
    paper_bgcolor="black")
    fig.layout.yaxis.color = 'rgb(159, 241, 253)'
    fig.layout.xaxis.color = 'rgb(159, 241, 253)'
    fig.update_traces(
    hovertemplate="<br>".join(["Department: {}".format(deptmt),
    "City: %{label}",
    "Abstention : %{y}%"]))

    return fig, "visible-graph"


@callback(
    dash.dependencies.Output("dep-city-results-div", "children"),
    dash.dependencies.Input("select-departement", "value"))
def display_name_dept(deptmt):
    # We return an P HTML component with the dept name.
    return html.P(children=f"Choose one of the city from the selected departement of {deptmt} ({df[df['Libellé du département'] == deptmt]['Code du département'].values[0]})")


@callback(
    dash.dependencies.Output('select-dep-city', 'options'), #to make a subfilter by city for the 2nd dropdown
    dash.dependencies.Input('select-departement', 'value'))#depending on the dept you choose in the 1st filter

def set_cities_options(deptmt : str in dept_list):
    dfdep = df[df['Libellé du département'] == deptmt].reset_index(drop=True)

    return [{'label': city, 'value': city} for city in dfdep['Libellé de la commune'].unique().tolist()]


@callback(
    dash.dependencies.Output("dep-city-results", "figure"),
    dash.dependencies.Output("dep-city-results", "className"),
    dash.dependencies.Input("select-dep-city", "value"))

def resultcity4dep(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop= True)

    test = pd.DataFrame(round(dfcity.groupby('Nom')['Voix'].sum()/(dfcity['Voix'].sum())*100,2))
    

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.5],
        specs=[[{"type": "pie"}, {"type": "bar"}]],)

    fig.add_trace(go.Pie(labels=test.index,
                                values=test['Voix'],
                            legendgroup="group",
                            name='Results',
        textinfo='label',
        textfont={'color':"rgb(159, 241, 253)","size":12},
        hovertemplate="<br>".join(["Departement: {}".format(dfcity['Libellé du département'].values[0]),
        "City: {}".format(city),
        "Candidate: %{label}",
        "Score: %{percent}"])),
        row=1, col=1)
    fig.update_traces(hole=.5)

    fig.add_trace(go.Bar(x=test.index, y=test['Voix'],
    marker_color=test['Voix'],
    legendgroup="group",
    name='Bar chart',
    hovertemplate="<br>".join(["Departement: {}".format(dfcity['Libellé du département'].values[0]),
    "City: {}".format(city),
    "Candidate: %{label}",
    "Score : %{y}%"])),row=1, col=2)

    fig.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
    fig.update_yaxes(color="rgb(159, 241, 253)") #change color of yaxes labels
    fig.update_layout( 
    xaxis={'categoryorder':'total descending'},
    yaxis_title="Score (%)",
    paper_bgcolor="black", #to change the background color of the figure
    plot_bgcolor="black",#to change the background colour of the graph
    showlegend=True,
    legend=dict(font=dict(color="rgb(159, 241, 253)")), #to change color of the legend 
                 title = "Votes results for city of {} in departement of {} ({})".format(city,dfcity['Libellé du département'].values[0],dfcity['Code du département'].values[0]),
                title_font_color="rgb(159, 241, 253)") #to change the color of the figure title
    fig.update_annotations(font=dict(family="Helvetica", size=10,color="rgb(159, 241, 253)"))#to change the subplot title colour

    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("result-cities-table-city", "data"),
    dash.dependencies.Output("result-cities-table-city", "columns"),
    dash.dependencies.Input("select-dep-city", "value"))

def resultcitytable(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop= True)

    test = pd.DataFrame(round(dfcity.groupby('Nom')['Voix'].sum()/(dfcity['Voix'].sum())*100,2))
    test['Candidate']=test.index
    test = test.sort_values('Voix',ascending=False)
    test = test.reset_index(drop = True)

    for i in range(0,len(test)):
        test['Voix'][i] = str(test['Voix'][i])
        test['Voix'][i] = (test['Voix'][i]) + str(' %')

    return test.to_dict(orient='records'),columns_table_results_city


@callback(
    dash.dependencies.Output("stats-dep-per-city", "figure"),
    dash.dependencies.Output("stats-dep-per-city", "className"),
    dash.dependencies.Input("select-dep-city", "value"))

def resultdepcity1(city: str in city_list):
    dfrescity = df[df['Libellé de la commune'] == city]
    stats = pd.DataFrame(round(dfrescity.groupby('Libellé de la commune')[dfrescity.columns[5:8]].mean(),2))
    stats = stats.rename(columns= {'% Abs/Ins':"Abstention", '% Blancs/Vot':'Blanc voted', '% Nuls/Vot':'Nul voted'})
    columns_to_plot=[stats.columns.values[0],stats.columns.values[1],stats.columns.values[2]]

    fig = px.bar(x=columns_to_plot,
                y=stats.values[0],
                labels={'y':'Score (%)',
        'x':'Type of vote'},
    color=columns_to_plot,
    title='Statistics for city of {}'.format(city))
 
    fig.update_layout(legend_title_text='Score (%)',
        title_font_color="rgb(159, 241, 253)",
        
        legend_title_font_color="rgb(159, 241, 253)",
        plot_bgcolor="black",
        paper_bgcolor="black")
    fig.layout.yaxis.color = 'rgb(159, 241, 253)'
    fig.layout.xaxis.color = 'rgb(159, 241, 253)'

    fig.update_traces(width = 0.5,
    hovertemplate="<br>".join([
            "Departement: {}".format(dfrescity['Libellé du département'].values[0]),
            "City: {}".format(city),
            "{}: {}%".format(stats.columns[0],stats.values[0][0]),
            "{}: {}%".format(stats.columns[1],stats.values[0][1]),
            "{}: {}%".format(stats.columns[2],stats.values[0][2])

    ]))
    
    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("abst-cities-table-city", "data"),
    dash.dependencies.Output("abst-cities-table-city", "columns"),
    dash.dependencies.Input("select-dep-city", "value"))

def resultcitytable(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop=True)

    stats_figures = pd.DataFrame(round(dfcity.groupby('Libellé de la commune')['% Abs/Ins'].mean(),2))
    stats_figures['City'] = stats_figures.index
    stats_figures['Blanc voted'] = (round(dfcity.groupby('Libellé de la commune')['% Blancs/Vot'].mean(),2))
    stats_figures['Null voted'] = (round(dfcity.groupby('Libellé de la commune')['% Nuls/Vot'].mean(),2))
    stats_figures= stats_figures.rename(columns={'% Abs/Ins':'Vote abstention'})
    stats_figures= stats_figures[['City','Vote abstention','Blanc voted','Null voted']].reset_index(drop=True)
    for i in range(0,len(stats_figures)):
        stats_figures['Vote abstention'][i] = str(stats_figures['Vote abstention'][i])
        stats_figures['Vote abstention'][i] = (stats_figures['Vote abstention'][i])+ str(' %')
        stats_figures['Blanc voted'][i] = str(stats_figures['Blanc voted'][i])
        stats_figures['Blanc voted'][i] = (stats_figures['Blanc voted'][i])+ str(' %')
        stats_figures['Null voted'][i] = str(stats_figures['Null voted'][i])
        stats_figures['Null voted'][i] = (stats_figures['Null voted'][i])+ str(' %')

    return stats_figures.to_dict(orient='records'),columns_table_city


@callback(
    dash.dependencies.Output("result-per-city", "figure"),
    dash.dependencies.Output("result-per-city", "className"),
    dash.dependencies.Input("select-city", "value"))

def resultcity4dep(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop= True)

    test = pd.DataFrame(round(dfcity.groupby('Nom')['Voix'].sum()/(dfcity['Voix'].sum())*100,2))
    

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.5, 0.5],
        row_heights=[0.5],
        specs=[[{"type": "pie"}, {"type": "bar"}]],)

    fig.add_trace(go.Pie(labels=test.index,
                                values=test['Voix'],
                            legendgroup="group",
                            name='Results',
        textinfo='label',
        textfont={'color':"rgb(159, 241, 253)","size":12},
        hovertemplate="<br>".join(["Departement: {}".format(dfcity['Libellé du département'].values[0]),
        "City: {}".format(city),
        "Candidate: %{label}",
        "Score: %{percent}"])),
        row=1, col=1)
    fig.update_traces(hole=.5)

    fig.add_trace(go.Bar(x=test.index, y=test['Voix'],
    marker_color=test['Voix'],
    legendgroup="group",
    name='Bar chart',
    hovertemplate="<br>".join(["Departement: {}".format(dfcity['Libellé du département'].values[0]),
    "City: {}".format(city),
    "Candidate: %{label}",
    "Score : %{y}%"])),row=1, col=2)

    fig.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
    fig.update_yaxes(color="rgb(159, 241, 253)") #change color of yaxes labels
    fig.update_layout(
    xaxis={'categoryorder':'total descending'},
    yaxis_title="Score (%)",
    paper_bgcolor="black", #to change the background color of the figure
    plot_bgcolor="black",#to change the background colour of the graph
    showlegend=True,
    legend=dict(font=dict(color="rgb(159, 241, 253)")), #to change color of the legend 
                 title = "Votes results for city of {} in departement of {} ({})".format(city,dfcity['Libellé du département'].values[0],dfcity['Code du département'].values[0]),
                title_font_color="rgb(159, 241, 253)") #to change the color of the figure title
    fig.update_annotations(font=dict(family="Helvetica", size=10,color="rgb(159, 241, 253)"))#to change the subplot title colour

    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("abst-cities-table-dunno-dept", "data"),
    dash.dependencies.Output("abst-cities-table-dunno-dept", "columns"),
    dash.dependencies.Input("select-city", "value"))

def resultcitytable(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop= True)

    test = pd.DataFrame(round(dfcity.groupby('Nom')['Voix'].sum()/(dfcity['Voix'].sum())*100,2))
    test['Candidate']=test.index
    test = test.sort_values('Voix',ascending=False)
    test = test.reset_index(drop = True)

    for i in range(0,len(test)):
        test['Voix'][i] = str(test['Voix'][i])
        test['Voix'][i] = (test['Voix'][i]) + str(' %')

    return test.to_dict(orient='records'),columns_table_results_city


@callback(
    dash.dependencies.Output("stats-per-city", "figure"),
    dash.dependencies.Output("stats-per-city", "className"),
    dash.dependencies.Input("select-city", "value"))

def resultdepcity1(city: str in city_list):
    dfrescity = df[df['Libellé de la commune'] == city]
    stats = pd.DataFrame(round(dfrescity.groupby('Libellé de la commune')[dfrescity.columns[5:8]].mean(),2))
    stats = stats.rename(columns= {'% Abs/Ins':"Abstention", '% Blancs/Vot':'Blanc voted', '% Nuls/Vot':'Nul voted'})
    columns_to_plot=[stats.columns.values[0],stats.columns.values[1],stats.columns.values[2]]

    fig = px.bar(x=columns_to_plot,
                y=stats.values[0],
                labels={'y':'Score (%)',
        'x':'Type of vote'},
    color=columns_to_plot,
    title='Statistics for city of {}'.format(city))
 
    fig.update_layout(legend_title_text='Score (%)',
        title_font_color="rgb(159, 241, 253)",
        
        legend_title_font_color="rgb(159, 241, 253)",
        plot_bgcolor="black",
        paper_bgcolor="black")
    fig.layout.yaxis.color = 'rgb(159, 241, 253)'
    fig.layout.xaxis.color = 'rgb(159, 241, 253)'

    fig.update_traces(width = 0.5,
    hovertemplate="<br>".join([
            "Departement: {}".format(dfrescity['Libellé du département'].values[0]),
            "City: {}".format(city),
            "{}: {}%".format(stats.columns[0],stats.values[0][0]),
            "{}: {}%".format(stats.columns[1],stats.values[0][1]),
            "{}: {}%".format(stats.columns[2],stats.values[0][2])

    ]))
    
    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("abst-table-city", "data"),
    dash.dependencies.Output("abst-table-city", "columns"),
    dash.dependencies.Input("select-city", "value"))

def resultcitytable(city: str in city_list):
    dfcity = df[df['Libellé de la commune'] == city].reset_index(drop=True)

    stats_figures = pd.DataFrame(round(dfcity.groupby('Libellé de la commune')['% Abs/Ins'].mean(),2))
    stats_figures['City'] = stats_figures.index
    stats_figures['Blanc voted'] = (round(dfcity.groupby('Libellé de la commune')['% Blancs/Vot'].mean(),2))
    stats_figures['Null voted'] = (round(dfcity.groupby('Libellé de la commune')['% Nuls/Vot'].mean(),2))
    stats_figures= stats_figures.rename(columns={'% Abs/Ins':'Vote abstention'})
    stats_figures= stats_figures[['City','Vote abstention','Blanc voted','Null voted']].reset_index(drop=True)
    for i in range(0,len(stats_figures)):
        stats_figures['Vote abstention'][i] = str(stats_figures['Vote abstention'][i])
        stats_figures['Vote abstention'][i] = (stats_figures['Vote abstention'][i])+ str(' %')
        stats_figures['Blanc voted'][i] = str(stats_figures['Blanc voted'][i])
        stats_figures['Blanc voted'][i] = (stats_figures['Blanc voted'][i])+ str(' %')
        stats_figures['Null voted'][i] = str(stats_figures['Null voted'][i])
        stats_figures['Null voted'][i] = (stats_figures['Null voted'][i])+ str(' %')

    return stats_figures.to_dict(orient='records'),columns_table_city