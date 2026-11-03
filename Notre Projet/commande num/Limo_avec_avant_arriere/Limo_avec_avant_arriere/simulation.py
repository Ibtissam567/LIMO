# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:59:06 2023

@author: MissVava
"""
import numpy as np
import time
import matplotlib.pyplot as plt
    
k_rho = 1
k_alpha = 20
k_beta = -10
L = 322 * 10**(-3)
T = 0.01

def mesures(x, y, theta, v, gamma) : #calcule x, y et theta à l'instant T pour faire un observateur

    thetap = v/L * np.tan(gamma)
    theta = theta + T*thetap
    
    xp = v * np.cos(theta)
    x = x + T*xp
    
    yp = v * np.sin(theta)
    y = y + T*yp
    
    return x, y, theta


def controleur(x, y, theta, x_star, y_star, theta_star, v=k_rho, gamma=k_beta+k_alpha) :#calcule rho, alpha et beta pour renvoyer gamma et v
    (x,y,theta) = mesures(x, y, theta, v, gamma)
    x1 = -x+x_star
    y1 = -y+y_star
    
    rho = np.sqrt(x1**2 + y1**2)    
    beta = - theta_star - np.arctan2(y1,x1) # beta_tilde selon les calcules
    alpha = np.arctan2(y1,x1) - theta # -beta - theta avec le beta sans prendre en compte theta_star
    
    
    if (-1.57 <= alpha <= 1.57) :
        sens = 1
    else :
        sens = -1
    
    v = rho * k_rho *sens
    omega = k_alpha*alpha + k_beta*beta
    gamma = np.arctan2(L * omega, abs(v)) * sens
    
    return x,y,theta,v, gamma

def boucle(x0, y0, theta0, x_star, y_star, theta_star) :
    X=[x0]
    Y=[y0]
    THETA=[theta0]
    (x,y,theta,v,gamma)=controleur(x0, y0, theta0, x_star, y_star, theta_star)
    epsilon = 10**(-3)
    while (abs(x - x_star) > epsilon or abs(y - y_star) > epsilon or abs(theta - theta_star) > epsilon) :
        (x,y,theta, v,gamma) = controleur(x, y, theta, x_star, y_star, theta_star,v,gamma)
        X.append(x)
        Y.append(y)
        THETA.append(theta)
        time.sleep(T)
    return X,Y,THETA

(X,Y,THETA) = boucle(0.5, 1, 0, -0.5, 2, 0)

t=np.linspace(0, 1000, len(X))
#plt.plot(t, X, label='simulation de la trajectoire selon x')
#plt.plot(t, Y, label='simulation de la trajectoire selon y')
#plt.plot(t, THETA, label='simulation de la trajectoire selon theta')
plt.plot(X,Y, label='simulation de la trajectoire selon xy')

plt.show()