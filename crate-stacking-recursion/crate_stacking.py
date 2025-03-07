import sys

def moveCrates(n, A, B, C, output):
    if n ==1:
        line = f"Move crate 1 from rack {A} to rack {C}"
        output.write(line + "\n")
    else:
        moveCrates(n - 1, A, C, B, output)
        line = f"Move crate {n} from rack {A} to rack {C}."
        output.write(line + "\n")
        moveCrates(n - 1, B, A, C, output)

def main():
    n = None
    for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                val = int(line)
                if 1 <= val <= 20:
                    n = val
                    break
            except ValueError:
                pass
    if n is None:
        return

    with open("output.txt", "w") as output:
        moveCrates(n, 'A', 'B', 'C', output)

if __name__ == "__main__":
    main()
