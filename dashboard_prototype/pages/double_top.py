from dash import html, register_page


register_page(
    __name__,
    name='Double Top',
    top_nav=True,
    path='/double_top.py'
)



layout = html.Div([
    html.H2([
            " This feature is under construction right now, we will keep you updated "
        ])
    ], style={'padding': '100px'})