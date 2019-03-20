function pre = cycling(pre)

%
% Zyklenbedingung
%
% Aufruf: pre = cycling(pre)
%

for c = 1:1:(size(pre,2))
   
x = find(pre(3,c) == pre(3,:) & pre(1,c) <= pre(1,:) & pre(2,c) >= pre(2,:));
x(x==c) = []; 

pre(:,x) = 0;

end


