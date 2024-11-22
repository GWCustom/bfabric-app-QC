from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import dash
from dash import dash_table
import json
import os
from dash import callback_context as ctx
from objects.QCDataset import QC_Dataset as QC
# import bfabric
from utils import auth_utils, components
from utils.upload_utils import parse_contents as pc
from utils.objects import Logger

if os.path.exists("./PARAMS.py"):
    try:
        from PARAMS import PORT, HOST, DEV
    except:
        PORT = 8050
        HOST = 'localhost'
        DEV = True
else:
    PORT = 8050
    HOST = 'localhost'
    DEV = True
    

####### Main components of a Dash App: ########
# 1) app (dash.Dash())
# 2) app.layout (html.Div())
# 3) app.callback()

#################### (1) app ####################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

#################### (2) app.layout ####################

app.layout = html.Div(
    children=[
        dcc.Location(
            id='url',
            refresh=False
        ),
        dbc.Container(
            children=[    
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            className="banner",
                            children=[
                                html.Div(
                                    children=[
                                        html.P(
                                            'QC Upload App',
                                            style={'color':'#ffffff','margin-top':'15px','height':'80px','width':'100%',"font-size":"40px","margin-left":"20px"}
                                        )
                                    ],
                                    style={"background-color":"#000000", "border-radius":"10px"}
                                ),
                            ],
                        ),
                    ),
                ),
                dbc.Row(
                    dbc.Col([
                        html.Div(
                            children=[html.P(id="page-title",children=[str("QC Upload App")], style={"font-size":"40px", "margin-left":"20px", "margin-top":"10px"})],
                            style={"margin-top":"0px", "min-height":"80px","height":"6vh","border-bottom":"2px solid #d4d7d9"}
                        ),
                        dcc.Loading([    
                            html.Div(
                                children=components.alerts,
                            ),
                        ]),
                    ])
                ),
                components.tabs,
            ], style={"width":"100vw"},  
            fluid=True
        ),
        dcc.Store(id='token', storage_type='session'), # Where we store the actual token
        dcc.Store(id='entity', storage_type='session'), # Where we store the entity data retrieved from bfabric
        dcc.Store(id='token_data', storage_type='session'), # Where we store the token auth response
        dcc.Store(id='qc-data', storage_type='session'),
        dcc.Store(id='log', storage_type='session'), # Where we store the log data
        dcc.Store(id='dummy-output', storage_type='memory'), # Dummy output for logger
        components.modal_submit,
    ],style={"width":"100vw", "overflow-x":"hidden", "overflow-y":"scroll"}
)


#Callback to safe the log data in the dcc store
@app.callback(
    Output('dummy-output', 'data'),#dummy output!
    [Input('log', 'data')]
)
def process_data(log):
    if log:
        Logger.from_pickle(log)
        return None  # Dummy output, not used



@app.callback(
    [
        Output("alert-fade-bug", "is_open"),
        Output("alert-fade-bug-fail", "is_open")
    ],
    [
        Input("submit-bug-report", "n_clicks")
    ],
    [
        State("token", "data"),
        State("entity", "data"),
        State("bug-description", "value"),
        State("log", "data")
    ]
)
def submit_bug_report(n_clicks, token, entity_data, bug_description, log_data):

    if token: 
        token_data = json.loads(auth_utils.token_to_data(token))
    else:
        token_data = ""

    if n_clicks:
        try:
            sending_result = auth_utils.send_bug_report(
                token_data=token_data,
                entity_data=entity_data,
                description=bug_description,
                log_data = log_data
            )

            if sending_result:
                return True, False
            else:
                return False, True
        except:
            print("sending_results")
            return False, True

    return False, False


