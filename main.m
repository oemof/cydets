

profile = csvread('cav_level.csv');
profile = transpose(profile);

#[cycle] = zyklendetektion(profile, 0.001)
[cycle] = zyklendetektion(profile, 0.25)

% Vektor 4xn mit Spalten: "t_1", "t_3", "Minimum", "DOC"
csvwrite('cycles.csv', transpose(cycle));

%disp(cycle)

clear;
