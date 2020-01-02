import numpy as np
import sys
sys.path.append("/classes/")
from classes.OrbitTime import OrbitTimePoint


class SolarWing:
    def __init__(self, VOC: float, ISC: float, VMP: float, IMP: float, VOC_T_COEFF: float, ISC_T_COEFF: float, VMP_T_COEFF: float, IMP_T_COEFF: float, VOC_EOL_FACTOR: float, ISC_EOL_FACTOR: float, VMP_EOL_FACTOR: float, IMP_EOL_FACTOR: float, STRING_SIZE: int, SEGMENT_SIZE: int, temperature: float, distanceFactor: float):
        
        self.sunAngles = []
        self.roll = 0
        self.pitch = 0

        self.SEGEMENT_SIZE = SEGMENT_SIZE


        #Factor in temperature coefficients
        self.VOC = (((temperature-28)*VOC_T_COEFF)+VOC)*VOC_EOL_FACTOR * STRING_SIZE
        self.ISC = (((temperature-28)*ISC_T_COEFF)+ISC)*ISC_EOL_FACTOR * distanceFactor
        self.VMP = (((temperature-28)*VMP_T_COEFF)+VMP)*VMP_EOL_FACTOR * STRING_SIZE
        self.IMP = (((temperature-28)*IMP_T_COEFF)+IMP)*IMP_EOL_FACTOR * distanceFactor

        '''
        Generates IV curve data for wing. Increments voltage by given amount and calculates power and current at each voltage point. Loop ends when current is 0 or negative. Also finds peak power for PPT. Does not include any losses for L1/2 distance or cosine angle loses
        '''

        self.voltageIVList = []
        self.currentIVList = []
        self.powerIVList = []

        voltage = 0
        while True:
            self.voltageIVList.append(voltage)
            voltage = voltage + 0.1
            current = self.calculateCurrentIVCurve(voltage)
            if current <= 0:
                self.currentIVList.append(0)
                self.powerIVList.append(0)
                break
            else:
                self.currentIVList.append(current)
                self.powerIVList.append(voltage * current)

        self.maxConstPower = max(self.powerIVList)

    '''
    Uses solar cell formula to derive current from voltage and specs on the cell's datasheet
    '''
    def calculateCurrentDETSunAngles(self, voltage: float, index:int):
        try:
            self.C2 = ((self.VMP / self.VOC) - 1) / (np.log(1-(self.IMP / self.ISC))) 
            self.C1 = (1 - (self.IMP / self.ISC)) * np.exp((-1 * self.VMP) / (self.C2 * self.VOC))
            x = self.ISC * (1 - self.C1 * (np.exp(voltage / (self.C2 * self.VOC)) - 1)) * self.SEGEMENT_SIZE * self.calculateAngleFactorSunAngles(index)
            if x < 0:
                x = 0
        except ZeroDivisionError:
            x=0 #TODO: let user know
        
        #TODO: Make these global for all wings, including other constants

        np.nan_to_num(0)
        return x

    def calculateCurrentDET(self, voltage: float):
        try:
            self.C2 = ((self.VMP / self.VOC) - 1) / (np.log(1-(self.IMP / self.ISC)))
            self.C1 = (1 - (self.IMP / self.ISC)) * np.exp((-1 * self.VMP) / (self.C2 * self.VOC))
            x = self.ISC * (1 - self.C1 * (np.exp(voltage / (self.C2 * self.VOC)) - 1)) * self.SEGEMENT_SIZE * self.calculateAngleFactorPitchRoll(self.pitch, self.roll)
            if x < 0:
                x = 0
            np.nan_to_num(0)
        except ZeroDivisionError:
            x = 0
        return x

    '''
    Calculate function for solar wing current on IV graph
    '''

    def calculateCurrentIVCurve(self, voltage: float):
        try:
            self.C2 = ((self.VMP / self.VOC) - 1) / (np.log(1-(self.IMP / self.ISC)))
            self.C1 = (1 - (self.IMP / self.ISC)) * np.exp((-1 * self.VMP) / (self.C2 * self.VOC))
            x = self.ISC * (1 - self.C1 * (np.exp(voltage / (self.C2 * self.VOC)) - 1)) * self.SEGEMENT_SIZE
            np.nan_to_num(0)
        except ZeroDivisionError:
            x = 0
        return x
    

    '''
    Calculates cosine loss based on sun angles or pitch and roll
    '''

    def calculateAngleFactorSunAngles(self, index:int):
        x = np.cos(np.deg2rad(self.sunAngles[(index % len(self.sunAngles))]))
        if x > 0:
            return x
        else:
            return 0

    def calculateAngleFactorPitchRoll(self, pitchDegrees: float, rollDegrees: float):
        x = np.cos(np.deg2rad(pitchDegrees)) * np.cos(np.deg2rad(rollDegrees))
        if x > 0:
            return x
        else:
            return 0

    '''
    Factors in cosine angle loss in PPT power calculation
    '''

    def calculateMaxPowerPPTSunAngles(self, efficiency: float, index:int):
        x = self.maxConstPower * self.calculateAngleFactorSunAngles(index) * efficiency
        if x > 0:
            return x
        else:
            return 0

    def calculateMaxPowerPPT(self, efficiency: float):
        x = self.maxConstPower * self.calculateAngleFactorPitchRoll(self.pitch, self.roll) * efficiency
        if x > 0:
            return x
        else:
            return 0



