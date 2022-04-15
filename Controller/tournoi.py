from Model import model
from Controller import chargement
from View import view
import time
import uuid

def addPlayer():
    nom = input("Saisir le nom de famille du joueur : ")
    prenom = input("Saisir le prénom du joueur : ")
    date = input("Saisir la date de naissance du joueur : ")
    classement = input("Saisir le classement du joueur : ")
    id = str(uuid.uuid4())
    joueur = model.Player(nom, prenom, date, classement, id)
    model.Acteurs.joueurs.append(joueur)
    chargement.players_table.insert(chargement.serialize_player(joueur))


def createTournoi():
    nom = input("Saisir le nom du tournoi : ")
    lieu = input("Saisir le lieu du tournoi : ")
    date = input("Saisir la date du tournoi : ")
    tours = int(input("Saisir le nombre de tours (4 par défaut) : "))
    print("Saisir le temps pour chaque round :")
    print("[1] Bullet    [2] Blitz    [3] Rapide")
    timer = input()
    description = input("Saisir la description (facultatif) : ")

    players = []
    while len(players) < 8:
        print("Saisir les noms des joueurs à ajouter :")
        reponse = input()
        found = False
        for joueur in model.Acteurs.joueurs:
            if reponse.lower() == joueur.nom.lower():
                players.append(joueur)
                found = True
                break
        if found == False:
            print("Ce joueur n'existe pas, voulez-vous l'ajouter ?")
            print("[1] Oui")
            print("[2] Non")
            reponse_ajout = input()
            match reponse_ajout:

                case "1":
                    addPlayer()
                
                case _:
                    pass

    tournoi = model.Tournoi(nom, lieu, date, players, timer, description, tours)
    tournoi.tour_actuel = 1
    model.Acteurs.tournois.append(tournoi)
    return tournoi


def run_tournoi(tournoi):
    """Fonction de début de tournoi, prépare un tableau des scores et lance les tours"""

    model.Acteurs.last_tournoi = tournoi
#   Prépare le tableau des scores

    sorted_players = sorted(tournoi.players, key=lambda Player: int(Player.classement))        
    score_table = []
    
    for index, player in enumerate(sorted_players):
        sorted_players[index] = player.id
        score_table.append([player.id, 0])
#   Prépare le dictionnaire des joueurs déjà affrontés
    already_played = {}
    for player in sorted_players:
        already_played[player] = []
    

#   Met à jour le tableau des scores à partir du second tour
    if tournoi.tour_actuel >= 2:
        for number, player in enumerate(score_table):
            sorted_players[number] = player[0]

    nom_tour = "Round " + str(tournoi.tour_actuel)
    tour = model.Tour(nom_tour, sorted_players, already_played)
    tournoi.liste_tours.append(tour)
    run_tour(tour)
    tournoi.score_table = end_tour(tour, score_table)

#   Print le tableau des scores
    for joueur in score_table:
            print(model.Player.find_by_id(joueur[0])[0].__str__() + " : " + str(joueur[1]))

    tournoi.tour_actuel += 1


def run_tour(tour):
    """Fonction de début de tour, lance les matchs"""
    print("\n" + tour.nom + " :\n")
#       Assignation de l'heure de début        
    tour.heure_debut = time.strftime("%H:%M", time.localtime())
    nombre_tours = int(len(tour.players) / 2)
    copy_players = tour.players.copy()

#       Créer les matchs
    for match in range(nombre_tours):
        if tour.nom == "Round 1":
            tour.liste_matchs.append(model.Match(tour.players[match], tour.players[match + nombre_tours]))
#               On ajoute les joueurs affrontés dans le dictionnaire du joueur
            tour.already_played[tour.players[match]].append(tour.players[match + nombre_tours])
            tour.already_played[tour.players[match + nombre_tours]].append(tour.players[match])
        else:
#######         Vérifier si deux joueurs se sont déjà affronté avant de créer le match
            joueur1 = copy_players.pop(0)
            for index, player in enumerate(copy_players):
                if player not in tour.already_played[joueur1]:
                    joueur2 = copy_players.pop(index)
                    break

            tour.liste_matchs.append(model.Match(joueur1, joueur2))
#               On ajoute les joueurs affrontés dans le dictionnaire du joueur
            tour.already_played[joueur1].append(joueur2)
            tour.already_played[joueur2].append(joueur1)
            
#       Impression des matchs
    showMatchs(tour.liste_matchs)


def end_tour(tour, score_table):
    """Fonction de fin de tour, met à jour le tableau des scores"""

    tour.heure_fin = time.strftime("%H:%M", time.localtime())
    for match in tour.liste_matchs:
        endTurn(match)
    setScore(tour.liste_matchs, score_table)

    return sorted(score_table, key=lambda score: score[1], reverse=True)


def showMatchs(liste_matchs):
    for match in liste_matchs:
        print(match.__str__())
    print("\n")


def endTurn(match):
    print("\nQui a gagné le match ?\n")
    print("[1] " + model.Player.find_by_id(match.joueur1[0])[0].__str__())
    print("[2] " + model.Player.find_by_id(match.joueur2[0])[0].__str__())
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


def setScore(matchs, score_table):
    for match in matchs:
        for joueur in score_table:
            pass
            if match.result[0][0] == joueur[0]:
                joueur[1] += match.result[0][1]
            if match.result[1][0] == joueur[0]:
                joueur[1] += match.result[1][1]


