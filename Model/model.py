from collections import defaultdict


class Acteurs:

    joueurs = []
    tournois = []


class Tournoi:
    def __init__(
        self,
        nom,
        lieu,
        date,
        players,
        timer,
        description,
        tour_actuel,
        score_table,
        already_played,
        nombre_tours=4,
    ):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_tours = nombre_tours
        self.players = players
        self.description = description
        self.tour_actuel = tour_actuel
        self.liste_tours = []
        self.score_table = score_table
        self.already_played = already_played
        match timer:
            case "1":
                self.timer = "Bullet"

            case "2":
                self.timer = "Blitz"

            case "3":
                self.timer = "Rapid"

            case "Bullet" | "Blitz" | "Rapid":
                self.timer = timer

    def __str__(self):
        return self.nom + ", " + self.date + ", " + self.lieu


class Player:
    id_list = defaultdict(list)

    def __init__(self, nom, prenom, date, classement, id):
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.classement = classement
        self.id = id
        Player.id_list[self.id].append(self)

    @classmethod
    def find_by_id(cls, id):
        return Player.id_list[id][0]

    def __str__(self):
        return self.nom + " " + self.prenom


class Tour:
    def __init__(self, nom, players):
        self.nom = nom
        self.players = players
        self.liste_matchs = []


class Match:
    def __init__(self, joueur1, joueur2, score1, score2):
        self.joueur1 = [joueur1, score1]
        self.joueur2 = [joueur2, score2]
        self.result = (self.joueur1, self.joueur2)

    def __str__(self):
        player1 = Player.find_by_id(self.joueur1[0])
        player2 = Player.find_by_id(self.joueur2[0])
        return player1.__str__() + " vs " + player2.__str__()

    def show_score(cls):
        return " (" + str(cls.joueur1[1]) + "-" + str(cls.joueur2[1]) + ")"
