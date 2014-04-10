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
##            print "Now looking at state", state
            seq = state[0]
            val = state[1]

            # Only get new states if the state was created in the previous
            # state space
            if len(seq) == i-1:
                
                # Create new state after a square root.
                # If i>3, results 1 and 2 are found. So then taking the square 
                # root is useless if prev result < 9
                if i > 3:
                    if not val < 9:
##                        print "    square root"
                        newState = (seq + "w", val**.5)
                        s.append(newState)
                else:
##                    print "    sqauare root"
                    newState = (seq + "w", val**.5)
                    s.append(newState)

                # Create new state after a floor

                valf = math.floor(val)

                # Do not floor the number if we assume that it is an int.
                if not val - valf < 10**-42:
##                    print "    floor"
                    newState = (seq + "f", valf)
                    s.append(newState)

                # Create new state after a factorial
                # Only if prev value > 2. Because 1! = 1 and 2! = 2. 
                if (val > 2 and val < 200):
                    try:
                        newState = (seq + "!", math.factorial(val))
                        s.append(newState)
##                        print "    factorial"
                    except ValueError:
                        continue
                    except OverflowError:
                        continue

        return s
