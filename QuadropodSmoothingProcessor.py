from numpy import linspace
from QuadropodServos import ServoInstructions
print("Mounting smoother... ")

def LinearSmoothing(OldPosition, NewPosition, StepCount):
    (oldRF, oldRH, oldLF, oldLH) = (OldPosition.RFAngles, OldPosition.RHAngles,
                                    OldPosition.LFAngles, OldPosition.LHAngles)
    (newRF, newRH, newLF, newLH) = (NewPosition.RFAngles, NewPosition.RHAngles,
                                    NewPosition.LFAngles, NewPosition.LHAngles)

    #RF
    angleRF = [linspace(oldRF[0], newRF[0], StepCount),
               linspace(oldRF[1], newRF[1], StepCount),
               linspace(oldRF[2], newRF[2], StepCount)]
    #RH
    angleRH = [linspace(oldRH[0], newRH[0], StepCount),
               linspace(oldRH[1], newRH[1], StepCount),
               linspace(oldRH[2], newRH[2], StepCount)]
    #LF
    angleLF = [linspace(oldLF[0],newLF[0], StepCount),
               linspace(oldLF[1], newLF[1], StepCount),
               linspace(oldLF[2], newLF[2], StepCount)]
    #LH
    angleLH = [linspace(oldLH[0], newLH[0], StepCount),
               linspace(oldLH[1], newLH[1], StepCount),
               linspace(oldLH[2], newLH[2], StepCount)]

    return [ServoInstructions([angleRF[0][i], angleRF[1][i], angleRF[2][i]], 
            [angleRH[0][i], angleRH[1][i], angleRH[2][i]],
            [angleLF[0][i], angleLF[1][i], angleLF[2][i]],
            [angleLH[0][i], angleLH[1][i], angleLH[2][i]]) for i in range(StepCount)]
    