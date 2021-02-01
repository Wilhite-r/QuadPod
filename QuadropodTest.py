from HelperFunctions import AwaitIntInput, AwaitDoubleInput
from QuadropodEngine import QuadropodEngine
from QuadropodInverseKinematics import get_angles as GetAngles
print("Setting Testbed... ")
Quadropod = QuadropodEngine()


def MoveForward():
    print("How many steps should I take? input int (1-10)")
    stepsToComplete = AwaitIntInput(1, 10)

    Quadropod.CurrentCommand = "Forward"
    for currentStep in range(0, stepsToComplete):
        Quadropod.RunSystem()


def Turn():
    print("How many steps should I take? input int (1-10)")
    stepsToComplete = AwaitIntInput(1, 10)

    Quadropod.CurrentCommand = "Turn"
    for currentStep in range(0, stepsToComplete):
        Quadropod.RunSystem()


def Jump():
    Quadropod.CurrentCommand = "Jump"

    Quadropod.RunSystem()


def CorrectAfterJump():
    Quadropod.CurrentCommand = "Correct"

    Quadropod.RunSystem()


def TestMeasurements():
    print("Input coordinates, X:")
    x = AwaitDoubleInput(-100, 100)
    print("Input coordinates, Y:")
    y = AwaitDoubleInput(-100, 100)
    print("Input coordinates, Z:")
    z = AwaitDoubleInput(-100, 100)

    angles = GetAngles([x,y,z],[x,y,z],[-x,y,z],[-x,y,z], 1.5, 2.5, 3)
    print(str(angles))
    """
    print ("RF angles: " + str(angles.RFAngles))
    print ("RH angles: " + str(angles.RHAngles))
    print ("LF angles: " + str(angles.LFAngles))
    print ("LH angles: " + str(angles.LHAngles))
    """
    #[2.6875, 1.59375, -5.0]


# main loop
print("Environment Ready.")
while True:
    print("")
    functionSwitcher = {
        1: MoveForward,
        2: Turn,
        3: Jump,
        4: CorrectAfterJump,
        5: TestMeasurements
    }

    print("Select a command (DEBUG MENU):")
    print("1 = Move Forward")
    print("2 = Turn")
    print("3 = Jump")
    print("4 = Correct After Jump")
    print("5 = Test measurements for Inverse Kinematics")

    userSelection = AwaitIntInput(1, 5)
    func = functionSwitcher.get(userSelection, lambda: "Invalid Selection")

    response = func()
