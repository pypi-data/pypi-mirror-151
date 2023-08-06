from time import time
import numpy as np, pandas as pd, PyCO2SYS as pyco2

# Switch to CO2SYS-MATLAB v3.1.1 conditions (note: not identical to v2.0.5)
pyco2.solve.get.initial_pH_guess = 8.0  # don't use the more sophisticated pH guess
pyco2.solve.get.pH_tolerance = 0.0001  # use a looser tolerance for pH solvers
pyco2.solve.get.update_all_pH = False  # True keeps updating all pH's until all solved
pyco2.solve.get.halve_big_jumps = True  # different way to prevent too-big pH jumps
pyco2.solve.get.assume_pH_total = True  # replicate pH-Total assumption bug
pyco2.solve.delta.use_approximate_slopes = True  # don't use Autograd for solver slopes

# Import input conditions: "compare_MATLABv3_1_1.csv" was generated in MATLAB
# using "compare_MATLABv3_1_1.m".
co2matlab = pd.read_csv("manuscript/results/compare_MATLABv3_1_1.csv")

# Convert constants options
co2matlab["KSO4CONSTANTS"] = pyco2.convert.options_new2old(
    co2matlab["KSO4CONSTANT"].values, co2matlab["BORON"].values
)

# Run PyCO2SYS.CO2SYS under the same conditions
co2inputs = [
    co2matlab[var].values
    for var in [
        "PAR1",
        "PAR2",
        "PAR1TYPE",
        "PAR2TYPE",
        "SAL",
        "TEMPIN",
        "TEMPOUT",
        "PRESIN",
        "PRESOUT",
        "SI",
        "PO4",
        "NH3",
        "H2S",
        "pHSCALEIN",
        "K1K2CONSTANTS",
        "KSO4CONSTANT",
        "KFCONSTANT",
        "BORON",
    ]
]
go = time()
# co2py = pyco2.CO2SYS(*co2inputs, opt_buffers_mode=1, WhichR=3)
co2py = pyco2.api.CO2SYS_MATLABv3(*co2inputs)
print("PyCO2SYS runtime = {:.6f} s".format(time() - go))
co2py = pd.DataFrame(co2py)

# Compare the results
cvars = list(co2matlab.keys())
co2py_matlab = co2py.subtract(co2matlab)  # PyCO2SYS.CO2SYS vs MATLAB

# # Having fixed the pH scale conversion in AlkParts, can now only compare where input
# # pH scale is Total (which worked correctly before) - as of v1.6.0.
# co2py_matlab = co2py_matlab[co2py["pHSCALEIN"] == 1]

# Get maximum absolute differences in each variable
mad_co2py_matlab = co2py_matlab.abs().max()

# Max. abs. diff. as a percentage
pmad_co2py_matlab = 100 * mad_co2py_matlab / co2matlab.mean()

# Grouped differences - opt_k_carbonic isn't the problem
mad__k_carbonic = co2py_matlab.abs()
mad__k_carbonic["opt_k_carbonic"] = co2py.K1K2CONSTANTS
mad__k_carbonic = mad__k_carbonic.groupby(by="opt_k_carbonic").max()

# Grouped differences - opt_k_bisulfate isn't the problem
mad__opt_k_bisulfate = co2py_matlab.abs()
mad__opt_k_bisulfate["opt_k_bisulfate"] = co2py.KSO4CONSTANT
mad__opt_k_bisulfate = mad__opt_k_bisulfate.groupby(by="opt_k_bisulfate").max()

# Grouped differences - opt_pH_scale isn't the problem
mad__opt_pH_scale = co2py_matlab.abs()
mad__opt_pH_scale["opt_pH_scale"] = co2py.pHSCALEIN
mad__opt_pH_scale = mad__opt_pH_scale.groupby(by="opt_pH_scale").max()

# Grouped differences - par1/par2 combo IS the problem: 17 and (less so) 18
mad__par1_par2 = co2py_matlab.abs()
mad__par1_par2["par1_type"] = co2py.PAR1TYPE
mad__par1_par2["par2_type"] = co2py.PAR2TYPE
mad__par1_par2 = mad__par1_par2.groupby(by=["par1_type", "par2_type"]).max()
mad__par1_par_core = mad__par1_par2[
    ["TAlk", "TCO2", "pHin", "pCO2in", "fCO2in", "CO3in", "HCO3in", "CO2in"]
]


def test_co2py_matlab():
    # Test to 1e-5 %
    checkcols = [
        col
        for col in pmad_co2py_matlab.index
        if col
        not in [
            "RFin",
            "RFout",
            "PO4",
            "SAL",
            "SI",
            "H2S",
            "NH3",
            "KSO4CONSTANTS",
            "CO2in",  # because of imprecision in different ways to calculate it
            "OHout",  # who knows?
        ]
    ]
    assert np.all(
        (pmad_co2py_matlab[checkcols] < 1e-5).values
        | np.isnan(pmad_co2py_matlab[checkcols].values)
    )
    # Test to 1e-3 %
    checkcols_1em3 = ["CO2in"]
    assert np.all(
        (pmad_co2py_matlab[checkcols_1em3] < 1e-3).values
        | np.isnan(pmad_co2py_matlab[checkcols_1em3].values)
    )
    # Test to 1e-4 %
    checkcols_1em4 = ["OHout"]
    assert np.all(
        (pmad_co2py_matlab[checkcols_1em4] < 1e-4).values
        | np.isnan(pmad_co2py_matlab[checkcols_1em4].values)
    )


# Compare new n-d approach
co2nd = pd.DataFrame(
    pyco2.sys(
        co2inputs[0],
        co2inputs[1],
        co2inputs[2],
        co2inputs[3],
        salinity=co2inputs[4],
        temperature=co2inputs[5],
        temperature_out=co2inputs[6],
        pressure=co2inputs[7],
        pressure_out=co2inputs[8],
        total_silicate=co2inputs[9],
        total_phosphate=co2inputs[10],
        total_ammonia=co2inputs[11],
        total_sulfide=co2inputs[12],
        opt_pH_scale=co2inputs[13],
        opt_k_carbonic=co2inputs[14],
        opt_k_bisulfate=co2inputs[15],
        opt_k_fluoride=co2inputs[16],
        opt_total_borate=co2inputs[17],
        opt_gas_constant=3,
    )
)


def test_nd():
    assert np.all(co2nd.isocapnic_quotient_out.values == co2py.isoQout.values)
    assert np.all(co2nd.pH_sws.values == co2py.pHinSWS.values)


# test_co2py_matlab()
# test_nd()


# Reset to PyCO2SYS conditions
pyco2.solve.get.initial_pH_guess = None
pyco2.solve.get.pH_tolerance = 1e-8
pyco2.solve.get.update_all_pH = False
pyco2.solve.get.halve_big_jumps = False
pyco2.solve.get.assume_pH_total = False
pyco2.solve.delta.use_approximate_slopes = False
