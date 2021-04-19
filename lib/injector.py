import math
import CoolProp.CoolProp as cp
from lib.nozzle import radius


def injector_area(mdot, Cd, rho, delta_P):
    '''returns total area of injector required to achieve a given mass flow rate,
    given Cd for injector, density of fuel, and pressure drop across injector.
    assumes incompressible fluid flow through a hydraulic orifice (perhaps unreasonable for our oxidiser, GOX...)'''
    return mdot / Cd / math.sqrt(2 * rho * delta_P * 1e5)


def calculate(data: dict):
    # fuel injector
    # fuel volume flow rate, used to pick a spray nozzle part
    data['injector']['fuel_volume_flow'] = data['engine']['fuel_mass_flow'] / \
        data['propellants']['fuel_density']

    # oxidiser injector
    # lookup oxidiser density at injector inlet using CoolProp
    ox_density = cp.PropsSI('D', 'T', data['propellants']['ox_initial_temp'],
                            'P', (data['engine']['chamber_pressure'] +
                                  data['injector']['ox_pressure_drop'])*1e5,
                            data['propellants']['ox_chem'])
    data['propellants']['ox_density'] = ox_density
    data['injector']['ox_volume_flow'] = data['engine']['ox_mass_flow'] / ox_density
    # injector area
    data['injector']['ox_injector_area'] = injector_area(
        data['engine']['ox_mass_flow'],
        data['injector']['ox_discharge_coeff'],
        ox_density,
        data['injector']['ox_pressure_drop'])

    # INDIVIDUAL injector hole dimensions
    data['injector']['ox_injector_radius'] = radius(
        data['injector']['ox_injector_area'] / data['injector']['num_ox_injectors'])
