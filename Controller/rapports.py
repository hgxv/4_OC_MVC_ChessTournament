from Model.model import Acteurs
from tabulate import tabulate

def showPlayers(what, ordre):
    
    match what:
        case "all":
            joueurs = Acteurs.joueurs

        case tournoi:
            joueurs = tournoi.players

    match ordre:

        case "1":
            joueurs.sort(key=lambda Player: Player.__str__())
            print("Ordre alphabétique :\n")
            

        case "2":
            joueurs.sort(key=lambda Player: int(Player.classement))
            print("Par classement :\n")

        case _:
            return print("\nCommande non reconnue\n")
    
    noms = []
    prenoms = []
    dates = []
    classements = []

    for joueur in joueurs:
        noms.append(joueur.nom)
        prenoms.append(joueur.prenom)
        dates.append(joueur.date)
        classements.append(joueur.classement)
    
    table = [noms, prenoms, dates, classements]

    print(tabulate({
        "Noms" : noms,
        "Prenoms" : prenoms,
        "Date de naissance" : dates,
        "Classement" : classements
    }, headers="keys"))


def showTournois():

    noms = []
    lieux = []
    dates = []
    timers = []
    nombre_tours = []
    descriptions = []

    table = [noms, lieux, dates, timers, nombre_tours, descriptions]

    for tournoi in Acteurs.tournois:
        noms.append(tournoi.nom)
        lieux.append(tournoi.lieu)
        dates.append(tournoi.date)
        timers.append(tournoi.timer)
        nombre_tours.append(tournoi.nombre_tours)
        descriptions.append(tournoi.description)

    print(tabulate({
        "Nom" : noms,
        "Lieu" : lieux,
        "Date" : dates,
        "Timer" : timers,
        "Nombre de tours" : nombre_tours,
        "Description" : descriptions
    }, headers="keys"))


def showTours(tournoi):
    pass

