%Chamber temperature as a function of chamber pressure
%For various mixture ratios
figure(1);
temp_plot=plot(chamber_pressures,temperatures);
title("95% C2H5OH(l) & N2O(g) @ 298K, 1.013bar exit pressure");
xlabel("Chamber pressure (bar)");
ylabel("Chamber temperature (K)");
lgd=legend(cellstr(num2str(oxidiser_fuel_mass_ratio','%.2f')));
lgd.Location='northwest';
title(lgd, 'O/F ratio (mass)');

%Effective exhaust velocity as a function of chamber pressure
%For various mixture ratios
figure(2);
plot(chamber_pressures,isps);
title("95% C2H5OH(l) & N2O(g) @ 298K, 1.013bar exit pressure");
xlabel("Chamber pressure (bar)");
ylabel("Theoretical exhaust velocity (c=Isp/g0) (m/s)");
lgd=legend(cellstr(num2str(oxidiser_fuel_mass_ratio','%.2f')));
lgd.Location='northwest';
title(lgd, 'O/F ratio (mass)');
