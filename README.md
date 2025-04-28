# Bomberman

Phase 1 : Conception du jeu
	1.	Choisir un jeu : Bomberman (difficulté: moyenne)
	
	
	2.	Définir les règles : Écrire une spécification claire des règles du jeu.
			- Deux joueurs 
			- Deux Joueurs apparaissent à l'opposé de chacun
			
			- Coup par coup
			- Une case du jeu fait 10px*10px
			
			- Joueur est de taille 10px*10px
			- Joueur peut placer une seul bombe après que sa dernière bombe a explosé 
			- Joueur peut se déplacer en x ou en y
			- Joueur ne peut pas pousser une bombe
			
			- Bombe est de taille 10px*10px
			- Bombe explose sur une distance de 3 en x et y à partir du centre
			- Bombe explose après 3 coups du même joueur
			- Bombe est un obstacle pour Joueur
			- Bombe ne peut pas casser un mur 
			- Bombe peut casser une Brique			
			
			- Map est de taille 13*13 soit 130px*130px 
			- Map possède des murs de taille 10px*10px
			- Map peut arrêter l'explosion de Bombe
			
			- Brique est de taille 10px*10px
			- Brique est un mur cassable par Joueur
			- Brique peut arrêter l'explosion de Bombe mais se casse après
	
	
	3.	Définir la structure des données 			
	3.1	Représentation de l’état du jeu (plateau, positions, sgames, etc.).
			- plateau = graphe (x, y) de (0, 0) à (130, -130)
			
			- Vivant = état Joueur 
			- Mort = état Joueur
			
	3.2	Actions possibles pour chaque joueur.
			- Joueur peut poser Bombe
			- Joueur peut se déplacer (fléchette directionnelle) dans n'importe quelle case libre
			- Joueur peut casser Brique grâce à Bombe
			- Joueur ne peut pas traverser Bombe, Obstacle et Brique
			
			- Si Joueur se trouve à porté d'explosion, alors Joueur meurt
			- Si Joueur meurt, alors Joueur ressuscité dans un des 4 coins de Map à l'opposé de l'autre Joueur
	
	3.3	Evenements possibles
			- Lorsqu'une Bombe est posée elle prend 3 tours pour le joueur pour exploser
			- Lorsque la Bombe explose, l'explosion laisse une trace qui dure 1 tour



Phase 2 : Implémentation du moteur de jeu
	1.	Créer une représentation du plateau.
			- Map = classe Map
			- Joueur = classe Joueur (sprite + position + vie + mouvement)
			- Bombe = classe Bombe (sprite + dégât + position)
			- Obstacle = classe Mur groupée
			
			
	2.	Implémenter les règles du jeu :
	2.1	Vérification de la validité des coups.
			- si Joueur est en collision avec un Mur du groupe Obstacle, le joueur ne peut pas s'y déplacer	
			- si Joueur est en contact avec l'explosion d'une bombe, le joueur meurt
			
			
	2.2	Conditions de victoire ou d’égalité.
			- si Joueur n'a plus de vie alors la partie est terminée
			- si les deux joueurs meurent en même temps, ils ré-apparaissent à leur point de départ
			- si les deux joueurs meurent en même temps et qu'ils n'ont plus de vie, c'est égalité
	
	
	3.	Créer un affichage (texte ou graphique) pour visualiser la partie.
			- une map (modifiable dans le futur) peut être représenter par:
				###############
				#S00000000000S#
				#0#0#0#0#0#0#0#
				#0000000000000#
				#0#0#0#0#0#0#0#
				#0000000000000#
				#0#0#0#0#0#0#0#
				#0000000000000#
				#0#0#0#0#0#0#0#
				#0000000000000#
				#0#0#0#0#0#0#0#
				#0000000000000#
				#0#0#0#0#0#0#0#
				#S00000000000S#
				###############
				
				où # est un mur, 0 est une case libre et S sont les points de spawn possible
				
			- texture (début): 
				Joueur1 est un block de couleur blanc 
				Joueur2 est un block de couleur noir
				
				Bombe est un block de couleur bleu foncé
				Explosion est un block de couleur rouge
				
				Case libre est un block de couleur vert	
				
				Obstacle est un block de couleur gris
				Brique est un block de couleur marron
				
				chaque block est de taille 10px*10px
			
			
	4.	Ajouter une interface pour le joueur humain.

