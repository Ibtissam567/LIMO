# -*- coding: utf-8 -*-

"""
@author: sabrina
"""


from utils import *

fen = Tk()

######### CENTRER LA FENÊTRE #############
screen_width = fen.winfo_screenwidth()
screen_height = fen.winfo_screenheight()
fen_width = screen_width-200
fen_height = screen_height-150
center_x = int((screen_width/2) - (fen_width/2))
center_y = int((screen_height/2) - (fen_height/2))-50 #-50 pour la barre des tâches en bas


fen.config(background=main_background_color)
fen.geometry(f'{fen_width}x{fen_height}+{center_x}+{center_y}')
fen.title("Princesse LIMO")

icon_robot = create_photoImage(icon)
fen.wm_iconphoto(True,icon_robot)



map_canva = Canvas(fen,width=map_width, height=map_height,highlightthickness=0)
title_canva = Canvas(fen,width=300, height=100,bg=main_background_color,highlightthickness=0)
camera_canva = Canvas(fen,width=200, height=200, highlightbackground='black', highlightthickness=2)
desc_canva = Canvas(fen,width=fen_width-500, height=100, highlightbackground='black', highlightthickness=2)

menu_canva = Canvas(fen,width=100, height=200, highlightbackground='black', highlightthickness=2)
etat_canva = Canvas(fen,width=100, height=80, highlightbackground='black', highlightthickness=2)

# video = webcam.Box(camera_canva, width = 200, height=200)

########### IMAGE DU ROBOT ET TITRE #################
img = create_photoImage(image_robot)
img_container = title_canva.create_image(50,40, image=img)
title_canva.create_text(175,50,text="LIMO",font=("Helvetica", 46), fill="black")

########### Image map ###################
img_map = create_photoImage('./images/map.jpg',(map_width,map_height))
map_canva.create_image(map_width/2,map_height/2,anchor='center',image=img_map)

############# descriptif ###############
desc_canva.create_text(10,10,anchor='nw',text=descriptif, font=("Helvetica", 14), fill="black")

etat_canva.create_text(5,5,anchor='nw',text=txt_pos, font=("Helvetica", 12), fill="black",tags="txt_pos")

############### BOUTONS #################################
up = create_photoImage("./images/up.jpg", (25,25))
right = create_photoImage("./images/right.jpg", (25,25))
left = create_photoImage("./images/left.jpg", (25,25))
down = create_photoImage("./images/down.jpg", (25,25))
bouton_avant = Button(master=menu_canva,image=up, command=marche_avant)
bouton_droite = Button(master=menu_canva,image=right, command=droite)
bouton_gauche = Button(master=menu_canva,image=left, command=gauche)
bouton_arriere = Button(master=menu_canva,image=down, command=marche_arriere)
bouton_stop = Button(master=menu_canva,text='stop', command=stop, width=2)
bouton_clavier = Button(master=menu_canva,text='Commande\nclavier', command=stop, width=6)

################# CLICK ####################
def clic(event):
    """ Gestion de l'événement clic gauche sur la carte """
    map_canva.delete(map_canva.find_withtag('goal')) # effacer le point précédent
    X = event.x
    Y = event.y
    r=5
    map_canva.create_oval(X-r, Y-r, X+r, Y+r, outline = 'black',fill = 'green', tags='goal')
    #################### mise à jour positions affichées
    etat_canva.delete(etat_canva.find_withtag("txt_pos"))
    etat_canva.create_text(5,5,anchor='nw',text=f"Position réelle\nx = \ny = \ntheta = \n\nPosition demandée\nX = {X}\nY = {Y}", font=("Helvetica", 12), fill="black",tags="txt_pos")
    x_start,y_start = get_position()
    x_goal = X*750/map_width # changement d'échelle
    y_goal = Y*750/map_height
    print(x_goal,y_goal)
    find_path(x_start,y_start,x_goal,y_goal)

map_canva.bind('<Button-1>', clic)

###########################

camera_canva.place(x=fen_width-210,y=10)
title_canva.place(x=fen_width/2-150,y=5)
map_canva.place(x=fen_width/2-map_width/2,y=130) #y = title_height + 30pady
desc_canva.place(x=250,y=fen_height-110)
menu_canva.place(x=10,y=10)
etat_canva.place(x=10,y=10+300+10)

bouton_avant.place(x=33,y=10)
bouton_arriere.place(x=33,y=80)
bouton_droite.place(x=55,y=45)
bouton_gauche.place(x=10,y=45)
bouton_stop.place(x=30,y=125)
bouton_clavier.place(x=20,y=160)

# video.show_frames() #flux vidéo

fen.mainloop()
        
