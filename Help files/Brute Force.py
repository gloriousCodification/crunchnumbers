## Brute Force Number Crunching

import math

def getS(i):
    """
    Function returns the state space as a list after maximal i opreations
    """

    if i == 0:
        s = []
        return s

    elif i == 1:
        # Define states after one operation. Floor not included because
        # this operation doesn't make sense. 
        s = [("w", 4**.5), ("!", math.factorial(4))]
        return s

    else:
        prevS = getS(i-1)
        s = prevS[:]    # copy previous state space

        for state in prevS:
            sequence = state[0]
            value = state[1]
            
            # Create new states and append to state space
            newState1 = (sequence + "w", value**.5)

            newState2 = (sequence + "f", math.floor(value))
            
            s.append(newState1)
            s.append(newState2)

            # Factorial of a not integer doesn't exist
            try:
                newState3 = (sequence + "!", math.factorial(value))
            except  ValueError:
                continue
            except OverflowError:
                continue

            s.append(newState3)
            
        return s
