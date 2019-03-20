function pre = searchprecycle(index_max, soc_profile, t_1, t_3)

%
% Präzyklen schaffen mit Zeitstempel
%
% Aufruf pre = searchprecycle(index_max, soc_profile, t_1, t_3)
%

x = size(index_max,2);
pre1 = zeros(4,x);
pre3 = zeros(4,x);
mini1 = zeros(1,x);
miniloc1 = zeros(1,x);
mini3 = zeros(1,x);
miniloc3 = zeros(1,x);

for c = 1:1:size(index_max,2)
   
    if t_1(c) < index_max(c)
      
      [mini1(c), miniloc1(c)] = min(soc_profile(t_1(c):index_max(c)));
      miniloc1(c) = miniloc1(c) + t_1(c) - 1;
      pre1(1,c) = t_1(c);
      pre1(2,c) = index_max(c);
      pre1(3,c) = miniloc1(c);
      pre1(4,c) = mini1(c);
      
    else
    end
   
    if t_3(c) > index_max(c)
       
      [mini3(c), miniloc3(c)] = min(soc_profile(index_max(c):t_3(c)));  
      miniloc3(c) = miniloc3(c) + index_max(c) - 1;
      pre3(1,c) = index_max(c);
      pre3(2,c) = t_3(c);
      pre3(3,c) = miniloc3(c);
      pre3(4,c) = mini3(c);
      
    else
    end 
    
end

pre = [pre1 pre3];