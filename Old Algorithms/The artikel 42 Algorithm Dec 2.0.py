## The Artikel 42 Algorithm 2.0
## 
## Algorithm to solve Number Crunching
## may 2014
##
## Dec 2.0 uses Decimal objects and check whether a new result has a shorter
## sequence than the previous found.

import bisect, csv
from math import *
from decimal import *
import pylab as plt

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

def isInt(num):
    """
    Checks if num is possibly an int
    num = number to check (Decimal)
    output: True if num is an int and False if not

    This part is only important for low numbers. For high numbers it is not so
    easy to determine wheter a Decimal object is a real number or not. So we
    assume that for high numbers it holds that they are not integer. This is
    reasonable because for high numbers it is very rare that a square root
    returns in an integer.

    """

    # Check only for number lower than a trillion
    # Otherwise this checking method is not accurate
    if num < 10 ** 12:
        i = int(num)
        f = float(num)

        # If there is no difference between the integere (rounded) and the
        # float, the number is an integer.
        if i - f == 0:
            return True
        else:
            return False
    else:
        False


def artikel42(endNum = 100, frac = 1, startNum = 4):
    """
    Solves the Number Crunching problem. i.e. Gets the sequences to find all
    numbers smaller than endNum when starting at startNum
    input: startNum (int), endNum (int)
    output: Dictionary with the numbers and their sequences
    """

    # Initialize variables
    curNum = Decimal(startNum)
    results = [startNum]
    usedFacs = [1, 2]
    seq = ""
    seqDic = {startNum: ""}
    outputDic = {startNum: ""}
    maxStreak = getS(results)

    # For visualization
    numFound = [startNum]

    # Go on untill the fraction of all numbers below endNum is found
    while len(outputDic) < frac * endNum:

        # If the square root of the current number is higher than the highest
        # number of the streak from 1, it is usefull to explore this result.
        if curNum.sqrt() >= maxStreak + 1:
            curNum = curNum.sqrt()
            seq += 'w'

            # Convert Decimal into int (floors automatically)
            potentialResult = int(curNum)

            # Get sequence of potential number, add floor if needed
            if isInt(curNum):
                potentialSeq = seq
            else:
                potentialSeq = seq + 'f'

            # Add potential result to results if it doesn't allready exist
            if potentialResult not in results:
                
                # Adjust variables
                bisect.insort(results, potentialResult)
                maxStreak = getS(results)
                seqDic[potentialResult] = potentialSeq
                if potentialResult <= endNum:
                    outputDic[potentialResult] = potentialSeq
                    numFound.append(potentialResult)
                    print len(outputDic), potentialResult
            else:
                if len(seqDic[potentialResult]) > len(potentialSeq):

                    # Adjust variables
                    bisect.insort(results, potentialResult)
                    maxStreak = getS(results)
                    seqDic[potentialResult] = potentialSeq
                    if potentialResult <= endNum:
                        outputDic[potentialResult] = potentialSeq
                        numFound.append(potentialResult)
                        print len(outputDic), potentialResult
                    
        # If the square root of the current number is lower than the highest
        # number of the streak from 1 we allready found, we have to take
        # the factorial of the number.
        else:
            p = getP(results, usedFacs)
            bisect.insort(usedFacs, p)
            curNum = factorial(p)
            bisect.insort(results, curNum)
            seq = seqDic[p] + "!"
            seqDic[int(curNum)] = seq

            if curNum <= endNum:
                outputDic[curNum] = seq
                numFound.append(curNum)
                print len(outputDic), curNum
                
            curNum = Decimal(curNum)

    return outputDic, numFound

def storeResults(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outfile = open("Results/Rusults_Dec_2.0_" + str(endNum) + "_" + str(frac) + "_" +
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

    for num in outputDic:
        numbers.append(num)
        try:
            seqLen.append(len(outputDic[num]))
        except KeyError:
            seqLen.append(0)
    
    plt.hist(numbers, weights = seqLen, facecolor='red', bins = endNum)
    plt.xlabel('numbers')
    plt.ylabel('length of sequence')
    plt.title(r'Histogram of length of sequences (DEC)')
    plt.show()

def plotNumSeq(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outputDic, numFound = artikel42(endNum, frac, startNum)

    plt.plot(numFound, 'o')
    plt.plot(numFound)
    plt.title('Order in which the first %i numbers are found (DEC)' %(frac*endNum))
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
            
