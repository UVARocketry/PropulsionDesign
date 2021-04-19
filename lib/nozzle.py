import math
from lib.constants import *


# def c_star(exhaust_gamma, exhaust_molar_mass, chamber_temp):
#     exhaust_R = R / exhaust_molar_mass
#     c_star = math.sqrt(exhaust_gamma * exhaust_R * chamber_temp) / exhaust_gamma * \
#         ((exhaust_gamma + 1) / 2) ** ((exhaust_gamma + 1) / (2 * (exhaust_gamma - 1)))
#     return c_star

def exhaust_velocity(exhaust_gamma, exhaust_molar_mass, chamber_temp, chamber_pressure, ambient_pressure):
    '''returns exhaust velocity, assuming isentropic expansion of gases to ambient pressure at exit'''
    k = exhaust_gamma
    R = R_u / exhaust_molar_mass
    PR = ambient_pressure / chamber_pressure
    exhaust_velocity = math.sqrt((2*k)/(k-1) * R * chamber_temp *
                                 (1 - PR ** ((k - 1) / k)))
    return exhaust_velocity


def expansion_ratio(exhaust_gamma, chamber_pressure, ambient_pressure):
    '''returns optimum expansion ratio, assuming isentropic expansion of gases to ambient pressure at exit'''
    k = exhaust_gamma
    PR = ambient_pressure / chamber_pressure
    expansion_ratio = 1 / ((((k+1)/2)**(1/(k-1))) * (PR**(1/k))
                           * math.sqrt((k + 1) / (k-1) * (1 - PR ** ((k - 1) / k))))
    return expansion_ratio


def throat_area(exhaust_gamma, exhaust_molar_mass, mass_flow, chamber_temp, chamber_pressure):
    '''returns throat area required for choked flow to occur'''
    k = exhaust_gamma
    R = R_u / exhaust_molar_mass
    throat_area = mass_flow / \
        (chamber_pressure*1e5 * k / math.sqrt(k*R*chamber_temp)
         * (2 / (k + 1)) ** ((k + 1) / 2 / (k - 1)))
    return throat_area


def radius(area):
    '''radius corresponding to a given circular cross-sectional area'''
    return math.sqrt(area / math.pi)


def cone_length(r1, r2, theta):
    '''length of cone with top and bottom radii r1, r2 and half-angle theta'''
    return abs(r2-r1) / math.tan(math.radians(theta))


def chamber_length(Vch, Lcon, Ach, At):
    '''length of cylindrical part of chamber, given total chamber volume (cylinder + conical converging section), 
    length of converging section, areas of chamber and throat'''
    Vcon = Ach * Lcon * (1 + math.sqrt(At / Ach) + At / Ach)
    return (Vch - Vcon) / Ach


def calculate(data: dict):
    '''takes a dictionary of design data containing original config plus data from CEA as input.
    Calculates nozzle dimensions and performance, then adds those parameters to the dictionary'''

    data_engine = data['engine']
    data_propellants = data['propellants']
    data_dimensions = data['dimensions']

    # performance
    data_engine['exhaust_velocity'] = exhaust_velocity(
        data_engine['exhaust_gamma'], data_engine['exhaust_molar_mass'], data_engine['chamber_temp'], data_engine['chamber_pressure'], data_engine['ambient_pressure'])
    data_engine['specific_impulse'] = data_engine['exhaust_velocity'] / g0

    # propellant mass flow rates
    mdot = data_engine['mass_flow'] = data_engine['thrust'] / \
        data_engine['exhaust_velocity']
    r = data_propellants['of_ratio']
    data_engine['fuel_mass_flow'] = mdot / (1 + r)
    data_engine['ox_mass_flow'] = r * data_engine['fuel_mass_flow']

    # engine cross-sectional areas
    data_dimensions['expansion_ratio'] = expansion_ratio(
        data_engine['exhaust_gamma'], data_engine['chamber_pressure'], data_engine['ambient_pressure'])
    data_dimensions['throat_area'] = throat_area(data_engine['exhaust_gamma'], data_engine['exhaust_molar_mass'],
                                                 data_engine['mass_flow'], data_engine['chamber_temp'], data_engine['chamber_pressure'])
    data_dimensions['exit_area'] = data_dimensions['throat_area'] * \
        data_dimensions['expansion_ratio']
    data_dimensions['chamber_area'] = data_dimensions['throat_area'] * \
        data_dimensions['contraction_ratio']

    # engine dimensions
    data_dimensions['chamber_radius'] = radius(data_dimensions['chamber_area'])
    data_dimensions['throat_radius'] = radius(data_dimensions['throat_area'])
    data_dimensions['exit_radius'] = radius(data_dimensions['exit_area'])

    data_dimensions['diverging_length'] = cone_length(
        data_dimensions['throat_radius'], data_dimensions['exit_radius'], data_dimensions['diverging_angle'])
    data_dimensions['converging_length'] = cone_length(
        data_dimensions['throat_radius'], data_dimensions['chamber_radius'], data_dimensions['converging_angle'])

    data_dimensions['chamber_volume'] = data_dimensions['throat_area'] * \
        data_propellants['characteristic_length']
    data_dimensions['chamber_length'] = chamber_length(
        data_dimensions['chamber_volume'], data_dimensions['converging_length'], data_dimensions['chamber_area'], data_dimensions['throat_area'])

    # wall thickness (uniform over entire chamber/nozzle part.
    # Size based on max. stress, which occurs in chamber, where pressure and radius are largest
    data_dimensions['wall_thickness'] = data_engine['wall_safety_factor'] * data_engine['chamber_pressure']*1e5 * \
        data_dimensions['chamber_radius'] / \
        data_engine['material_yield_strength']
