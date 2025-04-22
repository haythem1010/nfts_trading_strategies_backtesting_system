from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github"),
                        " "  # Text beside icon
                    ],
                    href="https://github.com/orgs/Laevitas/teams/nfts",
                    target="_blank"
                )

            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-twitter"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="https://twitter.com/Suipa_xyz",
                    target="_blank"
                )

            ),
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-linkedin"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href='https://www.linkedin.com/company/laevitas/',
                    target="_blank"
                )

            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Features",
                align_end=True,
                children=[
                    dbc.DropdownMenuItem("Home", href='/home.py'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Strategies", href='/Strategies.py'),
                    dbc.DropdownMenuItem(children=[dbc.DropdownMenuItem('Bollinger Band', href='/BollingerBand.py'),
                                                    dbc.DropdownMenuItem('Buy the floor', href='/Buythefloor.py'),
                                                    dbc.DropdownMenuItem('Triple RSI', href='/triple_rsi.py'),
                                                    dbc.DropdownMenuItem('Moving Average Crossover', href='/movingaverage_crossover.py'),
                                                    ],
                                         ),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Predictions", href='/Predictions.py'),
                    dbc.DropdownMenuItem(children=[dbc.DropdownMenuItem('Average Trading Price', href='/average_trading_price.py'),
                                                   dbc.DropdownMenuItem('Floor Price', href='/floor_price.py'),
                                                   ],
                                         ),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Pattern Recognition", href='/PatternDetection.py'),

                ],
            ),
        ],
        brand='Suipa Home',
        brand_href="https://app.suipa.xyz/home",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="#614A8A",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar