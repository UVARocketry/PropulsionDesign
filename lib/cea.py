# cea.py
# Henry Nester
# 1 March 2021 (based on the old MATLAB program from Nov. '20)

# Program to interface with NASA's CEA (Chem. Eqbr. w/ Appns.) program
# Basically creates a .inp file to CEA's spec, then runs CEA.exe to create a .out file.
# Parses .out file to get data we want

# CEA has a bunch of other options besides what this program does
# peek the manual at http://akrmys.com/public/cea/doc/xRP-1311P2.pdf if you hate urself

import subprocess
import os
import pathlib
import numpy as np
from dataclasses import dataclass

CEA_PATH = pathlib.Path(__file__).parent / 'CEA'
CEA_EXE = CEA_PATH / 'FCEA2m.exe'
CEA_INP = CEA_PATH / 'ceadata.inp'
CEA_OUT = CEA_PATH / 'ceadata.out'


@dataclass
class CEAInputData:
    pcham = None
    pamb = None
    of = None
    fuel_chems = None
    fuel_chem_mass_percs = None
    fuel_initial_temp = None
    ox_chem = None
    ox_initial_temp = None
    equilibrium = None


def create_inp_file(inp: CEAInputData):
    '''creates a .inp file for CEA based on the design parameters in data.'''
    with open(CEA_INP, mode='w') as f:
        f.write('problem\n')
        f.write('rocket\n')

        eqbr_arg = 'equilibrium' if inp.equilibrium else 'frozen nfz=1'
        # equilibrium assumes rxns stay at equilibrium (inf. rxn rates) throughout nozzle flow
        # allowing rxns to absorb energy from flow. slightly underestimates engine performance
        # frozen nfz=1 assumes all equilbria fix at the nozzle throat. overestimates performance
        f.write(f'{eqbr_arg}\n')

        # parameters for problem
        f.write(f"p,bar={inp.pcham:.3f}\n")
        f.write(
            f"pip={inp.pcham/inp.pamb:.3f}\n")
        f.write(f"o/f={inp.of}\n")

        # specify reactants (fuel/ox)
        f.write('react\n')
        for fuel_chem, fuel_chem_mass_perc in zip(inp.fuel_chems, inp.fuel_chem_mass_percs):
            f.write(
                f"fuel={fuel_chem} wt={fuel_chem_mass_perc:.3f} t,K={inp.fuel_initial_temp:.3f}\n")
        f.write(
            f"ox={inp.ox_chem} wt 100 t,K {inp.ox_initial_temp:.3f}\n")

        f.write('end')  # last thing in the file. required!


def run_executable() -> str:
    '''runs the FCEA2m.exe executable on ceadata.inp. returns the full path to the output file'''
    # FCEA2m.exe is *special*
    # it takes no cmd line arguments, but when you run it it expects you to type something in
    # namely, the name of the input file, without the .inp ext.

    # this method will make the program crash if there are any issues running the command line
    subprocess.run([CEA_EXE], input=f'ceadata\n', cwd=CEA_PATH,
                   check=True, shell=True,  stdout=subprocess.DEVNULL,
                   encoding='ascii')


@dataclass
class CEAOutputData:
    chamber_temp: float = 0
    exhaust_gamma: float = 0
    exhaust_molar_mass: float = 0
    cstar: float = 0
    exhaust_velocity: float = 0


def parse_out_file() -> CEAOutputData:
    '''parses the ceadata.out file. returns a dictionary of design parameters that resulted from running CEA'''
    r = CEAOutputData()
    with open(CEA_OUT, 'r') as f:
        relevant_flag = False  # True when we're in the section of the outfile with numbers
        for line in f.readlines():
            if relevant_flag:
                if 'T, K' in line:
                    r.chamber_temp = float(
                        line.split()[2])  # [K]
                elif 'GAMMAs' in line:
                    r.exhaust_gamma = float(
                        line.split()[3])  # [~] #index 3: exit
                elif 'M, (1/n)' in line:
                    r.exhaust_molar_mass = float(
                        line.split()[4])  # [kg/kmol] #index 4: exit
                elif 'CSTAR, M/SEC' in line:
                    r.cstar = float(
                        line.split()[3])  # [m/s]
                elif 'Isp, M/SEC' in line:
                    r.exhaust_velocity = float(
                        line.split()[3])  # [m/s]

            if 'THEORETICAL ROCKET PERFORMANCE' in line:
                relevant_flag = True  # start of results section of .out file
            elif 'PRODUCTS WHICH WERE CONSIDERED' in line:
                relevant_flag = False  # end of results section
    return r


