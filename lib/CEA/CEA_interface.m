%Uses CEA program to calculate performance of propellant for range of 
%oxidiser/fuel ratios.

chamber_pressures = 12:0.5:22; %bar
ambient_pressure = 1.013; %bar
ethanol_mass_percent = 90; %kg ethanol per 100kg propellant
oxidiser_fuel_mass_ratio = 4.2:0.1:4.7; %kg ox/kg fuel
%1.3...1.7 is good for O2. 4.2...4.7 is good for N2O

%these store values in plottable matrix
%each col is values for a given mixture ratio
%each row is values for a given pressure ratio
temperatures = [];
isps = [];

for chamber_pressure = chamber_pressures
    chamber_ambient_pressure_ratio=chamber_pressure/ambient_pressure;
    create_CEA_inp_file(chamber_pressure,chamber_ambient_pressure_ratio, ...
        oxidiser_fuel_mass_ratio,ethanol_mass_percent);
    run_CEA();
    %read latest CEA output file
    warning('off','all') %suppress rarded error
    data = readtable('data.csv');
    warning('on','all') %suppress rarded error

    %data appears in rows in order
    %first o/f value: values in combustion chamber
    %first o/f value: values at throat of nozzle
    %first o/f value: values at nozzle exit
    %second o/f value...etc.

    chamber_temp_table = data(1:3:end, ["o_f","t"]);
    
    specific_impulse_table = data(3:3:end, ["o_f","isp"]);
    
    %we want temperatures in chamber, which is first value of every
    %three-row set. append row of temperatures for this chamber pressure to
    %matrix
    temperatures = [temperatures; data.t(1:3:end)'];
    %we want Isp with supersonic expansion included, so take values at
    %exit, which is last value of every three-value set. append row of isps
    %for this chamber pressure to matrix
    isps = [isps; data.isp(3:3:end)'];
end

%Generates data.inp file for FCEA2.exe to run on.
function create_CEA_inp_file(p,pip,of,eth_perc)
    CEA_inp_path = "./data.inp";
    CEA_inp = fopen(CEA_inp_path, "w");
    
    fprintf(CEA_inp,"problem\n");
    fprintf(CEA_inp,"\trocket\n"); %tell CEA we're doing a rocket calculation 
    %with an infinite area combustor.
    %assume reaction rates are infinite - things go right to equilibrium.
    %underestimates performance slightly
    %shifting equilibrium calc is done, which overestimates performance slightly
    fprintf(CEA_inp,"\tequilibrium\n");
    %chamber pressure
    fprintf(CEA_inp,"\tp="+p+"\n");
    %chamber/ambient pressure ratio
    fprintf(CEA_inp,"\tpip="+pip+"\n");
    %ox/fuel ratios. sprintf converts array to comma sep string.
    %added newline between values so that line length limit would not be 
    %a problem
    fprintf(CEA_inp,"\to/f="+sprintf('%.5e,\n',of)+"\n");
    %tell CEA what reactants to use
    fprintf(CEA_inp,"react\n");
    %fuel is partly ethanol at 25C
    fprintf(CEA_inp,"\tfuel=C2H5OH(L) wt="+eth_perc+" t,k=298\n");
    %rest is water at 25C
    fprintf(CEA_inp,"\tfuel=H2O(L) wt="+(100-eth_perc)+" t,k=298\n");
    %ox is gaseous oxygen, also at 25C (check assumption)
    fprintf(CEA_inp,"\toxid=N2O wt=100 t,k=298\n");
    %tell CEA what values to print to the .plt and .csv plotting files
    fprintf(CEA_inp,"output\n");
    fprintf(CEA_inp,"\tplot o/f t isp\n");
    fprintf(CEA_inp,"end\n");

    fclose(CEA_inp);
end

%Actually runs FCEA2m.exe, the CEA program executable.
%CEA will look at data.inp, do the maths, then spit out a long printout,
%data.out, which we don't need, plus a file with the data we asked to plot
%in .txt and .csv formats. We want the data.csv file.
function run_CEA()
    %FCEA2m.exe prompts for the name of the .inp file when it runs, so we
    %prep a text file with the word "data" in it.
    file=fopen("FCEA2mcommands.txt","w");
    fprintf(file,"data");
    fclose(file);
    %run the executable with that text file as input.
    [spam,eggs]=system("FCEA2m.exe < FCEA2mcommands.txt");
end


