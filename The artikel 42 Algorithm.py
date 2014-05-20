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
    Returns p for listst r and f; p is the largest element in r that is not an
    element of f.
    r = sorted list
    f = sorted list
    returns: element p
    """
    for elem in r:
        if elem not in f:
            return elem

def isInt(num):
    """
    Checks if num is possibly an int
    num = number to check (Decimal)
    returns: True if num is an int and False if not

    This part is only important for low numbers. For high numbers it is not so
    easy to determine wheter a Decimal object is a real number or not. So we
    assume that for high numbers it holds that they are not integer. This is
    reasonable because for high numbers it is very rare that a square root
    returns in an integer.
    """

    # Check only for number lower than a billion
    # Otherwise this checking method is not accurate
    if num < 10 ** 9:
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
    result = result for which we want to get the sequence (int)
    seqDic = all results found with their sequence (dictionary)
    returns: sequence (string)
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
    result = result for which we want to get the length of the sequence(int)
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
    endNum = highest number of the output (int)
    frac = fraction of all numbers below endNum we want to find (float 0-1)
    output: - Dictionary with the numbers as keys and value
              (parent, sequence from parent, total sequence length)
            - numFound (list) with the order in which the results are found
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
    percentages = []
    
    # Go on untill the fraction of all numbers below endNum is found
    while len(numFound) < frac * endNum:

        # Print progress
        fracFound = float(len(numFound)) / (frac * endNum)
        perFound = int(fracFound * 100)
        if perFound % 10 == 0 and perFound not in percentages:
            percentages.append(perFound)
            print str(perFound) + "% found"

        # Change current number by taking square root
        curNum = curNum.sqrt()
        seq += 'w'

        # Continue if curNum is greater than 1 million because these results are
        # not really useful and it saves a lot of memory
        if curNum > 10 ** 6:
            continue 
        
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
        else:
            # Compare new sequence to existing sequence
            existingLength = seqDic[potentialResult][2]
            if  potentialSeqLength < existingLength:
                # When new seq is shorter, adjust result and go on with another
                # square root.
                seqDic[potentialResult] = (parent, potentialSeq,
                                           potentialSeqLength)
                
            else:
                # When a potential result is allready found with a shorter sequence
                # we need to take the factorial of 'p' to get new results.
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

                parent = curNum     #curNum is the new parent
                curNum = Decimal(curNum)

    # Create output (seqDic with only results <= endNum)
    outputDic = {}
    for result in results[:int(frac*endNum)]:
            outputDic[result] = getSeq(result, seqDic)
    
    return outputDic, numFound

""" -------------------- Code for Storing Results -------------------- """

def storeResults(endNum = 100, frac = 1):
    """
    Stores the results of the artikel42 algorithm.
    endNum = highest number of the output (int)
    frac = fraction of all numbers below endNum we want to find (float 0-1)
    output: csv file with the results and their sequences
    """

    outfile = open("Results/Results_bla_" + str(endNum) + "_" + str(frac) + ".csv",
                   'w')
    writer = csv.writer(outfile, lineterminator="\n")
    writer.writerow(["Number", "Sequence"])

    outputDic, numFound = artikel42(endNum, frac)

    # first order results
    orderedResults = []
    for num in outputDic:
        bisect.insort(orderedResults, num)

    for num in orderedResults:
        writer.writerow([num, outputDic[num]])

    outfile.close()


""" -------------------- Code for Visualizations -------------------- """

def uploadResults(fileName):
    """
    Uploads results from a csv file.
    fileName = name of the file to upload (string)
    output: results (list), all results in the csv file
            seqLen (list), sequence length of the results
    """
    results = []
    seqLen = []
    
    with open(fileName, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        
        for line in lines:
            if not line[0] == 'Number':
                results.append(int(line[0]))
                seqLen.append(len(line[1]))

    return results, seqLen

def plotSeqLenHist(fileName):
    """
    Plots a histogram of the length of the sequences for the results stored in
    the given file.
    fileName = name of the file with the results (string)
    output: Histogram of sequence lengths
    """

    results, seqLen = uploadResults("Results/" + fileName)
    
    plt.hist(results, weights = seqLen, facecolor='red', bins = results[-1])
    plt.xlabel('results')
    plt.ylabel('length of sequence')
    plt.title(r'Histogram of length of sequences')
    plt.show()


def plotResultOrder(endNum = 100, frac = 1):
    """
    Plots the order in which the results are found.
    endNum = highest number of the output (int)
    frac = fraction of all numbers below endNum we want to find (float 0-1)
    output: graph of the order of results
    """

    outputDic, numFound = artikel42(endNum, frac)

    plt.plot(numFound, 'o')
    plt.plot(numFound)
    plt.title('Order in which the first %i results below %i are found' %(frac*endNum, endNum))
    plt.xlabel('order')
    plt.ylabel('result')
    plt.show()


""" -------------------- Code for Checking Sequences -------------------- """

def performSeq(seq, startNum=4):
    """
    This functions preforms the given sequence (string) on the startnumber
    startNum (int) to check the result.
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
