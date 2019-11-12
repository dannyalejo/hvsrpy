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

"""This file contains an integration test for hvsrpy."""

import numpy as np
import hvsrpy as hv
import pandas as pd
import matplotlib.pyplot as plt

timerecords = [
    "test/data/a2/UT.STN11.A2_C50.miniseed",
    "test/data/a2/UT.STN11.A2_C150.miniseed",
    "test/data/a2/UT.STN12.A2_C50.miniseed",
    "test/data/a2/UT.STN12.A2_C150.miniseed",
]

known_solutions = [
    "test/data/integration/UT_STN11_c050.hv",
    "test/data/integration/UT_STN11_c150.hv",
    "test/data/integration/UT_STN12_c050.hv",
    "test/data/integration/UT_STN12_c150.hv",
]

settings = {"length": 60,
            "width": 0.1,
            "b": 40,
            "resampling": {"minf": 0.3,
                           "maxf": 40,
                           "nf": 2048, "res_type": "log"}
            }
bp_filter = {"flag": False, "flow": 0.001, "fhigh": 49.9, "order": 5}
ratio_type = 'squared-average'
distribution_type = 'log-normal'

for fname, fname_geopsy in zip(timerecords, known_solutions):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(3, 2))

    sensor = hv.Sensor3c.from_mseed(fname)
    my_hv = sensor.hv(settings["length"], bp_filter, settings["width"],
                      settings["b"], settings["resampling"], ratio_type)    
    for amp in my_hv.amp:
        plt.plot(my_hv.frq, amp, color='#aaaaaa')
    ax.plot(my_hv.frq, my_hv.mean_curve(), color='k', label="hvsrpy")
    if distribution_type == "log-normal":
        ax.plot(my_hv.frq, np.exp(np.log(my_hv.mean_curve()) +
                                  my_hv.std_curve()), color='k', linestyle='--')
        ax.plot(my_hv.frq, np.exp(np.log(my_hv.mean_curve()) -
                                  my_hv.std_curve()), color='k', linestyle='--')
    elif distribution_type == "normal":
        ax.plot(my_hv.frq, my_hv.mean_curve(distribution_type) +
                my_hv.std_curve(distribution_type), color='k', linestyle='--')
        ax.plot(my_hv.frq, my_hv.mean_curve(distribution_type) -
                my_hv.std_curve(distribution_type), color='k', linestyle='--')
    else:
        raise ValueError

    geopsy_hv = pd.read_csv(fname_geopsy, delimiter="\t", comment="#", names=[
                            "frq", "avg", "min", "max"])
    ax.plot(geopsy_hv.frq, geopsy_hv["avg"], color='r', linestyle="--", label="Geopsy")
    ax.plot(geopsy_hv.frq, geopsy_hv["min"], color='r', linestyle=':', label='')
    ax.plot(geopsy_hv.frq, geopsy_hv["max"], color='r', linestyle=':', label='')
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("H/V Ampltidue (#)")
    ax.set_xscale('log')
    ax.legend()
    plt.savefig(f"../figs/multiwindow_{fname_geopsy[-13:-3]}.png", dpi=200, bbox_inches='tight')