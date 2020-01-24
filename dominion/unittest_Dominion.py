from unittest.mock import patch
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


    def test_action_init(self):
        self.setup()
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5

        card = Dominion.Action_card(name, cost, actions, cards, buys, coins)

        self.assertEqual(name, card.name)
        self.assertEqual(cost, card.cost)
        self.assertEqual(actions, card.actions)
        self.assertEqual(cards, card.cards)
        self.assertEqual(buys, card.buys)
        self.assertEqual(coins, card.coins)


    def test_action_init_failure(self):
        self.setup()
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5

        with self.assertRaises(TypeError):
            card = Dominion.Action_card(name, cost, actions, cards, buys)


    def test_action_use(self):
        self.setup()
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5

        card = Dominion.Action_card(name, cost, actions, cards, buys, coins)
        self.player.hand.append(card)
        self.assertEqual(self.player.hand[-1], card)

        card.use(self.player, self.trash)
        self.assertNotEqual(self.player.hand[-1], card)
        self.assertEqual(self.player.played[-1], card)


    # https://stackoverflow.com/questions/18161330/using-unittest-mock-to-patch-input-in-python-3
    @patch('builtins.input', lambda *args: '')
    def test_action_augment(self):
        self.setup()
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5

        card = Dominion.Action_card(name, cost, actions, cards, buys, coins)

        self.player.turn(self.players, self.supply, self.trash)

        # add values from `card` to the current values in `player` to calculate expected values
        actions += self.player.actions
        cards += len(self.player.hand)
        buys += self.player.buys
        coins += self.player.purse

        card.augment(self.player)

        # test to make sure the new values in `player` match the expected values after augmenting with `card`
        self.assertEqual(actions, self.player.actions)
        self.assertEqual(cards, len(self.player.hand))
        self.assertEqual(buys, self.player.buys)
        self.assertEqual(coins, self.player.purse)


    def test_react(self):
        pass
