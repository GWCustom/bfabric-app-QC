import dash_bootstrap_components as dbc
from dash import html, dcc

DEVELOPER_EMAIL = "gwhite@fgcz.ethz.ch"

default_sidebar = [
    html.P(id="sidebar_text", children="Select instrument:"),
    dcc.Dropdown(
        id="dropdown-select-inst",
        options=[
            {
                "label": "Fragment Analyzer",
                "value": "Frag"
            },
            {
                "label": "Tapestation RNA",
                "value": "RNA",
            },
            {
                "label": "Tapestation DNA",
                "value": "DNA",
            },
            {
                "label": "Glowmax",
                "value": "Glow",
                "disabled": True
            },
            {
                "label": "Qbit",
                "value": "Qbit",
                "disabled": True
            },
            {
                "label": "BioAnalyzer",
                "value": "BioA",
                "disabled": True
            },
            {
                "label": "BioRad",
                "value": "BioRad",
                "disabled": True
            },
            {
                "label": "FemtoPulse",
                "value": "Femto",
                "disabled": True
            },
        ],
        clearable=False,
        searchable=False,
        value="Frag"),
    html.Br(),
    dbc.Card(
        id="next-card", 
        style={"border": "none"},
        children=[
            dcc.Dropdown(
                id="qc-type",
            ),
            html.Br(),
            dcc.Dropdown(
                id="upload-type",
            ),
        ]
    ),
    html.Br(),
    dcc.Upload([
        'Drag and Drop or ',
        html.A('Select a File'),
        
    ], style={
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center'
    },
    id="drag-drop"),
    html.Br(), 
    dbc.Button('Submit', id='submit-val-intro', color='primary'),
    html.Br(),
]

