# # constants
# R = 8.314  # ideal gas constant J/(K*mol)
# g0 = 9.81  # gravity on Earth m/s^2

# # engine parameters
# F = 150  # thrust (N)
# dt_burn = 7  # burn duration (s)
# Pc = 15e5  # chamber pressure (Pa)
# Pe = 1.013e5  # exit pressure (Pa)
# tch = 0.002  # combustion chamber wall thickness (m)
# Lstar = 0.7  # characteristic chamber length (m)
# CR = 10  # contraction ratio, ie chamber area / throat area (dimensionless)

# # propellants
# OF = 4.4  # oxidiser/fuel mass ratio (dimensionless)
# rho_fuel = 789  # fuel density (kg/m^3)
# cp_fuel = 2570  # specific heat of coolant (J/(kg*K))
# M_fuel = 0.0461  # molar mass of fuel (kg/mol)
# T0_fuel = 298  # initial fuel temp (K)
# M_ox = 0.0440  # molar mass of oxidiser (kg/mol)
# rho_ox = 700  # density of oxidiser in tank (kg/m^3)
# T0_ox = 298  # inital ox temp (K)
# M_pressurant = 0.0280  # fuel tank pressurant molar mass (kg/mol)
# gamma_pressurant = 1.4  # pressurant specific heat ratio

# # propellant combustion properties (found with CEA)
# gamma = 1.1633  # specific heat ratio (dimensionless)
# M = 0.0251  # molar mass (kg/mol)
# Tc = 3026  # chamber temperature (K)

# # material strengths
# strength_steel = 290e6  # 316L alloy (Pa)
# strength_copper = 55e6  # (Pa)

# # regenerative cooling parameters
# dTcool = 50  # maximum permissible temperature rise of coolant (degC)
# qcool = 5e6  # expected heat flux through wall (W/m^2)
# vcool = 10  # coolant velocity (m/s)

# # injector parameters
# dP_fuel = 5e5  # fuel pressure drop (Pa)
# dP_ox = 5e5  # ox pressure drop (Pa)
# Pinj_fuel = Pc + dP_fuel  # fuel press at inj (Pa)
# Pinj_ox = Pc + dP_ox  # ox press at inj (Pa)
# Ninj_fuel = 4  # number of fuel injectors
# Ninj_ox = 4  # number of ox injectors
# Cd_inj = 0.7  # discharge coefficient for injector

# # tank parameters
# pressurant_frac = 1/2  # amount of fuel tank that is filled with pressurant at start
# ox_ullage_frac = 0.05  # amount of ox tank filled with vapor
# P0_ox_tank = 65e5  # oxidiser tank pressure (Pa)
