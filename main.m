

profile = csvread('cav_level.csv');
profile = transpose(profile);

% Ungetestet: normieren der Zeitreihe
% Siehe:
% https://www.mathworks.com/matlabcentral/answers/
% 196798-how-to-normalize-values-in-a-matrix-to-be-between-0-and-1
profile = profile - min(profile(:))
profile = profile ./ max(profile(:))

#[cycle] = zyklendetektion(profile, 0.001)
[cycle] = zyklendetektion(profile, 0.25)

% Vektor 4xn mit Spalten: "t_1", "t_3", "Minimum", "DOC"
csvwrite('cycles.csv', transpose(cycle));

%disp(cycle)

clear;
