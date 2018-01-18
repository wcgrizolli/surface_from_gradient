
%=========================================================
% Matlab code for ECCV 2006 paper
% Copyright: Amit Agrawal, 2006
% http://www.umiacs.umd.edu/~aagrawal/
% Permitted for personal use and research purpose only
% Refer to the following citations:

%   1.  A. Agrawal, R. Raskar and R. Chellappa, "What is the Range of
%   Surface Reconstructions from a Gradient Field? European Conference on
%   Computer Vision (ECCV) 2006

%   2.  A. Agrawal, R. Chellappa and R. Raskar, "An Algebraic approach to surface reconstructions from gradient fields?
%   Intenational Conference on Computer Vision (ICCV) 2006
%=========================================================

clear all;close all;clc;

restoredefaultpath();
addpath(genpath('../g2sAgrawal/AgrawalECCV06CodeMFiles/'));
addpath(genpath('../g2sHarker/grad2Surf/'));
addpath(genpath('../g2sHarker/DOPBox/'));
addpath('~/Height data from gradient fields/codes/wg_scripts/')

%graphics_toolkit fltk
pkg load signal
pkg load image

USE_ALGORITH_3 = 0;  % it needs to run an cpp script. Skip it

global RMSE_TH;
global maxZ;


ADD_OUTLIERS = 0
ADD_NOISE = 1
NOISE_LEVEL = 5
RMSE_TH = 0.01
SAVE_ASC = 1
PLOT_ALL = 0 % Plot is not working in octave < 4.0
SAVE_PLOT = 0
OUT_PREFIX = 'output/fermidirac_5pct_noise_'


% generate synthetic surface (im)
%  synthetic_ramppeaks
im = sample_fermi_diracs(101, 101);

% maxZ = max(im(:));
[H,W] = size(im)
[ogx,ogy] = calculate_gradients(im,0,0);


%%

% ogx2 = importdata('data/dpcHorizontal_output.dat');
% ogy2 = importdata('data/dpcVertical_output.dat');

% ogx = importdata('data/dpc_Belens_hor.dat');
% ogy = importdata('data/dpc_Belens_ver.dat');

%
% ogx2 = importdata('data/dpc_spheres_hor.dat');
% ogy2 = importdata('data/dpc_spheres_ver.dat');

% ogx = ogx2(2*end/4:4*end/4, 1*end/4:3*end/4);
% ogy = ogy2(2*end/4:4*end/4, 1*end/4:3*end/4);

%%

[H,W] = size(ogx)

% add noise in gradients
if(ADD_NOISE)
    tt = sqrt(ogx.^2 + ogy.^2);
    sigma = NOISE_LEVEL*max(tt(:))/100
    clear tt
else
    sigma = 0
end

gx = ogx + sigma*randn(H,W);
gy = ogy + sigma*randn(H,W);

%add uniformly distributed outliers in gradients
if(ADD_OUTLIERS)
    fac = 3
    outlier_x = rand(H,W) > 0.999;
    outlier_x(:,end) = 0;

    gx = gx + fac*outlier_x.*(2*(rand(H,W)>0.5)-1);

    outlier_y = rand(H,W) > 0.999;
    outlier_y(end,:) = 0;

    gy = gy + fac*outlier_y.*(2*(rand(H,W)>0.5)-1);
    outlier_x = double(outlier_x);
    outlier_y = double(outlier_y);
    disp(sprintf('Gx outliers = %d',sum(outlier_x(:))));
    disp(sprintf('Gy outliers = %d',sum(outlier_y(:))));
end



gx(:,end) = 0;
gy(end,:) = 0;




%% =========================================================
disp('============================================');
disp('Algorithm I. Least squares solution by solving Poisson Equation')
tic
r_ls = poisson_solver_function_neumann(gx,gy);
alg_1_toc = toc;
r_ls = r_ls - min(r_ls(:));


%% =========================================================
disp('============================================');
disp('Algorithm II. Frankot-Chellappa Algorithm')
tic
fc = frankotchellappa(gx,gy);
alg_2_toc = toc;


if(USE_ALGORITH_3)
    %% ==================================
    disp('============================================');
    disp('Algorithm III. Alpha-Surface')

    % assign weights to edges
    gmag = sqrt(gx.^2 + gy.^2);
    WM1 = abs(gx);  %gmag;
    WM2 = abs(gy);  %gmag;

    % Find MST minimum spanning tree
    mask_gx = ones(H,W);
    mask_gy = ones(H,W);
    [mask_gx_new,mask_gy_new] = RunMSTCCode(H,W,mask_gx,mask_gy,WM1,WM2);

    % Integrate using the gradients corresponding to the edges in the spanning
    % tree
    [gx1,gy1] = curlcorrection_2d_neumann(gx,gy,mask_gx_new,mask_gy_new);
    Z_alpha_init = poisson_solver_function_neumann(gx1,gy1);
    Z_alpha_init = Z_alpha_init - min(Z_alpha_init(:));
    clear gx1 gy1


    % Iteratively add gradients using tolerance alpha
    C = calculate_curl(gx,gy);
    sigma_new = sqrt(var(abs(C(:)))/4)
    invalid_estimation = zeros(H,W);
    [Z_alpha,mask_final_gx,mask_final_gy] = iterative_add_gradients(Z_alpha_init,gx,gy,sigma_new,mask_gx_new,mask_gy_new,invalid_estimation);
    Z_alpha = Z_alpha - min(Z_alpha(:));

end


%% ====================================================
disp('============================================');
disp('Algorithm IV. M estimator');
tic
r_M = M_estimator(gx,gy,0);
alg_4_toc = toc;
r_M = r_M - min(r_M(:));

