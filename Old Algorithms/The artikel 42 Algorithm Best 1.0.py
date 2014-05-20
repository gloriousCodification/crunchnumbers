## The Artikel 42 Algorithm
## 
## Algorithm to solve Number Crunching
## may 2014

import bisect, csv
from math import *
from decimal import *
import pylab as plt
import cProfile

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

def getSeq(result, seqDic):
    """
    Returns the sequence for the given result and sequence dictionary
    result = (int)
    seqDic = all results found with their sequence (dictionary)
    returns: length (int)
    """

    num = result
    parent = seqDic[num][0]
    seqSoFar = seqDic[num][1]

    # Go on till 4 with parent None
    while parent:
        num = parent
        parent = seqDic[num][0]
        seqSoFar = seqDic[num][1] + seqSoFar

    return seqSoFar

def getSeqLength(result, seqDic):
    """
    Returns the length of a sequence for the given result and sequence dictionary
    result = (int)
    seqDic = all results found with their sequence (dictionary)
    returns: length (int)
    """
    
    seq = getSeq(result, seqDic)
    length = len(seq)
    return length

def artikel42(endNum = 100, frac = 1):
    """
    Solves the Number Crunching problem. i.e. Gets the sequences to find all
    numbers smaller than endNum when starting at startNum
    input: startNum (int), endNum (int)
    output: Dictionary with the numbers as keys and value
            (parent, sequence from parent, total sequence length)
    """

    # Initialize variables
    startNum = 4
    curNum = Decimal(startNum)
    results = [startNum]
    usedFacs = [1, 2]
    seq = "" 
    seqDic = {startNum: (None,"",0)}
    parent = startNum
    
    # Keep track of all numbers found that are lower than endNum. 
    numFound = [startNum]

    # Go on untill the fraction of all numbers below endNum is found
    while len(numFound) < frac * endNum:
##        print curNum
        curNum = curNum.sqrt()
        seq += 'w'
        
        # Get new potential result (int function floors automatically)
        potentialResult = int(curNum)
        
        # Get sequence of potential number, add floor if needed
        if isInt(curNum):
            potentialSeq = seq
        else:
            potentialSeq = seq + 'f'
        potentialSeqLength = seqDic[parent][2] + len(potentialSeq)
                
        if potentialResult not in results:
            # Store new result
            bisect.insort(results, potentialResult)
            seqDic[potentialResult] = (parent, potentialSeq, potentialSeqLength)
            if potentialResult <= endNum:
                numFound.append(potentialResult)
                print len(numFound), potentialResult     
        else:
            # Compare new sequence to existing sequence
            existingLength = seqDic[potentialResult][2]
            if  potentialSeqLength < existingLength:
                # Replace result
                seqDic[potentialResult] = (parent, potentialSeq,
                                           potentialSeqLength)
                if potentialResult <= endNum:
                    print len(numFound), potentialResult

            # When a potential result is allready found we need to take the
            # factorial of 'p' to get new results.
            p = getP(results, usedFacs)
            bisect.insort(usedFacs, p)
            # p is the new current number. Assume that result p! is not allready
            # found so append p! to results
            curNum = factorial(p)
            bisect.insort(results, curNum)
            seqDic[int(curNum)] = (p, "!", seqDic[p][2] + 1)
            seq = ""    # new seq from p!
            if curNum <= endNum:
                numFound.append(curNum)
                print len(numFound), curNum

            parent = curNum     #curNum is the new parent
            curNum = Decimal(curNum)

    # Create output (seqDic with only results <= endNum)
    outputDic = {}
    for result in results[:endNum]:
            outputDic[result] = getSeq(result, seqDic)
            
    return outputDic, numFound

def storeResults(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outfile = open("Results/Results_" + str(endNum) + "_" + str(frac) + "_" +
                   str(startNum) + ".csv", 'w')
    writer = csv.writer(outfile, lineterminator="\n")
    writer.writerow(["Number", "Sequence"])

    outputDic, numFound = artikel42(endNum, frac)

    for num in outputDic:
        writer.writerow([num, outputDic[num]])

    outfile.close()

def plotNumSeq(endNum = 100, frac = 1, startNum = 4):
    """
    """

    outputDic, numFound = artikel42(endNum, frac)

    plt.plot(numFound, 'o')
    plt.plot(numFound)
    plt.title('Order in which the first %i results are found' %(frac*endNum))
    plt.xlabel('order')
    plt.ylabel('result')
    plt.show()

def performSeq(seq, startNum=4):
    """
    This functions preforms the given sequence (string) on the startnumber
    startNum (int) to see the result.
    """
    curNum = Decimal(startNum)
    
    for operator in seq:
        if operator == "w":
            curNum = curNum.sqrt()
        elif operator == "f":
            curNum = Decimal(int(curNum))
        else:
            curNum = Decimal(factorial(curNum))

    return curNum
