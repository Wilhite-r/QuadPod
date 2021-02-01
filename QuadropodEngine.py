from time import time, sleep
from QuadropodServos import QuadropodServos
from QuadropodServos import ServoInstructions
from QuadropodGait import DiscreteRippleGait
import QuadropodSmoothingProcessor as SmoothingProcessor
from ConvertCommands import ConvertCommands
from QuadropodInverseKinematics import get_angles as GetAngles

print("Engineering Engine... ")
# global constants
READTIMEINTERVAL = 0.5  # Interval between sensor readings
INSTRUCTTIMEINTERVAL = 0.01  # Default Interval between servo updates
SMOOTHINGSCALE = 100 # Default scale for smoothing


StrideTime = 1 #How many seconds one stride takes


# MAIN PROCESSING FUNCTIONS:
class QuadropodEngine:
    def __init__(self):
        # set pwm pulse width range for each channel
        print("Igniting Engine...")
        self.CurrentCommand = None
        self.lastReadTime = None
        self.lastInstructTime = None

        restPosition = GetAngles([2.6875, 1.59375, -5.0],[2.6875, 1.59375, -5.0],
                                 [-2.6875, 1.59375, -5.0], [-2.6875, 1.59375, -5.0],
                                 1.5, 2.5, 3)
        self.Servos = QuadropodServos(restPosition)
        self.QuadropodGaitComputer = DiscreteRippleGait(1.0, [2.5,1.5,-5.0])
        print("Going To Rest Position... ")
        self.Servos.GoToStancePosition()

    # Right now this just does one full command, but in the future
    # we can make it take
    def RunSystem(self):
        #thisTime = time()
        #readTimeDifference = thisTime - self.lastReadTime \
        #    if self.lastReadTime is not None else READTIMEINTERVAL
        currCommand = self.CurrentCommand

        #In here we get the data to make a new command
        #if (readTimeDifference >= READTIMEINTERVAL):
            # Here we get data drom the sensors
            #SensorData = QuadropodSensors.GetSensorUpdate()
            # Here We process the sensor data
            #currCommand = QuadropodAnalyzer.RunSensorAnalysis
            #self.lastReadTime = time()

        gaitCommand = ConvertCommands(currCommand)
        print("New gait instructions: " + str(currCommand))
        if currCommand == "Jump":
            self.ProcessJump()
        else:
            gaitInstructions = \
                self.QuadropodGaitComputer.oneCycle(gaitCommand[0], gaitCommand[1], gaitCommand[2])
            self.ProcessWalk(gaitInstructions)
        
        self.SmoothlyGoToPosition(self.Servos.StancePosition, 2)
        return

    def ProcessWalk(self, gaitInstructions):
        #if (instructTimeDifference >= INSTRUCTTIMEINTERVAL):
        for newPositionInstructions in gaitInstructions:
            #thisTime = time()
            #instructTimeDifference = thisTime - self.lastInstructTime\
            #    if self.lastInstructTime is not None else INSTRUCTTIMEINTERVAL

            #self.lastInstructTime = time()
            newServoInstructions = GetAngles(
                newPositionInstructions[0], newPositionInstructions[1],
                newPositionInstructions[2], newPositionInstructions[3],
                1.5, 2.5, 3)
            self.SmoothlyGoToPosition(newServoInstructions, StrideTime/12)

        return

    def ProcessJump(self):
        self.SmoothlyGoToPosition(self.Servos.CrouchPosition, 5)

        print("Ready in jump position. Jumping in 10 seconds")
        sleep(5)
        print("5")
        sleep(1)
        print("4")
        sleep(1)
        print("3")
        sleep(1)
        print("2")
        sleep(1)
        print("1")
        sleep(1)
        print("We have ignition!")
        self.Servos.ActivateSpring()
        sleep(3)
        print("Settling...")
        sleep(4)
        print("Done!")

        return

    def SmoothlyGoToPosition(self, newServoInstructions, speed = None):
        #Set the interval so that the whole function takes $speed seconds to finish
        interval = INSTRUCTTIMEINTERVAL
        if (speed is not None):
            interval = speed / SMOOTHINGSCALE

        oldServoInstructions = self.Servos.CurrentInstructions
        smoothedServoInstructions = SmoothingProcessor.LinearSmoothing(oldServoInstructions, newServoInstructions, SMOOTHINGSCALE)

        for eachServoInstruction in smoothedServoInstructions:
            sleep(interval)
            self.Servos.SetNextInstructions(eachServoInstruction.RFAngles,
                                            eachServoInstruction.RHAngles,
                                            eachServoInstruction.LFAngles,
                                            eachServoInstruction.LHAngles)
            self.Servos.ApplyAngles()