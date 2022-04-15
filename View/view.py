from Controller import rapports
from Controller import chargement
from Controller import tournoi
from Model import model
import time

def Menu():
    print("Veuillez choisir un menu :")
    print("")
    print("[1] Menu des tournoi")
    print("[2] Ajouter un nouveau joueur")
    print("[3] Afficher la liste de...")
    print("[4] Sauvegarder")
    print("[5] Quitter")


def MenuListes():
    print("[1] Tous les joueurs")
    print("[2] Tous les joueurs d'un tournoi")
    print("[3] Tous les tournois")
    print("[4] Tous les tours d'un tournoi")
    print("[5] Tous les matchs d'un tournoi")


def MenuTournoi():
    print("[1] Créer un tournoi")
    print("[2] Reprendre un tournoi")


def run():
    while(True):

        print()
        Menu()
        print()
        reponse = input("")
        print()
        match reponse:
            case "0":
                print(model.Player.id_list)
                
            case "1":
                MenuTournoi()
                reponse_tournoi = input()

                match reponse_tournoi:
                    
                    case "1":
                        tournament = tournoi.createTournoi()
                        print("Voulez vous lancer le tournoi maintenant ?\n")
                        print("[1] Oui")
                        print("[2] Non")
                        reponse_start_tournoi = input()

                        match reponse_start_tournoi:

                            case "1":
                                tournoi.run_tournoi(tournament)

                            case "2":
                                pass


                    case "2":
                        pass

            case "2":
                tournoi.addPlayer()

            case "3":
                MenuListes()
                reponse_list = input()
                match reponse_list:
                    case "1":
                        print("Afficher par ordre...")
                        print("[1] Alphabétique")
                        print("[2] Classement")
                        rapports.showPlayers("all", input())
                        

                    case "2":
#                        tournoi =
                        rapports.showPlayers(tournoi, input())

                    case "3":
                        rapports.showTournois()

                    case "4":
                        rapports.showTours()
                        
                    case "5":
                        pass
            
            case "4":
                chargement.save_data()
                print("\nDonnées sauvegardées\n")

            case "5":
                quit()

            case _:
                print("\nCommande non reconnue\n")

        time.sleep(1)
