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
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
            ),
            html.Br(),
            html.P(id="sidebar_text_3", children="Select data format:"),
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

not_qc_plate = [
    html.P("The plate you've selected is not a QC plate. Please select a QC plate to continue."),
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
                        html.H2("Welcome to The QC Upload App"),
                        html.P([
                            "This app serves as a user interface for uploading QC data directly to BFabric plate objects, to reduce the overall impact of manual data entry on laboratory efficiency."
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
                            This app is designed to allow users to add QC values from laboratory instruments en masse to B-Fabric. """
                        ]),
                        html.Br(),
                        html.P([
                            """

                            This app communicates with the B-Fabric API to fetch and save data in bfabric.
                            Please make sure to manually validate that any action taken on this application, to add QC values to B-Fabric plates, has been executed successfully in B-Fabric.
                            """
                        ]),
                        html.Br(),
                        html.P("""
                            \n\n
                            The app uses in-memory storage to make it simple to reset the barcodes to their initial state (by simply refreshing the page).
                            However, this means that the app will not remember the state of your samples if the page is refreshed. 
                            Only refresh the page after you have saved the samples in B-Fabric, or if you wish to reset the application to its initial state.
                            """
                        ),
                        html.H4("Update QC Values Tab"),
                        html.P([
                            html.B(
                                "Select Instrument --"
                            ), " Select the instrument which produced the data you intend to upload.",
                            html.Br(),html.Br(),
                            html.B(
                                "Select Data Type --"
                            ), " Select the data type (for instruments which can produce data for more than one sample type).",
                            html.Br(),html.Br(),
                            html.B(
                                "Select Data Format --"
                            ), " Select the format of the file which you'll upload.",
                            html.Br(),html.Br(),
                            html.B(
                                "Drag and Drop or Select a File --"
                            ), " This is where you can upload the file which was produced by the instrument.",
                            html.Br(),html.Br(),
                            html.B(
                                "Submit --"
                            ), " Once you've uploaded data, you should see \"Merged Dataset\" appear instead of \"B-Fabric Data\". Now your data is ready for upload. In this instance, you can click \"Submit\" to trigger the upload to B-Fabric.",
                            html.Br(),html.Br(),
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
        dbc.Tab(main_tab, label="Update QC Values"),
        dbc.Tab(docs_tab, label="Documentation"),
        dbc.Tab(report_bug_tab, label="Report a Bug"),
    ]
)

alerts = [    
    dbc.Alert(
        children=[],
        id="alert-n-samples",
        dismissable=True,
        is_open=False,
        color="warning",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[],
        id="alert-merge-success",
        dismissable=True,
        is_open=False,
        color="success",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[],
        id="alert-not-qc-plate",
        dismissable=True,
        is_open=False,
        color="danger",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[], 
        id="alert-upload-error",
        dismissable=True,
        is_open=False,
        color="danger",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[],
        id="alert-upload-success",
        dismissable=True,
        is_open=False,
        color="success",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[],
        id="alert-merge-error",
        dismissable=True,
        is_open=False,
        color="danger",
        style={"max-width":"80vw", "margin":"10px"}
    ),
    dbc.Alert(
        "Failed to submit bug report! Please email the developers directly at the email below!",
        id="alert-fade-bug-fail", 
        dismissable=True,
        is_open=False, 
        color="danger",
        style={"max-width":"50vw", "margin":"10px"}
    ),
    dbc.Alert(
        "You're bug report has been submitted. Thanks for helping us improve!",
        id="alert-fade-bug",
        dismissable=True,
        is_open=False,
        color="info",
        style={"max-width":"50vw", "margin":"10px"}
    ),
    dbc.Alert(
        children=[],
        id="alert-no-data",
        dismissable=True,
        is_open=False,
        color="warning",
        style={"max-width":"80vw", "margin":"10px"}
    ),
]