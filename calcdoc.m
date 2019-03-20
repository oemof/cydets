function DOC = calcdoc(soc_profile, pre)

%
% DOC berechnen
%
% Aufruf: DOC = calcdoc(soc_profile, pre)
%

for c = 1:1:(size(pre,2))
   
    DOC(c) = min(soc_profile(pre(1,c)), soc_profile(pre(2,c))) - pre(4,c);
    
end