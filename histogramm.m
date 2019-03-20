function histogramm(DOC, docbin)

%
% DOC-Histogramm ausgeben
% 
% Aufruf: histogramm(DOC, docbin) 
%

x = 0:docbin:1;
hist(DOC, x)

alte_limits = axis;                                 % Achsen
axis([0, 1, alte_limits(3), alte_limits(4)]);       % skalieren
xlabel('DOC','Fontsize',30);                        % und
ylabel('number of cycles n','Fontsize',30);         % beschriften
set(gca,'FontSize',28);