# Functions to create visualisations of the solutions to Number Crunching

import csv
import pylab as plt

def uploadResults(fileName):

    results = []
    seqLen = []
    
    with open(fileName, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        
        for line in lines:
            if not line[0] == 'Number':
                results.append(int(line[0]))
                seqLen.append(len(line[1]))

    return results, seqLen


def plotFreqHist(fileName):
    """
    """

    results, seqLen = uploadResults(fileName)
    
    plt.hist(results, weights = seqLen, facecolor='red', bins = results[-1])
    plt.xlabel('results')
    plt.ylabel('length of sequence')
    plt.title(r'Histogram of length of sequences (DEC)')
    plt.show()
