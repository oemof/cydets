function [cycle] = zyklendetektion(soc_profile,docbin)

%
% Funktion Zyklendetektion mit entsprechenden DOCs aus SOC-Profil
%
% Aufruf: [cycle] = zyklendetektion(SOC-Profil, Balkenbreite)
%
% Input: SOC-Profil - Werte zwischen 0 und 1,
%					  k�nnen aber auch gr��er und kleiner sein (Vektor 1xn)
%        Balkenbreite - sinnvolle Werte sind zwischen 0.001 und 0.5 (Skalar)
% Output: cycle - Zyklusinformation
%				  (Vektor 4xn mit Spalten "t_1", "t_3", "Minimum", "DOC")
%
% Ben�tigte Hilfsfunktionen: findpeaks.m - Maxima finden
%							 soc_eq_find_b2.m - Findet letztes gr��eres Maximum
%    						 soc_eq_find_a2.m - Findet n�chstes gr��eres Maximum
%							 searchprecycle.m - Entwickelt alle Pr�zyklen
%							 preunique.m - Selbe Pr�zyklen werden entfernt
%							 cycling.m - Zyklenbedingung(gr��eres Intervall)
%							 zerocolumns.m - Nullspalten werden gestrichen
%							 calcdoc.m - DOC wird berechnet
%							 histogramm.m - Histrogramm wird geplottet
%
%
% Diese Funktion filtert aus einem SOC-Profil einzelne Zyklen inklusive
% deren entsprechenden DOC und Grenzen (jedoch Extrema,
% Erweiterung auf exakte Grenzen verlangsamt wahrscheinlich)
% "Rausschmei�en" von Zyklen unter einem bestimmten Wert ist im
% letzten Schritt m�glich
%


% Finden der Extrema samt Indexnummer
soc_profile = [0,soc_profile,0];
[maxima, index_max] = findpeaks(soc_profile);
soc_profile = soc_profile(2:(end-1));
index_max = index_max-1;

% Ende f�r soc_eq_find_b
end_soc_eq_find = size(maxima);
end_soc_eq_find = end_soc_eq_find(2);

% Vektor t_1, der alle t enth�lt

t_1 = soc_eq_find_b2(maxima, index_max);


% Vektor t_3, der alle t enth�lt

t_3 = soc_eq_find_a2(maxima, index_max);


% Pr�zyklen schaffen mit Zeitstempel

pre = searchprecycle(index_max, soc_profile, t_1, t_3);

% Selbe Pr�zyklen rausschmei�en

pre = preunique(pre);

% Zyklen --> Pr�zyklen

pre = cycling(pre);

% Nullspalten rauswerfen

pre = zerocolumns(pre);

% DOCs berechnen

DOC = calcdoc(soc_profile, pre);

pre(4,:) = DOC;
cycle = pre;

% Histogramm

%histogramm(DOC, docbin)

% Zyklen unter bestimmten Wert rausschmei�en

%c = 1;
%
%while c < size(cycle,2)
%
%    if cycle(4,c) < 0.09
%        cycle(:,c) = [];
%    else
%       c = c+1;
%    end
%
%end

end
