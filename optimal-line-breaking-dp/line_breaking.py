# i have these as globals so I can keep opt(i) as just having they i similarly to the lectures
n = 0.0
wordLengths = []
b = 0.0
L = 0.0
vlv = []
bestJs = []

#helper function to help with the width calc
def computeWidth(i, j):
    totalLen = 0.0
    for k in range(i, j+1):
        totalLen += wordLengths[k-1] 

    spaces = (j - i)
    return totalLen + spaces * b
def opt(i):
    if i > n:
        return 0.0

    # memoization check
    if vlv[i] is not None:
        return vlv[i]

    smallestSlack = 9999999 #don't think i'd run into anything bigger than this

    for j in range(i, n+1):
        lineWidth = computeWidth(i, j)
        if lineWidth > L:
            break
        if j == n:
            slackSquared = 0.0
        else:
            diff = L - lineWidth
            slackSquared = diff * diff
        #reccursive case 
        attempt = slackSquared + opt(j+1)
        if attempt < smallestSlack:
            smallestSlack = attempt
            bestJs[i] = j

    vlv[i] = smallestSlack
    return smallestSlack
def solve(filename="input.txt"):

    global n, wordLengths, b, L, vlv, bestJs

    with open(filename, "r") as input:
        wordLengths = list(map(float, input.readline().split()))
        b = float(input.readline().strip()) #should have said that it was looking for floats in the directions saw this last min in discussion
        L = float(input.readline().strip())

    n = len(wordLengths)

    #intitializes arrays use for memoization
    vlv = [None] * (n+2)
    bestJs = [-1] * (n+2)

    minimalCost = opt(1)

    lineBreaks = []
    i = 1
    while i <= n and bestJs[i] != -1:
        j = bestJs[i]
        lineBreaks.append(j)
        i = j + 1

    return minimalCost, lineBreaks


if __name__ == "__main__":
    cost, breaks = solve("input.txt")
    print(cost)
    print(breaks)