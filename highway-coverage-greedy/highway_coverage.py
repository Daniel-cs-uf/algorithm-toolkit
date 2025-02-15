import sys

def timHortons(K, L, H):
    #following my psudocode pretty much exactly
    S = []
    covered = 0
    i = 0
    n = len(H)

    while covered < (K - L):
        max = 0

        while i < n and H[i] <= covered + L:
            if H[i] > covered:
                max = H[i]
            i += 1

        S.append(max)
        covered = max

    # include furthest off ramp location
    endCheck = len(S)
    if S[endCheck - 1] != H[n - 1]:
        S.append(H[n -1])
    return S

def main():
    # source I used to do this https://www.w3schools.com/python/python_file_open.asp
    reading = open('input.txt', 'r')
    line = reading.readline().strip()
    K, L = map( int, line.split())
    nAsString = reading.readline().strip()

    # n doesn't really need to be used in my implementation as in python 
    # you can just create H by populating the list as it's read, though
    # I still need to read it to access H
    n = int(nAsString)
    HAsString = reading.readline().strip()
    H = list(map(int, HAsString.split()))

    solution = timHortons(K, L, H)

    # source I used to do this https://www.geeksforgeeks.org/writing-to-file-in-python/
    writing = open('output.txt', 'w')
    writing.write(' '.join(map(str, solution)))

if __name__ == "__main__":
    main()