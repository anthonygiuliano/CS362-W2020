from unittest import TestCase
import testUtility
import Dominion

class TestCard(TestCase):

    def setup(self):
        # Get player names
        self.player_names = testUtility.init_player_names()

        # number of curses and victory cards
        self.nV, self.nC = testUtility.init_victory_curse_count(self.player_names)

        # Define box
        self.box = testUtility.init_box(self.nV)

        self.supply_order = testUtility.init_supply_order()

        self.supply = testUtility.init_supply(self.box, self.player_names, self.nV, self.nC)

        # initialize the trash
        self.trash = testUtility.init_trash()

        # Costruct the Player objects
        self.players = testUtility.init_players(self.player_names)
        self.player = self.players[0]

    def test_init(self):
        self.setup()
        cost = 1
        buypower = 5

        card = Dominion.Coin_card(self.player.name, cost, buypower)

        self.assertEqual('Annie', card.name)
        self.assertEqual(buypower, card.buypower)
        self.assertEqual(cost, card.cost)
        self.assertEqual('coin', card.category)
        self.assertEqual(0, card.vpoints)

    def test_react(self):
        pass
