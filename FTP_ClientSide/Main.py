import sys

from src.CommandLineInterface import CmdLineProgram


if __name__ == '__main__':
    ADDR = sys.argv[1:3]
    if len(ADDR) == 1:
        ADDR.append(21)
    else:
        ADDR[1] = int(ADDR[1])
    ADDR = ('localhost', 9999)

    Program = CmdLineProgram(tuple(ADDR))
    Program.run()
