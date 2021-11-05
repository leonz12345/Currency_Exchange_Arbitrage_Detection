"""
Math 560
Project 3
Fall 2021

Partner 1: Leon Zhang, lz198
Partner 2: Casper Hsiao, ph139
Date: Nov 5th, 2021
"""

# Import math and p3tests.
import math
from p3tests import *

"""
detectArbitrage
"""
def detectArbitrage(adjList, adjMat, tol=1e-15):
    # adjMat[i][j] refers to the -log(rate) from currency i to currency j

    # Initialize currency exchange graph
    for currency in adjList:
        currency.prev = None
        currency.dist = float('inf')
    
    # Set the first currency in the adjList to be start
    adjList[0].dist = 0
    # Iterate |V|-1 iterations
    for _ in range(len(adjList)-1):
        # Iterate each currency
        for currency in adjList:
            # Iterate over the currecy to be exchanged
            for n in currency.neigh:
                 if n.dist > currency.dist + adjMat[currency.rank][n.rank] + tol:
                    n.dist = currency.dist + adjMat[currency.rank][n.rank]
                    n.prev = currency
    
    # Run one extra iteration to detect cycle
    foundCycle = False
    global curr
    for currency in adjList:
        # Iterate over the currecy to be exchanged
        for n in currency.neigh:
            # There is still update, meaning there is a negative cycle
            if n.dist > currency.dist + adjMat[currency.rank][n.rank] + tol:
                n.prev = currency
                foundCycle = True
                curr = n
                break
        if foundCycle:
            break

    if foundCycle:
        # Get the first vertex that has been visited twice
        visited = set()
        while curr.rank not in visited:
            visited.add(curr.rank)
            curr = curr.prev
        # This is the first vertex of the negative cycle
        firstnode = curr
        # Now start build the arbitrage
        circle = [firstnode.rank]
        curr = firstnode.prev
        # Backtrace to recover the arbitrage
        while not curr.isEqual(firstnode):
            circle.append(curr.rank)
            curr = curr.prev
        # Add the first currency in to form the cycle
        circle.append(curr.rank)
        return [i for i in reversed(circle) if i is not None]
    else:
        return []


"""
rates2mat
"""
def rates2mat(rates):
    # Convert each rate into -log(rate)
    return [[-math.log(R) for R in row] for row in rates]

"""
Main function.
"""
if __name__ == "__main__":
    testRates()
