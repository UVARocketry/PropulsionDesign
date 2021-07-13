import math
from lib import const

# def c_star(exhaust_gamma, exhaust_molar_mass, chamber_temp):
#     exhaust_R = R / exhaust_molar_mass
#     c_star = math.sqrt(exhaust_gamma * exhaust_R * chamber_temp) / exhaust_gamma * \
#         ((exhaust_gamma + 1) / 2) ** ((exhaust_gamma + 1) / (2 * (exhaust_gamma - 1)))
#     return c_star


def exhaust_velocity(exhaust_gamma, exhaust_molar_mass, chamber_temp, chamber_pressure, ambient_pressure):
    '''returns exhaust velocity, assuming isentropic expansion of gases to ambient pressure at exit'''
    k = exhaust_gamma
    R = const.R_u / exhaust_molar_mass
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
    R = const.R_u / exhaust_molar_mass
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
