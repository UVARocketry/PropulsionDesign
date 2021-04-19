import math
import CoolProp.CoolProp as cp


def reynolds_number(mdot, diameter, viscosity):
    '''returns Reynolds number [~] for fluid flowing in circular pipe given:
    mdot [kg/s], diameter [m], viscosity (dynamic) [kg/m/s]'''
    area = math.pi * diameter**2 / 4
    return mdot * diameter / viscosity / area


def darcy_friction_factor(mdot, roughness, diameter, reynolds):
    '''returns Darcy friction factor [~] for fluid flowing in circular pipe given:
    mdot [kg/s], diameter [m], roughness [m], Reynolds number [~]
    uses Haaland approx. of Colebrook eqn. https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae'''
    f = 1 / (-1.8*math.log10((roughness/diameter/3.7)**1.11 + 6.9/reynolds))**2
    return f


def pressure_drop(length, mdot, diameter, roughness, rho, viscosity):
    '''returns pressure drop [bar] as fluid flows through circular tubing, given:
    length [m] of tubing
    mdot [kg/s]
    diameter [m]
    roughness [m]
    rho [kg/m3]
    viscosity [Pa-s]
    uses Darcy equation to figure pressure drop per unit length.
    https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation'''
    reynolds = reynolds_number(mdot, diameter, viscosity)
    friction = darcy_friction_factor(mdot, roughness, diameter, reynolds)
    dP = length * friction * 8 / (math.pi ** 2) * \
        (mdot ** 2) / rho / (diameter ** 5)
    return dP / 1e5  # to bar


def velocity(mdot, diameter, rho):
    '''returns velocity of flow in circular pipe [m/s] given:
    mdot [kg/s]
    diameter [m]
    rho [kg/m3]'''
    Vdot = mdot / rho
    area = math.pi * diameter ** 2 / 4
    vel = Vdot / area
    return vel


def calculate(data: dict):
    fuel_rho = data['propellants']['fuel_density']
    fuel_visc = data['propellants']['fuel_viscosity']
    roughness = data['plumbing']['roughness']

    dp_fuel = pressure_drop(data['plumbing']['fuel_length'], data['engine']['fuel_mass_flow'],
                            data['plumbing']['fuel_diam']*2.54e-2, roughness, fuel_rho, fuel_visc)
    data['plumbing']['fuel_pressure_drop'] = dp_fuel
    data['plumbing']['fuel_flow_vel'] = velocity(
        data['engine']['fuel_mass_flow'], data['plumbing']['fuel_diam']*2.54e-2, fuel_rho)

    ox_temp = data['propellants']['ox_initial_temp']
    ox_press = (data['engine']['chamber_pressure'] +
                data['injector']['ox_pressure_drop'])*1e5  # bar to Pa
    fl = data['propellants']['ox_chem']
    ox_rho = cp.PropsSI('D', 'T', ox_temp, 'P', ox_press, fl)
    ox_visc = cp.PropsSI('V', 'T', ox_temp, 'P', ox_press, fl)
    data['plumbing']['ox_pressure_drop'] = pressure_drop(data['plumbing']['ox_length'], data['engine']['ox_mass_flow'],
                                                         data['plumbing']['ox_diam'] * 2.54e-2, roughness, ox_rho, ox_visc)
    data['plumbing']['ox_flow_vel'] = velocity(
        data['engine']['ox_mass_flow'], data['plumbing']['ox_diam']*2.54e-2, ox_rho)
