import os
import random
import curses

def init_curses(lignes,cols,pos):
	"""Initialisation de paramètre graphique"""
	curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	
	window = curses.newwin(lignes,cols,pos[0],pos[1])
	window.border(0)
	window.keypad(1)
	return window
	
def close_curses():
	"""Restauration de paramètre graphique"""
	curses.echo()
	curses.nocbreak()
	curses.curs_set(1)
	curses.endwin()
	
def init_colors():
	"""Initialisation de couleur"""
	curses.start_color()
	curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_BLACK,curses.COLOR_BLUE)
	return ["RED","GREEN","BLUE"]
	
def color(code,l_color):
	"""Sélectionne une couleur"""
	return curses.color_pair(l_color.index(code) + 1)			

def charge_labyrinthe(nom):
	"""Charge le labyrinthe depuis un fichier.txt"""
	try:
		fic = open(nom + ".txt","r")
		data = fic.readlines()
		fic.close()
	except IOError:
		print("Impossible de lire le fichier {}.txt".format(nom))
		os._exit(1)
			
	for i in range(len(data)):
		data[i] = data[i].strip()
		
	return data
	
def barre_score(data,win,coul):
	"""affiche le score du jeu"""
	barre = "PV : {:2d} PO : {:4d} Level : {:3d}"
	win.addstr(21,1,barre.format(data["pv"],		       data["po"],data["level"]),color("BLUE",coul))		

def affiche_labyrinthe(lab,perso,pos_perso,tresor,win,coul):
	"""affichage d'un labyrinthe"""
	n_ligne=0
	for ligne in lab:
		for i in range(1,4):
			ligne = ligne.replace(str(i),tresor)
		if n_ligne == pos_perso[1]:
			win.addstr(n_ligne + 1,10,ligne[0:pos_perso[0]]+ perso + ligne[pos_perso[0] + 1:])
			win.addstr(n_ligne + 1,10 + pos_perso[0],perso,color("RED",coul))
		else:
			win.addstr(n_ligne + 1,10,ligne)
		n_ligne += 1								 					
					
def decouverte_tresor(categorie,data):
	"""Incrémente le nombre de pièce d'or"""
	if categorie == "1":
		data["po"] = data["po"] + random.randint(1,5)
	elif categorie == "2":
		data["po"] = data["po"] + random.randint(5,10)
	else:
		data["po"] = data["po"] + random.randint(0,25)
		
def combat(data):
	"""détérmine le nombre de point de vie perdus"""
	de = random.randint(1,10)
	if de == 1:
		data["pv"] = data["pv"] - random.randint(5,10)
	elif de >= 2 and de <= 4:
		data["pv"] = data["pv"] - random.randint(1,5)										
		
def verification_deplacement(lab,pos_col,pos_ligne,data):
	"""Deplacement du personnage"""
	n_cols = len(lab[0])
	n_lignes = len(lab)
	if pos_ligne < 0 or pos_col < 0 or pos_ligne > (n_lignes - 1) or \
	pos_col > (n_cols - 1):
		return None
	elif lab[pos_ligne][pos_col] == "O":
		return [-1,-1]	
	elif lab[pos_ligne][pos_col] == "1" or lab[pos_ligne][pos_col] \
	== "2" or lab[pos_ligne][pos_col] == "3":
		decouverte_tresor(lab[pos_ligne][pos_col], data)
		lab[pos_ligne] = lab[pos_ligne][:pos_col] + " " + \
		lab[pos_ligne][pos_col + 1:]
		return [pos_col,pos_ligne]
	elif lab[pos_ligne][pos_col] == "$":
		combat(data)
		lab[pos_ligne] = lab[pos_ligne][:pos_col] + " " + \
		lab[pos_ligne][pos_col + 1:]
		return [pos_col,pos_ligne]	
	elif lab[pos_ligne][pos_col] != " ":
		return None	
	else:
		return [pos_col,pos_ligne]
		
def choix_joueur(lab,pos_perso,data,win):
	"""Demande au joueur de saisir son deplacement"""
	dep = None
	choix = win.getch()
	if choix == curses.KEY_UP:
		dep = verification_deplacement(lab,pos_perso[0],\
		pos_perso[1] - 1,data)
	elif choix == curses.KEY_DOWN:
		dep = verification_deplacement(lab,pos_perso[0],\
		pos_perso[1] + 1,data)
	elif choix == curses.KEY_LEFT:
		dep = verification_deplacement(lab,pos_perso[0] - 1,\
		pos_perso[1],data)
	elif choix == curses.KEY_RIGHT:
		dep = verification_deplacement(lab,pos_perso[0] + 1,\
		pos_perso[1],data)
	elif choix == 27:
		close_curses()
		os.exit(1)
	if dep != None:
		pos_perso[0] = dep[0]
		pos_perso[1] = dep[1]
		
def jeu(level,data,perso,pos_perso,tresor,win,coul):
	"""Boucle principale du jeu"""
	while True:
		affiche_labyrinthe(level,perso,pos_perso,tresor,\
	win,coul)
		barre_score(data,win,coul)
		if data["pv"] <= 0:
			win.addstr(1,20,"PERDU",color("RED",coul))
			win.getch()
			close_curses()
			os._exit(1)
		choix_joueur(level,pos_perso,data,win)
		if pos_perso == [-1,-1]:
			win.addstr(22,1,"passe niveau",color("RED",coul))
			win.addstr(23,1,"Appuyez sur une touche pour continuer",color("RED",coul))
			win.getch()
			win.addstr(1,20," "*50)
			win.addstr(1,21," "*50)
			break
		
		
