from __future__ import annotations
import dash
from dash import html, dash_table, callback
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


df = pd.read_csv('df_global.csv')

nom_list = df['Nom'].unique().tolist()
result_France = pd.DataFrame(round(df.groupby('Nom')['Voix'].sum()/df['Voix'].sum()*100,2))

table_result_France=pd.DataFrame()
table_result_France['Candidate'] = result_France.index
table_result_France['Score'] =result_France.rename(columns= {'Voix':'Score'}).reset_index(drop=True)
table_result_France = table_result_France[['Candidate','Score']]


table_result_France = table_result_France.sort_values('Score',ascending=False)

for i in range(0,len(table_result_France)):
    table_result_France['Score'][i] = str(table_result_France['Score'][i])
    table_result_France['Score'][i] = (table_result_France['Score'][i])+ str(' %')


#we have to create columns first for DataTable
columns = [{'name': 'Departement', 'id': 'Libellé du département'}, 
 {'name': 'City', 'id': 'Libellé de la commune'},
 {'name': 'Score', 'id': 'Voix'},
 {'name': 'Departement code', 'id': 'Code du département'}]


#to make the choropleth map:
df_dep = pd.DataFrame((round(df.groupby(['Code du département','Libellé du département','Nom'])['Voix'].sum()/df.groupby('Libellé du département')['Voix'].sum()*100,2)))
df_dep['Code Departement'] = str
df_dep['Departement'] = str
df_dep['Nom'] = str

for i in range (0,len(df_dep)):
    df_dep['Code Departement'][i] = df_dep.index[i][0]
    df_dep['Nom'][i] = df_dep.index[i][2]
    df_dep['Departement'][i] = df_dep.index[i][1]

df_dep= df_dep[['Code Departement','Departement','Nom','Voix']]
df_dep = df_dep.reset_index(drop=True)

test = pd.DataFrame(df_dep.groupby(['Code Departement','Departement','Nom'])['Voix'].sum())
test1 =pd.DataFrame(test.groupby(['Departement'])['Voix'].nlargest(n=1))
test1['Code Departement'] = str
test1['Departement'] = str
test1['Nom'] = str

for i in range (0,len(test1)):
    test1['Code Departement'][i] = test1.index[i][1]
    test1['Nom'][i] = test1.index[i][3]
    test1['Departement'][i] = test1.index[i][2]



test1 = test1.reset_index(drop=True)
test1= test1[['Code Departement','Departement','Nom','Voix']]
test1 = test1.sort_values('Code Departement').reset_index(drop=True)
test_choropleth = test1.iloc[0:96]

figFrance = px.choropleth_mapbox(
    test_choropleth,
    geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
    featureidkey='properties.code',
    locations='Code Departement',
    color='Nom',
    title ='First round winner & score for each metropolitan departement',
    labels={"Nom" : "Candidate"},
    hover_data={'Departement','Voix'},
    mapbox_style='carto-positron',
    zoom=3.6,
    center={'lat': 47, 'lon': 2}, #to center the map
    opacity=0.8,
    custom_data=['Nom','Voix','Departement','Code Departement']
   )

figFrance.update_layout(#mapbox_style="open-street-map", #to make the style of the map like OSM
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ],
legend = dict(bgcolor = 'rgb(159, 241, 253)'),
title_font_color="white",
        legend_title_font_color="black",
        plot_bgcolor="black",
        paper_bgcolor="black")

figFrance.update_layout(margin=dict(l=80, r=80, t=30, b=20))      #to adjust graph size
                                                                # Where l r t b correspond to left, right, top, bottom.

figFrance.update_traces(hovertemplate="<br>".join([
        "Departement : %{customdata[2]} (%{customdata[3]})",
        "Candidate: %{customdata[0]}",
        "Score: %{customdata[1]} %",
        
    ]))


logo = 'https://avatars0.githubusercontent.com/u/5997976?s=400&v=4'

app = dash.Dash(__name__,suppress_callback_exceptions=True)
server= app.server,

app.scripts.config.serve_locally = True

dash.register_page(__name__)

layout = html.Div(children=[html.Div(                 # Alignement vertical de l'image et de l'accueil
            dbc.Row(
                [   #logo
                    dbc.Col(html.Img(src=logo, height="40px", style={'padding-left': '20px'})),
                                    ]),id="analysis"),
    html.Div([html.H5(children= "Let's analyze results by candidate",
    style={'textAlign' : 'center'},),
    
    html.Div(children=html.H6(children="Let's see the first round winner for each metropolitan departement on a map")),
    html.Br(),
    html.Div(id="country-map-winner-div"),
    dcc.Graph(id="map-dept-winner-country",className='show',figure=figFrance),
    html.Br(),
    
    
    html.H6('Candidate departemental results analysis'),
    html.Br(),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate', 
        options=sorted([{"label":nom, "value":nom} for nom in nom_list], key = lambda x: x['label']),
        style={"padding": "40px", 'color':'yellow'}, #to change the color for the Candidate's names
        inputStyle={"margin-right": "5px"}, #to add space between the tick and the Candidate name
        value="ARTHAUD",
        inline=True,
    ),
    html.Br(),

    html.Div(id="result-cand-div"),
    html.Div(id="map-div"),
    html.Br(),
    dcc.Graph(id="graph"),
    html.Br(),

    html.Div(id="name-dept-div"),
    dcc.Graph(id="result-per-name",className='test'),    
    html.Br(),

    html.Div(id="top15-cities-div"),
    dash_table.DataTable(id="top15-cities-table",
    data=[], #we need to declare an empty data list to then fill it with our updated datas
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
        'fontWeight': 'bold'
    }),
    html.Br(),
    dbc.NavLink("Let's go higher",href="#analysis",external_link=True),
    html.Br()

    ])])

