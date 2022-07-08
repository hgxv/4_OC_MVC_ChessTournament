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


""" def create_rounds(players, matchs, already_played, nombre_matchs):
    Créé des rounds à partir du second round.
    Les joueurs ne s'affrontent qu'une seule fois.
    index = 0
    exception_index = 1
    i = 0
    # Tableau des 2ème joueurs, ce sont les joueurs "disponibles"
    disponible = players[1::2]
    placed = players[::2]

    # Dictionnaire des joueurs valides à affronter
    can_duel = get_player_iterators(players, already_played)

    while index < nombre_matchs:
        match = matchs[index]
        joueur1 = match[0]
        joueur2 = match[1]
        
        i += 1
        print("itération n°" + str(i))
        print("match n°" + str(index))
        show_matchs(matchs)
        is_valid = True

        # Check si joueur 1 et joueur 2 se sont déjà affrontés
        if joueur2 in already_played[joueur1] or joueur1 == joueur2:
                print(affiche(joueur2) + " is in " + affiche(joueur1))
                is_valid = False
                joueur2 = next(can_duel[joueur1])
                matchs[index][1] = joueur2
                print("is now " + affiche(joueur2))
                print()
                continue

        # Check si joueur 1 ou joueur 2 apparaissent dans les matchs précédents
        for rencontre in matchs[:index]:
            if joueur1 in rencontre or joueur1 == joueur2:
                is_valid = False

                # Si le joueur 1 est déjà dans les matchs, on le remplace avec le 1er joueur "disponible"
                disponible.append(joueur1)

                joueur1 = disponible.pop(0)
                matchs[index][0] = joueur1

                # Le joueur 1 devient donc disponible

                # Avec le joueur 1 devenu disponible, on reset les iterateurs
                can_duel = get_player_iterators(players, already_played)

            if joueur2 in rencontre:
                is_valid = False
                try:
                    # Si joueur 2 est déjà dans le match on essaie le prochain "disponible"
                    matchs[index][1] = next(can_duel[joueur1])
                    print("try")
                    print(index)
                    break
                except StopIteration:
                    # Si on atteint le dernier, on revient au match précédent
                    print("\nException")
                    disponible.append(joueur1)
                    disponible.remove(joueur2)

                    print(affiche(joueur2))
                    matchs[index][0] = joueur2
                    matchs[index][1] = joueur1

                    can_duel = get_player_iterators(players, already_played)
                    index = 0
                    continue

        if is_valid is True:
            index += 1
            print("match n°" + str(index) + " is valid") """


def create_rounds(players, already_played, nombre_matchs):
    global matchs
    global disponible
    global seeds
    global can_duel

    index = 0
    can_duel = {}
    disponible = players.copy()
    seeds = []
    matchs = []

    get_player_iterators(players, already_played, can_duel)

    while index < nombre_matchs:
        print("\nitération\n")
        joueur1 = disponible[0]

        if joueur1 not in seeds:
            seeds.append(joueur1)

        print()
        print("joueur 1 : " + affiche(joueur1))
        print()

        try:
            joueur2 = next(can_duel[joueur1])
            print("joueur2 : " + affiche(joueur2))
            print()
            index = is_possible(joueur1, joueur2, index)

        except StopIteration:
            print("\nexcept\n")
            index = get_next(matchs, index, can_duel, already_played, players)

        show_matchs()
        print()
        print(index)
        print()
        """ goto = input("\nContinue ?\n")
        if goto == "q":
            break """

    print()
    return matchs


def get_player_iterators(players, already_played, can_duel):
    for player in players:
        can_duel[player] = iter([p for p in players if p not in already_played[player] and p is not player])

    return can_duel

def get_next(matchs, index, can_duel, already_played, players):
    
    index -= 1
    for i in disponible:
        print(affiche(i))
    print()

    get_player_iterators(disponible, already_played, can_duel)
    print("index get_next:")
    print(index)
    print()
    try:
        print("\ntry")
        print(affiche(matchs[index][0]) + " vs " + affiche(matchs[index][1]) + "\n")
        disponible.append(matchs[index][1])
        joueur1 = matchs[index][0]

        isreturn = input("continue ?")
        if isreturn == "q":
            return

        joueur2 = next(can_duel[joueur1])
        matchs[index][1] = joueur2
        disponible.remove(joueur2)
        index = is_possible(joueur1, joueur2, index)
        return index
    
    except StopIteration:
        print("get_next Except")
        disponible.append(matchs[index][0])
        matchs.pop()
        get_next(matchs, index, can_duel, already_played, players)
        return index


def is_possible(joueur1, joueur2, index):
    if joueur2 in disponible:
        disponible.remove(joueur2)
        disponible.remove(joueur1)
        matchs.append([joueur1, joueur2])
        index += 1
    return index


def show_matchs():
    for match in matchs:
        j1 = affiche(match[0])
        j2 = affiche(match[1])
        print(j1 + " vs " + j2)
    print()


def affiche(joueur):
    return model.Player.find_by_id(joueur).__str__()
