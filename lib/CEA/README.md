# CEA
NASA CEA (Chemical Equilibrium with Applications) is a bit of *old* software used 
to assess combustion physics in rocket engines, ramjets, turbines, etc.

So far for this project, we've only used it to assess the combustion temperature versus specific impulse tradeoff
as we vary the mixture ratio of oxidizer and fuel. But there are MANY other uses, even for solid motors.

Any chemical, or a mixture, can be used as a propellant. 

The software was written in FORTRAN, but I managed to find a copy (don't remember where) of a .exe that runs
the FORTRAN on Windows (at least). Those using another OS should shop around the Internet
for another copy of CEA that works. I believe there are a few versions with a Java GUI interface
as well, instead of just the command line.

Anyway, the way this version of CEA works is, you write an input file (file.inp), then run FCEA2m.exe 
from the command line. A prompt appears asking you for the input file name without the extension
(so just "file" here). Hit enter and CEA will run, spitting out its results in, for example, file.out
(it's just a text file). All kinds of useful calculation results show up there, so take a look.

## Example .inp file
(remove the comments that come after // :) )
```
problem
rocket //infinite combustor approx.
equilibrium //tells CEA to use a shifting chemical equilibrium along nozzle
p,bar=30.000 //chamber pressure, bar
pip=29.615 //chamber/ambient pressure ratio, bar/bar
o/f=1.85 //ox/fuel mass ratio, kg/kg
react
fuel=JP-5 wt=100.000 t,K=298.000 //burn 100% by mass JP-5 initially at 298K
ox=O2 wt 100 t,K 298.000 //with 100% by mass gaseous O2 ditto
end
```
To use a mixture of fuels (wt are MASS fractions) do
```
fuel=FORMULA_1 wt=75 t,K=298
fuel=FORMULA_2 wt=10 t,K=298
fuel=FORMULA_3 wt=15 t,K=298
```