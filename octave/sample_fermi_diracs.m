function func = sample_fermi_diracs( m, n, radius )
%SAMPLE_FERMI_DIRACS Summary of this function goes here
%   Detailed explanation goes here

if nargin < 3
  radius = fix(n/20);
end


xoo = fix(n/4);

xo_vec = ([3*xoo, 2*xoo, xoo]);

yoo = fix(m/4);
yo_vec = ([3*yoo, 2*yoo, yoo]);

sigma_list = ([.01, .025, .05, .1, .25, .5, 1., 2.5, 5.]);



[xx, yy] = meshgrid(1:m,1:n);


func = zeros(m, n);

counter = 0;
for xo=xo_vec
    for yo=yo_vec
        
        counter = counter + 1;
        sigma_list(counter);
        
        func = func + 1.0./(1 + exp((sqrt((xx-xo).^2+(yy-yo).^2)-radius)./sigma_list(counter)));
    end
end

func = real(func);

