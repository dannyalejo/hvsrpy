# This file is part of hvsrpy a Python module for horizontal-to-vertical 
# spectral ratio processing.
# Copyright (C) 2019 Joseph P. Vantassel (jvantassel@utexas.edu)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https: //www.gnu.org/licenses/>.

"""This file contains a performance test for hvsr calculation."""

import hvsrpy
import cProfile
import pstats

def main():
    windowlength = 60
    bp_filter = {"flag": True, "flow": 0.1, "fhigh": 45, "order": 5}    
    width = 0.1
    bandwidth = 40
    resampling = {"minf": 0.1, "maxf": 50, "nf": 256, "res_type": "log"}
    method = 'geometric-mean'
    n = 2
    max_iter = 10

    sensor = hvsrpy.Sensor3c.from_mseed("test/data/a2/UT.STN11.A2_C50.miniseed")
    hv = sensor.hv(windowlength, bp_filter, width, bandwidth, resampling, method)
    hv.reject_windows(n, max_iter)
    
fname = "test/.tmp_profiler_run"
data = cProfile.run('main()', filename=fname)
stat = pstats.Stats(fname)
stat.sort_stats('tottime')
stat.print_stats(0.01)

# YEAR - MO - DY : TIME UNIT
# -------------------------
# 2019 - 11 - 12 : 1.242 s