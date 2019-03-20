function [DOC] = threepoint(soc_profile, docbin)

%
%
%
%
%
%
%
%
%
%

soc_profile = [0 soc_profile 0];
soc_negativ = -soc_profile;

% Finden der Extrema samt Indexnummer und zu einem Vektor zusammenfügen
[maxima, index_max] = findpeaks(soc_profile);
[minima, index_min] = findpeaks(soc_negativ);

a = size(maxima,2);
b = size(minima,2);

stop=size(minima);
stop=stop(2);
for c=1:stop
    minima(c)=soc_profile(index_min(c));
end


if a>b
   minima = [minima 0];
   index_min = [index_min 0];
   
   extrema = vertcat(maxima, minima);
   extrema = extrema(:)';
   extrema = extrema(1:(end-1));

   index_ext = vertcat(index_max, index_min);
   index_ext = index_ext(:)';
   index_ext = index_ext(1:(end-1));
   index_ext = index_ext - 1;

   soc_profile = soc_profile(2:(end-1));
else
    
   extrema = vertcat(maxima, minima);
   extrema = extrema(:)';

   index_ext = vertcat(index_max, index_min);
   index_ext = index_ext(:)';
   index_ext = index_ext - 1;

    
end



% Three-Point-Algorithm

halt = size(extrema);
halt = halt(2);
c = 1;
d = 1;
l = 0;

while halt > 3 && (c+2)<size(extrema,2)
    
    
    X = abs(extrema(c+2)-extrema(c+1));
    Y = abs(extrema(c+1)-extrema(c));
    
    if X < Y
       
        c = c+1;
        l = l+1;
        
    else
        DOC(d) = Y;
        d = d+1;
        
        
        extrema(c+1) = [];
        extrema(c) = [];
        
        c = c-l;
        l = 0;
    
    end    
        

    
    halt = size(extrema);
    halt = halt(2);
    if halt == 3
        DOC(d) = abs(extrema(c+1) - extrema(c));
        break
    else
         
    end
   
 
    
end

% Histogramm

histogramm(DOC, docbin)

end