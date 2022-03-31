class Tournoi():

    def __init__(self, nom, lieu, date, players, timer, description, nombre_tours=4):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nombre_tours = nombre_tours
        self.players = players
        self.timer = timer
        self.description = description
        self.liste_tours = []

    @classmethod
    def runTournoi(cls):
        sorted_players = sorted(cls.players, key=lambda Player: Player.classement)
        for tours in range(int(cls.nombre_tours)):
            nom_tour = "Round " + str(len(cls.liste_tours))
            cls.liste_tours.append(Tour(nom_tour, sorted_players))


class Player():

    def __init__(self, nom, prenom, date, classement):
        self.nom = nom
        self.prenom = prenom
        self.date = date
        self.classement = classement


class Tour():

    def __init__(self, name, players):
        self.liste_matchs = []
        self.name = name
        self.players = players

    def runTour(cls):
        for match in range(len(cls.players / 2)):
            pass


class Match():

    def __init__(self):
        pass


class Acteurs():

    joueurs = []
    tournois = []

    def __init__(self):
        pass
