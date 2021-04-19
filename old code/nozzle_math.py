# # nozzle_math.py
# # Henry Nester
# # 15 November 2020

# # Script to calculate nozzle dimensions from parameters found using CEA.
# # See Ch. 4 of Rocket Science and Engineering for formulas used.

# import math
# from parameters import *

# # find exit velocity assuming isentropic expansion, constant gamma and M
# PR = Pe / Pc
# # ve = math.sqrt((2*gamma/(gamma-)) * ((R/M) * Tc)
#                * (1-(PR ** ((gamma-1)/gamma))))
# Isp = ve / g0

# # find required propellant flow for desired thrust
# m_dot = F / ve
# m_dot_fuel = m_dot * 1 / (OF+1)
# m_dot_ox = m_dot * OF / (OF+1)

# # find exit expansion ratio and cross-sections
# ER = math.sqrt(((gamma-1)/2) * ((2/(gamma+1)) ** ((gamma+1)/(gamma-1))
#                                 ) / ((PR**(2/gamma)) * (1 - (PR ** ((gamma-1)/gamma)))))
# At = m_dot / Pc * math.sqrt(R/M*Tc /
#                             (gamma*(2/(gamma+1))**((gamma+1)/(gamma-1))))
# Ae = At * ER
# Ach = At * CR

# # nozzle dimensions
# Rch = math.sqrt(Ach/math.pi)
# Rt = math.sqrt(At/math.pi)
# Re = math.sqrt(Ae/math.pi)

# Lcon = (Rch - Rt) / math.tan(math.radians(60))
# Ldiv = (Re - Rt) / math.tan(math.radians(15))

# # combustion chamber dimensions
# Vcon = (1/3) * (Ach * (Rch / math.tan(math.radians(60))) -
#                 At * (Rt / math.tan(math.radians(60))))
# Vch = At * Lstar - Vcon
# Lch = Vch / Ach

# # output
# if __name__ == '__main__':
#     print('Fuel requirements')
#     print('m_dot =', m_dot)
#     print('m_dot_fuel =', m_dot_fuel)
#     print('m_dot_ox =', m_dot_ox)
#     print('Nozzle Dimensions')
#     print('Rch =', Rch)
#     print('Rt =', Rt)
#     print('Re =', Re)
#     print('Lch =', Lch)
