import plotly.graph_objects as go

layout_hashtag_24 = go.Layout(
    title=go.layout.Title(
        text='24 hours',
        xref='paper',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='sans-serif',
            size=25,
            color='#7f7f7f'
        ),
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'

            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Hashtag',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        ),
        autorange="reversed",
        tickfont=dict(size=12),

    ),
)

layout_hashtag_all = go.Layout(
    title=go.layout.Title(
        text='7 days',
        xref='paper',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='sans-serif',
            size=25,
            color='#7f7f7f'
        ),
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'

            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Hashtag',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        ),
        autorange="reversed",
        tickfont=dict(size=12),
    ),
)

layout_trigram_24 = go.Layout(
    title=go.layout.Title(
        text='24 hours ',
        xref='paper',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='sans-serif',
            size=25,
            color='#7f7f7f'
        ),
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'

            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Trigram',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        ),
        autorange="reversed",
        tickfont=dict(size=12),

    ),
)

layout_trigram_all = go.Layout(
    title=go.layout.Title(
        text='7 days',
        xref='paper',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='sans-serif',
            size=25,
            color='#7f7f7f'
        ),
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'

            )
        ),
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Trigram',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        ),
        autorange="reversed",
        tickfont=dict(size=12),

    ),
)

layout_num_tweets_per_hour = go.Layout(
    title=go.layout.Title(
        text='Number of Tweets per hour',
        xref='paper',
        y=0.9,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(
            family='sans-serif',
            size=25,
            color='green'
        ),
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Hour',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='Number of tweets',
            font=dict(
                family='sans-serif',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
)