@app.callback(
    [
        Output("alert-upload-success", "children"),
        Output("alert-upload-success", "is_open"),
        Output("alert-upload-error", "children"),
        Output("alert-upload-error", "is_open"),
        Output("alert-no-data", "children"),
        Output("alert-no-data", "is_open"),
    ],
    [
        Input("submit-val", "n_clicks"),
    ],
    [
        State("qc-data", "data"),
        State("token", "data"),
        State("dropdown-select-inst", "value"),
        State("upload-type", "value"),
        State("qc-type", "value"),
        State("log", "data"),
    ]
)
def submit(n_clicks, qc_data, token, dropdown_select_inst_value, upload_type, qc_type, log_data):

    qc_types = {
        "Frag":"Agilent Fragment Analyzer",
        "RNA":"Agilent TapeStation",
        "DNA":"Agilent TapeStation",
        "Glow":"GloMax QuantiFluor",
        "Qbit":"Qubit Flourometric Quantitation",
        "BioA":"Agilent Bioanalyzer",
        "BioRad":"qPCR",
        "Femto":"Agilent Femto Pulse"
    }

    AD = {
        "id":"id",
        "Integrity":"integritynumber",
        "Range":"sizerange",
        "Size":"averagesizeinrange",
        "Conc":"concentrationinrange",
        # "Conc":"concentration",
        "Molarity":"concentrationmolarinrange",
        "Well":"qualitycontroltype"
    }

    rnaAD = {
        "id":"id",
        "Integrity":"integritynumber",
        "Range":"sizerange",
        "Size":"averagesizeinrange",
        "Conc":"concentration",
        "Molarity":"concentrationmolarinrange",
        "Well":"qualitycontroltype"
    }

    try:
    # if True:
        button_clicked = ctx.triggered_id
        if button_clicked == "submit-val":
            if qc_data:
                data = json.loads(qc_data)
            else:
                no_data_alert = [
                    html.H3("You haven't uploaded any data."),
                    html.P("Please upload data before submitting.")
                ]
                return [], False, [], False, no_data_alert, True
        
            objs = []

            for elt in data['data']:

                tmp_obj = {}

                for i in range(len(data['columns'])):
                    key = data['columns'][i]
                    if key == "Well":
                        tmp_obj[rnaAD[key]] = qc_types[qc_type]
                    else: 
                        tmp_obj[rnaAD[key]] = str(elt[i])
                # print(tmp_obj)
                objs.append(tmp_obj)

            tdata = json.loads(auth_utils.token_to_data(token))
            wrapper = auth_utils.token_response_to_bfabric(tdata)

            n_sammples_saved = 0

            try: 

                for elt in objs: 
                    #res = wrapper.save(endpoint="sample", obj=elt)
                    L = Logger.from_pickle(log_data)


                    qc_params = {
                        "instrument": dropdown_select_inst_value,
                        "data_type": qc_type,
                        "data_format": upload_type,
                        "submit_button_clicks": n_clicks,
                    }
                    
                    res = L.logthis(
                        api_call=wrapper.save,
                        endpoint="sample",
                        obj=elt,
                        qc_params=qc_params,
                        make_log_api_call = True,
                        )


                    print(res)
                    n_sammples_saved += 1


            except Exception as e:
                print(e)
                alert_children = [
                    html.H3("Upload Failed."),
                    html.P("Please try again. If you continue to encounter issues, please submit a bug report using the bug report tab."),
                    html.P(f"Internal Traceback: {e}")
                ]
                return [], False, alert_children, True, [], False

            success_alert_children = [
                html.H3("Upload Successful!"),
                html.P([html.B(f"{n_sammples_saved}"), " samples were uploaded to Bfabric."])
            ]
            return success_alert_children, True, [], False, [], False
        else: 
            return [], False, [], False, [], False

    except Exception as e: 
    # else:
        print(e)
        alert_children = [
            html.H3("Upload Failed."),
            html.P("Please try again. If you continue to encounter issues, please submit a bug report using the bug report tab."),
            html.P(f"Internal Traceback: {e}")
        ]
        return [], False, alert_children, True
            

