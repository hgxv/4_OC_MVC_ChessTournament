from datetime import date
from tinydb import TinyDB
from Model import model


db = TinyDB("db.json")
players_table = db.table("players")
tournois_table = db.table("tournois")


def serialize_player(player):
    serialized_player = {
        "nom" : player.nom,
        "prenom" : player.prenom,
        "date" : player.date,
        "classement" : player.classement
    }
    return serialized_player


def serialize_match(match):
    serialized_match = {
        "joueur1" : match.joueur1,
        "joueur2" : match.joueur2,
        "result" : match.result
    }
    return serialized_match


def serialize_tour(tour, players):
    serialized_matchs = []
    for match in tour.liste_match:
        serialized_matchs.append(serialize_match(match))

    serialized_tour = {
        "name" : tour.name,
        "players" : players,
        "liste_match" : serialized_matchs,
        "already_played" : tour.already_played
    }
    return serialized_tour


def serialize_tournoi(tournoi):
    serialized_players = []
    for player in tournoi.players:
        serialized_players.append(serialize_player(player))

    serialized_tours = []
    for tour in tournoi.liste_tours:
        serialized_tours.append(serialize_tour(tour), serialized_players)

    serialized_tournoi = {
        "nom" : tournoi.nom,
        "lieu" : tournoi.lieu,
        "date" : tournoi.date,
        "players" : serialized_players,
        "timer" : tournoi.timer,
        "description" : tournoi.description,
        "nombre_tours" : tournoi.nombre_tours,
        "liste_tours" :  serialized_tours
    }
    return serialized_tournoi


def deserialize_player(player):
    nom = player["nom"]
    prenom = player["prenom"]
    date = player["date"]
    classement = player["classement"]
    model.Acteurs.joueurs.append(model.Player(nom, prenom, date, classement))


def deserialize_tournoi(tournoi):
    players = []
    for player in tournoi["players"]:
        players.append(deserialize_player(player))

    liste_tours = []
    for tour in tournoi["liste_tours"]:
        liste_tours.append(deserialize_tour(tour, players))

    nom = tournoi["nom"]
    lieu = tournoi["lieu"]
    date = tournoi["date"]
    timer = tournoi["timer"]
    nombre_tours = tournoi["nombre_tours"]
    description = tournoi["description"]

    model.Tournoi(nom, lieu, date, players, timer, description, nombre_tours)


def deserialize_tour(tour, players):
    liste_matchs = []
    for match in tour["liste_matchs"]:
        liste_matchs.append(deserialize_match(match))

    nom = tour["nom"]
    already_played = tour["already_played"]

    return model.Tour(nom, players, liste_matchs, already_played)

    
def deserialize_match(match):
    joueur1 = match["joueur1"]
    joueur2 = match["joueur2"]
    result = match["result"]


def charge_data():
    serialized_players = players_table.all()
    serialized_tournois = tournois_table.all()

    for player in serialized_players:
        deserialize_player(player)
        

    for tournoi in serialized_tournois:
        deserialize_tournoi(tournoi)
       


def save_data():
    players_table.truncate()
    tournois_table.truncate()

    for player in model.Acteurs.joueurs:
        players_table.insert(serialize_player(player))

    for tournoi in model.Acteurs.tournois:
        tournois_table.insert(serialize_tournoi(tournoi))