class SolarArray:

    def __init__(self, solarWingList: list, linediodedrop: float, PPTefficiency: float):
        #Init variables
        self.wingList = solarWingList
        self.LINEDIODE_DROP = linediodedrop

        try:
            self.efficiency = PPTefficiency / 100
        except:
            self.efficiency = 1

        '''
        Same as wing function but generates IV curve data for the entire solar array. Does not include any losses for L1/2 distance or cosine angle loses
        '''
        self.voltageIVList = []
        self.currentIVList = []
        self.powerIVList = []

        voltage = 0
        while True:
            voltage = voltage + 0.1
            self.voltageIVList.append(voltage)
            current = self.calculateCurrentIVCurve(voltage)
            if current <= 0:
                self.currentIVList.append(0)
                self.powerIVList.append(0)
                break
            else:
                self.currentIVList.append(current)
                self.powerIVList.append(voltage * current)

    '''
    Same function as wing but adds all wing currents together to get the total solar array current output with or without sun angles. Also returns a 1D array of current values for each individual wing at that given time
    '''
    def calculateCurrentDETSunAngles(self, voltage: float, index):
        current = 0
        wingCurrentList = []
        for wing in self.wingList:
            wingCurrent = wing.calculateCurrentDETSunAngles(voltage + self.LINEDIODE_DROP, index)
            if wingCurrent > 0:
                current = current + wingCurrent
                wingCurrentList.append(wingCurrent)
            else:
                current = current + 0
                wingCurrentList.append(0)
        return current, wingCurrentList

    def calculateCurrentDET(self, voltage:float):
        current = 0
        wingCurrentList = []
        for wing in self.wingList:
            wingCurrent = wing.calculateCurrentDET(voltage + self.LINEDIODE_DROP)
            if wingCurrent > 0:
                current = current + wingCurrent
                wingCurrentList.append(wingCurrent)
            else:
                current = current + 0
                wingCurrentList.append(0)
        return current, wingCurrentList

    '''
    Calculate function for current on IV curve
    '''
    def calculateCurrentIVCurve(self, voltage:float):
        current = 0
        for wing in self.wingList:
            wingCurrent = wing.calculateCurrentIVCurve(voltage)
            if wingCurrent > 0:
                current = current + wingCurrent
            else:
                current = current + 0
        return current

    '''
    Runs function on each wing and sums them together to get the power output of the solar array with or without sun angles
    '''

    def calculateMaxPowerPPTSunAngles(self, OrbitTime: OrbitTimePoint):
        power = 0
        wingPowerList = []
        for wing in self.wingList:
            wingPower = wing.calculateMaxPowerPPTSunAngles(self.efficiency, OrbitTime)
            power = power + wingPower
            wingPowerList.append(wingPower)
        return power, wingPowerList

    def calculateMaxPowerPPT(self):
        power = 0
        wingPowerList = []
        for wing in self.wingList:
            wingPower = wing.calculateMaxPowerPPT(self.efficiency)
            power = power + wingPower
            wingPowerList.append(wingPower)
        return power, wingPowerList







