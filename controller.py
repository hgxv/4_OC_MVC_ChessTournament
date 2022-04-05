from re import M
import model


def addPlayer():
    nom = input("Saisir le nom de famille du joueur : ")
    prenom = input("Saisir le prénom du joueur : ")
    date = input("Saisir la date de naissance du joueur : ")
    classement = input("Saisir le classement du joueur : ")
    model.Acteurs.joueurs.append(model.Player(nom, prenom, date, classement))


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
                
                case "2":
                    pass


    tournoi = model.Tournoi(nom, lieu, date, players, timer, description, tours)
    model.Acteurs.tournois.append(tournoi)
    return tournoi


def showPlayers(ordre):

    match ordre:

        case "1":
            joueurs = sorted(model.Acteurs.joueurs, key=lambda Player: Player.nom)
            for joueur in joueurs:
                print(joueur.__str__())

        case "2":
            joueurs = sorted(model.Acteurs.joueurs, key=lambda Player: int(Player.classement))
            for joueur in joueurs:
                print(joueur.__str__())


def showTournoi():
    for tournoi in model.Acteurs.tournois:
        print(tournoi.__str__())


def showTours():
    pass


def showMatchs(liste_match):
    for match in liste_match:
        print(match.__str__())
    print("\n")


def endTurn(match):
    print("\nQui a gagné le match ?\n")
    print("[1] " + match.joueur1[0].__str__())
    print("[2] " + match.joueur2[0].__str__())
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
