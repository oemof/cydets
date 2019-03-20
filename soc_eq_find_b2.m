function [t_1] = soc_eq_find_b2(maxima, index_max)

% Funktion, um t_1 zu finden
%
% Aufruf: [t_1] = soc_eq_find(maxima, minima)
%
% Findet t_1 eines Zyklus, der von dem Maximum an t_2
% abgeschlossen wird

halt = size(maxima);
halt = halt(2);


for c = halt:-1:2
    
    for d=c-1:-1:1
    
    
    if maxima(d) >= maxima(c)
      t_1(c) = index_max(d);
      break
    elseif d==1
      t_1(c) = 1;
      break
    end
    
    end
    
end

t_1(1) = index_max(end);