import time
import controller

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


    def run(cls):
        """Fonction de début de tournoi, prépare un tableau des scores et lance les tours"""

#       Prépare le tableau des scores
        sorted_players = sorted(cls.players, key=lambda Player: int(Player.classement))
        score_table = []
        for player in sorted_players:
            score_table.append([player, 0])

#       Prépare le dictionnaire des joueurs déjà affrontés
        already_played = {}
        for player in sorted_players:
            already_played[player] = []
        
#       Lance les tours
        for index, tours in enumerate(range(cls.nombre_tours)):

#           Met à jour le tableau des scores à partir du second tour
            if index >= 1:
                for number, player in enumerate(score_table):
                    sorted_players[number] = player[0]

            nom_tour = "Round " + str(index + 1)
            tour = Tour(nom_tour, sorted_players, already_played)
            cls.liste_tours.append(tour)
            tour.run()
            score_table = tour.end(score_table)

#           Print le tableau des scores
            for joueur in score_table:
                print(joueur[0].__str__() + " : " + str(joueur[1]))


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


    def run(cls):
        """Fonction de début de tour, lance les matchs"""
        print("\n" + cls.name + " :\n")
#       Assignation de l'heure de début        
        cls.heure_debut = time.strftime("%H:%M", time.localtime())
        nombre_tours = int(len(cls.players) / 2)
        copy_players = cls.players.copy()

#       Créer les matchs
        for match in range(nombre_tours):
            if cls.name == "Round 1":
                cls.liste_match.append(Match(cls.players[match], cls.players[match + nombre_tours]))
#               On ajoute les joueurs affrontés dans le dictionnaire du joueur
                cls.already_played[cls.players[match]].append(cls.players[match + nombre_tours])
                cls.already_played[cls.players[match + nombre_tours]].append(cls.players[match])
            else:
#######         Vérifier si deux joueurs se sont déjà affronté avant de créer le match
                joueur1 = copy_players.pop(0)
                for index, player in enumerate(copy_players):
                    if player not in cls.already_played[joueur1]:
                        joueur2 = copy_players.pop(index)
                        break

                cls.liste_match.append(Match(joueur1, joueur2))
#               On ajoute les joueurs affrontés dans le dictionnaire du joueur
                cls.already_played[joueur1].append(joueur2)
                cls.already_played[joueur2].append(joueur1)
                
#       Impression des matchs
        controller.showMatchs(cls.liste_match)


    def end(cls, tableau_scores):
        """Fonction de fin de tour, met à jour le tableau des scores"""

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
