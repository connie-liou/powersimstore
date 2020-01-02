import json
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import base64
import string

'''
Import and Add Wings and Add EOL Factors callback 
'''
def importingCallback(app):
    '''
    Converts json to specific return values for import callback based on which type of component it is
    '''
    def parseJSON(jsonSTR: str, clicks, sides):
        #Create dict from json
        outputDict = json.loads(jsonSTR)
        fileNameOut = outputDict['fileName'].split('.')
        #Determine which component it is loading
        if '.system' in outputDict['fileName']:
            if outputDict['isDET']:
                DETout = 'DET'
            else:
                DETout = 'PPT'
            return fileNameOut[0], outputDict['batteryName'], outputDict['loadName'], outputDict['orbitName'], outputDict['solarName'], outputDict['useConstantLoadInput'], outputDict['constantLoadVal'], outputDict['useSpinnerInput'], outputDict['rpm'], outputDict['eclipseStart'], outputDict['eclipseEnd'], outputDict['efficiencyVal'], outputDict['orbitType'], outputDict['sunAngleRows'], outputDict['sunAngleCols'], outputDict['timeSunAngleRows'], outputDict['timeSunAngleCols'], outputDict['Imax'], outputDict['Vmax'], outputDict['SOC'], outputDict['capacity'], outputDict['lineDropSA'], outputDict['lineDropLoad'], outputDict['intResistC'], outputDict['intResistDC'], outputDict['numCells'], outputDict['battChgRows'], outputDict['battDchgRows'], outputDict['startTime'], outputDict['endTime'], outputDict['timeStep'], outputDict['period'], outputDict['eclipseTime'], outputDict['loadRows'], outputDict['solarRows'], outputDict['temprows'], outputDict['EOLrows'],dash.no_update, DETout, clicks, sides, dash.no_update, {'display':'none'}, outputDict['BOLrows'], outputDict['use-EOL'], outputDict['useSimpleSolarVal'], outputDict['simpleSolarVal']
        elif '.battery' in outputDict['fileName']:
            return dash.no_update,outputDict['batteryName'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['Imax'], outputDict['Vmax'], outputDict['SOC'], outputDict['capacity'], dash.no_update, dash.no_update, outputDict['intResistC'], outputDict['intResistDC'], outputDict['numCells'], outputDict['battChgRows'], outputDict['battDchgRows'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update,dash.no_update, clicks, sides, dash.no_update, {'display':'none'}, dash.no_update, dash.no_update,dash.no_update, dash.no_update
        elif '.load' in outputDict['fileName']:
            return dash.no_update, dash.no_update, outputDict['loadName'], dash.no_update, dash.no_update, outputDict['useConstantLoadInput'], outputDict['constantLoadVal'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['lineDropLoad'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['loadRows'], dash.no_update, dash.no_update, dash.no_update,dash.no_update,dash.no_update, clicks, sides, dash.no_update, {'display':'none'}, dash.no_update, dash.no_update,dash.no_update, dash.no_update
        elif '.orbit' in outputDict['fileName']:
            return dash.no_update,dash.no_update, dash.no_update, outputDict['orbitName'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['rpm'], outputDict['eclipseStart'], outputDict['eclipseEnd'], dash.no_update, outputDict['orbitType'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['startTime'], outputDict['endTime'], outputDict['timeStep'], outputDict['period'], outputDict['eclipseTime'], dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update,dash.no_update, clicks, sides, dash.no_update, {'display':'none'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        elif '.solar' in outputDict['fileName']:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['solarName'], dash.no_update, dash.no_update, outputDict['useSpinnerInput'], outputDict['rpm'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['sunAngleRows'], outputDict['sunAngleCols'], outputDict['timeSunAngleRows'], outputDict['timeSunAngleCols'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['lineDropSA'], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, outputDict['solarRows'], outputDict['temprows'], dash.no_update,dash.no_update,dash.no_update, clicks, sides, dash.no_update, {'display':'none'}, dash.no_update, dash.no_update, outputDict['useSimpleSolarVal'], outputDict['simpleSolarVal']
    
    @app.callback([Output('system-filename', 'value'),
                    Output('battery-filename', 'value'),
                    Output('load-filename', 'value'),
                    Output('orbit-filename', 'value'),
                    Output('solar-filename', 'value'),
                    Output('use-constant-load', 'value'),
                    Output('constant-load', 'value'),
                    Output('use-spinner', 'value'),
                    Output('rpm', 'value'),
                    Output('eclipse-start', 'value'),
                    Output('eclipse-end', 'value'),
                    Output('efficiency','value'),
                    Output('orbit-type', 'value'),
                    Output('sun-angle-table', 'data'),
                    Output('sun-angle-table', 'columns'),
                    Output('time-sun-angle-table', 'data'),
                    Output('time-sun-angle-table', 'columns'),
                    Output('max-current', 'value'),
                    Output('max-voltage', 'value'),
                    Output('initial-soc', 'value'),
                    Output('capacity', 'value'),
                    Output('line-drop-SA', 'value'),
                    Output('line-drop-load', 'value'),
                    Output('int-resistance-chg', 'value'),
                    Output('int-resistance-dchg', 'value'),
                    Output('num-cells', 'value'),
                    Output('battery-charging-table', 'data'),
                    Output('battery-discharging-table', 'data'),
                    Output('start-time', 'value'),
                    Output('end-time', 'value'),
                    Output('timestep', 'value'),
                    Output('period', 'value'),
                    Output('eclipse-length', 'value'),
                    Output('load-table', 'data'),
                    Output('Solar-Table', 'data'),
                    Output('Temp-Coeff', 'data'),
                    Output('Solar-Table-EOL', 'data'),
                    Output('prev_num_EOL', 'children'),
                    Output('power-reg-type', 'value'),
                    Output('prev_clicks_import', 'children'), 
                    Output('prev_num_sides', 'children'),
                    Output('import-upload-container', 'style'), 
                    Output('import-button-container', 'style'),
                    Output('Solar-Table-BOL', 'data'),
                    Output('use-EOL', 'value'),
                    Output('use-simple-solar', 'value'),
                    Output('simple-solar-power', 'value')
                    ],
                    [Input('num-EOL', 'value'), Input('num-sides','value'), Input('import-button', 'n_clicks'), 
                     Input('input_dropdown', 'value'), Input('import-upload', 'contents')],
                    [State('prev_num_EOL', 'children'), State('prev_clicks_import', 'children'), State('prev_num_sides', 'children'),
                    State('Solar-Table', 'data'), State('Solar-Table', 'columns'), 
                    State('sun-angle-table', 'columns'), State('time-sun-angle-table', 'columns'), State('Solar-Table-EOL', 'data')])
    def input(numEOL, numSides, importClicks, inputDropdown, importUpload, prevNumEOL, prevImportClicks, prevSides, rows, columns, angleCols, timeAngleCols, EOLrows):
        
        if prevImportClicks is None:
            prevImportClicks = 0
        else:
            prevImportClicks = int(prevImportClicks)

        if prevSides is None:
            prevSides = 0
        else:
            prevSides = int(prevSides)

        if importClicks is None:
            importClicks = 0

        if prevNumEOL is None:
            prevNumEOL = 0
        else:
            prevNumEOL = int(prevNumEOL)

        # Add row of EOLfactors for EOL table. Remove if the specified number is less than the number of rows
        if (numEOL != prevNumEOL):
            if (len(EOLrows)<numEOL):
                extra = numEOL - len(EOLrows)
                for i in range(extra):
                    EOLrows.append({'EOL-factor-names': 'Name',
                                'Voc-EOL': 1,
                                'Isc-EOL': 1,
                                'Vmp-EOL': 1,
                                'Imp-EOL': 1
                                })
            elif (len(EOLrows)>numEOL):
                extra = len(EOLrows) - numEOL
                for i in range(extra):
                    EOLrows.pop()
                
            return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, angleCols, dash.no_update, timeAngleCols, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, rows, dash.no_update, EOLrows, numEOL, dash.no_update, importClicks, numSides, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update
        
        #Same add row algorithms, but for number of sides for solar panel
        elif (numSides != prevSides):
            if (len(rows)<numSides):
                extra = numSides - len(rows)
                for i in range(extra):
                    rows.append({'current-temp': 107,
                                'string-size': 20,
                                'segment-size': 68,
                                'roll': 0,
                                'pitch': 0
                                })
                    angleCols.append({
                    'id': ('sun-angles-'+str(len(angleCols))), 'name': ('Sun Angle (Wing'+str(len(angleCols))+')'),
                    'renamable': True, 'deletable': False, 'editable':True
                    })
                    timeAngleCols.append({
                    'id': ('time-sun-angles-'+str(len(angleCols))), 'name': ('Sun Angle (Wing'+str(len(angleCols))+')'),
                    'renamable': True, 'deletable': False, 'editable':True
                    })
            elif (len(rows)>numSides):
                extra = len(rows) - numSides
                for i in range(extra):
                    rows.pop()
                    angleCols.pop()
                    timeAngleCols.pop()
                
            return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, angleCols, dash.no_update, timeAngleCols, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, rows, dash.no_update, dash.no_update,dash.no_update,dash.no_update, importClicks, numSides, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        #When update button is pressed, read in value of dropdown import selection and output accordingly
        elif (importClicks != prevImportClicks):
            if inputDropdown == 'custom':
                #TODO: TypeError handling for empty upload
                content_type, content_string = importUpload.split(',')
                decoded = base64.b64decode(content_string)
                return parseJSON(decoded, importClicks, numSides)
            else: 
                return parseJSON(open(inputDropdown).read(), importClicks, numSides)
        #Shows file select if custom is chosen
        elif (importClicks == prevImportClicks) and (numSides == prevSides) and (numEOL == prevNumEOL):
            if inputDropdown == 'custom':
                return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, dash.no_update, {'display':'block'}, {'display':'block'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            else:
                return dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,dash.no_update, dash.no_update, dash.no_update, {'display':'none'}, {'display':'block'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        else:
            raise PreventUpdate



    # @app.callback([Output('import-upload-container', 'style'), Output('import-button', 'hidden')],
    #                 [Input('input_dropdown', 'value'), Input('import-upload', 'contents')])
    # def update_import_select(inputVal, contents):
        
    #     if inputVal == 'custom':
    #         return [{'display':'block'}, False]
    #     else:
    #         return [{'display':'none'}, False]

