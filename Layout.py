import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table
import plotly.graph_objs as go
from os import listdir
from os.path import isfile, join, abspath
import os
'''
This file contains the HTML layout of the application.
'''
def layout(app):
    bV = go.Scatter(
        x=[0],
        y=[0],
        name='Voltage (V)',
        mode='lines', line=dict(color='rgb(255,0,0)')
    )
    ahrChange = go.Scatter(
        x=[0],
        y=[0],
        name='Ahr Change',
        mode='lines', line=dict(color='rgb(210,194,49)'),
        yaxis='y4'
    )
    SOC = go.Scatter(
        x=[0],
        y=[0],
        name='SOC',
        yaxis='y2',
        mode='lines', line=dict(color='rgb(0, 255, 100)')
    )
    current = go.Scatter(
        x=[0],
        y=[0],
        name='Current (A)',
        yaxis='y3',
        mode='lines', line=dict(color='rgb(0,0,255)')
    )
    power = go.Scatter(
        x=[0],
        y=[0],
        name='Power (W)',
        yaxis='y2',
        mode='lines', line=dict(color='rgb(0, 255, 100)')
    )
    lc = go.Scatter(
        x=[0],
        y=[0],
        name='Load Current (A)',
        yaxis='y3',
        mode='lines', line=dict(color='rgb(0, 0, 255)')
    )
    lv = go.Scatter(
        x=[0],
        y=[0],
        name='Load Voltage (V)',
        mode='lines', line=dict(color='rgb(255,0,0)')
    )

    sP = go.Scatter(
        x=[0],
        y=[0],
        name='Power (W)',
        yaxis='y2',
        mode='lines', line=dict(color='rgb(255,0,255)')
    )
    sI = go.Scatter(
        x=[0],
        y=[0],
        name='Current (A)',
        yaxis='y3',
        mode='lines', line=dict(color='rgb(0, 0, 255)')
    )
    sV = go.Scatter(
        x=[0],
        y=[0],
        name='Voltage (V)',
        mode='lines', line=dict(color='rgb(255,0,0)')
    )
    power = go.Scatter(
        x=[0],
        y=[0],
        name='Load Power (W)',
        yaxis='y4',
        mode='lines', line=dict(dash='dot', color='rgb(255, 0, 255)')
    )

    solarAP = go.Scatter(
        x=[0],
        y=[0],
        name='Solar Array Power',
        yaxis='y2',
        legendgroup='array',
        mode='lines', line=dict(color='rgb(255,0,0)')
    )
    solarAI = go.Scatter(
        x=[0],
        y=[0],
        name='Solar Array Current',
        legendgroup='array',
        mode='lines', line=dict(color='rgb(0,0,255)')
    )

    systempath = os.getcwd() + '/Presets/System/'
    batterypath = os.getcwd() + '/Presets/Battery/'
    loadpath = os.getcwd() + '/Presets/Load/'
    orbitpath = os.getcwd() + '/Presets/Orbit/'
    solarpath = os.getcwd() + '/Presets/Solar/'
    systemfiles = [f for f in listdir(systempath) if isfile(join(systempath, f))]
    batteryfiles = [f for f in listdir(batterypath) if isfile(join(batterypath, f))]
    loadfiles = [f for f in listdir(loadpath) if isfile(join(loadpath, f))]
    orbitfiles = [f for f in listdir(orbitpath) if isfile(join(orbitpath, f))]
    solarfiles = [f for f in listdir(solarpath) if isfile(join(solarpath, f))]
    optionList = []
    optionList.append({'label': 'Custom...', 'value': 'custom'})
    optionList.append({'label': '=========System=========', 'value': '', 'disabled': True})
    for i in systemfiles:
        optionList.append({'label': i, 'value': systempath + i})
    optionList.append({'label': '=========Battery========', 'value': '', 'disabled': True})
    for i in batteryfiles:
        optionList.append({'label': i, 'value': batterypath + i})
    optionList.append({'label': '=========Load===========', 'value': '', 'disabled': True})
    for i in loadfiles:
        optionList.append({'label': i, 'value': loadpath + i})
    optionList.append({'label': '=========Orbit==========', 'value': '', 'disabled': True})
    for i in orbitfiles:
        optionList.append({'label': i, 'value': orbitpath + i})
    optionList.append({'label': '======Solar Array=======', 'value': '', 'disabled': True})
    for i in solarfiles:
        optionList.append({'label': i, 'value': solarpath + i})
    app.layout = html.Div([
        html.Div(id='junk'), 
        html.Div(id='prev_clicks_run', hidden=True), 
        html.Div(id = 'prev_clicks_import', hidden = True),
        html.Div(id = 'prev_num_sides', hidden = True),
        html.Div(id = 'prev_num_EOL', hidden = True),
        dcc.ConfirmDialog(
            id='exportRaw'
        ),
        dcc.ConfirmDialog(
            id='confirm-zerodivision-error',
            message='Please fill out all fields or check for zero values',
        ),   
        html.Div([
            
            html.Div([
                html.Div([
                    # html.Img(src=app.get_asset_url('nasa-logo.png'), id='logo'),
                    html.Img(src=app.get_asset_url('eps design tool logo.png'), id = 'title'),
                ],id = 'logo-title-header'),
                html.Div([
                    html.Div([
                        html.Img(src=app.get_asset_url('show.png'), id = 'show-tabs', className = 'icon'), 
                        html.Div(html.P('Show Tabs')),
                        ], id = 'show-container', className = 'input-container'),
                    html.Div([
                        html.Img(src=app.get_asset_url('collapse.png'), id = 'hide-tabs', className = 'icon'),
                        html.Div(html.P('Hide Tabs')),
                        ], id = 'hide-container', className = 'input-container'),
                ]),
            ]),
            html.Div([ #naming
                html.Div([
                    html.Div([html.Img(src=app.get_asset_url('satellite icon.png'), className='icon'), html.P('System:', id='systemName')], className = 'input-container magnify'),
                    html.Div(children=[html.Img(src=app.get_asset_url('battery icon.png'), className='icon'), html.P('Battery:', id='batteryName')], className = 'input-container magnify'),
                    html.Div(children=[html.Img(src=app.get_asset_url('flash icon.png'), className='icon'), html.P('Load:', id='loadName')], className = 'input-container magnify')
                ], id='left-name'),
                html.Div([
                    html.Div([html.Img(src=app.get_asset_url('orbit.png'), className='icon'), html.P('Orbit:', id='orbitName')], className = 'input-container magnify'),
                    html.Div([html.Img(src=app.get_asset_url('solar panel.png'), className='icon'), html.P('Solar Array:', id='solarName')], className = 'input-container magnify')
                ], id='right-name') 
            ], id='name-container'),
            html.Div([
                html.Div([dcc.Dropdown(id='input_dropdown', options=optionList),]),
                html.Div([
                    html.Button('Update', id='import-button', hidden = True, className='button')
                ], id = 'import-button-container', style = {'display':'none'}),
            ], style = {'padding':'none'}),
            
            html.Div([
                dcc.Upload(
                id='import-upload',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                    ])
                )
            ], id = 'import-upload-container', style={'display':'none'}),
            
            
        ], className = 'input-container', id = 'header'),

        html.Div(children=[dcc.Loading(id='loadingRunButton', type='default', children=[html.A("Run", className='runButton', id='run_button')]), ], className='sticky', id='run-container'),
        # html.Div([html.Img(src=app.get_asset_url('blank-nasa-logo.png'), id='logo-button')]),
        html.Div([  # row with tabs and graphs
            # tabs
            
            html.Div([  # tabs
                dcc.Tabs(id="custom-tabs", children=[
                    #######################################################################################################
                    dcc.Tab(label='General', children=[
                        html.Div([
                            html.Div([html.H6("Select Power Topology"),],),
                            html.Div([
                                html.Div([
                                    dcc.RadioItems(
                                        id='power-reg-type',
                                        options=[{'label': 'PPT', 'value': 'PPT'}, {'label': 'DET', 'value': 'DET'}],
                                        className='save-dropdown',
                                        value='DET'
                                    )
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("PPT Efficiency(%)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100, 
                                                step = 0.0001, 
                                                disabled = True, 
                                                id = 'efficiency',
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ])
                            ], className='save-container'),
                            html.Hr(),
                            html.H6('Use Spinner Model?'),
                            html.Div([
                                dcc.RadioItems(
                                    options=[
                                        {'label': 'Yes', 'value': 'Yes'},
                                        {'label': 'No', 'value': 'No'}
                                    ],
                                    value='No',
                                    id='use-spinner'
                                ),
                            ], className='save-container'),
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='general-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')
                    ], className='custom-tab')
                    ######################################################################################################################3
                    , dcc.Tab(label='Battery', children=[
                        html.Div([
                            html.Div([
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Initial SOC (%)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100, 
                                                step=0.0001,
                                                id = 'initial-soc',
                                                value=90,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Capacity (AHr)"),
                                            dbc.Input(
                                                type = "number", 
                                                max=10000000000,
                                                min=0, 
                                                step=0.0001,
                                                id = 'capacity',
                                                value=1000,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Cells in Series"),
                                            dbc.Input(
                                                type = "number", 
                                                max=10000000000,
                                                min=0, 
                                                step=1,
                                                id = 'num-cells',
                                                value=8,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], className='save-container', id = 'battery-input-row'),
                            html.Div([  # input container
                                html.Div([
                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Max Charging Current"),
                                            dbc.Input(
                                                type = "number", 
                                                max=10000000000,
                                                min=0, 
                                                step=0.0001,
                                                id = 'max-current',
                                                value=40,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                    ]),
                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Int. Resistance (Chg)"),
                                            dbc.Input(
                                                type = "number", 
                                                max=10000000000,
                                                min=0, 
                                                step=0.0001,
                                                id = 'int-resistance-chg',
                                                value=0.01,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                    ]),
                                    dash_table.DataTable(
                                        id='battery-charging-table', style_table={
                                            'height': '300px',
                                            'overflowY': 'scroll',
                                            'border': 'thin lightgrey solid'
                                        },
                                        columns=[{
                                            'name': 'Charging SOC',
                                            'id': 'cSOC',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Charging V',
                                            'id': 'cV',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }
                                        ],
                                        data=[
                                            {'cSOC': 0,
                                             'cV': 0}
                                        ],
                                        editable=True,
                                        row_deletable=False,
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='input-container-l'),  # left input container
                                html.Div([
                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Max Charging Voltage"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000000, 
                                                step=0.0001,
                                                id = 'max-voltage',
                                                value=33.6,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Int. Resistance (Dischg)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000, 
                                                step=0.0001,
                                                id = 'int-resistance-dchg',
                                                value=0.01,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                    dash_table.DataTable(
                                        id='battery-discharging-table', style_table={
                                            'height': '300px',
                                            'overflowY': 'scroll',
                                            'border': 'thin lightgrey solid'
                                        },
                                        columns=[{
                                            'name': 'Discharging SOC',
                                            'id': 'dSOC',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Discharging V',
                                            'id': 'dV',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }
                                        ],
                                        data=[
                                            {'dSOC': 0,
                                             'dV': 0}
                                        ],
                                        editable=True,
                                        row_deletable=False,
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='input-container-r')  # right input container
                            ], className='input-container'),
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='battery-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')
                    ], className='custom-tab')
                    ##################################################################################################
                    , dcc.Tab(label='Load', children=[
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.P('Load Input', style={'font-size': '13px'}),
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Constant Load', 'value': 'constant'},
                                            {'label': 'Custom Load Profile', 'value': 'custom'},
                                            {'label': 'Custom Periodic Load Profile', 'value': 'custom-orbit'}
                                        ],
                                        value='custom',
                                        id='use-constant-load'
                                    ),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Line Drop (V)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000, 
                                                step=0.0001,
                                                id = 'line-drop-load',
                                                value=0,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], className='save-container')  # input container
                            , html.Div([dash_table.DataTable(
                                id='load-table', style_table={
                                    'height': '300px',
                                    'overflowY': 'scroll',
                                    'border': 'thin lightgrey solid'
                                },
                                columns=[{
                                    'name': 'Time (mins)',
                                    'id': 'time',
                                    'type': 'numeric',
                                    'deletable': False,
                                    'renamable': False,
                                    'clearable': True
                                }, {
                                    'name': 'Load Power',
                                    'id': 'Load',
                                    'type': 'numeric',
                                    'deletable': False,
                                    'renamable': False,
                                    'clearable': True
                                }
                                ],
                                data=[
                                    {'time': 0,
                                     'Load': 0}
                                ],
                                editable=True,
                                row_deletable=True,
                                export_headers='display',
                                style_cell={
                                    'color': 'black',
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'maxWidth': 50,
                                }
                            )
                            ], id='load-table-container', className='table-container'),
                            html.Div([
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Load Power (W)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000, 
                                                step=0.0001,
                                                id = 'constant-load',
                                                value=1000,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], id='constant-load-container'),
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='load-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')
                    ], className='custom-tab')
                    #######################################################################################################################3
                    , dcc.Tab(label='Orbit', children=[
                        html.Div([
                            html.Div([
                                html.P("Orbit Type", className='sc-bwzfXH.eYbLCt', id='orbit-label'),
                                dcc.Dropdown(
                                    id='orbit-type',
                                    options=[
                                        {'label': 'L1', 'value': 'L1'}, {'label': 'L2', 'value': 'L2'},
                                        {'label': 'LEO', 'value': 'LEO'}],
                                    value='LEO'
                                ),

                            ], id='orbit-picker'),
                            # html.P("Note: Choose a time interval less than or equal to your data time steps"),
                            html.Div([
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Start Time (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 1000000000, 
                                                step=0.0001,
                                                id = 'start-time',
                                                value=0,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("End Time (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000000, 
                                                step=0.0001,
                                                id = 'end-time',
                                                value=600,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Time Interval (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000000, 
                                                step=0.0001,
                                                id = 'timestep',
                                                value=1,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], className='save-container'),
                            html.Div([
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Orbit Period (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000, 
                                                step=0.0001,
                                                id = 'period',
                                                value=92,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Eclipse Length (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000, 
                                                step=0.0001,
                                                id = 'eclipse-length',
                                                value=31,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], id='LEO-orbit-container', className='save-container'),
                            html.Div([
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Eclipse Start Time (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000000, 
                                                step=0.0001,
                                                id = 'eclipse-start',
                                                value=10,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Eclipse End Time (mins)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 10000000000, 
                                                step=0.0001,
                                                id = 'eclipse-end',
                                                value=100,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                            ], id='constant-orbit-container', className='save-container'),
                            # TODO: some error if end time < start time?
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='orbit-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')

                    ], className='custom-tab')
                    #####################################################################################################################
                    , dcc.Tab(label='Solar Array', children=[
                        
                            html.Div([
                                html.Div([
                                    html.H6('Solar Model'),
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Simple', 'value': 'Simple'},
                                            {'label': 'Complex', 'value': 'Complex'}
                                        ],
                                        value='Complex',
                                        id='use-simple-solar'
                                    ),
                                    
                                
                            ], className='save-container'),
                            html.Hr(),
                            html.Div(id='complex-solar-container', children=[
                                html.Div([
                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Line/Diode Drop (V)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000, 
                                                step=0.0001,
                                                id = 'line-drop-SA',
                                                value=0,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                    daq.NumericInput(
                                        id='num-sides',
                                        label='Number of Wings',
                                        labelPosition='top',
                                        max=10000,
                                        min=1,
                                        value=3,
                                    ),
                                    html.Div([
                                        html.P('Use Sun Angles?', style={'font-size': '13px'}),
                                        dcc.RadioItems(
                                            options=[
                                                {'label': 'Yes', 'value': 'Yes'},
                                                {'label': 'No', 'value': 'No'}
                                            ],
                                            value='No',
                                            id='use-sunangles'
                                        ),
                                    ])
                                ], className='save-container'),  # input container
                                html.Div([

                                    html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label('RPM'),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                max = 100000, 
                                                step=0.0001,
                                                id = 'rpm',
                                                value=0,
                                                className = 'styled-numeric-input',
                                                debounce=True)
                                        ]),
                                ]),
                                ], className='save-container', id='spinner-inputs'),
                                html.Div([
                                    html.P("Temperature Factors"),
                                    dash_table.DataTable(
                                        id='Temp-Coeff',
                                        columns=[{
                                            'name': 'Voltage, Open Circuit',
                                            'id': 'Voc',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Current, Open Circuit',
                                            'id': 'Isc',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Voltage, Max Power',
                                            'id': 'Vmp',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Current, Max Power',
                                            'id': 'Imp',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }
                                        ],
                                        data=[
                                            {'Voc': -0.0063,
                                            'Isc': 0.00058,
                                            'Vmp': -0.0067,
                                            'Imp': 0.00045}
                                        ],
                                        editable=True,
                                        row_deletable=False,
                                        export_headers='display',
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='table-container'),  # temp coeff
                                html.Div([
                                    html.P("BOL/EOL Factors"),
                                    html.Div([daq.NumericInput(
                                        id='num-EOL',
                                        label='Num. of Factors',
                                        labelPosition='top',
                                        max=100,
                                        min=1,
                                        value=1,
                                    ),
                                    html.Div([
                                        html.P('Use EOL Factors?', style={'font-size': '13px'}),
                                        dcc.RadioItems(
                                            options=[
                                                {'label': 'Yes', 'value': 'Yes'},
                                                {'label': 'No', 'value': 'No'}
                                            ],
                                            value='No',
                                            id='use-EOL'
                                        ),
                                    ]),], className = 'save-container'),
                                    dash_table.DataTable(
                                        id='Solar-Table-BOL',
                                        columns=[{
                                            'name': 'Voc',
                                            'id': 'Voc-val',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Isc',
                                            'id': 'Isc-val',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Vmp',
                                            'id': 'Vmp-val',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Imp',
                                            'id': 'Imp-val',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }
                                        ],
                                        data=[
                                            {'Voc-val': 2.711,
                                            'Isc-val': 0.945,
                                            'Vmp-val': 2.387,
                                            'Imp-val': 0.916
                                            },],
                                        editable=True,
                                        row_deletable=False,
                                        export_headers='display',
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    ),
                                ], className = 'table-container'),
                                
                                html.Div([dash_table.DataTable(
                                    id='Solar-Table-EOL',
                                    columns=[{
                                        'name': 'Factors',
                                        'id': 'EOL-factor-names',
                                        'deletable': False,
                                        'renamable': False,
                                        'clearable': True
                                    },{
                                        'name': 'Voc',
                                        'id': 'Voc-EOL',
                                        'type': 'numeric',
                                        'deletable': False,
                                        'renamable': False,
                                        'clearable': True
                                    }, {
                                        'name': 'Isc',
                                        'id': 'Isc-EOL',
                                        'type': 'numeric',
                                        'deletable': False,
                                        'renamable': False,
                                        'clearable': True
                                    }, {
                                        'name': 'Vmp',
                                        'id': 'Vmp-EOL',
                                        'type': 'numeric',
                                        'deletable': False,
                                        'renamable': False,
                                        'clearable': True
                                    }, {
                                        'name': 'Imp',
                                        'id': 'Imp-EOL',
                                        'type': 'numeric',
                                        'deletable': False,
                                        'renamable': False,
                                        'clearable': True
                                    }
                                    ],
                                    data=[
                                        {'EOL-factor-names': 'LEO aphelion distance factor',
                                        'Voc-EOL': 1,
                                        'Isc-EOL': 0.967,
                                        'Vmp-EOL': 1,
                                        'Imp-EOL': 0.967
                                            },],
                                    editable=True,
                                    row_deletable=False,
                                    export_headers='display',
                                    style_cell={
                                        'color': 'black',
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'maxWidth': 50,
                                    }
                                )], id = 'EOL-table-container', className = 'table-container'),
                                
                                html.Div([
                                    # html.Button('Add Wing', id='add-rows-button', n_clicks=0),
                                    # wings
                                    html.P("Solar Wings"),
                                    dash_table.DataTable(
                                        id='Solar-Table',
                                        columns=[{
                                            'name': 'Current Temp (C)',
                                            'id': 'current-temp',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'String Size',
                                            'id': 'string-size',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Segment Size',
                                            'id': 'segment-size',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Roll Angle',
                                            'id': 'roll',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Pitch Angle',
                                            'id': 'pitch',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }
                                        ],
                                        data=[
                                            {'current-temp': 107,
                                            'string-size': 20,
                                            'segment-size': 68,
                                            'roll': 0,
                                            'pitch': 0
                                            },
                                            {'current-temp': 107,
                                            'string-size': 20,
                                            'segment-size': 68,
                                            'roll': 60,
                                            'pitch': 0
                                            },
                                            {'current-temp': 107,
                                            'string-size': 20,
                                            'segment-size': 68,
                                            'roll': -60,
                                            'pitch': 0
                                            }
                                        ],
                                        editable=True,
                                        row_deletable=False,
                                        export_headers='display',
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='table-container'),  # aolarwings
                                html.Div([
                                    html.P("Import sun angles for each wing from 0 to 360"),
                                    dash_table.DataTable(
                                        id='sun-angle-table', style_table={
                                            'height': '300px',
                                            'overflowY': 'scroll',
                                            'border': 'thin lightgrey solid'
                                        },
                                        columns=[{
                                            'name': 'Orbit Angles',
                                            'id': 'orbit-angles',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 1)',
                                            'id': 'sun-angles-1',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 2)',
                                            'id': 'sun-angles-2',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 3)',
                                            'id': 'sun-angles-3',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }],
                                        data=[
                                            {'orbit-angles': 0,
                                            'sun-angles-1': 0,
                                            'sun-angles-2': 0,
                                            'sun-angles-3': 0}
                                        ], editable=True, row_deletable=True,
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='table-container', id='sun-angle-table-container'),  # sunangles
                                html.Div([
                                    html.P("Import sun angles for each wing for one orbit"),
                                    dash_table.DataTable(
                                        id='time-sun-angle-table', style_table={
                                            'height': '300px',
                                            'overflowY': 'scroll',
                                            'border': 'thin lightgrey solid'
                                        },
                                        columns=[{
                                            'name': 'Time',
                                            'id': 'time-sun-angles',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 1)',
                                            'id': 'time-sun-angles-1',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 2)',
                                            'id': 'time-sun-angles-2',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }, {
                                            'name': 'Sun Angle (wing 3)',
                                            'id': 'time-sun-angles-3',
                                            'type': 'numeric',
                                            'deletable': False,
                                            'renamable': False,
                                            'clearable': True
                                        }],
                                        data=[
                                            {'time-sun-angles': 0,
                                            'time-sun-angles-1': 0,
                                            'time-sun-angles-2': 0,
                                            'time-sun-angles-3': 0}
                                        ], editable=True, row_deletable=True,
                                        style_cell={
                                            'color': 'black',
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                            'maxWidth': 50,
                                        }
                                    )
                                ], className='table-container', id='time-sun-angle-table-container'),
                            ]),
                            html.Div(id='simple-solar-container', children=[
                                html.Div([
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Solar Power (W)"),
                                            dbc.Input(
                                                type = "number", 
                                                min = 0, 
                                                step = 0.0001, 
                                                value=0, 
                                                id = 'simple-solar-power',
                                                className = 'styled-numeric-input')
                                        ]),
                                ])    
                            ], className='save-container'),
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='solar-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')
                    ], className='custom-tab')
                    ######################################################################################################################
                    , dcc.Tab(label='Export', children=[
                        html.Div([                     
                            html.Div(children=[], id = 'export-error-container'),
                              # input container
                            html.H6("Export options"),
                            html.Div([
                                html.Div([
                                    html.P("System name: "),
                                    html.P("Battery name: "),
                                    html.P("Load name: "),
                                    html.P("Orbit name: "),
                                    html.P("Solar name: "),
                                ], id = 'export-labels'),
                                html.Div([
                                    dcc.Input(id='system-filename', placeholder='Name', type="text"),
                                    dcc.Input(id='battery-filename', placeholder='Name', type="text"),
                                    dcc.Input(id='load-filename', placeholder='Name', type="text"),
                                    dcc.Input(id='orbit-filename', placeholder='Name', type="text"),
                                    dcc.Input(id='solar-filename', placeholder='Name', type="text")
                                ], id = 'export-inputs'),
                                html.Div([
                                    html.Div(id='system-export-container'),
                                    html.Div(id='battery-export-container'),
                                    html.Div(id='load-export-container'),
                                    html.Div(id='orbit-export-container'),
                                    html.Div(id='solar-export-container'),
                                ], id = 'export-buttons'),
                            ], className = 'export-tab-style'),
                                 
                            html.Div([], className='save-container', id='raw_data_container'),
                            html.Hr(),
                            html.Div([
                                html.P("Click for detailed help"),
                                html.Img(src=app.get_asset_url('help.png'), className = 'helpButton', id='export-help-button'),
                            ], className='help-button-container')
                        ], className='tab-container')
                    ], className='custom-tab')
                    ######################################################################################################################
                ])
            ], className='pretty_container', id='all-tab-container'),

            # graphs
            html.Div([  # graph layout
                html.Div([  # tabs of graphs
                    dcc.Tabs(id="graph-custom-tabs", children=[
                        dcc.Tab(label='Battery', children=[
                            dcc.Graph(
                                id='battery_graph', className='graph-style', 
                                figure={
                                    'data': [
                                        bV, SOC, current, ahrChange
                                    ],
                                    'layout': go.Layout(
                                        title='Battery Voltage & SOC',
                                        autosize=True,
                                        legend_orientation='h',
                                        legend=dict(x=0.2, y=-0.05),
                                        margin=dict(l=50, r=50, t=50, b=50),
                                        xaxis=dict(domain=[0.1, 0.9], title='Orbit Time (minutes)', position=0),
                                        yaxis=dict(
                                            title='V', titlefont=dict(
                                                color='rgb(255, 0, 0)'

                                            ),
                                            tickfont=dict(
                                                color='rgb(255, 0, 0)'
                                            )
                                        ),
                                        yaxis2=dict(
                                            title='%',
                                            titlefont=dict(
                                                color='rgb(0, 255, 100)'
                                            ),
                                            tickfont=dict(
                                                color='rgb(0, 255, 100)'
                                            ),
                                            overlaying='y',
                                            side='right'

                                        ),
                                        yaxis3=dict(title="Current (A)",
                                                    titlefont=dict(
                                                        color="rgb(0,0,255)"
                                                    ),
                                                    tickfont=dict(
                                                        color="rgb(0,0,255)"
                                                    ),
                                                    anchor="free",
                                                    overlaying="y",
                                                    side="left",
                                                    position=0.05),
                                        yaxis4=dict(title="Ahr",
                                                    titlefont=dict(
                                                        color="rgb(210,194,49)"
                                                    ),
                                                    tickfont=dict(
                                                        color="rgb(210,194,49)"
                                                    ),
                                                    anchor="free",
                                                    overlaying="y",
                                                    side="right",
                                                    position=0.95)
                                    )
                                }
                            )
                        ]),
                        dcc.Tab(label='Load', children=[
                            dcc.Graph(
                                id='load_graph', className='graph-style', 
                                figure={
                                    'data': [
                                        power, lc, lv
                                    ],
                                    'layout': go.Layout(
                                        title='Load Profile',
                                        legend_orientation='h',
                                        legend=dict(x=0.2, y=-0.04),
                                        margin=dict(l=50, r=50, t=50, b=75),
                                        xaxis=dict(domain=[0.1, 0.95], title='Orbit Time (minutes)'),
                                        yaxis=dict(
                                            title='V', titlefont=dict(
                                                color='rgb(255, 0, 0)'

                                            ),
                                            tickfont=dict(
                                                color='rgb(255, 0, 0)'
                                            )
                                        ),
                                        yaxis2=dict(
                                            title='Power (W)',
                                            titlefont=dict(
                                                color='rgb(0, 255, 100)'
                                            ),
                                            tickfont=dict(
                                                color='rgb(0, 255, 100)'
                                            ),
                                            overlaying='y',
                                            side='right',
                                            position=0.975

                                        ),
                                        yaxis3=dict(title="Current (A)",
                                                    titlefont=dict(
                                                        color="rgb(0,0,255)"
                                                    ),
                                                    tickfont=dict(
                                                        color="rgb(0,0,255)"
                                                    ),
                                                    anchor="free",
                                                    overlaying="y",
                                                    side="left",
                                                    position=0.04)
                                    )
                                }
                            )
                        ]),
                        dcc.Tab(label='Solar Array', children=[
                            dcc.Graph(
                                id='solar_graph', className='graph-style',
                                figure={
                                    'data': [
                                    sV, sP, sI
                                ],
                                'layout': go.Layout(
                                    title='Solar Array Profile',
                                    legend_orientation='h',
                                    legend=dict(x=0.2, y=-0.04),
                                    margin=dict(l=50, r=75, t=50, b=75),
                                    xaxis=dict(domain=[0.1, 1], title='Orbit Time (minutes)'),
                                    yaxis=dict(
                                        title='V', titlefont=dict(
                                            color='rgb(255, 0, 0)'

                                        ),
                                        tickfont=dict(
                                            color='rgb(255, 0, 0)'
                                        )
                                    ),
                                    yaxis2=dict(
                                        title='Power (W)',
                                        titlefont=dict(
                                            color='rgb(255, 0, 255)'
                                        ),
                                        tickfont=dict(
                                            color='rgb(255, 0, 255)'
                                        ),
                                        overlaying='y',
                                        side='right'

                                    ),
                                    yaxis3=dict(title="Current (A)",
                                                titlefont=dict(
                                                    color="rgb(0,0,255)"
                                                ),
                                                tickfont=dict(
                                                    color="rgb(0,0,255)"
                                                ),
                                                anchor="free",
                                                overlaying="y",
                                                side="left",
                                                position=0.04)
                                )
                                }
                            )
                        ]),
                        dcc.Tab(label='IV Curves', children=[
                            dcc.Graph(
                                id='solarIV_graph',
                                className='graph-style',
                                figure={
                        'data': [solarAP, solarAI],
                        'layout': go.Layout(
                            title='Solar IV',
                            legend_orientation='h',
                            legend=dict(x=0.2, y=-0.08),
                            margin=dict(l=75, r=75, t=50, b=75),
                            xaxis=dict(domain=[0, 1], title=''),
                            yaxis=dict(
                                title='Current (A)', titlefont=dict(
                                    color='rgb(0,0,255)'

                                ),
                                tickfont=dict(
                                    color='rgb(0,0,255)'
                                )),
                            yaxis2=dict(
                                title='Power (W)', titlefont=dict(
                                    color='rgb(255,0,0)'

                                ),
                                tickfont=dict(
                                    color='rgb(255,0,0)'
                                ), overlaying='y',
                                side='right'
                            )
                        )

                    }
                            )
                        ])
                    ], vertical=True),
                ], id='graph-tab-container', className='pretty_container'),

                html.Div([  # system graph
                    dcc.Graph(
                        id='system_graph', className='graph-style',
                        style = {'width': '100%'},
                        figure={'data': [
            bV, SOC, current, sP, sI, sV, power, lc, lv
        ],
        'layout': go.Layout(
            title='Overall System',
            legend_orientation='h',
            legend=dict(x=0.2, y=-0.2),
            margin=dict(l=50, r=50, t=50, b=100),
            autosize=True,
            xaxis=dict(domain=[0.1, 0.90], title='Orbit Time (minutes)', position=0.1),
            yaxis=dict(
                title='V', titlefont=dict(
                    color='rgb(255, 0, 0)'

                ),
                tickfont=dict(
                    color='rgb(255, 0, 0)'
                )
            ),
            yaxis2=dict(
                title='%',
                titlefont=dict(
                    color='rgb(0, 255, 100)'
                ),
                tickfont=dict(
                    color='rgb(0, 255, 100)'
                ),
                overlaying='y',
                side='right'

            ),
            yaxis3=dict(title="Current (A)",
                        titlefont=dict(
                            color="rgb(0,0,255)"
                        ),
                        tickfont=dict(
                            color="rgb(0,0,255)"
                        ),
                        anchor="free",
                        overlaying="y",
                        side="left",
                        position=0.04),
            yaxis4=dict(title="Power (W)", titlefont=dict(
                color="rgb(255,0,255)"
            ),
                        tickfont=dict(
                            color="rgb(255,0,255)"
                        ),
                        anchor="free",
                        overlaying="y",
                        side="right",
                        position=0.98)
        )}
                    ),
                ], id='sys-graph', className='pretty_container'),
            ], className='block-display')

        ], className='flex-display'),

        # modal popouts for each tab section
        ####################################
        # help text will be populated with callbacks
        # general help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-general-popup', className='closeButton')], className = 'close-container'),
                html.H6("General Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                ****Make sure to click the Update button after selecting a preset or uploading a file****

                __*Power topology:*__ Allows you to select a DET or PPT topology.

                __*Spinner model:*__ When chosen, you can build a multi-sided spinner spacecraft. Note that this option assumes a polygonal shape and a normal sun angle to the exposed side.
                
                __*Importing:*__ Select from any of the presets or upload your own custom file. Any file type can be uploaded to the custom file select. Each file type corresponds to a tab in the simulation. EOL Factors are only stored in the system files.
                
                '''
                ],className='modal-text'),
            ], className='modal-content'),
                
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='general-help-container'),
        # battery help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-battery-popup', className='closeButton')], className = 'close-container'),
                html.H6("Battery Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                __*Initial SOC:*__ Allows you to specify a starting SOC for the simulation. 

                __*Capacity:*__ Specify battery capacity in Amp hours

                __*Cells in Series:*__ Specify number of cells in series for the battery. This simulation assumes that the charge/discharge curves you provide are for 8 cells in series.
                
                __*Max Charging Current/Voltage:*__ Given in Amps/Volts
                
                __*Internal Resistance:*__ Given in Ohms
                
                __*Charging/Discharging curves:*__ Upload battery charging curve data for 8 cells in series
                '''
                ],className='modal-text'),
            ], className='modal-content'),
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='battery-help-container'),
        # load help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-load-popup', className='closeButton')], className = 'close-container'),
                html.H6("Load Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                __*Constant load:*__  Allows you to specify one load for the entire duration of the simulation.

                __*Custom load:*__  Upload your own load profile for the length of the simulation. If the given profile is shorter than the load, it will take the last given value for the rest of the simulation.
               
                __*Custom periodic load:*__  Same functionality as custom load. If the given profile is shorter than the load, it will go back to the start of the profile. (Loop until the simulation ends)
                '''
                ],className='modal-text'),
            ], className='modal-content'),
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='load-help-container'),
        # orbit help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-orbit-popup', className='closeButton')], className = 'close-container'),
                html.H6("Orbit Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                __*Time Interval:*__ Specify the number of minutes between each time a point is generated. You can input decimal values to specify an interval less than one minute (input might be a little finicky, so use your arrow keys!).
                
                **Make sure this interval is smaller than the interval at which you specify load profile or sun angles in order to make full use of the given data.**

                __*LEO:*__ The simulation starts at the orbit’s noon point (middle of sun time). Changing the start time will change this starting position, i.e. If you had a 90 min orbit with a 40 min eclipse, you can adjust to start at the beginning of an eclipse by setting your start time at 25 mins.
                '''
                ],className='modal-text'),

                html.Img(src=app.get_asset_url('eclipse graphic.png'), width = '350px'),

                dcc.Markdown(['''
                __*L1/L2:*__ The specified eclipse time will occur relative to the given start and end times. It is a one time eclipse that does not occur periodically. 
                The distance factors used are: 
                * L1:(149.6/(148.11+2.5))**2
                * L2:(149.6/(151.1+2.5))**2
                '''
                ],className='modal-text'),
            ], className='modal-content'),
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='orbit-help-container'),
        # SA help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-solar-popup', className='closeButton')], className = 'close-container'),
                html.H6("Solar Array Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                __*Num. of Wings:*__ Specify number of wings on spacecraft or sides on a spinning spacecraft

                __*Sun Angles:*__ Specify if you want to use a custom sun angle profile on top of the constant roll and pitch angles. 
                * __*For LEO:*__ Enter sun angles for each degree orbit angle (0 to 360)
                * __*For L1/L2:*__ Enter sun angles for one orbit starting from t=0. This corresponds to t=0 provided as the start time. Note that if you start your simulation at t=25, then the program will choose the sun angle at t=25 for calculation.
                
                __*BOL Factors:*__ These parameters were measured at 28C

                __*EOL Factors:*__ Specify EOL Factors for the mission. These will only be saved in the .system file, and not the individual .solar file. You have the option of enabling them or disabling them for calculations. 
                
                __*Solar Wings:*__ Each row of the table represents one wing. For the spinner model, the roll and pitch angles will not be used for calculation and are grayed out.
                '''
                ],className='modal-text'),
            ], className='modal-content'),
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='solar-help-container'),
        # Export Help
        html.Div([
            html.Div([html.Div(children=[
                html.Div([html.Button("X", id='close-export-popup', className='closeButton')], className = 'close-container'),
                html.H6("Export Instructions"),
                html.Hr(),
                dcc.Markdown(['''
                ****Press the Run button if no export options show up****

                __*Export Options:*__ Select which parts of the setup to capture and export in a config file. 

                __*Export Raw Data:*__ Exports each graph outputted as raw Excel data in different sheets
                '''
                ],className='modal-text'),
            ], className='modal-content'),
            ], className='popup-container')
        ], style={"display": 'none'}, className='modal', id='export-help-container'),
        ###################################################################################################################

    ], id='mainContainer')