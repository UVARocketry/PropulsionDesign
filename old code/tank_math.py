# # tank_math.py
# # Henry Nester
# # 30 November 2020

# # Script to calculate tank dimensions from other engine params

# from cooling_math import *

# # tanks are the same size as engine cooling jacket
# Rtank = 0.050 / 2

# # fuel tank sizing
# m_fuel = m_dot_fuel * dt_burn
# V_fuel = m_fuel / rho_fuel
# V_pressurant = V_fuel * pressurant_frac / (1 - pressurant_frac)
# Vtank_fuel = V_fuel + V_pressurant
# Htank_fuel = Vtank_fuel / math.pi / Rtank ** 2

# # fuel tank initial pressure, assuming final pressure is Pinj_fuel
# # assume pressurant expands isentropically
# P0_fuel_tank = Pinj_fuel * (Vtank_fuel / V_pressurant) ** gamma_pressurant

# # fuel tank wall thickness
# ttank_fuel = P0_fuel_tank * Rtank / strength_steel

# # ox tank sizing
# m_ox = m_dot_ox * dt_burn
# V_ox = m_ox / rho_ox
# V_ullage = V_ox * ox_ullage_frac / (1 - ox_ullage_frac)
# Vtank_ox = V_ox + V_ullage
# Htank_ox = Vtank_ox / math.pi / Rtank ** 2

# # ox tank wall thickness
# ttank_ox = P0_ox_tank * Rtank / strength_steel

# if __name__ == '__main__':
#     print('Fuel tank')
#     print('m_fuel =', m_fuel)
#     print('Vtank_fuel =', Vtank_fuel)
#     print('Rtank =', Rtank)
#     print('Htank_fuel =', Htank_fuel)
#     print('P0_fuel_tank =', P0_fuel_tank)
#     print('ttank_fuel =', ttank_fuel)
#     print('Oxidiser tank')
#     print('m_ox =', m_ox)
#     print('Vtank_ox =', Vtank_ox)
#     print('Rtank =', Rtank)
#     print('Htank_ox =', Htank_ox)
#     print('ttank_ox =', ttank_ox)
