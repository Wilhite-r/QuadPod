
from math import pi
print("Commanding Command Converter... ")

def ConvertCommands(command):
    if (command == "Forward"):
        return (0.0,1.0,0.0)

    if (command == "Turn"):
        return (0.0,0.0,pi/2)

    if (command == "Jump"):
        return (0.0,0.0,0.0)

    return None