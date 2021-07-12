from lib import cea, nozzle, injector, plumbing
import os
import yaml
import shutil


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def main():
    print('Propulsion Design Script')
    # ask the user to enter a name for the current case
    casename = ''  # input('Case name (enter for default): ').strip()
    if casename == '':
        casename = 'default'
    # filepaths nonsense
    DATAPATH = './data'
    INFILE, OUTFILE = os.path.join(DATAPATH, 'input.yaml'), os.path.join(
        DATAPATH, f'output_{casename}.yaml')
    # load design parameters input
    print(f'Loading design parameters from {INFILE}')
    data = yaml.safe_load(open(INFILE, 'r'))

    # run CEA to get propellant combustion data
    print('Generating CEA .inp file')
    cea_inp_path = cea.create_inp_file(data)
    print('Running CEA executable')
    cea_out_path = cea.run_executable()
    print('Parsing CEA .out file')
    cea.parse_out_file(data)
    print(f'Copying CEA files to {DATAPATH}')
    shutil.copy(cea_inp_path, DATAPATH)
    shutil.copy(cea_out_path, DATAPATH)

    print('Starting calculations')

    # calculate nozzle and combustion chamber dimensions, mass flow rates, performance
    nozzle.calculate(data)
    # calculate injector dimensions
    injector.calculate(data)
    # plumbing calcs. (just pressure drop for now)
    plumbing.calculate(data)

    print('Done calculations')

    # save all design parameters (input & calculated outputs)
    print(f'Writing design parameters to {OUTFILE}')
    yaml.dump(data, open(OUTFILE, 'w'))


if __name__ == '__main__':
    main()
