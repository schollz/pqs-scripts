#!/usr/bin/python
__author__ = "Zack Scholl"
__license__ = "GPL"
__version__ = "1.0.3"
__maintainer__ = "Zack Scholl"
__email__ = "zns@duke.edu"
__description__ = """This script parses PQS log files and exports the dist v. energy as well as a trajectory .xzy file"""

# CHANGELOG
# 1.01 - first version
# 1.02 - formatted .xyz correctly
# 1.03 - for sig figs for energy, parsing old files too


import sys
import os
import json

try:
    logFile = sys.argv[1]
except:
    print("You must specify a log file:\n\n\tpython parseLogFile.py LOGFILE\n")
    sys.exit(-1)

print("Parsing file %s" % sys.argv[1])
g = open("trajectory.xyz","w")
f = open(logFile,"r")
inConverged = False
toggle = True
structure = ""
for line in f:
    if len(line) < 2:
        if inConverged == True:
            if toggle:
                g.write("%d\n\n" % structure.count("\n"))
                g.write(structure)
            toggle = not toggle
        structure = ""
        inConverged = False
    if "CONVERGED GEOMETRY" in line:
        inConverged = True
    if inConverged and  "." in line:
        items = line.split()
        structure += "  " + items[0] + "       " + '{0:12.6f}'.format(float(items[1])) +  '{0:12.6f}'.format(
            float(items[2])) + '{0:12.6f}'.format(float(items[3])) + "\n"

print("Wrote trajectory.xyz with the structures at each step.")


g = open("energy.dat","w")
f = open(logFile,"r")
for line in f:
    if "Current value:" in line:
        items = line.split()
        g.write("%2.5f\t%2.9f\n" % (float(items[2]), float(items[5])))

print("Wrote energy.dat with the structures at each step.")
