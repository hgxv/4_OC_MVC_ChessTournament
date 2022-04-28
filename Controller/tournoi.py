from Model import model
from Controller import chargement
from View import inputs
import time


def create_tournoi():

    nom, lieu, date, nombre_tours, timer, description = inputs.tournoi_input()

    players = []
    while len(players) < 8:
        joueur = search_player()
        if joueur is not False:
            if joueur in players:
                print("\nCe joueur est déjà inscrit dans le tournoi\n")
            else:
                players.append(joueur)
                print("\nJoueur ajouté !\n")

    players.sort(key=lambda Player: int(Player.classement))

    players_id = []
    for player in players:
        players_id.append(player.id)

    score_table = []
    for player in players:
        score_table.append([player.id, 0])

    #   Prépare le dictionnaire des joueurs déjà affrontés
    already_played = {}
    for player in players_id:
        already_played[player] = []

    tour_actuel = 1
    tournoi = model.Tournoi(
        nom,
        lieu,
        date,
        players_id,
        timer,
        description,
        tour_actuel,
        score_table,
        already_played,
        nombre_tours,
    )

    model.Acteurs.tournois.append(tournoi)
    chargement.tournois_table.insert(chargement.serialize_tournoi(tournoi))
    return tournoi


def run_tournoi(tournoi):
    """Fonction de début de tournoi, prépare un tableau des scores et lance les tours"""

    if tournoi.tour_actuel != "Terminé":
        if len(tournoi.liste_tours) > 0:
            last_tour = tournoi.liste_tours[-1]
            if hasattr(last_tour, "heure_fin") is False:
                tournoi.score_table = end_tour(last_tour, tournoi.score_table)
                time.sleep(1)

        nom_tour = "Round " + str(tournoi.tour_actuel)
        tour = model.Tour(nom_tour, tournoi.players)
        tournoi.liste_tours.append(tour)
        run_tour(tour, tournoi.already_played, tournoi.score_table)

        time.sleep(1)

        print("\nLe tour est-il terminé ?")
        print("\n[1] Oui")
        print("[2] Non\n")

        inputs.is_turn_finished(tour, tournoi.score_table)

        tournoi.tour_actuel += 1

        if tournoi.tour_actuel > tournoi.nombre_tours:
            tournoi.tour_actuel = "Terminé"

    else:
        print("\nCe tournoi est terminé\n")


def reprendre_tournoi():
    """Cette fonction permet de reprendre un tournoi là où il en était"""

    tournois = model.Acteurs.tournois

    # Affiche la liste des 5 derniers tournois pour un accès plus rapide
    print()

    for index in range(5):
        if index == len(tournois):
            break
        print("[" + str(index + 1) + "] " + tournois[index].__str__())

    print("\n[6] Un autre")

    inputs.reprise_tournoi(tournois)


def run_tour(tour, already_played, score_table):
    """Fonction de début de tour, lance les matchs"""
    print("\n" + tour.nom + " :\n")
    #   Assignation de l'heure de début
    if hasattr(tour, "heure_debut") is False:
        tour.heure_debut = time.strftime("%H:%M", time.localtime())

    players = []
    for player in score_table:
        players.append(player[0])

    #   Créer les matchs
    nombre_matchs = int(len(tour.players) / 2)
    for match in range(nombre_matchs):
        if tour.nom == "Round 1":
            tour.liste_matchs.append(
                model.Match(
                    tour.players[match], tour.players[nombre_matchs + match], 0, 0
                )
            )
            # On ajoute les joueurs affrontés dans le dictionnaire du joueur
            already_played[tour.players[match]].append(
                tour.players[nombre_matchs + match]
            )
            already_played[tour.players[nombre_matchs + match]].append(
                tour.players[match]
            )
        else:
            # Vérifier si deux joueurs se sont déjà affronté avant de créer le match
            joueur1 = players.pop(0)
            for index, player in enumerate(players):
                if player not in already_played[joueur1]:
                    joueur2 = players.pop(index)
                    break

            tour.liste_matchs.append(model.Match(joueur1, joueur2, 0, 0))
            # On ajoute les joueurs affrontés dans le dictionnaire du joueur
            already_played[joueur1].append(joueur2)
            already_played[joueur2].append(joueur1)

    # Impression des matchs
    show_matchs(tour.liste_matchs)


def end_tour(tour, score_table):
    """Fonction de fin de tour, met à jour le tableau des scores"""

    tour.heure_fin = time.strftime("%H:%M", time.localtime())

    for match in tour.liste_matchs:
        joueur1 = model.Player.find_by_id(match.joueur1[0]).__str__()
        joueur2 = model.Player.find_by_id(match.joueur2[0]).__str__()
        inputs.set_score(match, joueur1, joueur2)

    set_scores(tour.liste_matchs, score_table)

    score_table.sort(key=lambda score: score[1], reverse=True)

    #   Print le tableau des scores
    print()
    for joueur in score_table:
        print(model.Player.find_by_id(joueur[0]).__str__() + " : " + str(joueur[1]))

    return score_table


def show_matchs(liste_matchs):
    for match in liste_matchs:
        print(match.__str__())
    print("\n")


def set_scores(matchs, score_table):
    for match in matchs:
        for joueur in score_table:
            if match.result[0][0] == joueur[0]:
                joueur[1] += match.result[0][1]
            if match.result[1][0] == joueur[0]:
                joueur[1] += match.result[1][1]


def to_norme(string):
    table = string.maketrans("âàäçéèêëîïùû", "aaaceeeeiiuu")
    return string.translate(table)


def search_player():

    nom, prenom = inputs.search_player_input()
    found = False

    for joueur in model.Acteurs.joueurs:
        if to_norme(nom) == to_norme(joueur.nom.lower()):
            if to_norme(prenom) == to_norme(joueur.prenom.lower()):
                return joueur

    if found is False:
        reponse_ajout = inputs.want_add()
        match reponse_ajout:

            case "1":
                add_player()

            case _:
                return False


def search_tournoi():
    nom = inputs.nom_tournoi()
    found = False

    for tournoi in model.Acteurs.tournois:
        if to_norme(tournoi.nom).lower() == to_norme(nom):
            return tournoi

    if found is False:
        print("\nCe tournoi n'existe pas.")
        search_tournoi()


def add_player():
    nom, prenom, date, classement, id = inputs.player_input()
    joueur = model.Player(nom, prenom, date, classement, id)
    model.Acteurs.joueurs.append(joueur)
    chargement.players_table.insert(chargement.serialize_player(joueur))
