#!/usr/bin/env python3
pWins = [0, 0]
comb = {}

def cp(players):
    cpy = []
    for p in players:
        cpy.append(p.copy())
    return cpy

def qRoll(players, turn, dice, count):
    p = players[turn]
    p['pos'] = (p['pos'] + dice - 1) % 10 + 1
    p['score'] += p['pos']
    if p['score'] >= 21:
        pWins[turn] += count
        return

    turn = (turn + 1) % 2
    for d, c in comb.items():
        qRoll(cp(players), turn, d, count * c)

def simulate(players):
    for d, c in comb.items():
        qRoll(cp(players), 0, d, c)

with open("21.input") as file:
    players = []
    pos = []
    dice = {'next': 1, 'rolls': 0}
    for row in file.readlines():
        player = {}
        player['id'] = int(row.split()[1])
        player['pos'] = int(row.split()[4])
        pos.append(player['pos'])
        player['score'] = 0
        players.append(player)

    players2 = players.copy()

    while max([p['score'] for p in players]) < 1000:
        for p in players:
            d = 0
            for i in range(3):
                d += dice['next']
                dice['next'] = dice['next'] % 100 + 1
            dice['rolls'] += 3
            p['pos'] = (p['pos'] + d - 1) % 10 + 1
            p['score'] += p['pos']

            if p['score'] >= 1000:
                break

    print(min([p['score'] for p in players]) * dice['rolls'])

    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(1, 4):
                if (i + j + k) not in comb:
                    comb[i + j + k] = 0
                comb[i + j + k] += 1

    for i, p in enumerate(players):
        p['pos'] = pos[i]
        p['score'] = 0

    simulate(players)

    print(max(pWins))
