#!/usr/bin/env python3

from optparse import OptionParser
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)+"\\..\\"))
from scenario.constants import ROUTEFILE_DEFAULT, END_TIME_DEFAULT

FLOW_DIRECTIONS = [
    # NW NS NE
    ("gneE2", "51812054"), ("gneE2", "-gneE4"), ("gneE2", "-51812135"),
    # EN EW ES
    ("51812135", "554747354"), ("51812135", "51812054"), ("51812135", "-gneE4"),
    # SE SN SW
    ("gneE4", "-51812135"), ("gneE4", "554747354"), ("gneE4", "51812054"),
    # WS WE WN
    ("-51812054", "-gneE4"), ("-51812054", "-51812135"), ("-51812054", "554747354")
]
FLOW_DIRECTION_STRINGS = [
    "NW", "NS", "NE", "EN", "EW", "ES", "SE", "SN", "SW", "WS", "WE", "WN"
]


def read_commandline_arguments():
    optParser = OptionParser(usage="Usage: %s [options]" % sys.argv[0])
    optParser.add_option('-f', '--flows', dest='flows', nargs=len(FLOW_DIRECTIONS),
                         help="%i vehicles per hour in NW NS NE EN EW ES SE SN SW WS WE WN order" % len(
                             FLOW_DIRECTIONS),
                         default=('200', '600', '15', '5', '5', '5', '15', '600', '200', '200', '5', '200'))
    optParser.add_option('--end_time', dest='end_time', help="end time of simulation, default: %.1f" % END_TIME_DEFAULT,
                         default=END_TIME_DEFAULT, type=float)
    optParser.add_option('--filename', dest='filename', default=ROUTEFILE_DEFAULT,
                         help="destination file name, default: '%s'" % ROUTEFILE_DEFAULT)
    options, _ = optParser.parse_args()
    flows = [float(f) for f in options.flows]
    assert (len(FLOW_DIRECTION_STRINGS) == len(FLOW_DIRECTIONS))
    for i in range(0, len(FLOW_DIRECTIONS)):
        print(FLOW_DIRECTION_STRINGS[i], ":\t", flows[i], sep="")
    if options.filename != ROUTEFILE_DEFAULT:
        print("filename:\t", options.filename, sep="")
    if options.end_time != END_TIME_DEFAULT:
        print("end_time:\t", options.end_time, sep="")
    return flows, options.end_time, options.filename


def create_route_file(flows, end_time=END_TIME_DEFAULT, filename=ROUTEFILE_DEFAULT):
    assert (len(flows) == len(FLOW_DIRECTIONS))
    with open(filename, "w") as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?>\n\n""")
        file.write(
            """<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n""")
        for i in range(0, len(flows)):
            file.write(
                """  <flow id="%s" begin="0.00" end="%f" from="%s" to="%s" probability="%f" departSpeed="max"/>\n""" %
                (FLOW_DIRECTION_STRINGS[i], end_time, FLOW_DIRECTIONS[i][0], FLOW_DIRECTIONS[i][1], flows[i] / 3600.0))
        file.write("</routes>")


if __name__ == "__main__":
    flows, end_time, filename = read_commandline_arguments()
    create_route_file(flows, end_time, filename)
