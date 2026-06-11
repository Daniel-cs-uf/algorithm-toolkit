from parse import parse


def parseFile(filename):
    #parsing input file based on allowability of the module as discussed in the discussion post

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # First line: "n = X"
    res = parse("n = {:d}", lines[0])
    n = res[0]

    # Identify where applicant prefs begin and company prefs begin
    appStart = None
    compStart = None
    for i, line in enumerate(lines):
        if "Applicants' Preferences:" in line:
            appStart = i + 1
        if "Companies' Preferences:" in line:
            compStart = i + 1

    applicantLines = lines[appStart : compStart - 1]
    companyLines   = lines[compStart :]

    applicantPrefs = [[] for _ in range(n)]
    companyPrefs   = [[] for _ in range(n)]

    #applicant preferences
    for line in applicantLines:
        result = parse("{idx:d}: [{prefs}]", line)
        idx = result["idx"] - 1
        prefsStr = result["prefs"]
        prefs = [int(x.strip()) - 1 for x in prefsStr.split(",")]
        applicantPrefs[idx] = prefs

    #company preferences
    for line in companyLines:
        result = parse("{idx:d}: [{prefs}]", line)
        idx = result["idx"] - 1
        prefsStr = result["prefs"]
        prefs = [int(x.strip()) - 1 for x in prefsStr.split(",")]
        companyPrefs[idx] = prefs

    return n, applicantPrefs, companyPrefs


def stableMatching(n, applicantPrefs, companyPrefs):
    #built based off psudocode given in slides using list of lists for preferences and a 2D list for ranking

    # ranking[company][applicant] = rank of applicant for company
    # Lower rank value -> higher preference
    ranking = [[0]*n for _ in range(n)]
    for company in range(n):
        for rank, applicant in enumerate(companyPrefs[company]):
            ranking[company][applicant] = rank

    applicantMatch = [-1] * n
    companyMatch   = [-1] * n

    nextProposalIndex = [0] * n

    freeApplicants = n

    while freeApplicants > 0:
        applicant = None
        for i in range(n):
            if applicantMatch[i] == -1 and nextProposalIndex[i] < n:
                applicant = i
                break

        company = applicantPrefs[applicant][ nextProposalIndex[applicant] ]
        nextProposalIndex[applicant] += 1  # Applicant won't propose to c again

        # If company c is free, match a and c
        if companyMatch[company] == -1:
            companyMatch[company] = applicant
            applicantMatch[applicant] = company
            freeApplicants -= 1
        else:
            previousApplicant = companyMatch[company]
            # If c prefers a over its current match, swap
            if ranking[company][applicant] < ranking[company][previousApplicant]:
                companyMatch[company] = applicant
                applicantMatch[applicant] = company
                applicantMatch[previousApplicant] = -1
            else:
                pass

    return [(applicant, applicantMatch[applicant]) for applicant in range(n)]


def outputFile(filename, solution):
    with open(filename, 'w') as f:
        f.write("Stable Matching:\n")
        solution = sorted(solution, key=lambda x: x[0])
        for (a, c) in solution:
            f.write(f"Applicant {a+1} -> Company {c+1}\n")


def main():
    #input and output files
    inputFileName = "test.txt"
    outputFileName = "output.txt"

    # Parse input
    n, applicantPrefs, companyPrefs = parseFile(inputFileName)
    # Run Gale-Shapley
    solution = stableMatching(n, applicantPrefs, companyPrefs)

    # creates/writes output file
    outputFile(outputFileName, solution)
    print(f"Done. Stable matching written to {outputFileName}.")


if __name__ == "__main__":
    main()
