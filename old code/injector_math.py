# # injector_math.py
# # Henry Nester
# # 30 November 2020

# # Script to calculate injector dimensions.
# # See Krzycki for equations used.

# from nozzle_math import *

# # fuel injector dimensions
# Ainj_fuel = m_dot_fuel / Cd_inj / math.sqrt(2 * rho_fuel * dP_fuel)
# Rinj_fuel = math.sqrt(Ainj_fuel / Ninj_fuel / math.pi)

# # oxidiser injector dimensions
# Ainj_ox = m_dot_ox / Cd_inj / math.sqrt(2 * rho_ox * dP_ox)
# Rinj_ox = math.sqrt(Ainj_ox / Ninj_ox / math.pi)

# if __name__ == '__main__':
#     print('Injector dimensions')
#     print('Rinj_fuel =', Rinj_fuel)
#     print('Rinj_ox =', Rinj_ox)
