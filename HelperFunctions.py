def AwaitIntInput(rangeMin, rangeMax):
    isAwaitingCorrectFormat = True

    while (isAwaitingCorrectFormat):
        # Get raw input from user
        userSelection = input("Enter selection in range " +
                              str(rangeMin) + "-" + str(rangeMax) + ": ")
        # Validate user input
        if not userSelection.isdigit() or int(userSelection) < rangeMin or int(userSelection) > rangeMax:
            print('Incorrect input format detected, please input an integer between ' +
                  str(rangeMin) + ' and ' + str(rangeMax) + ": ")
        else:
            # If input passes validation, end loop and convert to an integer
            isAwaitingCorrectFormat = False
            selection = int(userSelection)

    return selection

def AwaitDoubleInput(rangeMin, rangeMax):
    isAwaitingCorrectFormat = True

    while (isAwaitingCorrectFormat):
        # Get raw input from user
        userSelection = input("Enter selection in range " +
                              str(rangeMin) + "-" + str(rangeMax) + ": ")

        try:
            floatInput = float(userSelection)
            if floatInput < rangeMin or floatInput > rangeMax:
                print('Incorrect input format detected, please input an integer between ' +
                    str(rangeMin) + ' and ' + str(rangeMax) + ": ")
            else:
                # If input passes validation, end loop and convert to an integer
                isAwaitingCorrectFormat = False
                selection = floatInput

        except ValueError:
            print('Incorrect input format detected, please input an integer between ' +
                  str(rangeMin) + ' and ' + str(rangeMax) + ": ")

    return selection