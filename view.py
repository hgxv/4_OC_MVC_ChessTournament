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
        print("[4] Quitter")


class MenuListes():
    def __init__(self):
        print("[1] Tous les acteurs")
        print("[2] Tous les joueurs d'un tournoi")
        print("[3] Tous les tournois")
        print("[4] Tous les tours d'un tournoi")
        print("[5] Tous les matchs d'un tournoi")


class MenuTournoi():
    def __init__(self):
        print("[1] Créer un tournoi")
        print("[2] Lancer un tournoi")


def run():
    while(True):

        print()
        Menu()
        reponse = input("")
        print()
        match reponse:
            case "0":
                print()
                
            case "1":
                MenuTournoi()
                reponse_tournoi = input()

                match reponse_tournoi:
                    
                    case "1":
                        tournoi = controller.createTournoi()
                        print("Voulez vous lancer le tournoi maintenant ?\n")
                        print("[1] Oui")
                        print("[2] Non")
                        reponse_start_tournoi = input()

                        match reponse_start_tournoi:

                            case "1":
                                tournoi.run()

                            case "2":
                                pass


                    case "2":
                        pass

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
                quit()

            case "menu":
                pass
#           Enregistre où on en est et reviens au menu principal

        time.sleep(1)