@callback(
    dash.dependencies.Output("result-cand-div", "children"),
    dash.dependencies.Input("candidate", "value"))
    
def result_cand(nom : str in nom_list):
    table_result_France_cand = table_result_France[table_result_France['Candidate'] == nom]
    return html.P(children=f"Global score for candidate {nom} was {table_result_France_cand['Score'].values[0]} of vote")

@callback( dash.dependencies.Output("graph", "figure"),
    dash.dependencies.Input("candidate", "value"))
    
def display_choropleth(nom):
    df_cand = df_dep[df_dep['Nom'] == nom].reset_index(drop=True)
    df_cand = df_cand.iloc[0:96] #to have the dept code from 01 to 95 (number of french dept)

    fig = px.choropleth_mapbox(
        df_cand,
        geojson="https://france-geojson.gregoiredavid.fr/repo/departements.geojson",
        featureidkey='properties.code', #the first key to link geojson file & the df
        locations='Code Departement', #the second key to link geojson file & the df
        color='Voix',
        title ='First round score in metropolitan departements for candidate {}'.format(nom),
        labels={"Voix" : "Score (%)"},
        color_continuous_scale='YlOrRd',
        hover_data={'Departement','Voix'},
        mapbox_style='carto-positron',
        zoom=3.6,
        center={'lat': 47, 'lon': 2},
        opacity=0.8,
        custom_data=['Nom','Voix','Departement','Code Departement']
    )
    fig.update_layout(mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ], #to make the style of the map a white background replace by 'white-bg'
    legend = dict(bgcolor = 'rgb(159, 241, 253)'),
    title_font_color="rgb(159, 241, 253)",
        legend_title_font_color="black",
        plot_bgcolor="black",
        paper_bgcolor="black")
    fig.update_layout(margin=dict(l=80, r=80, t=30, b=20))   

    fig.update_traces(hovertemplate="<br>".join([
            "Departement : %{customdata[2]} (%{customdata[3]})",
            "Candidate: %{customdata[0]}",
            "Score: %{customdata[1]} %",
            
        ]))
    return fig

@callback(
    dash.dependencies.Output("result-per-name", "figure"),
    dash.dependencies.Output("result-per-name", "className"),
    dash.dependencies.Input("candidate", "value"))

def vote_candidat_dep(nom):
    df_cand = df[df['Nom'] == nom]
    res_cand_dep =pd.DataFrame(round(df_cand.groupby('Libellé du département')['Voix'].sum()/(df.groupby('Libellé du département')['Voix'].sum())*100,2))

    fig = px.bar(res_cand_dep, x=res_cand_dep.index,y ='Voix', color=res_cand_dep.index,
    title ="First round presidential elections results by departement for candidate {}".format(nom),
    labels={'Libellé du département':'Departements',
    'Voix':'Score (%)'}, #to change the legend label
    custom_data=['Voix'],
    color_discrete_sequence=px.colors.qualitative.T10, #to change bars' color
    )
    
    fig.update_layout(xaxis={'categoryorder':'total descending'},
    legend = dict(bgcolor = 'rgb(159, 241, 253)'),
    title_font_color="rgb(159, 241, 253)",
        legend_title_font_color="black",
        plot_bgcolor="black",
        paper_bgcolor="black")
    fig.layout.yaxis.color = 'rgb(159, 241, 253)'
    fig.layout.xaxis.color = 'rgb(159, 241, 253)'

    fig.update_traces(
    #marker_color= res_cand_dep['Voix'],
    hovertemplate="<br>".join([
            "Candidate: {}".format(nom),
            "Departement: %{x}",
            "Score: %{customdata[0]}%"
    ]))
    
    return fig, "visible-graph"

@callback(
    dash.dependencies.Output("top15-cities-div", "children"),
    dash.dependencies.Input("candidate", "value"))
    
def top15_cities_list(nom : str in nom_list):
    return html.P(children=f"Here is a list of 15 cities where candidate {nom} got top scores")


@callback(
    dash.dependencies.Output("top15-cities-table", "data"),
    dash.dependencies.Output("top15-cities-table", "columns"),
    dash.dependencies.Input("candidate", "value"))

def top15_cities_table(nom : str in nom_list):
    dfcand = df[df['Nom'] == nom].reset_index(drop = True)

    stats = round(dfcand.groupby(['Libellé de la commune','Libellé du département','Code du département'])['Voix'].sum()/df.groupby('Libellé de la commune')['Voix'].sum()*100,2)
    stats15 = pd.DataFrame(stats.nlargest(n=15))
    stats15['Libellé de la commune'] = str
    stats15['Libellé du département'] = str
    stats15['Code du département'] = str



    for i in range (0,len(stats15)):
        stats15['Libellé de la commune'][i] =stats15.index[i][0]
        stats15['Libellé du département'][i] =stats15.index[i][1]
        stats15['Code du département'][i] = stats15.index[i][2]

    stats15 = stats15.reset_index(drop = True)
    
    for i in range(0,len(stats15)):
        stats15['Voix'][i] = str(stats15['Voix'][i])
        stats15['Voix'][i] = (stats15['Voix'][i])+ str(' %')

    
    return stats15.to_dict(orient='records'),columns

