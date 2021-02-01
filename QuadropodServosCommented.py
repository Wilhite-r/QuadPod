"""
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from board import SCL, SDA
"""

print("Setting Servo Constants...")
RFLegLimitsMin = [0, 0, 0]
RFLegLimitsMax = [180, 180, 180]
RHLegLimitsMin = [0, 0, 0]
RHLegLimitsMax = [180, 180, 180]
LFLegLimitsMin = [0, 0, 0]
LFLegLimitsMax = [180, 180, 180]
LHLegLimitsMin = [0, 0, 0]
LHLegLimitsMax = [180, 180, 180]

SpringServoMin = 90
SpringServoMax = 180

ScannerBoundMin = 0
ScannerBoundMax = 180

LegServoSpeeds = 3
ScannerServoSpeed = 1

# global variables (This is bad coding practice!)
# 0 means we are scanning towards 0, 1 means we are scanning towards 180
ScannerServoDirection = 0

# Bias to Correct, hopefully we can keep this around 0
RHBias = [0, 0, 0]
RFBias = [0, 0, 0]
LHBias = [0, 0, 0]
LFBias = [0, 0, 0]

print("Initializing i2c...")
"""
i2c = busio.I2C(SCL, SDA)

# create pwm object with 50hz frequency
pca = PCA9685(i2c)
pca.frequency = 50

RHHip = servo.Servo(pca.channels[6], min_pulse = 500, max_pulse = 2500)
RHKnee = servo.Servo(pca.channels[7], min_pulse = 500, max_pulse = 2500)
RHAnkle = servo.Servo(pca.channels[8], min_pulse = 500, max_pulse = 2500)
RFHip = servo.Servo(pca.channels[9], min_pulse = 500, max_pulse = 2500)
RFKnee = servo.Servo(pca.channels[10], min_pulse = 500, max_pulse = 2500)
RFAnkle = servo.Servo(pca.channels[11], min_pulse = 500, max_pulse = 2500)
LHHip = servo.Servo(pca.channels[0], min_pulse = 500, max_pulse = 2500)
LHKnee = servo.Servo(pca.channels[1], min_pulse = 500, max_pulse = 2500)
LHAnkle = servo.Servo(pca.channels[2], min_pulse = 500, max_pulse = 2500)
LFHip = servo.Servo(pca.channels[3], min_pulse = 500, max_pulse = 2500)
LFKnee = servo.Servo(pca.channels[4], min_pulse = 500, max_pulse = 2500)
LFAnkle = servo.Servo(pca.channels[5], min_pulse = 500, max_pulse = 2500)
Spring = servo.Servo(pca.channels[13], min_pulse = 500, max_pulse = 2500)
"""

class ServoInstructions:
    def __init__(self, RFAngles, RHAngles, LFAngles, LHAngles):
        self.RFAngles = RFAngles
        self.RHAngles = RHAngles
        self.LFAngles = LFAngles
        self.LHAngles = LHAngles


