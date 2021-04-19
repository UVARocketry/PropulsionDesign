# # cooling_math.py
# # Henry Nester
# # 30 November 2020

# # Script to calculate dimensions of cooling passage for regenerative cooling.
# # Based on Kryzcki book equations.

# from nozzle_math import *

# # coolant flow rate to absorb heat flowing through wall
# Rch_outside = Rch + tch
# # area to be cooled. assume cone is 1/4 the area
# Acool = (2 * math.pi * Rch_outside) * Lch * 1.25
# Qcool = qcool * Acool
# m_dot_cool = Qcool / cp_fuel / dTcool
# # m_dot_cool > m_dot_fuel, ie, more fuel is required to cool the engine than to run it

# # coolant passage size. use smaller m_dot_fuel and hope it doesn't burn up?
# Rcj_inside = math.sqrt(
#     (m_dot_fuel / (math.pi * vcool * rho_fuel)) + Rch_outside ** 2)
# tcool = Rcj_inside - Rch_outside

# # cooling jacket thickness to withstand fuel pressure
# tcj = Pinj_fuel * Rcj_inside / strength_steel

# if __name__ == '__main__':
#     print('Coolant requirements')
#     print('m_dot_cool =', m_dot_cool)
#     print('Coolant passage dimensions')
#     print('tcool =', tcool)
#     print('tcj =', tcj)
