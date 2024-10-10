#!/usr/bin/env python

import os
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
ROUTEFILE_DEFAULT = os.path.join(THIS_DIR, "network/demand.rou.xml")
TRIPINFOS_DEFAULT = os.path.join(THIS_DIR, "output/tripinfos.xml")

END_TIME_DEFAULT=36000.0
STEPLENGTH_DEFAULT=1.0