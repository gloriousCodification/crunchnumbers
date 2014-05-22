## The Artikel 42 Algorithm
## 
## Algorithm to solve Number Crunching
## april 2014

import csv
import bisect, math
import pylab as plt
from decimal import Decimal
import cProfile

def getS(r):
    """
    Get the highest number of a streak from 1
    r = list of results
    output: s (int)
    """

    s = 0

    for i, elem in enumerate(r):
        if i + 1 != elem:
            s = i
            return s

    s = r[-1]
    return s

def getP(r, f):
    """
    Returns p for listst r and f. P is the largest element in p that is not an
    element in f.
    r = sorted list
    f = sorted list
    output: element p
    """
    for elem in r:
        if elem not in f:
            return elem

def isInt(num, e = 10**-15):
    """
    Checks if num is possibly an int
    num = number to check (float or int)
    e = very small number
    output: True if num is an int and False if not
    """

    numRound = round(num)

    if abs(numRound - num) < e:
        return True
    else:
        return False

def sqrt(num, seq=""):
    """
    Takes the square root of a number using a ten based logarithm.
    This is usefull because python is not able to take the root of large numbers.
    """
    # Try the build in sqrt function which is more precise. If an overflow error
    # occurs, use the logarithm to calculate the square root. 
    try:
        seq += "w"
        sqrtNum = math.sqrt(num)
    except OverflowError:
        sqrtNum, seq = logSqrt(num, seq)
        
    return sqrtNum, seq

def logSqrt(num, seq="", level=1):
    """
    Takes the square root of a number using a ten based logarithm.
    This is usefull because python is not able to take the root of large numbers.
    """
        
    logNum = math.log(num, 10)
    try:
        seq += "w"
        fraction = 1 / 2.0 ** level
        sqrtNum = 10 ** (fraction*logNum)
    except OverflowError:
        # When another overflow error occurs, take the square root another time
        level += 1
        sqrtNum, seq = logSqrt(num, seq, level)

    return sqrtNum, seq

def artikel42(endNum = 100, frac = 1, startNum = 4):
    """
    Solves the Number Crunching problem. i.e. Gets the sequences to find all
    numbers smaller than endNum when starting at startNum
    input: startNum (int), endNum (int)
    output: Dictionary with the numbers and their sequences
    """
    
    # Initialize variables
    curNum = startNum
    results = [startNum]
    usedFacs = [1, 2]
    seq = ""
    seqDic = {startNum: ""}
    outputDic = {startNum: ""}
    maxStreak = getS(results)

    # Keep track of the order of numbers that are found
    numFound = [startNum]

    # Go on untill the fraction of all numbers below endNum is found
    while len(outputDic) < frac * endNum:

        # If the square root of the current number is higher than the highest
        # number of the streak from 1, it is usefull to explore this result.
        if sqrt(curNum)[0] >= maxStreak + 1:
            curNum, seq = sqrt(curNum, seq)

            # Define potential result (use floor if needed)
            if isInt(curNum):
                potentialResult = round(curNum)
                potentialSeq = seq
            else:
                potentialResult = math.floor(curNum)
                potentialSeq = seq + 'f'

            # Add potential result to results if it doesn't allready exist
            if potentialResult not in results and potentialResult < 10 ** 6:
                potentialResult = int(potentialResult) # Only store ints

                # Adjust variables
                bisect.insort(results, potentialResult)
                maxStreak = getS(results)
                seqDic[potentialResult] = potentialSeq
                if potentialResult <= endNum:
                    outputDic[potentialResult] = potentialSeq
                    numFound.append(potentialResult)
##                    print len(outputDic), potentialResult

        # If the square root of the current number is lower than the highest
        # number of the streak from 1 we allready have found, we have to take
        # the factorial of the number.
        else:
            p = getP(results, usedFacs)
            bisect.insort(usedFacs, p)
            curNum = math.factorial(p)
            bisect.insort(results, curNum)
            seq = seqDic[p] + "!"
            seqDic[curNum] = seq

            if curNum <= endNum:
                outputDic[curNum] = seq
                numFound.append(curNum)
##                print len(outputDic), curNum

    return outputDic, numFound

def storeResults(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outfile = open("Results/Rusults_" + str(endNum) + "_" + str(frac) + "_" +
                   str(startNum) + ".csv", 'w')
    writer = csv.writer(outfile, lineterminator="\n")
    writer.writerow(["Number", "Sequence"])

    outputDic, numFound = artikel42(endNum, frac, startNum)

    for num in outputDic:
        writer.writerow([num, outputDic[num]])

    outfile.close()
    

""" Visualization """

def plotFreqHist(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outputDic, numFound = artikel42(endNum, frac, startNum)

    numbers = []
    seqLen = []

    for i in outputDic:
        numbers.append(i)
        try:
            seqLen.append(len(outputDic[i]))
        except KeyError:
            seqLen.append(0)
    
    plt.hist(numbers, weights = seqLen, facecolor='red', bins = endNum)
    plt.xlabel('numbers')
    plt.ylabel('length of sequence')
    plt.title(r'Histogram of length of sequences')
    plt.show()

def plotNumSeq(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outputDic, numFound = artikel42(endNum, frac, startNum)

    plt.plot(numFound, 'o')
    plt.plot(numFound)
    plt.title('Order in which the first %i numbers are found' %(frac*endNum))
    plt.xlabel('order')
    plt.ylabel('number')
    plt.show()
    
        
"""Functions to check the results"""

def performSeq(seq, startNum=4):
    """
    This functions preforms the given sequence (list) on the startnumber
    startNum (int) to see the result.
    """
    curNum = startNum
    
    for operator in seq:
##        print "Operator:", operator, "  curNum:", curNum
        if operator == "w":
            curNum = sqrt(curNum)[0]
        elif operator == "f":
            curNum = math.floor(curNum)
        else:
            curNum = math.factorial(curNum)

    return curNum
            
