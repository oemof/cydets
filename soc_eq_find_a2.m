function [t_3] = soc_eq_find_a2(maxima, index_max)

% Funktion, um t_3 zu finden
%
% Aufruf: [t_3] = soc_eq_find(x,t_2)
%
% Findet t_3 eines Zyklus, der von dem Maximum an t_2
% begonnen wurde


stop = size(maxima);
stop = stop(2);

for c = 1:stop
    
    for d=c+1:stop
    
    
    if maxima(d) >= maxima(c)
      t_3(c) = index_max(d);
      break
    elseif d == stop
      t_3(c) = -1;               %falls rechts kein Präzyklus
      break                      
    else 
    
    end
    
    end
    
end

t_3(end+1) = -1;

    
