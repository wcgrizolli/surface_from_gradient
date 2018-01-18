
H = 64
W = 64

im = zeros(64,64);
[x,y] = meshgrid(-8:8,-8:8);
%tt = 1*sqrt((abs(x)-8).*(abs(y)-8));
tt = (abs(x)-8).*(abs(y)-8);
[h,w] = size(tt);

st = 5
im(st:st+h-1,st:st+w-1) = im(st:st+h-1,st:st+w-1) + 0.5*tt;

st = 10
im(st:st+h-1,30+st:30+st+w-1) = im(st:st+h-1,30+st:30+st+w-1) + 0.5*tt;

st = 30
im(st:st+h-1,st:st+w-1) = im(st:st+h-1,st:st+w-1) + 0.15*tt;


for j = 10:50
    im(50:60,j) = (j-10)/4;
end

im = imfilter(im,fspecial('gaussian',6,1),'symmetric');