no_auth = [
    html.P("You are not currently logged into an active session. Please log into bfabric to continue:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

expired = [
    html.P("Your session has expired. Please log into bfabric to continue:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

no_entity = [
    html.P("There was an error fetching the data for your entity. Please try accessing the applicaiton again from bfabric:"),
    html.A('Login to Bfabric', href='https://fgcz-bfabric.uzh.ch/bfabric/')
]

dev = [html.P("This page is under development. Please check back later."),html.Br(),html.A("email the developer for more details",href="mailto:"+DEVELOPER_EMAIL)]

auth = [html.Div(id="auth-div")]

main_tab = dbc.Row(
    id="page-content-main",
    children = [
        dbc.Col(
            html.Div(
                id="sidebar",
                children=default_sidebar,
                style={"border-right": "2px solid #d4d7d9", "height": "100%", "padding": "20px", "font-size": "20px"}
            ),
            width=3,
        ),
        dbc.Col(
            html.Div(
                id="page-content",
                children=no_auth + [html.Div(id="auth-div")],
                style={
                    "margin-top":"2vh", 
                    "margin-left":"2vw", 
                    "font-size":"20px",
                    "max-height":"80%",
                    "overflow-y":"scroll",
                    "margin-bottom":"2vh"
                },
            ),
            width=9,
        ),
    ], 
    style={"margin-top": "0px", "min-height": "40vh"}
),
modal_submit =html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Ready to Submit? 🚀")),
                dbc.ModalBody("Are you sure you're ready to upload your instrument data to bfabric?"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Yes!", id="submit-val", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)

empty_sidebar = []

docs_tab = dbc.Row(
        id="page-content-docs",
        children=[
            dbc.Col(
                html.Div(
                    id="sidebar_docs",
                    children=empty_sidebar,
                    style={"border-right": "2px solid #d4d7d9", "height": "100%", "padding": "20px", "font-size": "20px"}
                ),
                width=3,
            ),
            dbc.Col(
                [html.Div(
                    id="page-content-docs-children",
                    children=[
                        html.H2("Welcome to The Barcode Dashboard"),
                        html.P([
                            "This app serves as a user interface for updating barcodes of run samples within B-Fabric."
                        ]),
                        html.Br(),
                        html.H4("Developer Info"),
                        html.P([
                            "This app was written by Griffin White, for the FGCZ. If you wish to report a bug, please use the \"bug reports\" tab. If you wish to contact the developer for other reasons, please use the email:",
                            html.A(" griffin@gwcustom.com", href="mailto:griffin@gwcustom.com"),
                        ]),
                        html.Br(),

                        html.H4("Some Notes on this App\'s Functionality"),
                        html.P([
                            """
                            This app is designed to allow users to update the barcodes of samples
                            in B-Fabric. """
                        ]),
                        html.Br(),
                        html.P([
                            """

                            This app communicates with the B-Fabric API to fetch and save data in bfabric.
                            However the B-Fabric API currently does not support updating whitespace as barcodes.
                            It is therfore impossible to set a barcode to an empty string, or a space (for instance). 
                            In cases where clearing out a barcode is imperative for successful demultiplexing, I reccomend 
                            setting the barcode to a placeholder value such as 'G', and then demultiplexing 
                            using the draugrUI with an additional barcode mismatch. 
                            """
                        ]),
                        html.Br(),
                        html.P("""
                            \n\n
                            The app uses in-memory storage to make it simple to reset the barcodes to their initial state (by simply refreshing the page).
                            However, this means that the app will not remember the state of the barcodes if the page is refreshed. 
                            Only refresh the page after you have saved the barcodes in B-Fabric, or if you wish to reset the barcodes to their initial state.
                            """
                        ),
                        html.H4("Update Barcodes Tab"),
                        html.P([
                            html.B(
                                "Load / Reload --"
                            ), " Load the order you'd like to update barcodes for.",
                            html.Br(),html.Br(),
                            html.B(
                                "Swap Indices --"
                            ), " Swap the indices of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "RevComp index 1 --"
                            ), " Reverse complement the first index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "RevComp index 2 --"
                            ), " Reverse complement the second index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "RevSeq index 1 --"
                            ), " Reverse the sequence of the first index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "RevSeq index 2 --"
                            ), " Reverse the sequence of the second index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "Trim index 1 --"
                            ), " Trim the first index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "Trim index 2 --"
                            ), " Trim the second index of the selected rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "Set index 1 --"
                            ), " Set the first index of the selected rows to a specific value.",
                            html.Br(),html.Br(),
                            html.B(
                                "Set index 2 --"
                            ), " Set the second index of the selected rows to a specific value.",
                            html.Br(),html.Br(),
                            html.B(
                                "Reset Value"
                            ), " -- Set the value to reset the selected rows to.",
                            html.Br(),html.Br(),
                            html.B(
                                "Check / Uncheck All --"
                            ), " Check or uncheck all rows.",
                            html.Br(),html.Br(),
                            html.B(
                                "Update B-Fabric --"
                            ), " Update the barcodes of the selected rows in B-Fabric."
                        ], style={"margin-left": "2vw"}),
                        html.Br(),            
                        ], style={"margin-left": "2vw"}),
                        html.H4("Report a Bug Tab"),
                        html.P([
                            "If you encounter a bug while using this app, please fill out a bug report in the \"Report a Bug\" tab, so that it can be addressed by the developer."
                    ],
                    style={"margin-top":"2vh", "margin-left":"2vw", "padding-right":"40px"},
                ),],
                width=9,
            ),
        ],
    style={"margin-top": "0px", "min-height": "40vh", "height":"70vh", "max-height":"70vh", "overflow-y":"scroll", "padding-right":"40px", "padding-top":"20px"}
)

report_bug_tab = dbc.Row(
    id="page-content-bug-report",
    children=[
        dbc.Col(
            html.Div(
                id="sidebar_bug_report",
                children=empty_sidebar,
                style={"border-right": "2px solid #d4d7d9", "height": "100%", "padding": "20px", "font-size": "20px"}
            ),
            width=3,
        ),
        dbc.Col(
            html.Div(
                id="page-content-bug-report-children",
                children=[
                    html.H2("Report a Bug"),
                    html.P([
                        "Please use the form below to report a bug in the Draugr UI. If you have any questions, please email the developer at ",
                        html.A(" griffin@gwcustom.com", href="mailto:griffin@gwcustom.com"),
                    ]),
                    html.Br(),
                    html.H4("Session Details: "),
                    html.Br(),
                    html.P(id="session-details", children="No Active Session"),
                    html.Br(),
                    html.H4("Bug Description"),
                    dbc.Textarea(id="bug-description", placeholder="Please describe the bug you encountered here.", style={"width": "100%"}),
                    html.Br(),
                    dbc.Button("Submit Bug Report", id="submit-bug-report", n_clicks=0, style={"margin-bottom": "60px"}),
                    html.Br(),
                ],
                style={"margin-top":"2vh", "margin-left":"2vw", "font-size":"20px", "padding-right":"40px"},
            ),
            width=9,
        ),
    ],
    style={"margin-top": "0px", "min-height": "40vh"}
)


tabs = dbc.Tabs(
    [
        dbc.Tab(main_tab, label="Update Barcodes"),
        dbc.Tab(docs_tab, label="Documentation"),
        dbc.Tab(report_bug_tab, label="Report a Bug"),
    ]
)