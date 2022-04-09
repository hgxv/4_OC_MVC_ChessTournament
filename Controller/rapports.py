from Model.model import Acteurs
from tabulate import tabulate

def showPlayers(ordre):
    
    match ordre:

        case "1":
            joueurs = sorted(Acteurs.joueurs, key=lambda Player: Player.__str__())
            

        case "2":
            joueurs = sorted(Acteurs.joueurs, key=lambda Player: int(Player.classement))

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


def showTournoi():
    for tournoi in Acteurs.tournois:
        print(tournoi.__str__())


def showTours():
    pass
