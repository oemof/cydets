function pre = zerocolumns(pre)

%
% Nullspalten entfernen
%
% Aufruf pre = zerocolumns(pre)
%

c=1;

while c <= size(pre,2)
    
    x = sum(pre(:,c));
    if x == 0
        pre(:,c) = [];
        c = c-1;
    else
    end
    
    c = c+1;
    
end