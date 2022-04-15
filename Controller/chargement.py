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
    "id": player.id
}
    return serialized_player


def serialize_match(match):

    serialized_match = {
    "joueur1": match.joueur1,
    "joueur2": match.joueur2,
}
    return serialized_match


def serialize_tour(tour, players_id):
    serialized_matchs = []
    for match in tour.liste_matchs:
        serialized_matchs.append(serialize_match(match))

    serialized_tour = {
    "nom": tour.nom,
    "players": players_id,
    "liste_matchs": serialized_matchs,
    "already_played": tour.already_played
}
    return serialized_tour


def serialize_tournoi(tournoi):
    players_id = []
    for player in tournoi.players:
        players_id.append(player.id)

    serialized_tours = []
    for tour in tournoi.liste_tours:
        serialized_tours.append(serialize_tour(tour, players_id))

    serialized_tournoi = {
    "nom": tournoi.nom,
    "lieu": tournoi.lieu,
    "date": tournoi.date,
    "players": players_id,
    "timer": tournoi.timer,
    "description": tournoi.description,
    "nombre_tours": tournoi.nombre_tours,
    "liste_tours":  serialized_tours,
    "tour_actuel": tournoi.tour_actuel
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
    players = []
    for player in tournoi["players"]:
        players.append(model.Player.find_by_id(player))

    liste_tours = []
    for tour in tournoi["liste_tours"]:
        liste_tours.append(deserialize_tour(tour, players))

    nom = tournoi["nom"]
    lieu = tournoi["lieu"]
    date = tournoi["date"]
    timer = tournoi["timer"]
    nombre_tours = tournoi["nombre_tours"]
    description = tournoi["description"]

    tournament = model.Tournoi(nom, lieu, date, players, timer, description, nombre_tours)
    model.Acteurs.tournois.append(tournament)


def deserialize_tour(tour, players):
    liste_matchs = []
    for match in tour["liste_matchs"]:
        liste_matchs.append(deserialize_match(match))

    nom = tour["nom"]
    already_played = tour["already_played"]

    tour = model.Tour(nom, players, already_played)
    tour.liste_matchs = liste_matchs
    return tour

    
def deserialize_match(match):
    joueur1 = match["joueur1"]
    joueur2 = match["joueur2"]
    
    return model.Match(joueur1, joueur2)

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