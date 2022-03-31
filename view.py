import model
import controller
import time


class Menu():

    def __init__(self):
        print("Veuillez choisir un menu :")
        print("")
        print("[1] Lancer un tournoi")
        print("[2] Ajouter un nouveau joueur")
        print("[3] Afficher la liste de...")


class MenuListes():
    def __init__(self):
        print("[1] Tous les acteurs")
        print("[2] Tous les joueurs d'un tournoi")
        print("[3] Tous les tournois")
        print("[4] Tous les tours d'un tournoi")
        print("[5] Tous les matchs d'un tournoi")


def run():
    while(True):

        print()
        Menu()
        reponse = input("")
        print()
        match reponse:
            case "1":
                controller.createTournoi()

            case "2":
                controller.addPlayer()

            case "3":
                MenuListes()
                reponse_list = input()
                match reponse_list:
                    case "1":
                        pass

                    case "2":
                        print("Afficher par ordre...")
                        print("[1] Alphabétique")
                        print("[2] Classement")
                        controller.showPlayers(input())

                    case "3":
                        controller.showTournoi()

                    case "4":
                        controller.showTours()

                    case "5":
                        pass

            case "4":
                for tournoi in model.Acteurs.tournois:
                    tournoi.runTournoi()
                    print(tournoi.nom)
                    print(tournoi.liste_tours)
                    print()

        time.sleep(1)
