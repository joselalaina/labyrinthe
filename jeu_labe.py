import Labe

if __name__ == "__main__":
	perso = "X"
	pos_perso = [1,1]
	tresor = "#"
	n_levels_total = 20
	data = {
		"po" : 0,
		"pv" : 25,
		"level" : 1
		}
	 	
	win = Labe.init_curses(25,41,(0,0))
	coul = Labe.init_colors()
		
	for n_level in range(1, n_levels_total + 1):
		level = Labe.charge_labyrinthe("level_" + str(n_level))
		data["level"] = n_level
		Labe.jeu(level,data,perso,pos_perso,tresor,win,coul)
	win.addstr(1,22,"Vous avez gagné !!",Lab.color("RED",coul))
	win.getch()
	Labe.close_curses()
