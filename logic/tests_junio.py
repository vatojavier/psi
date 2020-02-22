from django.core.exceptions import ValidationError

from datamodel import tests
from datamodel.models import Game, GameStatus, Move, Ganador
from logic.views import mueve_ia


class GameMoveTests(tests.BaseModelTest):
    def setUp(self):
        super().setUp()

    def test1(self):
        """IA debe mover hacia adelante"""

        game = Game.objects.create(
            cat_user=self.users[0], es_AI=True, mouse_user=self.users[1])

        Move.objects.create(game=game, player=self.users[0], origin=0, target=9)
        mueve_ia(game)
        self.assertLess(game.mouse, 59)

    def test2(self):
        """IA debe mover hacia adelante con gatos ocupando una pos de alante"""

        game = Game.objects.create(
            cat_user=self.users[0], es_AI=True, mouse_user=self.users[1])

        game.mouse = 25
        game.cat2 = 18

        Move.objects.create(game=game, player=self.users[0], origin=0, target=9)
        mueve_ia(game)
        self.assertEqual(game.mouse, 16)

    def test3(self):
        """IA debe mover hacia atrás"""

        game = Game.objects.create(
            cat_user=self.users[0], es_AI=True, mouse_user=self.users[1])

        game.mouse = 25
        game.cat2 = 18
        game.cat3 = 16

        Move.objects.create(game=game, player=self.users[0], origin=0, target=9)
        mueve_ia(game)
        self.assertGreater(game.mouse, 25)

    def test4(self):
        """IA puede ganar partida"""

        game = Game.objects.create(
            cat_user=self.users[0], es_AI=True, mouse_user=self.users[1])

        game.mouse = 25
        game.cat2 = 18
        game.cat3 = 20
        game.cat1 = 22
        game.cat4 = 29

        Move.objects.create(game=game, player=self.users[0], origin=29, target=36)
        mueve_ia(game)
        self.assertEqual(game.ganador, Ganador.RATON)
        self.assertEqual(game.status, GameStatus.FINISHED)

    def test5(self):
        """Se pude ganar a la IA"""

        game = Game.objects.create(
            cat_user=self.users[0], es_AI=True, mouse_user=self.users[1])

        game.mouse = 25
        game.cat2 = 18
        game.cat3 = 16
        game.cat1 = 32
        game.cat4 = 27

        Move.objects.create(game=game, player=self.users[0], origin=27, target=34)
        self.assertEqual(game.ganador, Ganador.GATO)
        self.assertEqual(game.status, GameStatus.FINISHED)
