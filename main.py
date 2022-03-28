#!/usr/bin/python
# coding = utf-8
import os
import sys

import pandas as pd

from RiskQuantLib.Module import *
from downloadData import downloadData
path = sys.path[0]
downloadData()
print("GV_Spread Finish")