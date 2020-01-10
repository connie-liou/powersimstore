import sys
sys.path.append("/classes/")
from threading import Thread
import dash_html_components as html
from ExportRawData import generateJSON
from Graphing import *
from exceptions import *
from Importing import *
from classes.OrbitTime import *
import json
#####################################################
'''
Used in multithreading to allow functions to return values while multithreading
'''
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return
####################################################
# master callback
def masterCallback(app):
    @app.callback(
        [Output('battery_graph', 'figure'),
         Output('load_graph', 'figure'),
         Output('solar_graph', 'figure'),
         Output('system_graph', 'figure'),
         Output('solarIV_graph', 'figure'),
         Output('run_button', 'hidden'),
         Output('prev_clicks_run', 'children'),
         Output('system-export-container', 'children'),
         Output('battery-export-container', 'children'),
         Output('load-export-container', 'children'),
         Output('orbit-export-container', 'children'),
         Output('solar-export-container', 'children'),
         Output('raw_data_container', 'children'),
         Output('export-error-container', 'children'),
         Output('confirm-zerodivision-error','message'),
         Output('systemName', 'children'),
         Output('batteryName', 'children'),
         Output('loadName', 'children'),
         Output('orbitName', 'children'),
         Output('solarName', 'children')],
        [Input('run_button', 'n_clicks'),
         Input('use-constant-load', 'value'),
         Input('constant-load', 'value'),
         Input('use-spinner', 'value'),
         Input('rpm', 'value'),
         Input('num-sides', 'value'),
         Input('eclipse-start', 'value'),
         Input('eclipse-end', 'value'),
         Input('use-sunangles', 'value'),
         Input('efficiency', 'value'),
         Input('orbit-type', 'value'),
         Input('sun-angle-table', 'data'),
         Input('sun-angle-table', 'columns'),
         Input('time-sun-angle-table', 'data'),
         Input('time-sun-angle-table', 'columns'),
         Input('max-current', 'value'),
         Input('max-voltage', 'value'),
         Input('initial-soc', 'value'),
         Input('capacity', 'value'),
         Input('line-drop-SA', 'value'),
         Input('line-drop-load', 'value'),
         Input('int-resistance-chg', 'value'),
         Input('int-resistance-dchg', 'value'),
         Input('num-cells', 'value'),
         Input('battery-charging-table', 'data'),
         Input('battery-discharging-table', 'data'),
         Input('start-time', 'value'),
         Input('end-time', 'value'),
         Input('timestep', 'value'),
         Input('period', 'value'),
         Input('eclipse-length', 'value'),
         Input('load-table', 'data'),
         Input('Solar-Table', 'data'),
         Input('Temp-Coeff', 'data'),
         Input('Solar-Table-EOL', 'data'),
         Input('Solar-Table-BOL', 'data'),
         Input('num-EOL', 'disabled'),
         Input('efficiency', 'disabled'),
         Input('use-simple-solar', 'value'),
         Input('simple-solar-power', 'value'),
         Input('system-filename', 'value'),
         Input('battery-filename', 'value'),
         Input('load-filename', 'value'),
         Input('orbit-filename', 'value'),
         Input('solar-filename', 'value')], [State('prev_clicks_run', 'children')])
    def battery_output(clicks, useConstantLoadInput, constantLoadVal, useSpinnerInput, rpm,
                       numSides, eclipseStart, eclipseEnd, useSunAnglesInput, efficiencyVal, orbitType, sunAngleRows,
                       sunAngleCols, timeSunAngleRows, timeSunAngleCols, Imax, Vmax, SOC, capacity, lineDropSA,
                       lineDropLoad, intResistC, intResistDC, numCells, battChgRows, battDchgRows, startTime, endTime,
                       timeStep, period, eclipseTime, loadRows, solarRows, tempRows, EOLrows, BOLrows, notUseEOL, isDET, useSimpleSolarVal, simpleSolarVal, systemName, batteryName, loadName, orbitName, solarName, prevClicks):
        try:
            # Generate blank graphs on startup
            if clicks is None:
                clicks = 0

            # Ensure file name is valid

            if systemName == None or systemName == '':
                systemName = 'Untitled'
            else:
                try:
                    check_valid_filename(systemName)
                except ValueError:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [],[], [],[], [], [], [html.P("Invalid file name", className='error-msg')], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            #make sure name inputs are not empty
            if batteryName == None or batteryName == '':
                batteryName = 'Untitled'
            else:
                try:
                    check_valid_filename(batteryName)
                except ValueError:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [],[], [],[], [], [], [html.P("Invalid file name", className='error-msg')], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

            if loadName == None or loadName == '':
                loadName = 'Untitled'
            else:
                try:
                    check_valid_filename(loadName)
                except ValueError:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [],[], [],[], [], [], [html.P("Invalid file name", className='error-msg')], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
            if orbitName == None or orbitName == '':
                orbitName = 'Untitled'
            else:
                try:
                    check_valid_filename(orbitName)
                except ValueError:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [],[], [],[], [], [], [html.P("Invalid file name", className='error-msg')], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
            if solarName == None or solarName == '':
                solarName = 'Untitled'
            else:
                try:
                    check_valid_filename(solarName)
                except ValueError:
                    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [],[], [],[], [], [], [html.P("Invalid file name", className='error-msg')], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            # Error handling for prevClicks
            if prevClicks is None:
                prevClicks = 0
            else:
                prevClicks = int(prevClicks)
            
            

            # User changed an input so do not update output and show run button and hide export buttons

            if clicks is prevClicks:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, False, dash.no_update, [], [],[],[],[], [], [], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
            
            # Run button is pressed so update graphs and export dictionary
            elif clicks > prevClicks:
                #try:
                '''
                Step 0: Capture setup in dict
                '''
                outputDict = {}
                outputDictBattery = {}
                outputDictLoad = {}
                outputDictOrbit = {}
                outputDictSolar = {}
                
                outputDict['fileName'] = systemName + ".system"
                outputDict["useConstantLoadInput"] = useConstantLoadInput
                outputDict['constantLoadVal'] = constantLoadVal
                outputDict['useSpinnerInput'] = useSpinnerInput
                outputDict['rpm'] = rpm
                outputDict['eclipseStart'] = eclipseStart
                outputDict['eclipseEnd'] = eclipseEnd
                outputDict['useSunAnglesInput'] = useSunAnglesInput
                outputDict['efficiencyVal'] = efficiencyVal
                outputDict['orbitType'] = orbitType
                outputDict['sunAngleRows'] = sunAngleRows
                outputDict['sunAngleCols'] = sunAngleCols
                outputDict['timeSunAngleRows'] = timeSunAngleRows
                outputDict['timeSunAngleCols'] = timeSunAngleCols
                outputDict['Imax'] = Imax
                outputDict['Vmax'] = Vmax
                outputDict['SOC'] = SOC
                outputDict['capacity'] = capacity
                outputDict['lineDropSA'] = lineDropSA
                outputDict['lineDropLoad'] = lineDropLoad
                outputDict['intResistC'] = intResistC
                outputDict['intResistDC'] = intResistDC
                outputDict['numCells'] = numCells
                outputDict['battChgRows'] = battChgRows
                outputDict['battDchgRows'] = battDchgRows
                outputDict['startTime'] = startTime
                outputDict['endTime'] = endTime
                outputDict['timeStep'] = timeStep
                outputDict['period'] = period
                outputDict['eclipseTime'] = eclipseTime
                outputDict['loadRows'] = loadRows
                outputDict['solarRows'] = solarRows
                outputDict['temprows'] = tempRows
                outputDict['isDET'] = isDET
                outputDict['batteryName'] = batteryName
                outputDict['loadName'] = loadName
                outputDict['orbitName'] = orbitName
                outputDict['solarName'] = solarName
                outputDict['EOLrows'] = EOLrows
                outputDict['BOLrows'] = BOLrows
                if notUseEOL:
                    outputDict['use-EOL'] = 'No'
                else:
                    outputDict['use-EOL'] = 'Yes'
                outputDict['useSimpleSolarVal'] = useSimpleSolarVal
                outputDict['simpleSolarVal'] = simpleSolarVal

                
                outputDictBattery['fileName'] = batteryName + ".battery"
                outputDictBattery['Imax'] = Imax
                outputDictBattery['Vmax'] = Vmax
                outputDictBattery['SOC'] = SOC
                outputDictBattery['capacity'] = capacity
                outputDictBattery['intResistC'] = intResistC
                outputDictBattery['intResistDC'] = intResistDC
                outputDictBattery['numCells'] = numCells
                outputDictBattery['battChgRows'] = battChgRows
                outputDictBattery['battDchgRows'] = battDchgRows
                outputDictBattery['batteryName'] = batteryName
                
                outputDictLoad['fileName'] = loadName + ".load"
                outputDictLoad["useConstantLoadInput"] = useConstantLoadInput
                outputDictLoad['constantLoadVal'] = constantLoadVal
                outputDictLoad['lineDropLoad'] = lineDropLoad
                outputDictLoad['loadRows'] = loadRows
                outputDictLoad['loadName'] = loadName
                
                outputDictOrbit['fileName'] = orbitName + ".orbit"
                outputDictOrbit['rpm'] = rpm
                outputDictOrbit['eclipseStart'] = eclipseStart
                outputDictOrbit['eclipseEnd'] = eclipseEnd
                outputDictOrbit['useSunAnglesInput'] = useSunAnglesInput
                outputDictOrbit['orbitType'] = orbitType
                outputDictOrbit['startTime'] = startTime
                outputDictOrbit['endTime'] = endTime
                outputDictOrbit['timeStep'] = timeStep
                outputDictOrbit['period'] = period
                outputDictOrbit['eclipseTime'] = eclipseTime
                outputDictOrbit['orbitName'] = orbitName
                
                outputDictSolar['fileName'] = solarName + ".solar"
                outputDictSolar['useSpinnerInput'] = useSpinnerInput
                outputDictSolar['rpm'] = rpm
                outputDictSolar['useSunAnglesInput'] = useSunAnglesInput
                outputDictSolar['sunAngleRows'] = sunAngleRows
                outputDictSolar['sunAngleCols'] = sunAngleCols
                outputDictSolar['timeSunAngleRows'] = timeSunAngleRows
                outputDictSolar['timeSunAngleCols'] = timeSunAngleCols
                outputDictSolar['lineDropSA'] = lineDropSA
                outputDictSolar['solarRows'] = solarRows
                outputDictSolar['temprows'] = tempRows
                outputDictSolar['solarName'] = solarName
                outputDictSolar['useSimpleSolarVal'] = useSimpleSolarVal
                outputDictSolar['simpleSolarVal'] = simpleSolarVal
                '''
                Step 1: Read in data from every datatable. 
                        Find the longest list and use that as the for loop bounds. If the list is shorter than the 
                        longest list, then we will continue reading in the data and populating it into arrays. 
                        Also check if the cell is empty, if it is, then do not append it to the array. 
                '''

                listLengths = [len(battChgRows), len(battDchgRows), len(loadRows), len(tempRows), len(sunAngleRows),
                            len(timeSunAngleRows), len(EOLrows)]

                chargingSOC = []
                dischargingSOC = []
                chargingV = []
                dischargingV = []
                loadPower = []
                loadTime = []
                orbitAngleList = []
                sunAngleList = []
                timeSunAngleList = []
                timesForSunAngles = []
                orbitTimeList = []
                VocEOL= 1
                IscEOL = 1
                VmpEOL = 1
                ImpEOL = 1

                if (useSunAnglesInput == 'Yes'):
                    useSunAngles = True
                else:
                    useSunAngles = False

                if (orbitType == 'LEO'):
                    isLEO = True
                    isL1 = False
                    dFactor = 1
                elif (orbitType == 'L1'):
                    isLEO = False
                    isL1 = True
                    dFactor = (149.6 / (148.11 + 2.5)) ** 2
                else:  # L2
                    isLEO = False
                    isL1 = False
                    dFactor = (149.6 / (151.1 + 2.5)) ** 2


                if (useSpinnerInput == 'Yes'):
                    useSpinner = True
                else:
                    useSpinner = False

                if (useConstantLoadInput == "constant"):
                    useConstantLoad = True
                    useOrbitLoad = False
                elif (useConstantLoadInput == "custom-orbit"):
                    useOrbitLoad = True
                    useConstantLoad = False
                else:
                    useOrbitLoad = False
                    useConstantLoad = False

                if(useSimpleSolarVal == 'Simple'):
                    useSimpleSolar = True
                else:
                    useSimpleSolar = False

                for i in range(len(sunAngleCols)):
                    sunAngleList.append([])

                for i in range(len(timeSunAngleCols)):
                    timeSunAngleList.append([])

                for index in range(max(listLengths)):
                    if index < listLengths[0]:
                        r_battChgRows = battChgRows[index]
                        if all([cell != None for cell in r_battChgRows.values()]):
                            chargingSOC.append(float(r_battChgRows['cSOC']))
                            chargingV.append(float(r_battChgRows['cV']))

                    if index < listLengths[1]:
                        r_battDchgRows = battDchgRows[index]
                        if all([cell != None for cell in r_battDchgRows.values()]):
                            dischargingSOC.append(float(r_battDchgRows['dSOC']))
                            dischargingV.append(float(r_battDchgRows['dV']))

                    if not useConstantLoad:
                        if index < listLengths[2]:
                            r_loadRows = loadRows[index]
                            if all([cell != None for cell in r_loadRows.values()]):
                                loadPower.append(float(r_loadRows['Load']))
                                loadTime.append(float(r_loadRows['time']))

                    if index < listLengths[3]:
                        r_tempRows = tempRows[index]
                        TVoc, TIsc, TVmp, TImp = float(r_tempRows['Voc']), float(
                            r_tempRows['Isc']), float(r_tempRows['Vmp']), float(r_tempRows['Imp'])

                    if not useSpinner:
                        if useSunAngles:
                            if index < listLengths[4]:
                                r_sunAngleRows = sunAngleRows[index]
                                i = 0
                                if all([cell != None for cell in r_sunAngleRows.values()]):
                                    for c in sunAngleCols:
                                        if i == 0:
                                            if type(r_sunAngleRows[c['id']]) == float:
                                                orbitAngleList.append(float(r_sunAngleRows[c['id']]))
                                        if type(r_sunAngleRows[c['id']]) == float:
                                            sunAngleList[i - 1].append(float(r_sunAngleRows[c['id']]))
                                            i = i + 1
                            if index < listLengths[5]:
                                r_timeSunAngleRows = timeSunAngleRows[index]
                                i = 0
                                if all([cell != None for cell in r_timeSunAngleRows.values()]):
                                    for c in timeSunAngleCols:
                                        if i == 0:
                                            if type(r_timeSunAngleRows[c['id']]) == float:
                                                timesForSunAngles.append(float(r_timeSunAngleRows[c['id']]))
                                        if type(r_timeSunAngleRows[c['id']]) == float:
                                            timeSunAngleList[i - 1].append(float(r_timeSunAngleRows[c['id']]))
                                        i = i + 1
                    if not notUseEOL:
                        if index < listLengths[6]:
                            r_EOLrows = EOLrows[index]
                            VocEOL= VocEOL * float(r_EOLrows['Voc-EOL'])
                            IscEOL = IscEOL * float(r_EOLrows['Isc-EOL'])
                            VmpEOL = VmpEOL * float(r_EOLrows['Vmp-EOL'])
                            ImpEOL = ImpEOL * float(r_EOLrows['Imp-EOL'])
                
                r = BOLrows[0]
                Vocval = float(r['Voc-val'])
                Iscval = float(r['Isc-val'])
                Vmpval = float(r['Vmp-val'])
                Impval = float(r['Imp-val'])

                if useConstantLoad:
                    loadPower.append(constantLoadVal)
                    loadTime.append(1)
                '''
                Step 2: Manually handle some specific value errors
                '''
                
                if (VocEOL*IscEOL*VmpEOL*ImpEOL > 1):
                    raise ValueError('Invalid EOL Factors')
                if (startTime > endTime):
                    raise ValueError('Start Time is greater than End Time')

                if (useSpinner and useSimpleSolar):
                    raise ValueError ('Cannot use Simple Solar Model and Spinner at same time')
                # if (eclipseTime > period):
                #     raise ValueError('Eclipse Length is greater than Orbit Period')       
                '''
                Step 3: Generate constant time list based on given end time and time step.
                        Populate orbitTimeList with lists of OrbitTimePoints based on orbit type and sunangle usage.
                        Create SolarWing objects based on user input and append each wing to create SolarArray objects. 
                '''
                totalTimeList = np.arange(0, endTime, timeStep).tolist()
                solarWingList = []
                # creates solar objects based on if we are using sun angles


                if useSpinner:
                    orbitTimeList = generateTimeListfromConstant(isLEO, endTime, period, eclipseTime, eclipseStart, eclipseEnd,
                                                                timeStep)  # generates sun angles based off of time list
                    spinnerSunAngles = generateSpinnerList(rpm, numSides, timeStep, endTime)
                    i = 0
                    for r in solarRows:
                        wing = SolarWing(Vocval, Iscval, Vmpval, Impval,
                                        TVoc, TIsc, TVmp, TImp, VocEOL, IscEOL,
                                        VmpEOL, ImpEOL, float(r['string-size']), float(r['segment-size']),
                                        float(r['current-temp']), dFactor)
                        wing.sunAngles = spinnerSunAngles[i]
                        solarWingList.append(wing)
                        i = i + 1

                    array = SolarArray(solarWingList, lineDropSA, efficiencyVal)
                    useSunAngles = True

                elif useSunAngles:  # using sun angles and not a spinner

                    if isLEO:  # generates orbit time points based off of given orbit angles calculated to time
                        orbitTimeList = generateTimeListfromSunAnglesLEO(orbitAngleList, period, endTime, eclipseTime)
                    else:  # generates orbit time points based off of times vs. sun angles
                        orbitTimeList = generateTimeListfromSunAnglesL1L2(timesForSunAngles, endTime, eclipseStart, eclipseEnd,
                                                                        timeStep)

                    for r in solarRows:
                        i = 0
                        wing = SolarWing(Vocval, Iscval, Vmpval, Impval,
                                        TVoc, TIsc, TVmp, TImp, VocEOL, IscEOL,
                                        VmpEOL, ImpEOL, float(r['string-size']), float(r['segment-size']),
                                        float(r['current-temp']), dFactor)
                        wing.sunAngles = sunAngleList[i]
                        solarWingList.append(wing)
                        i = i + 1
                    array = SolarArray(solarWingList, lineDropSA, efficiencyVal)

                else:  # not using sun angles and not a spinner

                    orbitTimeList = generateTimeListfromConstant(isLEO, endTime, period, eclipseTime, eclipseStart, eclipseEnd,
                                                                timeStep)
                    for r in solarRows:
                        wing = SolarWing(Vocval, Iscval, Vmpval, Impval,
                                        TVoc, TIsc, TVmp, TImp, VocEOL, IscEOL,
                                        VmpEOL, ImpEOL, float(r['string-size']), float(r['segment-size']),
                                        float(r['current-temp']),
                                        dFactor)
                        wing.pitch = float(r['pitch'])
                        wing.roll = float(r['roll'])
                        solarWingList.append(wing)
                    array = SolarArray(solarWingList, lineDropSA, efficiencyVal)

                
                '''
                Step 4: Generate graphs simultaneously by multithreading.
                '''
                batt = Battery(chargingSOC, chargingV, dischargingSOC, dischargingV, capacity, SOC, intResistC, Vmax, Imax,
                            intResistDC, numCells, lineDropLoad, array, loadPower, loadTime, totalTimeList, startTime,
                            orbitTimeList, timeStep, useOrbitLoad, isDET, useSunAngles)
                
                batt.generateBatteryDataPoints(loadPower, loadTime, isDET, totalTimeList, startTime, orbitTimeList, timeStep, useOrbitLoad, useSunAngles, useSimpleSolar, simpleSolarVal)
                # multithreading
                t1 = ThreadWithReturnValue(target=solarOverTime, args=(batt,))
                t2 = ThreadWithReturnValue(target=systemGraph, args=(batt,))
                t3 = ThreadWithReturnValue(target=batteryGraph, args=(batt,))
                t4 = ThreadWithReturnValue(target=loadProfileGraph, args=(batt,))
                t5 = ThreadWithReturnValue(target=solarIV, args=(array, batt,))
                t1.start()
                t2.start()
                t3.start()
                t4.start()
                t5.start()

                SA_graph = t1.join()
                SYS_graph = t2.join()
                BATT_graph = t3.join()
                LOAD_graph = t4.join()
                IV_graph = t5.join()

                return BATT_graph, LOAD_graph, SA_graph, SYS_graph, IV_graph, True, clicks, [
                    html.A('Export', href='/exporttojson?value={}'.format(json.dumps(outputDict)),
                        className='button', id='exportjsonbutton', hidden=False)],[
                    html.A('Export', href='/exporttojson?value={}'.format(json.dumps(outputDictBattery)),
                        className='button', id='exportbatteryjsonbutton', hidden=False)],[
                    html.A('Export', href='/exporttojson?value={}'.format(json.dumps(outputDictLoad)),
                        className='button', id='exportloadjsonbutton', hidden=False)],[
                    html.A('Export', href='/exporttojson?value={}'.format(json.dumps(outputDictOrbit)),
                        className='button', id='exportorbitjsonbutton', hidden=False)],[
                    html.A('Export', href='/exporttojson?value={}'.format(json.dumps(outputDictSolar)),
                        className='button', id='exportsolarjsonbutton', hidden=False)], [
                        html.A('Export Graph Data to Excel', id='export-data',
                                href='/exportrawdata?value={}'.format(json.dumps(generateJSON(batt, array))),
                                className='button')], [], dash.no_update, "System: " + systemName, "Battery: " + batteryName, "Load: " + loadName, "Orbit: " + orbitName, "Solar Array: " + solarName
        except Exception as inst:
            #Captures any error and displays as a popup message by triggering another callback by updating a 'junk' component
            message = 'An error has occured :( \n Error: ' + str(type(inst)) + str(inst) 
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, clicks, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, message, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