@app.callback(
    Output("modal", "is_open"),
    [Input("submit-val-intro", "n_clicks"), Input("submit-val", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    [
        Output('token', 'data'),
        Output('token_data', 'data'),
        Output('entity', 'data'),
        Output('page-content', 'children'),
        Output('page-title', 'children'),
        Output('dropdown-select-inst', 'disabled'),
        Output('drag-drop', 'disabled'),
        Output('submit-val-intro', 'disabled'),
        Output('alert-not-qc-plate', 'children'),
        Output('alert-not-qc-plate', 'is_open'),
        Output('log', 'data')
    ],
    [
        Input('url', 'search'),
    ],
    [
        State("dropdown-select-inst", "value"),
        State("upload-type", "value"),
        State("qc-type", "value"),
    ]
)
def display_page(url_params, dropdown_select_inst_value, qc_type, upload_type):
    
    base_title = ""

    if not url_params:
        return None, None, None, components.no_auth, base_title, True, True, True, [], False, None
    
    token = "".join(url_params.split('token=')[1:])
    tdata_raw = auth_utils.token_to_data(token)
    
    if tdata_raw:
        if tdata_raw == "EXPIRED":
            return None, None, None, components.expired, base_title, True, True, True, [], False, None

        else: 
            tdata = json.loads(tdata_raw)
    else:
        return None, None, None, components.no_auth, base_title, True, True, True, [], False, None
    
    if tdata:

        qc_params = {
            "instrument": dropdown_select_inst_value,
            "data_type": qc_type,
            "data_format": upload_type,
        }

        entity_data_json, logger_instance = auth_utils.entity_data(tdata, qc_params)
        entity_data = json.loads(entity_data_json)
        page_title = f"{base_title}{tdata['entityClass_data']} {tdata['entity_id_data']}: {entity_data['name']}" if tdata else "Bfabric App Interface"

        if entity_data['type'] != "Quality Control":
            alert = [
                html.H3("This plate is not a Quality Control plate."),
                html.P("Please make sure you're using the correct plate type, and try again.")
            ]
            return token, tdata, entity_data, components.not_qc_plate, page_title, True, True, True, alert, True, None

        
        if not tdata:
            return token, None, None, components.no_auth, page_title, True, True, True, [], False, None
        
        elif not entity_data:
            return token, None, None, components.no_entity, page_title, True, True, True, [], False, None
        
        else:
            if not DEV:
                return token, tdata, entity_data, components.auth, page_title, False, False, False, [], False, logger_instance.to_pickle()
            else: 
                return token, tdata, entity_data, components.dev, page_title, True, True, True, [], False, None
    else: 
        return None, None, None, components.no_auth, base_title, True, True, True, [], False, None


@app.callback(Output('next-card', 'children'),
              [Input('dropdown-select-inst', 'value')])
def generate_qc_dropdown(obj):

    if obj == "RNA":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "Standard Sensitivity RNA",
                        "value": "RNA"
                    },
                    {
                        "label": "High Sensitivity RNA",
                        "value": "HSRNA",
                    },],
                clearable=False,
                searchable=False,
                value="RNA",
                
            ),
            html.Br(), 
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "Sample Table",
                        "value": "ST"
                    },
                    {
                        "label": "Compact Region Table",
                        "value": "CRT",
                    },],
                clearable=False,
                searchable=False,
                value="CRT",
                
            ),
        ]
    elif obj == "DNA":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
            id="qc-type",
            options=[
                {
                    "label": "Standard Sensitivity D1000",
                    "value": "D1k"
                },
                {
                    "label": "High Sensitivity D1000",
                    "value": "HSD1k",
                },
                {
                    "label": "gDNA",
                    "value": "gDNA",
                },
                {
                    "label": "Standard Sensitivity D5000",
                    "value": "D5k",
                },
                {
                    "label": "High Sensitivity D5000",
                    "value": "HSD5k",
                },
            ],
            clearable=False,
            searchable=False,
            value="D1k",
            
        ),
        html.Br(), 
        html.P(id="sidebar_text_3", children="Select data format:"),
        dcc.Dropdown(
            id="upload-type",
            options=[
                {
                    "label": "Sample Table",
                    "value": "ST"
                },
                {
                    "label": "Compact Region Table",
                    "value": "CRT",
                },],
            clearable=False,
            searchable=False,
            value="CRT",
            
        ),]

    elif obj == "Qbit":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "Qubit DNA",
                        "value": "QDNA"
                    },
                    {
                        "label": "Qubit RNA",
                        "value": "QRNA",
                    },
                ],
                clearable=False,
                searchable=False,
                value="QO",
                
            ),
            html.Br(), 
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "Qubit CSV Upload",
                        "value": "QbitUpload"
                    },
                ],
                clearable=False,
                searchable=False,
                value="QO",
                
            ),
        ]

    elif obj == "BioA":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "DNA",
                        "value": "BioA-DNA"
                    },
                    {
                        "label": "RNA",
                        "value": "BioA-RNA",
                    },],
                clearable=False,
                searchable=False,
                value="DNA",
                
            ),
            html.Br(),
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "BioAnalyzer Output",
                        "value": "BioAnalyzerUpload"
                    },
                ],
                clearable=False,
                searchable=False,
                value="BAO",
                
            ),
        ]

    elif obj == "BioRad":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "DNA",
                        "value": "BioRad-DNA"
                    },
                    {
                        "label": "RNA",
                        "value": "BioRad-RNA",
                    },],
                clearable=False,
                searchable=False,
                value="DNA",
                
            ),
            html.Br(),
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "BioRad Output",
                        "value": "BioRadUpload"
                    },
                ],
                clearable=False,
                searchable=False,
                value="BRO",
                
            ),
        ]

    elif obj == "Femto":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "DNA",
                        "value": "Femto-DNA"
                    },
                    {
                        "label": "RNA",
                        "value": "Femto-RNA",
                    },],
                clearable=False,
                searchable=False,
                value="DNA",
                
            ),
            html.Br(),
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "FemtoPulse Output",
                        "value": "FemtoPulseUpload"
                    },
                ],
                clearable=False,
                searchable=False,
                value="FPO",
                
            ),
        ]

    elif obj == "Frag":
        new_drop = [
            html.P(id="sidebar_text_2", children="Select data type:"),
            dcc.Dropdown(
                id="qc-type",
                options=[
                    {
                        "label": "RNA",
                        "value": "RNA"
                    },
                    {
                        "label": "NGS",
                        "value": "DNA",
                    },],
                clearable=False,
                searchable=False,
                value="DNA",
                
            ),
            html.Br(),
            html.P(id="sidebar_text_3", children="Select data format:"),
            dcc.Dropdown(
                id="upload-type",
                options=[
                    {
                        "label": "Fragment Analyzer Output",
                        "value": "FAO"
                    },
                ],
                clearable=False,
                searchable=False,
                value="FAO",
            ),
        ]

    else:
        new_drop = []

    return new_drop