# def run_propellant_study(data: dict, chamber_pressures: [float], of_ratios: [float]) \
#         -> [[(float, float)]]:
#     '''runs CEA to calculate performance and chamber temperature over the supplied of_ratios and
#     chamber_presures. use_cea_isp False will calculate the ideal IsReturns a 2D array of(isp, chamber_temp) with pressures as rows and ratios as cols'''
#     data = data.copy()  # so we don't overwrite the design parameters
#     print('Starting CEA calculations')
#     table = []
#     n, N = 0, len(chamber_pressures) * len(of_ratios)  # progress bar
#     for pcham in chamber_pressures:
#         row = []
#         for of_ratio in of_ratios:
#             data['engine']['chamber_pressure'] = pcham
#             data['propellants']['of_ratio'] = of_ratio

#             create_inp_file(data)
#             run_executable()
#             parse_out_file(data)
#             # cea isp max: 2.25
#             # cea cstar max: 2.05
#             # calculated cstar max: 2.15
#             isp = data['engine']['cea_exhaust_velocity']  # nozzle.c_star(
#             # output['exhaust_gamma'], output['exhaust_molar_mass'], output['chamber_temp'])
#             chamber_temp = data['engine']['chamber_temp']

#             row.append((isp, chamber_temp))
#             n += 1
#         table.append(row)
#         print(f'{n} of {N} CEA calculations done.')
#     print('CEA calculations done')
#     return table


# def plot_propellant_study(table: [[(float, float)]], pchams, ofs, show=False) -> str:
#     '''takes a 2D array of(isp, chamber_temp) with pressures as rows and ratios as cols and plots series across of ratios for each chamber pressure
#     returns full path to plot files'''
#     print('Plotting data')
#     import matplotlib.pyplot as plt
#     fig = plt.figure(1, figsize=(12, 5))
#     axL = fig.add_subplot(1, 2, 1)
#     axR = fig.add_subplot(1, 2, 2)
#     axL.set_xlabel('O/F ratio (kg/kg)')
#     axL.set_ylabel('Isp (m/s)')
#     axR.set_xlabel('O/F ratio (kg/kg)')
#     axR.set_ylabel('Tcham (K)')
#     for i in range(len(pchams)):
#         row = table[i]
#         c_stars, temps = zip(*row)
#         a = i/len(table)
#         linecolor = (a, 1 - a, 0)
#         axL.plot(ofs, c_stars, color=linecolor)
#         axR.plot(ofs, temps, color=linecolor, label=f'{pchams[i]:.1f}')
#     axR.legend(title='Pcham (bar)')
#     fig.tight_layout()  # stops margin overlap
#     filename = 'propellant_study_plot'
#     plt.savefig(fname=filename, bbox_inches='tight')
#     if show:
#         plt.show()
#     return os.path.join(PATH, filename+'.png')


# def optimize_of_ratio_for_isp(table: [[(float, float)]], pchams: [float], ofs: [float], pcham: float) -> (float, float):
#     '''given a table from a propellant study, returns the optimal o/f ratio and the isp it gives'''
#     import scipy.interpolate
#     import scipy.optimize
#     print('Started optimizing')
#     isp_table = [[isp for isp, tcham in row] for row in table]
#     of_table, pcham_table = np.meshgrid(ofs, pchams)
#     interpolate_isp = scipy.interpolate.interp2d(
#         of_table, pcham_table, isp_table, bounds_error=True)
#     optimal_of = scipy.optimize.fmin(lambda of: -interpolate_isp(of,
#                                                                  pcham), (min(ofs) + max(ofs)) / 2)
#     print('Done optimizing')
#     return optimal_of[0], (interpolate_isp(optimal_of, pcham))[0]
