k_rho = 1; %positif
k_alpha =2 ; %superieur à k_rho
k_beta =-2 ;% négatif
L = 322e-3; %322mm

%choisir une position initiale
x0 = -0.5;
y0 = 0; 
theta0 = -1.1;

%choisir une position finale
x_star = 5;
y_star = 5;
theta_star = 1;

% theta et theta0 compris dans + ou - 1.2
% x0 doit être <= à x_star
% y0 doit être <= à y_star

% alpha doit appartenir à l'intervalle -pi/2, pi/2

%Pour la marche arrière, v = -v et gamma = -gamma