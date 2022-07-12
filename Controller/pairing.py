from Model import model


def first_round(tour, already_played, nombre_matchs):
    """Créé le premier round"""
    for match in range(nombre_matchs):
        tour.liste_matchs.append(
            model.Match(
                tour.players[match], tour.players[nombre_matchs + match], 0, 0
            )
        )
        # On ajoute les joueurs affrontés dans le dictionnaire du joueur
        already_played[tour.players[match]].append(
            tour.players[nombre_matchs + match]
        )
        already_played[tour.players[nombre_matchs + match]].append(
            tour.players[match]
        )


def create_rounds(players, already_played, nombre_matchs):
    """Pour chaque itération :
    Joueur 1 est le joueur avec le plus de point
    Joueur 2 est le joueur avec le plus de point que joueur 1 peut affronter
    Si joueur 2 n'est pas disponible, revient en arrière"""
    global matchs
    global disponible
    global seeds
    global can_duel

    index = 0
    can_duel = {}
    disponible = players.copy()
    seeds = []
    matchs = []

    # Prépare le dictionnaire d'itérateurs
    get_player_iterators(players, already_played, can_duel)

    while index < nombre_matchs:
        # print("\nitération\n")
        # Réinitialise les itérateurs des joueurs disponibles
        get_player_iterators(disponible, already_played, can_duel)
        joueur1 = disponible[0]

        if joueur1 not in seeds:
            seeds.append(joueur1)

        # print()
        # print("joueur 1 : " + affiche(joueur1))
        # print()

        try:
            joueur2 = next(can_duel[joueur1])
            # print("joueur2 : " + affiche(joueur2))
            # print()
            index = is_possible(joueur1, joueur2, index)

        except StopIteration:
            # print("\nexcept\n")
            index = get_next(matchs, index, can_duel, already_played, players)

        show_matchs()
        # print()
        # print(index)
        # print()

    # print()
    return matchs


def get_player_iterators(players, already_played, can_duel):
    """Met à jour le dictionnaire can_duel"""
    for player in players:
        # Chaque joueur se voit attribuer comme valeur parmis les joueurs du tournoi:
        # Un joueur qu'il n'a pas affronté
        # Pas lui même
        can_duel[player] = iter([p for p in players if p not in already_played[player] and p is not player])

    return can_duel


def get_next(matchs, index, can_duel, already_played, players):
    """Reviens en arrière dans un match pour essayer le prochain
    adversaire du joueur 1"""

    index -= 1

    # Debug :
    # for i in disponible:
    #    print(affiche(i))
    # print()
    # print("index get_next:")
    # print(index)
    # print()

    try:
        # Debug :
        # print("\ntry")
        # print(affiche(matchs[index][0]) + " vs " + affiche(matchs[index][1]) + "\n")

        # Rend le joueur 2 disponible
        disponible.append(matchs[index][1])

        # Le joueur 2 devient le prochain itérable de joueur 1
        joueur1 = matchs[index][0]
        joueur2 = next(can_duel[joueur1])
        matchs[index][1] = joueur2

        # On retire le nouvel adversaire des joueurs disponibles
        disponible.remove(joueur2)
        index += 1
        return index

    except StopIteration:
        # Erreur si le joueur 1 du match précédent n'a
        # plus d'adversaire disponible

        # Debug :
        # print("get_next Except")

        # Le joueur 1 devient donc disponible
        disponible.append(matchs[index][0])
        # On supprime le match
        matchs.pop()
        # On revient encore plus loin dans les matchs
        index = get_next(matchs, index, can_duel, already_played, players)
        return index


def is_possible(joueur1, joueur2, index):
    """Retire les joueurs d'un match du tableau des joueurs disponibles"""
    if joueur2 in disponible:
        disponible.remove(joueur2)
        disponible.remove(joueur1)
        matchs.append([joueur1, joueur2])
        index += 1
    return index


def show_matchs():
    """ Fonction de debug
    Permet d'afficher les matchs à chaque boucle"""
    for match in matchs:
        j1 = affiche(match[0])
        j2 = affiche(match[1])
        print(j1 + " vs " + j2)
    print()


def affiche(joueur):
    """Fonction de debug, permet d'afficher rapidement le nom d'un joueur"""
    return model.Player.find_by_id(joueur).__str__()
