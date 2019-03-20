function pre = preunique(pre)

%
% Selbe Pr‰zyklen rausschmeiﬂen
%
% Aufruf pre= preunique(pre)
%

pre = pre';
pre = unique(pre,'rows');
pre = pre';

for c = 1:1:(size(pre,2)-1)
    
    x = sum(pre(:,c));
    if x == 0
        pre(:,c) = [];
        c = c-1;
    else
    end
    
end