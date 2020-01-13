# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 15:40:47 2020

@author: giuliana
"""

import Dominion
import testUtility

# Get player names
player_names = testUtility.init_player_names()

# number of curses and victory cards
nV, nC = testUtility.init_victory_curse_count(player_names)

# Define box
box = testUtility.init_box(nV)

supply_order = testUtility.init_supply_order()

supply = testUtility.init_supply(box, player_names, nV, nC)

# initialize the trash
trash = testUtility.init_trash

# Costruct the Player objects
players = testUtility.init_players(player_names)

# Play the game
turn = 0
while not Dominion.gameover(supply):
    turn += 1
    print("\r")
    for value in supply_order:
        print(value)
        for stack in supply_order[value]:
            if stack in supply:
                print(stack, len(supply[stack]))
    print("\r")
    for player in players:
        print(player.name, player.calcpoints())
    print("\rStart of turn " + str(turn))
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players, supply, trash)

# Final score
dcs = Dominion.cardsummaries(players)
vp = dcs.loc['VICTORY POINTS']
vpmax = vp.max()
winners = []
for i in vp.index:
    if vp.loc[i] == vpmax:
        winners.append(i)
if len(winners) > 1:
    winstring = ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0], 'wins!'])

print("\nGAME OVER!!!\n" + winstring + "\n")
print(dcs)
