import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import base64
from datetime import datetime
import regex as re
import data_input

today = datetime.now().strftime("%d/%m/%Y - %H:%M")
regexp = re.compile(r"(https:|http:|www\.)\S*")

term_1 = 'Coronavirus, Covid'

search_term_statistics = """
            data
            statistics

            """

search_term_education = """
            Schools, 
            School closure, 
            School opening, 
            School statistics, 
            School figures

            """


# -------------------------- FUNCTIONS --------------------

image_filename = 'image/twitter_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


def Table(dataframe):
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            # update this depending on which
            # columns you want to show links for
            # and what you want those links to be
            if col == 'Popular url':
                cell = html.Td(html.A(href=value, children=value),
                               style={'border': 'solid', 'border-width': 'thin', 'column-width': '700px'})
            elif col == 'Number of retweets':
                cell = html.Td(html.A(children=value),
                               style={'border': 'solid', 'border-width': 'thin', 'text-align': 'center',
                                      'column-width': '200px'})
            elif col == 'Link to tweet':
                cell = html.Td(html.A(href=value, children=value),
                               style={'border': 'solid', 'border-width': 'thin', 'text-align': 'center',
                                      'column-width': '200px', 'word-wrap': 'break-word'})
            elif col == 'Tweet':
                match = re.search(regexp, value)
                if match:
                    cell = html.Td([re.sub(regexp, "", value), html.A(href=match.group(), children=match.group())],
                                   style={'border': 'solid', 'border-width': 'thin', 'column-width': '700px'})
                else:
                    cell = html.Td(children=value,
                                   style={'border': 'solid', 'border-width': 'thin', 'column-width': '700px'})
            else:
                cell = html.Td(children=value,
                               style={'border': 'solid', 'border-width': 'thin', 'column-width': '700px'})
            row.append(cell)
        rows.append(html.Tr(row))
    return html.Table(
        # Header
        [html.Tr([html.Th(col, style={'border': 'solid', 'border-width': 'thin'}) for col in dataframe.columns])] +

        rows, style={'table-layout': 'fixed'}
    )


def build_banner():
    return html.Div(
        id='banner',
        className='banner',
        children=[
            html.Img(src=app.get_asset_url('Twitter_bird_logo.png'),
                     height='50',
                     width='300'),
        ],
    )


