from Model import model
from View import view
from Controller import chargement


if __name__ == "__main__":

    model.Acteurs()
    chargement.charge_data()
    print("Bienvenue sur le logiciel du tournoi")
    view.run()
