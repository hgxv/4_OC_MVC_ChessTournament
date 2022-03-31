import time
import controller

class Acteurs():

    joueurs = []
    tournois = []

    def __init__(self):
        pass   


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
        self.tableau_scores = []
        for player in players:
            self.tableau_scores.append([player, 0])

    
    def __str__(self):
        return self.nom + " " + self.date + " " + self.lieu


    def run(cls):
        
        for index, tours in enumerate(range(cls.nombre_tours)):
            nom_tour = "Round " + str(index + 1)
            sorted
            if index == 0:
                sorted_players = sorted(cls.players, key=lambda Player: int(Player.classement))
            tour = Tour(nom_tour, sorted_players)
            cls.liste_tours.append(tour)
            tour.run()
            sorted_players = tour.end(cls.tableau_scores)


class Player():

    def __init__(self, nom, prenom, date, classement):
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.classement = classement
    
    def __str__(self):
        return self.nom + " " + self.prenom


class Tour():

    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.liste_match = []


    def run(cls):
        print(cls.name)
        cls.heure_debut = time.strftime("%H:%M", time.localtime())
        nombre_joueurs = int(len(cls.players) / 2)
        
        for index, match in enumerate(range(nombre_joueurs)):
            cls.liste_match.append(Match(cls.players[index], cls.players[index + nombre_joueurs]))
        
        for match in cls.liste_match:
            print(match.__str__())

    def end(cls, tableau_scores):
        cls.heure_fin = time.strftime("%H:%M", time.localtime())
        for match in cls.liste_match:
            controller.endTurn(match)
        controller.setScore(cls.liste_match, tableau_scores)

        return sorted(tableau_scores, key=lambda score: score[1], reverse=True)


class Match():

    def __init__(self, joueur1, joueur2):
        self.joueur1 = [joueur1, 0]
        self.joueur2 = [joueur2, 0]
        self.result = (self.joueur1, self.joueur2)

    def __str__(self):
        return self.joueur1[0].__str__() + " vs " + self.joueur2[0].__str__()