%% ====================================================
disp('============================================');
disp('Algorithm V. Regularization using energy minimization')
tic
rr = halfquadractic(gx,gy);
alg_5_toc = toc;


%% ====================================================
disp('============================================');
disp(' Algorithm VI. Affine transformation of gradients using Diffusion tensor')
tic
[x,D11,D12,D22] = AffineTransformation(gx,gy);
alg_6_toc = toc;


%% ====================================================
disp('============================================');
disp(' Algorithm VII. GLS Solution with Tikhonov Regularization')
lambda = 0.025 ;
deg = 0 ;
N = 3;
Z0 = zeros(H, W) ;
tic
[ r_tik, Res ] = g2sTikhonov( gx, gy, linspace(1,H,H)', linspace(1,W,W)', N, lambda, deg, Z0 ) ;
alg_7_toc = toc;

close all;

disp('=== Race results:')
disp(sprintf('Algorithm I  : %.3g s', alg_1_toc))
disp(sprintf('Algorithm II : %.3g s', alg_2_toc))
disp(sprintf('Algorithm IV : %.3g s', alg_4_toc))
disp(sprintf('Algorithm V  : %.3g s', alg_5_toc))
disp(sprintf('Algorithm VI : %.3g s', alg_6_toc))
disp(sprintf('Algorithm VII: %.3g s', alg_7_toc))

if(SAVE_ASC)

  save('-ascii', [OUT_PREFIX 'algorithm_0.txt'], 'im');
  save('-ascii', [OUT_PREFIX 'algorithm_1.txt'], 'r_ls');
  save('-ascii', [OUT_PREFIX 'algorithm_2.txt'], 'fc');
  save('-ascii', [OUT_PREFIX 'algorithm_4.txt'], 'r_M');
  save('-ascii', [OUT_PREFIX 'algorithm_5.txt'], 'rr');
  save('-ascii', [OUT_PREFIX 'algorithm_6.txt'], 'x');
  save('-ascii', [OUT_PREFIX 'algorithm_7.txt'], 'r_tik');


end

%% ALL plots
if(PLOT_ALL)

  mydisplay(im);
  title('original');axis on;

  %  %%
  %  figure; contourf(gx, 'LineColor','none'); title('Gradient Horz');
  %  figure; contourf(gy, 'LineColor','none'); title('Gradient Vert');
  %
  mydisplay(im - r_ls);
  [mse_ls,rmse_ls] = calculate_mse(im,r_ls,RMSE_TH);
  axis on;
  title(sprintf('Least Squares, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));

  %
  mydisplay(im - fc);
  [mse_ls,rmse_ls] = calculate_mse(im,fc,RMSE_TH);
  axis on;
  title(sprintf('Frankot Chellappa, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));


  %

  if(USE_ALGORITH_3)
    mydisplay(im - Z_alpha_init);
    [mse_ls,rmse_ls] = calculate_mse(im,Z_alpha_init,RMSE_TH);
    axis on;
    title(sprintf('Initial spanning tree, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));


    mydisplay(im - Z_alpha);
    [mse_ls,rmse_ls] = calculate_mse(im,Z_alpha,RMSE_TH);
    axis on;
    title(sprintf('Alpha Surface, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));
  end

  %
  mydisplay(im - r_M);
  [mse_ls,rmse_ls] = calculate_mse(im,r_M,RMSE_TH);
  axis on;title(sprintf('M estimator, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));

  %
  mydisplay(im - rr);
  [mse_ls,rmse_ls] = calculate_mse(im,rr,RMSE_TH);
  axis on;
  title(sprintf('Energy Minimization, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));

  %
  mydisplay(im - x);
  [mse_ls,rmse_ls] = calculate_mse(im,x,RMSE_TH);
  axis on;
  title(sprintf('Affine Transformation, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));

  %%
  mydisplay(im - r_tik);
  [mse_ls,rmse_ls] = calculate_mse(im,r_tik,RMSE_TH);
  axis on;
  title(sprintf('GLS Solution with Tikhonov Regularization, MSE = %.3g, Relative MSE = %.3g',mse_ls,rmse_ls));

  %%
  %figure
  %plot(im(30,:))
  %
  %figure
  %plot(r_tik(30,:))

  %
  %sombrero(); axis ij; shading faceted; colormap jet;
  %axis off;
  %%

  if(SAVE_PLOT)
    figlist=findobj('type','figure');
    for i=1:numel(figlist)
      disp(['==> Saving figure ' num2str(i)])
      saveas(figure(i), [OUT_PREFIX num2str(i) '.png']);
    end
  end

end

disp('This is the end.')



%
%[mse_ls,rmse_ls] = calculate_mse(im,r_ls,RMSE_TH);
%disp(sprintf('LS: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%[mse_ls,rmse_ls] = calculate_mse(im,fc,RMSE_TH);
%disp(sprintf('FC: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%[mse_ls,rmse_ls] = calculate_mse(im,r_M,RMSE_TH);
%disp(sprintf('M estimator: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%if(USE_ALGORITH_3)
%    [mse_ls,rmse_ls] = calculate_mse(im,Z_alpha_init,RMSE_TH);
%    disp(sprintf('MST: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%    [mse_ls,rmse_ls] = calculate_mse(im,Z_alpha,RMSE_TH);
%    disp(sprintf('MST final: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%end
%
%
%[mse_ls,rmse_ls] = calculate_mse(im,rr,RMSE_TH);
%disp(sprintf('Energy: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%[mse_ls,rmse_ls] = calculate_mse(im,x,RMSE_TH);
%disp(sprintf('Affine Transformation: MSE = %f, Relative MSE = %f',mse_ls,rmse_ls));
%
%diary off;