@app.callback(
    output=[
        # Output('div-graphs-qc','children'),
        Output('auth-div','children'),
        Output('qc-data','data'),
        Output('alert-n-samples','children'),
        Output('alert-n-samples','is_open'),
        Output('alert-merge-error','children'),
        Output('alert-merge-error','is_open'),
    ],
    inputs = [
        Input('drag-drop', 'contents')
    ],
    state=[
        State('dropdown-select-inst','value'),
        State('token','data'),
        State('qc-type','value'),
        State('upload-type','value'),
        State('entity','data')
    ]
)
def generate_graph(fl, instrument, token, qcType, uploadType, entity_data): 

    alert_n_samples_title = [html.P("")]
    alert_merge_title = [html.P("")]
    alert_merge_open = False
    alert_n_samples_open = False

    print("INSTRIMENT")
    print(instrument)

    print("QC TYPE")
    print(qcType)

    print("UPLOAD TYPE")
    print(uploadType)

    try:

        token_data = auth_utils.token_to_data(token)
        if token_data is None:
            return components.no_auth, None, alert_n_samples_title, alert_n_samples_open, alert_merge_title, alert_merge_open
        plate = json.loads(token_data)['entity_id_data']

        send = html.Div()
        title = ""

        D = QC(entity_data)

        D.table_type = uploadType
        if instrument != "Frag":
            D.TS_type = qcType
        elif qcType is None: 
            pass
        else:
            D.TS_type = "FRAG_"+qcType

        if type(None) != type(fl):
            D.upload_dataset = pc(fl)

        if type(None) != type(plate):
            D.plate_number = plate

        if type(None) != type(plate) and type(None) != type(fl):
            D.merged()

            # send = html.Div([
            df = D.merged_dataset
            send = dash_table.DataTable(
                    df.to_dict("records"),
                    [{"name": i, "id": i} for i in df.columns],
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_cell={'padding':'10px'},
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                )
            
            if len(D.bfabric_dataset) != len(D.upload_dataset):
                alert_n_samples_title = [
                    html.H3("Warning: N Samples in your file ≠ N Samples on the bfabric plate."),
                    html.P("Please double-check that you've uploaded the correct data for the correct plate."),
                    html.P([f"Number of samples in the file you uploaded: ", html.B(f"{len(D.upload_dataset)}")]),
                    html.P([f"Number of samples assigned to the plate in Bfabric: ", html.B(f"{len(D.bfabric_dataset)}")])
                ]
                alert_n_samples_open = True
            title = "Merged Data"

        elif type(None) != type(plate) and type(None) == type(fl):
            df = D.bfabric_dataset
            send = dash_table.DataTable(
                    df.to_dict("records"),
                    [{"name": i, "id": i} for i in df.columns],
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220, 220, 220)',
                        }
                    ],
                    style_cell={'padding':'10px'},
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white'
                    },
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold'
                    }
                )
            title = "Bfabric Data"
            
        div_send = html.Div(
            children=[
                html.H3(title),
                html.Br(),
                send
            ],
            style={"margin-left":"2vw", "margin-right":"10vw", "font-size":"20px"}

        )
        
        return div_send, D.json, alert_n_samples_title, alert_n_samples_open, alert_merge_title, alert_merge_open

    except Exception as e: 

        print("ERROR")
        print(e)

        alert_merge_title = [
            html.H3("There was an error merging your file with the plate data in Bfabric."),
            html.P("Please double-check that the type of dataset you've specified matches the file you're uploading. If you've checked this and you're still having trouble, please submit a bug report using the bug report tab."),
            html.P(f"Internal Traceback: {e}")
        ]
        alert_merge_open = True

        return html.Div(), None, alert_n_samples_title, alert_n_samples_open, alert_merge_title, alert_merge_open

if __name__ == '__main__':
    app.run_server(debug=True, port=PORT, host=HOST)