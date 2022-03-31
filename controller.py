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
    tours = input("Saisir le nombre de tours (4 par défaut) : ")
    joueurs = model.Acteurs.joueurs
    print("Saisir le temps pour chaque round :")
    print("[1] Bullet    [2] Blitz    [3] Rapide")
    timer = input()
    description = input("Saisir la description (facultatif) : ")
    model.Acteurs.tournois.append(model.Tournoi(nom, lieu, date, joueurs, timer, description, tours))


def showPlayers(ordre):

    match ordre:

        case "1":
            joueurs = sorted(model.Acteurs.joueurs, key=lambda Player: Player.nom)
            for joueur in joueurs:
                print(joueur.__dict__)

        case "2":
            joueurs = sorted(model.Acteurs.joueurs, key=lambda Player: int(Player.classement))
            for joueur in joueurs:
                print("    ".join(joueur.__dict__.values()))


def showTournoi():
    for tournoi in model.Acteurs.tournois:
        print(tournoi.__dict__)


def showTours():
    pass