# --------------------------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# app.css.append_css({'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'})

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
             style={'height': '10%', 'width': '10%', 'margin-left': '20px'}),
    html.H1(
        children=[
            # build_banner(),
            html.P(
                id='instructions',
                children='Coronavirus Tweets Analysis',
                style={'font-size': '35px',
                       'font-family': 'sans-serif',
                       'margin-left': '20px'
                       }
            ),
        ]
    ),
    html.H1(
        children=[
            'Data as of {}'.format(today, style={'color': 'green'})],
        style={'font-size': '25px',
               'font-family': 'sans-serif',
               'margin-left': '20px'
               }
    ),
    # -------------------- comment out ----------------------
    dbc.Row([
        # Status dropdown
        dbc.Col([
            html.H1(
                children=[
                    'Please select the topic of tweets you are interested in:'],
                style={'font-size': '25px',
                       'font-family': 'sans-serif',
                       'margin-left': '20px',
                       'margin-top': '20px',
                       'color': '#6495ED'
                       }
            ),
            dcc.Dropdown(id='domain-dropdown',
                         options=[{'label': 'Statistics and Data', 'value': 'General'},
                                  {'label': 'Education', 'value': 'Education'}
                                  ],
                         value='General',
                         multi=False,
                         placeholder='Please select a topic...',
                         style={'font-size': '15px',
                                'font-family': 'sans-serif',
                                'width': '500px',
                                'margin-left': '10px'
                                }
                         ),
        ]),
    ]),
    dbc.Row(
        html.H3(
            '''
            Search Terms
            ''',
            style={'font-size': '25px',
                   'font-family': 'sans-serif',
                   'color': 'green',
                   }

        ), style={'margin-left': '20px',
                  'margin-top': '20px'}
    ),
    dbc.Row(
        html.H3(
            '''
            Term 1:
            ''',
            style={'font-size': '20px',
                   'font-family': 'sans-serif',
                   'color': 'green',
                   }

        ), style={'margin-left': '20px',
                  'margin-top': '10px'}
    ),
    dbc.Row(
        html.H3(
            term_1,
            style={'font-size': '22px',
                   'font-family': 'sans-serif',
                   }

        ), style={'margin-left': '20px'
                  }
    ),
    dbc.Row(
        html.H3(
            '''
            Term 2:
            ''',
            style={'font-size': '20px',
                   'font-family': 'sans-serif',
                   'color': 'green',
                   }

        ), style={'margin-left': '20px',
                  'margin-top': '20px'}
    ),
    dbc.Row(
        html.Div(
            id='search_term',
            style={'font-size': '22px',
                   'font-family': 'sans-serif'
                   }

        ), style={'margin-left': '20px',
                  'margin-bottom': '20px'}

    ),
    dbc.Row([
        dbc.Col([
            html.H3(
                '''
                Most retweeted tweet in the last 24 hours:

                 ''',

                style={'font-size': '25px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       'color': 'green',
                       'margin-left': '20px'
                       }

            ),
            html.H4(
                id="most_retweet_24",

                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       },

            ),
            html.H4(
                id='most_retweet_number',
                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       }

            ),
            html.H4(
                '''
                Other retweets:
                 ''',
                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       'color': 'green'
                       }

            ),
            html.Div(
                id='other_24',
                style={'height': '340px', 'overflowY': 'scroll',
                       'overflowX': 'scroll', 'minWidth': '100px', 'maxWidth': 'auto',
                       'border-style': 'solid', 'margin-top': '10px', 'margin-left': '20px',
                       'border': 'solid'}
            ),
        ], style={'margin-top': '10px'}, width=6),

        dbc.Col([
            html.H3(
                '''
                Most retweeted tweet in the last 7 days:

                 ''',

                style={'font-size': '25px',
                       'font-family': 'sans-serif',
                       'margin-left': '40px',
                       'color': 'green',
                       'margin': '20px'
                       }

            ),
            html.H4(
                id='retweet_7',
                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       }

            ),
            html.H4(
                id='retweet_all_number',
                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       }

            ),
            html.H4(
                '''
                Other retweets:
                 ''',
                style={'font-size': '22px',
                       'font-family': 'sans-serif',
                       'margin': '20px',
                       'color': 'green'
                       }

            ),
            html.Div(
                id='retweet_all_table',
                style={'height': '320px', 'overflowY': 'scroll',
                       'overflowX': 'scroll', 'minWidth': '100px', 'maxWidth': 'auto',
                       'border-style': 'solid', 'margin-top': '10px', 'margin-left': '20px',
                       'border': 'solid'}
            ),
        ], width=6)
    ]),
    dbc.Row(
        dbc.Col([
            dcc.Graph(
                id='tweets_per_hour',
                style={'height': '500px'})
        ]),
        style={'margin-top': '10px'},
    ),
    dbc.Row([
        html.H3(children=
                '''
            Most popular hashtags
             ''',
                style={'textAlign': 'center',
                       'font-size': '30px',
                       'font-family': 'sans-serif',
                       'margin-left': '550px',
                       'margin-top': '30px',
                       'color': 'green'
                       }

                ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='hashtag_24_fig',
                style={'height': '650px'})
        ]),
        dbc.Col([
            dcc.Graph(
                id='hashtag_all_fig',
                style={'height': '650px'})
        ]),
    ], style={'margin-top': '10px'},
    ),
    dbc.Row([
        html.H3(children=
                '''
                Most popular trigrams
                 ''',
                style={'textAlign': 'center',
                       'font-size': '30px',
                       'font-family': 'sans-serif',
                       'margin-left': '550px',
                       'margin-top': '30px',
                       'color': 'green'
                       }

                ),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='trigram_24_fig',
                style={'height': '650px'})
        ]),
        dbc.Col([
            dcc.Graph(
                id='trigram_all_fig',
                style={'height': '650px'})
        ]),
    ], style={'margin-top': '10px'},
    ),
    dbc.Row([
        html.H3(children=
                '''
                Popular Links in the last 24 hours:
                 ''',
                style={'textAlign': 'center',
                       'font-size': '30px',
                       'font-family': 'sans-serif',
                       'margin-left': '20px',
                       'margin-top': '30px',
                       'color': 'green'
                       }

                ),
    ]),
    dbc.Row([
        html.Div(
            id='url_24',
            style={'height': '300px', 'overflowY': 'scroll',
                   'overflowX': 'scroll', 'minWidth': '100px', 'maxWidth': '1400px',
                   'margin-left': '20px'}
        ),
    ]),
    dbc.Row([
        html.H3(children=
                '''
                Popular Links in the last 7 days:
                 ''',
                style={'textAlign': 'center',
                       'font-size': '30px',
                       'font-family': 'sans-serif',
                       'margin-left': '20px',
                       'margin-top': '30px',
                       'color': 'green'
                       }

                ),
    ]),
    dbc.Row([
        html.Div(
            id='url_all',
            style={'height': '300px', 'overflowY': 'scroll',
                   'overflowX': 'scroll', 'minWidth': '100px', 'maxWidth': '1400px',
                   'margin-top': '10px', 'margin-left': '20px', 'margin-bottom': '20px'}
        ),
    ]),
])


