from Model.model import Acteurs
from Model.model import Player
from View import inputs
from tabulate import tabulate


def show_players(what, ordre):
    """Effectue le rapport des instances Joueurs"""
    match what:
        case "all":
            joueurs = Acteurs.joueurs

        case tournoi:
            joueurs = []
            for joueur in tournoi.players:
                joueurs.append(Player.find_by_id(joueur))

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

    print(
        tabulate(
            {
                "Noms": noms,
                "Prenoms": prenoms,
                "Date de naissance": dates,
                "Classement": classements,
            },
            headers="keys",
        )
    )
    print()


def showTournois():
    """EFfectue le rapport des instances Tournois"""
    noms = []
    lieux = []
    dates = []
    timers = []
    tours_actuel = []
    nombre_tours = []
    descriptions = []

    for tournament in Acteurs.tournois:
        noms.append(tournament.nom)
        lieux.append(tournament.lieu)
        dates.append(tournament.date)
        timers.append(tournament.timer)
        tours_actuel.append(tournament.tour_actuel)
        nombre_tours.append(tournament.nombre_tours)
        descriptions.append(tournament.description)

    print(
        tabulate(
            {
                "Nom": noms,
                "Lieu": lieux,
                "Date": dates,
                "Timer": timers,
                "Tour actuel": tours_actuel,
                "Nombre de tours": nombre_tours,
                "Description": descriptions,
            },
            headers="keys",
        )
    )
    print()


def showTours():
    """Effecture le rapport des instances Tours"""
    tournament = inputs.last_tournois()

    noms = []
    heure_debut = []
    heure_fin = []

    for tour in tournament.liste_tours:
        noms.append(tour.nom)
        heure_debut.append(tour.heure_debut)
        if hasattr(tour, "heure_fin") is True:
            heure_fin.append(tour.heure_fin)
        else:
            heure_fin.append("Pas terminé")

    print(
        tabulate(
            {"Nom": noms, "Heure de début": heure_debut, "Heure de fin": heure_fin},
            headers="keys",
        )
    )
    print()


def show_tournoi_matchs():
    """Affiche le tableau des scores quand l'utilisateur a fini de rentrer les scores"""
    tournament = inputs.last_tournois()
    for tour in tournament.liste_tours:
        print("\n" + tour.nom + " :\n")
        joueurs1 = []
        joueurs2 = []
        vs = []
        scores = []
        for match in tour.liste_matchs:
            joueurs1.append(Player.find_by_id(match.joueur1[0]).__str__())
            joueurs2.append(Player.find_by_id(match.joueur2[0]).__str__())
            vs.append("vs")
            scores.append(match.show_score())
        print(
            tabulate(
                {"Joueur 1": joueurs1, "Vs": vs, "Joueur 2": joueurs2, "Score": scores},
                headers="keys",
            )
        )
        print("\n\n")
