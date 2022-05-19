import uuid
from Controller import tournoi
from Model import model


def player_input():
    """Demande à l'utilisateur les données de l'instance Joueur"""
    nom = input("\nSaisir le nom de famille du joueur : \n")
    prenom = input("\nSaisir le prénom du joueur : \n")
    date = input("\nSaisir la date de naissance du joueur : \n")

    while True:
        try:
            classement = int(input("\nSaisir le classement du joueur : \n"))
            break
        except ValueError:
            print("Merci de saisir un nombre entier")

    # Attribue un identifiant unique au joueur
    id = str(uuid.uuid4())

    return nom, prenom, date, classement, id


def tournoi_input():
    """Demande à l'utilisateur les données de l'instance Tournoi"""

    nom = input("Saisir le nom du tournoi : \n")
    lieu = input("Saisir le lieu du tournoi : \n")
    date = input("Saisir la date du tournoi : \n")
    # Demande 8 joueurs
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
    """Demande à l'utilisateur s'il souhaite terminer le tour"""
    match input():

        case "1":
            score_table = tournoi.end_tour(tour, score_table)

        case _:
            pass


def last_tournois():
    """Affiche les 5 derniers tournois créés pour faciliter l'accès"""
    tournois = model.Acteurs.tournois
    print()

    for index in range(5):
        if index == len(tournois):
            break
        print("[" + str(index + 1) + "] " + tournois[-index - 1].__str__())

    print("\n[6] Un autre")

    reponse = input()
    match reponse:

        case "1" | "2" | "3" | "4" | "5":
            return tournois[-int(reponse)]

        # Propose à l'utilisateur de chercher un autre tournoi
        case "6":
            tournament = tournoi.search_tournoi()
            return tournament

        case _:
            print("\nCommande non reconnue\n")
            last_tournois(tournois)


def set_score(match, joueur1, joueur2):
    """Demande à l'utilisateur qui a gagné un Match"""
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
    """Demande à l'utilisateur le nom et prénom du joueur qu'il recherche"""

    print("\nSaisir le nom du joueur à ajouter :")
    nom = input().lower()
    print("\nSaisir le prénom du joueur à ajouter :")
    prenom = input().lower()

    return nom, prenom


def want_add():
    """Demande à l'utilisateur s'il souhaite créer un Joueur"""

    print("\nCe joueur n'existe pas, voulez-vous l'ajouter ?")
    print("[1] Oui")
    print("[2] Non\n")
    reponse_ajout = input()

    return reponse_ajout


def modify_player(player):
    """Demande quel attribut d'un joueur il souhaite modifier"""
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
