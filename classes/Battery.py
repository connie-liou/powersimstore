from classes.Solar import SolarArray
from classes.binarysearch import *
import numpy as np


class Battery:
    def __init__(self, charging_SOC, charging_V, discharging_SOC, discharging_V, capacity, initialSOC, internalresistancecharging, maxvoltage, maxcurrent, internalresistancedischarging, numberofcells, linedrop, solarArray:SolarArray, loadPowerList: list, loadTimeList: list, timeList: list, initTime: float, orbitTimeList: list, timeStep: float, useOrbitLoad, isDET: bool, useSunAngles:bool):

        #User Input Constants
        self.CAPACITY = capacity
        self.INITIAL_SOC = initialSOC
        self.INTERNAL_RESISTANCE_CHARGING = internalresistancecharging
        self.INTERNAL_RESISTANCE_DISCHARGING = internalresistancedischarging
        self.MAX_VOLTAGE = maxvoltage
        self.MAX_CURRENT = maxcurrent
        self.CELLS = numberofcells
        self.LINE_DROP = linedrop

        #User Input Lists
        self.chargingV = charging_V
        self.chargingSOC = charging_SOC
        self.dischargingSOC = discharging_SOC
        self.dischargingV = discharging_V

        #Solar Array Init
        self.solarArray = solarArray
        self.wingListI = [[] for _ in range(len(self.solarArray.wingList))] #2d array of currents for each wing

        self.batteryVoltageList = []
        self.stateOfCharge =[]
        self.timeList=[]
        self.currentList=[]

        self.loadVList=[]
        self.loadCurrentList=[]

        self.solarI=[]
        self.solarP=[]
        self.solarV=[]
        self.MAX_VOLTAGE_REACHED = 0
        
    '''
    Main loop for calculating values for graphs
    '''

    def generateBatteryDataPoints(self, loadPowerList: list, loadTimeList: list, isDET: bool, timeList: list, initTime: float, orbitTimeList: list, timeStep: float, useOrbitLoad:bool, useSunAngles:bool, useSimpleSolar:bool, simpleSolarValue:float):
        #Initialize variables for calculations and lists for graph data
        prevAhrChange = 0
        self.loadPowerList = []
        self.loadTimeList = loadTimeList
        self.ahrchangeList = []
        SOC = self.INITIAL_SOC

        # Determine the initial battery Ahr
        Ahr = self.CAPACITY * (SOC / 100)

        #Determine initial battery voltage by mapping the SOC to voltage from charging curve data
        index = binarySearch(self.chargingSOC, SOC)
        batteryVoltage = self.chargingV[index]

        #Set the start time when the calculations will start. This is the offset
        index = binarySearch(timeList, initTime)

        #Main loop for battery calculations
        for i in range (index, len(timeList)):
            #Determine time index in loop
            j = binarySearchPointList(orbitTimeList, timeList[i])

            #set current time to the specified OrbitTimePoint
            point = orbitTimeList[j]
            #determines solar model
            if useSimpleSolar:
                if point.inSunlight:
                    SA_I = simpleSolarValue / batteryVoltage
                    wingCurrents = [0] * len(self.solarArray.wingList)
                else:
                    SA_I = 0
                    wingCurrents = [0] * len(self.solarArray.wingList)
            else:
                 #Calculations for solar array current. Checks to see if the system is PPT or DET then based on the eclipse data from OrbitTimePoint it will determine which calculation to use for determining solar array current
                if isDET: #DET case
                    if point.inSunlight:
                        if(useSunAngles):
                            #if using sun angles calculate the solar array current and individual wing current using the provided sun angle
                            SA_I, wingCurrents = self.solarArray.calculateCurrentDETSunAngles(batteryVoltage, j)
                        else:
                            #if not using sun angles just calculate the current based off of the battery voltage for the solar array and individual wing currents
                            SA_I, wingCurrents = self.solarArray.calculateCurrentDET(batteryVoltage)
                    else:
                        #if in eclipse ignore calculations from the solar class and just set all solar currents to 0
                        SA_I = 0
                        wingCurrents = [0] * len(self.solarArray.wingList)
                else: #PPT case
                    if point.inSunlight:
                        wingCurrents = []
                        if useSunAngles:
                            #Determine max power based on IV curve and calculate SA current with sunangles. Return the solar array power and a list of solar wing powers at the given point in time
                            power, powerList = self.solarArray.calculateMaxPowerPPTSunAngles(j)
                            #Calculate solar array current by using SA power and battery voltage and line diode drop
                            SA_I = power / (batteryVoltage + self.solarArray.LINEDIODE_DROP)
                            #Wing voltage is set equal to the battery voltage plus the line diode drop
                            wingV = [batteryVoltage + self.solarArray.LINEDIODE_DROP] * len(self.solarArray.wingList)
                            #Calculates the wing currents by dividing the wing power by the wing voltage
                            wingCurrents = np.divide(powerList, wingV).tolist()
                        else:
                            #Determine max power based on IV curve and calculate SA current without sunangles
                            power, powerList = self.solarArray.calculateMaxPowerPPT()
                            #Calculate solar array current by using SA power and battery voltage and line diode drop
                            SA_I = power / (batteryVoltage + self.solarArray.LINEDIODE_DROP)
                            #Wing voltage is set equal to the battery voltage plus the line diode drop
                            wingV = [batteryVoltage + self.solarArray.LINEDIODE_DROP] * len(self.solarArray.wingList)
                            #Calculates the wing currents by dividing the wing power by the wing voltage
                            wingCurrents = np.divide(powerList,wingV).tolist()
                    else:
                        #if in eclipse ignore calculations from the solar class and just set all solar currents to 0
                        SA_I = 0
                        wingCurrents = [0] * len(self.solarArray.wingList)

            #Append wing currents to 2D array that contains every wing current at every instance in time
            for k in range(len(wingCurrents)):
                self.wingListI[k].append(wingCurrents[k])

            #Determine Load Current
            if useOrbitLoad:
                loadIndex = binarySearch(self.loadTimeList, timeList[i]%len(self.loadTimeList))
                load_I = loadPowerList[loadIndex] / (batteryVoltage - self.LINE_DROP)
            else:
                loadIndex = binarySearch(self.loadTimeList, timeList[i])
                load_I = loadPowerList[loadIndex] / (batteryVoltage - self.LINE_DROP)

            #Append load calculations to list for graphing functions
            self.loadVList.append(batteryVoltage - self.LINE_DROP)
            self.loadCurrentList.append(load_I)
            self.loadPowerList.append(loadPowerList[loadIndex])

            #Determine Battery Current
            battery_I = SA_I - load_I

            #Determine if the battery is charging or discharging

            #Charging Case
            timeStep = timeStep
            if SA_I > load_I:
                #Update battery EMF
                index = binarySearch(self.chargingSOC, SOC)
                Vchrg = float(self.chargingV[index]) * (self.CELLS / 8)

                #Limit Check for current
                if battery_I > self.MAX_CURRENT:
                    battery_I = self.MAX_CURRENT

                #Voltage calculation based off EMF and current
                batteryVoltage = Vchrg + (self.INTERNAL_RESISTANCE_CHARGING * battery_I)

                #Limit Check for voltage
                if batteryVoltage > self.MAX_VOLTAGE:
                    batteryVoltage = self.MAX_VOLTAGE
                    battery_I = (batteryVoltage - Vchrg) / self.INTERNAL_RESISTANCE_CHARGING

                #Add charge to battery
                deltaAhrs = battery_I * (timeStep / 60)
                ahrchange = (prevAhrChange + (battery_I * (timeStep / 60)))
                prevAhrChange = ahrchange
                self.ahrchangeList.append(ahrchange)
                Ahr = Ahr + deltaAhrs

            #Discharging Case
            else:
                # Update battery EMF
                index = binarySearch(self.dischargingSOC, SOC)
                Vdischrg = float(self.dischargingV[index])*(self.CELLS / 8)
                batteryVoltage = Vdischrg + (self.INTERNAL_RESISTANCE_DISCHARGING * battery_I)

                #Remove charge from the battery
                deltaAhrs = battery_I * (timeStep / 60)
                ahrchange = (prevAhrChange + (battery_I * (timeStep / 60)))
                prevAhrChange = ahrchange

                #Append ahrchange to the list for graphing function
                self.ahrchangeList.append(ahrchange)
                Ahr = Ahr + deltaAhrs

                #Limit check on battery Ahrs
                if Ahr < 0:
                    Ahr = 0

            #SOC Calculation
            SOC = (Ahr / self.CAPACITY) * 100

            #SOC Limit Check
            if SOC >= 100:
                SOC = 100

            #Append battery calculation values for graphing functions
            self.batteryVoltageList.append(batteryVoltage)
            self.stateOfCharge.append(SOC)
            self.timeList.append(timeList[i])
            self.currentList.append(battery_I)

            # Append solar array calculations to lists for graphing functions
            self.solarI.append(SA_I)
            self.solarP.append(SA_I * (batteryVoltage + self.solarArray.LINEDIODE_DROP))
            self.solarV.append(batteryVoltage + self.solarArray.LINEDIODE_DROP)

        #Set max solar array voltage in constants class
        self.MAX_VOLTAGE_REACHED = max(self.solarV)