@app.callback(
    [Output(component_id='search_term', component_property='children'),
     Output(component_id='most_retweet_24', component_property='children'),
     Output(component_id='most_retweet_number', component_property='children'),
     Output(component_id='other_24', component_property='children'),
     Output(component_id='retweet_7', component_property='children'),
     Output(component_id='retweet_all_number', component_property='children'),
     Output(component_id='retweet_all_table', component_property='children'),
     Output(component_id='tweets_per_hour', component_property='figure'),
     Output(component_id='hashtag_24_fig', component_property='figure'),
     Output(component_id='hashtag_all_fig', component_property='figure'),
     Output(component_id='trigram_24_fig', component_property='figure'),
     Output(component_id='trigram_all_fig', component_property='figure'),
     Output(component_id='url_24', component_property='children'),
     Output(component_id='url_all', component_property='children')],
    [Input(component_id='domain-dropdown', component_property='value')]
)
def update_tweet(input_value):
    if input_value == 'General':
        return search_term_statistics, \
               ' {} '.format(data_input.most_retweet_24.at[0, 'text']), \
               'retweeted {} times. Link to tweet: {}'.format(str(data_input.most_retweet_24.at[0, 'n']),
                                                              str(data_input.most_retweet_24.at[0, 'tweet_url'])), \
               Table(data_input.other_retweet_24), \
               '{}'.format(data_input.most_retweeted_tweet.at[0, 'text']), \
               'retweeted {} times. Link to tweet: {}'.format(str(data_input.most_retweeted_tweet.at[0, 'n']),
                                                              str(data_input.most_retweeted_tweet.at[0, 'tweet_url'])), \
               Table(data_input.other_retweet_all), \
               data_input.tweets_per_hour_fig, \
               data_input.hashtag_24_fig, \
               data_input.hashtag_all_fig, \
               data_input.trigrams_24_fig, \
               data_input.trigrams_all_fig, \
               Table(data_input.url_24), \
               Table(data_input.url_all)
    elif input_value == 'Education':
        return search_term_education, \
               ' {} '.format(data_input.most_retweet_24_e.at[0, 'text']), \
               'retweeted {} times. Link to tweet: {}'.format(str(data_input.most_retweet_24_e.at[0, 'n']),
                                                              str(data_input.most_retweet_24_e.at[0, 'tweet_url'])), \
               Table(data_input.other_retweet_24_e), \
               '{}'.format(data_input.most_retweeted_tweet_e.at[0, 'text']), \
               'retweeted {} times. Link to tweet: {}'.format(str(data_input.most_retweeted_tweet_e.at[0, 'n']), str(
                   data_input.most_retweeted_tweet_e.at[0, 'tweet_url'])), \
               Table(data_input.other_retweet_all_e), \
               data_input.tweets_per_hour_fig_e, \
               data_input.hashtag_24_fig_e, \
               data_input.hashtag_all_fig_e, \
               data_input.trigrams_24_fig_e, \
               data_input.trigrams_all_fig_e, \
               Table(data_input.url_24_e), \
               Table(data_input.url_all_e)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)