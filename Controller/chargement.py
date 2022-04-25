from datetime import date
from tinydb import TinyDB
from Model import model


db = TinyDB("db.json")
players_table = db.table("players")
tournois_table = db.table("tournois")


def serialize_player(player):
    serialized_player = {
        "nom": player.nom,
        "prenom": player.prenom,
        "date": player.date,
        "classement": player.classement,
        "id": player.id,
    }
    return serialized_player


def serialize_match(match):

    serialized_match = {
        "joueur1": match.joueur1,
        "joueur2": match.joueur2,
    }
    return serialized_match


def serialize_tour(tour):
    serialized_matchs = []
    for match in tour.liste_matchs:
        serialized_matchs.append(serialize_match(match))

    serialized_tour = {
        "nom": tour.nom,
        "players": tour.players,
        "liste_matchs": serialized_matchs,
        "heure_debut": tour.heure_debut,
    }
    if tour.heure_fin is not None:
        serialized_tour["heure_fin"] = tour.heure_fin
    return serialized_tour


def serialize_tournoi(tournoi):
    serialized_tours = []
    for tour in tournoi.liste_tours:
        serialized_tours.append(serialize_tour(tour))

    serialized_tournoi = {
        "nom": tournoi.nom,
        "lieu": tournoi.lieu,
        "date": tournoi.date,
        "players": tournoi.players,
        "timer": tournoi.timer,
        "description": tournoi.description,
        "nombre_tours": tournoi.nombre_tours,
        "liste_tours": serialized_tours,
        "tour_actuel": tournoi.tour_actuel,
        "score_table": tournoi.score_table,
        "already_played": tournoi.already_played,
    }
    return serialized_tournoi


def deserialize_player(player):
    nom = player["nom"]
    prenom = player["prenom"]
    date = player["date"]
    classement = player["classement"]
    id = player["id"]
    model.Acteurs.joueurs.append(model.Player(nom, prenom, date, classement, id))


def deserialize_tournoi(tournoi):
    players = tournoi["players"]

    liste_tours = []
    for tour in tournoi["liste_tours"]:
        liste_tours.append(deserialize_tour(tour))

    nom = tournoi["nom"]
    lieu = tournoi["lieu"]
    date = tournoi["date"]
    timer = tournoi["timer"]
    nombre_tours = tournoi["nombre_tours"]
    description = tournoi["description"]
    tour_actuel = tournoi["tour_actuel"]
    score_table = tournoi["score_table"]
    already_played = tournoi["already_played"]
    tournament = model.Tournoi(
        nom,
        lieu,
        date,
        players,
        timer,
        description,
        tour_actuel,
        score_table,
        already_played,
        nombre_tours,
    )
    model.Acteurs.tournois.append(tournament)
    tournament.liste_tours = liste_tours
    return tournament


def deserialize_tour(tour):
    liste_matchs = []
    for match in tour["liste_matchs"]:
        liste_matchs.append(deserialize_match(match))

    nom = tour["nom"]
    players = tour["players"]
    heure_debut = tour["heure_debut"]
    heure_fin = tour["heure_fin"]

    tour = model.Tour(nom, players)
    tour.liste_matchs = liste_matchs
    tour.heure_debut = heure_debut
    tour.heure_fin = heure_fin

    return tour


def deserialize_match(match):
    joueur1 = match["joueur1"][0]
    joueur2 = match["joueur2"][0]
    score1 = match["joueur1"][1]
    score2 = match["joueur2"][1]

    match = model.Match(joueur1, joueur2, score1, score2)

    return match


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
