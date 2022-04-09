import time


class Acteurs():

    joueurs = []
    tournois = []  


class Tournoi():

    def __init__(self, nom, lieu, date, players, timer, description, nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_tours = nombre_tours
        self.players = players
        self.description = description
        self.liste_tours = []
        match timer:
            case "1":
                self.timer = "Bullet"
            
            case "2":
                self.timer = "Blitz"

            case "3":
                self.timer = "Rapid"


    def __str__(self):
        return self.nom + " " + self.date + " " + self.lieu


class Player():

    def __init__(self, nom, prenom, date, classement):
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.classement = classement
    
    def __str__(self):
        return self.nom + " " + self.prenom


class Tour():

    def __init__(self, name, players, already_played):
        self.name = name
        self.players = players
        self.liste_match = []
        self.already_played = already_played


class Match():

    def __init__(self, joueur1, joueur2):
        self.joueur1 = [joueur1, 0]
        self.joueur2 = [joueur2, 0]
        self.result = (self.joueur1, self.joueur2)

    def __str__(self):
        return self.joueur1[0].__str__() + " vs " + self.joueur2[0].__str__()
