#!/usr/bin/python
__author__ = "Zack Scholl"
__license__ = "GPL"
__version__ = "1.0.2"
__maintainer__ = "Zack Scholl"
__email__ = "zns@duke.edu"
__description__ = """This script parses PQS log files and exports the dist v. energy as well as a trajectory .xzy file"""

# CHANGELOG
# 1.01 - first version
# 1.02 - formatted .xyz correctly



import sys
import os
import json

try:
    logFile = sys.argv[1]
except:
    print("You must specify a log file:\n\n\tpython parseLogFile.py LOGFILE\n")
    sys.exit(-1)

print("Parsing file %s", sys.argv[1])
steps = []
with open(logFile, "r") as f:
    inScan = False
    readingCoordinates = False
    step = {}
    step["coords"] = ""
    for line in f:
        if "------------------------------------------" in line:
            inScan = False
            readingCoordinates = False
            if len(step["coords"]) > 0:
                steps.append(step)
            step = {}
            step["coords"] = ""
        if "ATOM" in line and inScan:
            readingCoordinates = True
        if "POTENTIAL SCAN" in line:
            scanNum = int(line.split()[-1])
            print("Working on step %d" % scanNum)
            step["scanNum"] = scanNum
            inScan = True
        if inScan and "Current value:" in line:
            step['distance'] = float(line.split()[2])
            step['energy'] = float(line.split()[5])
        if inScan and readingCoordinates and "." in line:
            items = line.split()
            step["coords"] += "  " + items[1] + "       " + '{0:12.6f}'.format(float(items[2])) +  '{0:12.6f}'.format(
                float(items[3])) + '{0:12.6f}'.format(float(items[4])) + "\n"


with open("energy.dat", "w") as f:
    with open("trajectory.xyz", "w") as g:
        for step in steps:
            f.write("%2.5f\t%2.5f\n" % (step["distance"], step["energy"]))
            g.write("%d\n\n" % steps[0]["coords"].count("\n"))
            g.write(step["coords"])


print("Wrote energy.dat with distance and energies.")
print("Wrote trajectory.xyz with the structures at each step.")
