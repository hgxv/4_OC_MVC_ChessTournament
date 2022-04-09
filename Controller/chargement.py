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


def serialize_tour(tour):
    for player in tour.players:
        pass

    serialized_tour = {
        "name" : tour.name,
        "players" : tour.players,
        "liste_match" : tour.liste_match,
        "already_played" : tour.already_played
    }


def charge_data():
    serialized_players = players_table.all()
    for player in serialized_players:
        nom = player["nom"]
        prenom = player["prenom"]
        date = player["date"]
        classement = player["classement"]
        model.Acteurs.joueurs.append(model.Player(nom, prenom, date, classement))

def save_data():
    players_table.truncate()
    tournois_table.truncate()

    for player in model.Acteurs.joueurs:
        players_table.insert(serialize_player(player))