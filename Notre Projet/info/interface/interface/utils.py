# -*- coding: utf-8 -*-

"""
@author: sabrina
"""

from tkinter import*
from PIL import Image, ImageTk
import numpy as np
from rrt_star import *

from tkinter_webcam import webcam

main_background_color = '#F6C7E4'  #Fairy tale
icon = "./images/limo_icone.jpg"
image_robot = "./images/limo.jpg"
map_height = 400
map_width = 400
descriptif = "* Déplacer le robot avec les flèches\n* Arrêter le robot avec le bouton stop\n* Choisir une destination en cliquant sur la carte\n"
L = 322 # mm

X_choix=0
Y_choix=0

X_reel=0
Y_reel=0
theta_reel = 0

txt_pos = f"Position réelle\nx = \ny = \ntheta = \n\nPosition demandée\nX = {0}\nY = {0}"

def get_position():
    print("tkt jrv bientôt")
    return(1.35, 3.9)

def create_photoImage(filename:str,size=(120,100)):
    """ create image from jpg """
    image = Image.open(filename)
    image = image.resize(size)
    img = ImageTk.PhotoImage(image)
    return img


def marche_avant():
    """ fonction marche avant """
    print("j'avaaaaaance")
def marche_arriere():
    """ fonction marche arriere """
    print("BIP BIP BIP")
def droite():
    """ fonction tourner a droite """
    print("je tourne à droiiiite")
def gauche():
    """ fonction tourner a gauche """
    print("je tourne à gauuuuche")
def stop():
    """ fonction d'arret """
    print("HALTE")

def find_path(pox_x,pox_y,x_goal,y_goal):
    """ calcule et retourne la trajectoire entre 
        la position du robot et un goal donné """
    start = Point(pox_x,pox_y)
    goal = Point(x_goal-L/2,y_goal-L/2) # L'algorithme considère le point comme centre du robot donc on décale pour éviter les collisions?
    rrt_star = RRTStar(arect_cspace, start, goal, eta=3., delta=2.)
    rrt_star.expand()
    path_pt = rrt_star.build_final_path() # retourne une liste de la classe Point
    print("Path : ",path_pt)
    if path_pt == []:
        raise ValueError
    path = [(p.x,p.y) for p in path_pt] # transforme le path_pt en liste de couple
    return path


def get_angle(pox_x,pox_y,x_goal,y_goal):
    """ retourne l'angle à atteindre pour un point """
    vect = (x_goal-pox_x,y_goal-pox_y)
    theta = np.arccos((x_goal-pox_x)/np.linalg.norm(vect))

    return theta