import uuid
from Controller import tournoi


def player_input():
    nom = input("\nSaisir le nom de famille du joueur : \n")
    prenom = input("\nSaisir le prénom du joueur : \n")
    date = input("\nSaisir la date de naissance du joueur : \n")

    while True:
        try:
            classement = int(input("\nSaisir le classement du joueur : \n"))
            break
        except ValueError:
            print("Merci de saisir un nombre entier")

    id = str(uuid.uuid4())

    return nom, prenom, date, classement, id


def tournoi_input():
    nom = input("Saisir le nom du tournoi : \n")
    lieu = input("Saisir le lieu du tournoi : \n")
    date = input("Saisir la date du tournoi : \n")
    while True:
        try:
            nombre_tours = int(input("Saisir le nombre de tours (4 par défaut) : \n"))
            if nombre_tours < 8:
                break

        except ValueError:
            print("Merci de saisir un nombre entier")

    print("Saisir le temps pour chaque round :\n")
    print("[1] Bullet    [2] Blitz    [3] Rapide")

    while True:
        timer = input()
        if timer in ("1", "2", "3"):
            break

    description = input("Saisir la description (facultatif) : \n")

    return nom, lieu, date, nombre_tours, timer, description


def is_turn_finished(tour, score_table):
    match input():

        case "1":
            score_table = tournoi.end_tour(tour, score_table)

        case _:
            pass


def reprise_tournoi(tournois):

    reponse = input()
    match reponse:

        case "1" | "2" | "3" | "4" | "5":
            tournoi.run_tournoi(tournois[int(reponse) - 1])

        case "6":
            tournament = tournoi.search_tournoi()
            tournoi.run_tournoi(tournament)

        case _:
            print("\nCommande non reconnue\n")


def set_score(match, joueur1, joueur2):
    print("\nQui a gagné le match ?\n")
    print("[1] " + joueur1)
    print("[2] " + joueur2)
    print("[3] Match nul\n")
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
            set_score(match, joueur1, joueur2)


def search_player_input():
    print("\nSaisir le nom du joueur à ajouter :")
    nom = input().lower()
    print("\nSaisir le prénom du joueur à ajouter :")
    prenom = input().lower()

    return nom, prenom


def want_add():
    print("\nCe joueur n'existe pas, voulez-vous l'ajouter ?")
    print("[1] Oui")
    print("[2] Non\n")
    reponse_ajout = input()

    return reponse_ajout


def modify_player(player):
    print("\nQue voulez vous modifier ?\n")
    print("[1] Nom de famille")
    print("[2] Prénom")
    print("[3] Date de naissance")
    print("[4] Classement\n")

    match input():

        case "1":
            player.nom = input("\nSaisir le nouveau nom de famille : \n")

        case "2":
            player.prenom = input("\nSaisir le nouveau prénom : \n")

        case "3":
            player.date = input("\nSaisir la nouvelle date de naissance : \n")

        case "4":
            player.classement = input("\nSaisir le nouveau classement : \n")

        case _:
            print("\nCommande non reconnue\n")
            modify_player(player)


def nom_tournoi():
    print("\nSaisir le nom du tournoi :")
    nom = input().lower()

    return nom