class QuadropodServos:
    """
    QuadropodServos holds the current parameters of the servo
    From here we can access the servo angles and update them
    """
    StancePosition = ServoInstructions([125, 150, 121], [55, 30, 39],
                                   [55, 30, 59], [125, 150, 141])
    CrouchPosition = ServoInstructions([180, 70, 0], [10, 160, 180],
                                    [0, 110, 180], [170, 20, 0])    

    def __init__(self):
        print("Winding Servos...")
        self.NextInstructions = ServoInstructions(None, None, None, None)
        self.CurrentInstructions = ServoInstructions(None, None, None, None)

    def GoToStancePosition(self):
        self.ApplyAngles(ServoInstructions(
            QuadropodServos.StancePosition.RFAngles, QuadropodServos.StancePosition.RHAngles,
            QuadropodServos.StancePosition.LFAngles, QuadropodServos.StancePosition.LHAngles))
        self.DeactivateSpring()

    def DeactivateSpring(self):
        return
        #Spring.angle = SpringServoMax

    def ActivateSpring(self):
        return
        #Spring.angle = SpringServoMin

    def ApplyAngles(self, newServoInstructions = None):
        if (newServoInstructions is None):
            newServoInstructions = self.NextInstructions
        if (newServoInstructions is None):
            return

        limitedServoInstructions = self.ApplyServoLimits(newServoInstructions)
        if (limitedServoInstructions.RFAngles is not None):
            newRFAngles = limitedServoInstructions.RFAngles
            self.CurrentInstructions.RFAngles = newRFAngles
            #(RFHip.angle, RFKnee.angle, RFAnkle) = newRFAngles
        if (limitedServoInstructions.RHAngles is not None):
            newRHAngles = limitedServoInstructions.RHAngles
            self.CurrentInstructions.RHAngles = newRHAngles
            #(RHHip.angle, RHKnee.angle, RHAnkle.angle) = newRHAngles
        if (limitedServoInstructions.LFAngles is not None):
            newLFAngles = limitedServoInstructions.LFAngles
            self.CurrentInstructions.LFAngles = newLFAngles
            #(LFHip.angle, LFKnee.angle, LFAnkle.angle) = newLFAngles
        if (limitedServoInstructions.LHAngles is not None):
            newLHAngles = limitedServoInstructions.LHAngles
            self.CurrentInstructions.LHAngles = newLHAngles
            #(LHHip.angle, LHKnee.angle, LHAnkle.angle) = newLHAngles

        self.NextInstructions = None

        # DEBUG TODO:
        print("RH servo Angles = " + str(self.CurrentInstructions.RHAngles))
        print("RF servo Angles = " + str(self.CurrentInstructions.RFAngles))
        print("LH servo Angles = " + str(self.CurrentInstructions.LHAngles))
        print("LF servo Angles = " + str(self.CurrentInstructions.LFAngles))

    def ApplyServoLimits(self, ServoInstructionsToLimit):
        if (ServoInstructionsToLimit is None):
            return None

        limitedServoInstructions = ServoInstructions(None, None, None, None)
        if (ServoInstructionsToLimit.RFAngles is not None):
            limitedServoInstructions.RFAngles = [0, 0, 0]
            RFAngles = ServoInstructionsToLimit.RFAngles

            for x in range(0, 3):
                if (RFAngles[x] < RFLegLimitsMin[x]):
                    limitedServoInstructions.RFAngles[x] = RFLegLimitsMin[x]
                elif (RFAngles[x] > RFLegLimitsMax[x]):
                    limitedServoInstructions.RFAngles[x] = RFLegLimitsMax[x]
                else:
                    limitedServoInstructions.RFAngles[x] = RFAngles[x]

        if (ServoInstructionsToLimit.RHAngles is not None):
            limitedServoInstructions.RHAngles = [0, 0, 0]
            RHAngles = ServoInstructionsToLimit.RHAngles

            for x in range(0, 3):
                if (RHAngles[x] < RHLegLimitsMin[x]):
                    limitedServoInstructions.RHAngles[x] = RHLegLimitsMin[x]
                elif (RHAngles[x] > RHLegLimitsMax[x]):
                    limitedServoInstructions.RHAngles[x] = RHLegLimitsMax[x]
                else:
                    limitedServoInstructions.RHAngles[x] = RHAngles[x]

        if (ServoInstructionsToLimit.LFAngles is not None):
            limitedServoInstructions.LFAngles = [0, 0, 0]
            LFAngles = ServoInstructionsToLimit.LFAngles

            for x in range(0, 3):
                if (LFAngles[x] < LFLegLimitsMin[x]):
                    limitedServoInstructions.LFAngles[x] = LFLegLimitsMin[x]
                elif (LFAngles[x] > LFLegLimitsMax[x]):
                    limitedServoInstructions.LFAngles[x] = LFLegLimitsMax[x]
                else:
                    limitedServoInstructions.LFAngles[x] = LFAngles[x]

        if (ServoInstructionsToLimit.LHAngles is not None):
            limitedServoInstructions.LHAngles = [0, 0, 0]
            LHAngles = ServoInstructionsToLimit.LHAngles

            for x in range(0, 3):
                if (LHAngles[x] < LHLegLimitsMin[x]):
                    limitedServoInstructions.LHAngles[x] = LHLegLimitsMin[x]
                elif (LHAngles[x] > LHLegLimitsMax[x]):
                    limitedServoInstructions.LHAngles[x] = LHLegLimitsMax[x]
                else:
                    limitedServoInstructions.LHAngles[x] = LHAngles[x]

        return limitedServoInstructions

    # EXTERNAL FUNCTION
    def SetNextInstructions(
            self,
            RFAngles = None,
            RHAngles = None,
            LFAngles = None,
            LHAngles = None):
        if (self.NextInstructions is None):
            self.NextInstructions = ServoInstructions(None, None, None, None)

        limitedServoInstructions = \
            self.ApplyServoLimits(ServoInstructions(
                RFAngles, RHAngles, LFAngles, LHAngles))
        if (limitedServoInstructions.RFAngles is not None):
            self.NextInstructions.RFAngles = limitedServoInstructions.RFAngles

        if (limitedServoInstructions.RHAngles is not None):
            self.NextInstructions.RHAngles = limitedServoInstructions.RHAngles

        if (limitedServoInstructions.LFAngles is not None):
            self.NextInstructions.LFAngles = limitedServoInstructions.LFAngles

        if (limitedServoInstructions.LHAngles is not None):
            self.NextInstructions.LHAngles = limitedServoInstructions.LHAngles
