from Model import model
from Controller import chargement
from View import view
import time
import uuid


def add_player():
    nom = input("Saisir le nom de famille du joueur : ")
    prenom = input("Saisir le prénom du joueur : ")
    date = input("Saisir la date de naissance du joueur : ")
    classement = input("Saisir le classement du joueur : ")
    id = str(uuid.uuid4())
    joueur = model.Player(nom, prenom, date, classement, id)
    model.Acteurs.joueurs.append(joueur)
    chargement.players_table.insert(chargement.serialize_player(joueur))


def create_tournoi():
    nom = input("Saisir le nom du tournoi : ")
    lieu = input("Saisir le lieu du tournoi : ")
    date = input("Saisir la date du tournoi : ")
    nombre_tours = int(input("Saisir le nombre de tours (4 par défaut) : "))
    print("Saisir le temps pour chaque round :")
    print("[1] Bullet    [2] Blitz    [3] Rapide")
    timer = input()
    description = input("Saisir la description (facultatif) : ")

    players = []
    while len(players) < 8:
        joueur = search_player()
        if joueur is not False:
            if joueur in players:
                print("Ce joueur est déjà inscrit dans le tournoi")
            else:
                players.append(joueur)
                print("\nJoueur ajouté !\n")
    sorted(players, key=lambda Player: int(Player.classement))

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
        nom_tour = "Round " + str(tournoi.tour_actuel)
        tour = model.Tour(nom_tour, tournoi.players)
        tournoi.liste_tours.append(tour)
        print(tournoi.liste_tours)
        run_tour(tour, tournoi.already_played, tournoi.nombre_tours)
        tournoi.score_table = end_tour(tour, tournoi.score_table)

        #   Print le tableau des scores
        for joueur in tournoi.score_table:
            print(model.Player.find_by_id(joueur[0]).__str__() + " : " + str(joueur[1]))

        tournoi.tour_actuel += 1

        if tournoi.tour_actuel > tournoi.nombre_tours:
            tournoi.tour_actuel = "Terminé"

    else:
        print("Ce tournoi est terminé")


def reprendre_tournoi():
    """Cette fonction permet de reprendre un tournoi là où il en était"""

    tournois = model.Acteurs.tournois

    for index in range(5):
        if index == len(tournois):
            break
        print("[" + str(index + 1) + "] " + tournois[index].__str__())

    print("\n[6] Un autre")
    reponse = input()
    match reponse:

        case "1" | "2" | "3" | "4" | "5":
            run_tournoi(tournois[int(reponse) - 1])

        case "6":
            tournoi = search_tournoi()
            reprendre_tournoi(tournoi)

        case _:
            print("\nCommande non reconnue\n")


def run_tour(tour, already_played, nombre_tours):
    """Fonction de début de tour, lance les matchs"""
    print("\n" + tour.nom + " :\n")
    #   Assignation de l'heure de début
    tour.heure_debut = time.strftime("%H:%M", time.localtime())
    copy_players = tour.players.copy()

    #   Créer les matchs
    for match in range(int(len(tour.players) / 2)):
        if tour.nom == "Round 1":
            tour.liste_matchs.append(
                model.Match(
                    tour.players[match], tour.players[match + nombre_tours], 0, 0
                )
            )
            # On ajoute les joueurs affrontés dans le dictionnaire du joueur
            already_played[tour.players[match]].append(
                tour.players[match + nombre_tours]
            )
            already_played[tour.players[match + nombre_tours]].append(
                tour.players[match]
            )
        else:
            # Vérifier si deux joueurs se sont déjà affronté avant de créer le match
            joueur1 = copy_players.pop(0)
            for index, player in enumerate(copy_players):
                if player not in already_played[joueur1]:
                    joueur2 = copy_players.pop(index)
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
        print("\nQui a gagné le match ?\n")
        print("[1] " + model.Player.find_by_id(match.joueur1[0]).__str__())
        print("[2] " + model.Player.find_by_id(match.joueur2[0]).__str__())
        print("[3] Match nul")
        reponse = input()

        match reponse:

            case "1":
                match.joueur1[1] += 1

            case "2":
                match.joueur2[1] += 1

            case "3":
                match.joueur1[1] += 0.5
                match.joueur2[1] += 0.5

            case _:
                print("\ncommande non reconnue\n")

    set_scores(tour.liste_matchs, score_table)

    return sorted(score_table, key=lambda score: score[1], reverse=True)


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
    print("\nSaisir le nom du joueur à ajouter :")
    nom = input().lower()
    print("\nSaisir le prénom du joueur à ajouter :")
    prenom = input().lower()
    found = False
    for joueur in model.Acteurs.joueurs:
        if to_norme(nom) == to_norme(joueur.nom.lower()):
            if to_norme(prenom) == to_norme(joueur.prenom.lower()):
                return joueur
    if found == False:
        print("Ce joueur n'existe pas, voulez-vous l'ajouter ?")
        print("[1] Oui")
        print("[2] Non")
        reponse_ajout = input()
        match reponse_ajout:

            case "1":
                add_player()

            case _:
                return False


def search_tournoi():
    print("\nSaisir le nom du tournoi :")
    nom = input().lower()
    for tournoi in model.Acteurs.tournois:
        if to_norme(tournoi.nom) == to_norme(nom):
            return tournoi
    print("\nCe tournoi n'existe pas.")
