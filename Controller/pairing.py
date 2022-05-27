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


def create_rounds(players, matchs, already_played, nombre_matchs):
    """Créé des rounds à partir du second round.
    Les joueurs ne s'affrontent qu'une seule fois."""
    index = 0
    exception_index = 1

    # Tableau des 2ème joueurs, ce sont les joueurs "disponibles"
    disponible = players[1::2]

    # Dictionnaire des joueurs valides à affronter
    can_duel = get_player_iterators(players, already_played)

    while index < nombre_matchs:
        match = matchs[index]
        joueur1 = match[0]
        joueur2 = match[1]
        is_valid = True

        # Check si joueur 1 et joueur 2 se sont déjà affrontés
        if joueur2 in already_played[joueur1]:
            is_valid = False
            matchs[index][1] = next(can_duel[joueur1])
            print("already played, move to : ")
            print(model.Player.find_by_id(matchs[index][1]))

        # Check si joueur 1 ou joueur 2 apparaissent dans les matchs précédents
        for rencontre in matchs[:index]:
            if joueur1 in rencontre or joueur1 == joueur2:
                is_valid = False

                # Si le joueur 1 est déjà dans les matchs, on le remplace avec le 1er joueur "disponible"
                matchs[index][0] = disponible.pop(0)

                # Le joueur 1 devient donc disponible
                disponible.append(joueur1)

                # Avec le joueur 1 devenu disponible, on reset les iterateurs
                can_duel = get_player_iterators(players, already_played)
                continue

            if joueur2 in rencontre:
                is_valid = False
                try:
                    # Si joueur 2 est déjà dans le match on essaie le prochain "disponible"
                    matchs[index][1] = next(can_duel[joueur1])
                except StopIteration:
                    # Si on atteint le dernier, on revient au match précédent
                    index -= exception_index
                    can_duel = get_player_iterators(players, already_played)
                    # On revient encore plus loin dans les rounds
                    exception_index += 1
                continue

        if is_valid is True:
            index += 1


def get_player_iterators(players, already_played):
    can_duel = {}
    for player in players:
        can_duel[player] = iter(
            [p for p in players if p not in already_played[player] and p is not player]
        )

    return can_duel
