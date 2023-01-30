import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import html, dash_table
from dash import dcc
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go



#df = pd.read_csv('df_global.csv')
result_France = pd.DataFrame(round(df.groupby('Nom')['Voix'].sum()/df['Voix'].sum()*100,2))


table_result_France=pd.DataFrame()
table_result_France['Candidate'] = result_France.index
table_result_France['Score'] =result_France.rename(columns= {'Voix':'Score'}).reset_index(drop=True)
table_result_France = table_result_France[['Candidate','Score']]


table_result_France = table_result_France.sort_values('Score',ascending=False)

for i in range(0,len(table_result_France)):
    table_result_France['Score'][i] = str(table_result_France['Score'][i])
    table_result_France['Score'][i] = (table_result_France['Score'][i])+ str(' %')


fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.5],
    row_heights=[0.5],
    specs=[[{"type": "pie"}, {"type": "bar"}]],
    subplot_titles=("Donut chart view","Bar chart view "))

fig.add_trace(go.Pie(labels=result_France.index,
                            values=result_France['Voix'],
                        legendgroup="group",
                        name='Results',
    #marker={'colors':["blue","white","red","green","rgb(159, 241, 253)","purple","yellow","orange","grey","black","pink","red"] },#to change the colors inside the pie
    textinfo='percent+label',#what will be shown inside the pie
    #textinfo='label',
    textfont={'color':"rgb(159, 241, 253)","size":12}, #to change the size and the text color inside the pie
    #textfont={'color':'white',"size":12},
    hovertemplate="<br>".join([
    "Candidate: %{label}",
"Score : %{percent}"])),
    row=1, col=1
                    )
fig.update_traces(hole=.5) #to make a donut chart


fig.add_trace(go.Bar(x=result_France.index, y=result_France['Voix'],marker_color=result_France['Voix'],legendgroup="group",
name='Bar Chart',
hovertemplate="<br>".join(["Candidate: %{label}",
"Score : %{y}%"])),row=1, col=2)
fig.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
fig.update_yaxes(color="rgb(159, 241, 253)") #change color of yaxes labels
fig.update_layout( # Add annotations in the center of the donut pies & in the bar chart graph
    annotations=[dict(text='2022',x=0.225, y=0.5,showarrow=False),
                 dict(text='2022', x=0.82, y=0.5, showarrow=False)],
xaxis={'categoryorder':'total descending'},
yaxis_title="Score (%)",
paper_bgcolor="black", #to change the background color of the figure
plot_bgcolor="black",#to change the background colour of the graph
showlegend=True,
legend=dict(font=dict(color="rgb(159, 241, 253)")), #to change color of the legend 
                title = "2022 french presidential elections first round final results",
                title_font_color="rgb(159, 241, 253)") #to change the color of the figure title
fig.update_annotations(font=dict(family="Helvetica", size=10,color="rgb(159, 241, 253)"))#to change the subplot title colour

dash.register_page(__name__, path='/')

logo = 'https://avatars0.githubusercontent.com/u/5997976?s=400&v=4'


layout = html.Div(children=[ html.Div(                 # Alignement vertical de l'image et de l'acceuil
            dbc.Row(
                [   #logo
                    dbc.Col(html.Img(src=logo, height="40px", style={'padding-left': '20px'})),

                ])),
    html.Br(),
    html.H5(
            "Welcome to this multipage dashboard made with plotly's Dash,\
             feel free to navigate into this app thanks to the 'Menu'",
             style={"color": "yellow",
             'textAlign' : 'center'},
        ),
    html.Br(),
    html.H5(children='Final results',
    style={'color': 'rgb(159, 241, 253)',
    'padding-left': '40px'}),
    html.Br(),
    html.P(children='''
        Here are the final figures regarding the first round of french presidential elections 2022.
    '''),

    
    html.Div(children= html.P('''The global abstention rate for this election was: {}%'''.format(round(df['% Abs/Ins'].mean(),2)))),
    html.Div(children= html.P('''The global blanc voted rate for this election was: {}%'''.format(round(df['% Blancs/Vot'].mean(),2)))),
    html.Div(children= html.P('''The global null voted rate for this election was: {}%'''.format(round(df['% Nuls/Vot'].mean(),2)))),
        html.Div(id="country-div"),
    dcc.Graph(id="result-country",className='notest',figure=fig), 
    
    dash_table.DataTable(id='results-table',data=table_result_France.to_dict('records'),
    columns=[{"name": i, "id": i} for i in table_result_France.columns],
    style_cell={'textAlign': 'left'},
    style_data={
        'color': 'black',
        'backgroundColor': 'rgb(159, 241, 253)',
        
    },
    fill_width=False,
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'color': 'rgb(159, 241, 253)',
            'backgroundColor': 'black',
        }],
    style_header={
        'backgroundColor': 'black',
        'color': 'rgb(159, 241, 253)',
        'fontWeight': 'bold'
    },
    
    style_table={'margin-left': '40vw', 'margin-top': '3vw'}), #to position the table in the center of the page

    ])
