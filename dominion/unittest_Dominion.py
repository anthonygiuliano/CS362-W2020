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

    def test_player_action_balance(self):
        self.setup()
        multiple = 70
        balance = 0

        for c in self.player.stack():
            if c.category == 'action':
                balance += c.actions
                balance -= 1

        self.assertEqual(multiple * balance / len(self.player.stack()), self.player.action_balance())

    def test_player_action_balance_with_action(self):
        self.setup()
        multiple = 70
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5
        card = Dominion.Action_card(name, cost, actions, cards, buys, coins)
        self.player.hand.append(card)
        balance = 0

        for c in self.player.stack():
            if c.category == 'action':
                balance += c.actions
                balance -= 1

        self.assertEqual(multiple * balance / len(self.player.stack()), self.player.action_balance())


    def test_player_calcpoints(self):
        self.setup()
        points = 3
        self.player.hand.append(Dominion.Province())
        points += Dominion.Province().vpoints
        self.player.hand.append(Dominion.Duchy())
        points += Dominion.Duchy().vpoints
        self.player.hand.append(Dominion.Estate())
        points += Dominion.Estate().vpoints
        self.player.hand.append(Dominion.Gardens())
        points += Dominion.Gardens().vpoints
        num_gardens = 1
        garden_vpoint_const = 10
        points += (len(self.player.stack()) // garden_vpoint_const) * num_gardens

        self.assertEqual(self.player.calcpoints(), points)


    def test_player_draw(self):
        self.setup()
        name = 'Test Name'
        cost = 1
        actions = 2
        cards = 3
        buys = 4
        coins = 5
        card = Dominion.Action_card(name, cost, actions, cards, buys, coins)
        self.player.discard.append(card)
        self.player.deck = []
        self.player.draw()

        self.assertEqual(self.player.discard, [])
        self.assertEqual(self.player.deck, [])
        self.assertEqual(self.player.hand[-1], card)

    def test_player_card_summary(self):
        self.setup()
        self.player.hand.append(Dominion.Province())
        self.player.hand.append(Dominion.Duchy())
        self.player.hand.append(Dominion.Estate())
        self.player.hand.append(Dominion.Gardens())
        num_estates = 4
        summary = self.player.cardsummary()

        self.assertEqual(self.player.calcpoints(), summary['VICTORY POINTS'])
        self.assertEqual(num_estates, summary[Dominion.Estate().name])


    def test_game_over_province(self):
        self.setup()
        self.supply['Province'] = []
        self.assertEqual(Dominion.gameover(self.supply), True)

    def test_game_over_supply(self):
        self.setup()
        self.supply['Copper'] = []
        self.supply['Silver'] = []
        self.supply['Gold'] = []
        self.assertEqual(Dominion.gameover(self.supply), True)

    def test_game_not_over(self):
        self.setup()
        self.assertNotEqual(Dominion.gameover(self.supply), True)

    def test_react(self):
        pass
