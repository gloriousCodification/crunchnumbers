## The Artikel 42 Algorithm
## 
## Algorithm to solve Number Crunching
## april 2014

import bisect, math
from decimal import Decimal

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

def sqrt(num):
    """
    Takes the square root of a number using a ten based logarithm.
    This is usefull because python is not able to take the root of large numbers.
    """

    logNum = math.log(num, 10)

    try:
        sqrtNum = 10 ** (.5*logNum)
    except OverflowError:
        ## take the sqrt two times
        sqrtNum = 10 ** (.25*logNum)
        
    return sqrtNum

def artikel42(startNum = 4, endNum = 2):
    """
    Solves the Number Crunching problem. i.e. Gets the sequences to find all
    numbers smaller than endNum when starting at startNum
    input: startNum (int), endNum (int)
    output: Dictionary with the numbers and their sequences
    """

    curNum = startNum
    results = [curNum]
    usedFacs = [1, 2]
    seq = ""
    seqDic = {startNum: ""}
    outputDic = {startNum: ""}
    maxStreak = getS(results)

    while maxStreak < endNum:
        print curNum
        if sqrt(curNum) >= maxStreak + 1:
            curNum = sqrt(curNum)
            seq += 'w'

            if isInt(curNum):
                potentialResult = curNum
                potentialSeq = seq
            else:
                potentialResult = math.floor(curNum)
                potentialSeq = seq + 'f'

            if potentialResult not in results:
                potentialResult = int(potentialResult)
                bisect.insort(results, potentialResult)
                maxStreak = getS(results)
                seqDic[potentialResult] = potentialSeq
                if potentialResult < endNum:
                    outputDic[potentialResult] = potentialSeq
        else:
            p = getP(results, usedFacs)
            bisect.insort(usedFacs, p)
            curNum = math.factorial(p)
            bisect.insort(results, curNum)
            seq += "!"
            seqDic[p] = seq
            if p < maxStreak:
                outputDic[p] = seq

    return outputDic
