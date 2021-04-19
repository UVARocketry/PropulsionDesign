import yaml
import numpy as np
from lib import cea
import os
import pickle

data = yaml.safe_load(open('./data/design_data.yaml', 'r'))
pchams = range(15, 40, 5)
ofs = np.linspace(1.8, 2.8, num=20)
results = cea.run_propellant_study(data, pchams, ofs)
# pickle.dump(results, open('results.pickle', 'wb'))

print('Plot saved to:', cea.plot_propellant_study(results, pchams, ofs))

pcham_desired = 30
optimal_of, optimal_isp = cea.optimize_of_ratio_for_isp(
    results, pchams, ofs, pcham_desired)
print(
    f'For Pcham={pcham_desired} bar, maximum Isp of {optimal_isp:.3f} m/s occurs at O/F mass ratio {optimal_of:.3f}')
