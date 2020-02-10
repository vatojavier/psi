"""
@author: A Javier Casado
"""

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from . import tests
from .models import Counter, Game, GameStatus, Move


class GameEndTests(tests.BaseModelTest):
    def setUp(self):
        super().setUp()

    def test1(self):
        """ Raton gana al llegar al final"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat2 = 50
        game.cat3 = 43
        game.cat4 = 54
        game.save()

        game.mouse = 11
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=43, target=52)
        Move.objects.create(game=game, player=self.users[1], origin=11, target=4)

        self.assertEqual(game.status, GameStatus.FINISHED)

    def test2(self):
        """ Rata gana al sobrepasar al último gato (tras movmiento de raton)"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat1 = 25
        game.cat2 = 31
        game.cat3 = 32
        game.cat4 = 45
        game.save()

        game.mouse = 36
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=32, target=41)
        Move.objects.create(game=game, player=self.users[1], origin=36, target=29)

        self.assertEqual(game.status, GameStatus.FINISHED)

    def test3(self):
        """ Ratón gana al sobrepasar al último gato (tras movmiento de gato)
            (abandona última línea)"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.cat1 = 29
        game.cat2 = 48
        game.cat3 = 50
        game.cat4 = 61

        game.mouse = 34

        Move.objects.create(game=game, player=self.users[0], origin=29, target=38)
        self.assertEqual(game.status, GameStatus.FINISHED)

    def test4(self):
        """Gatos ganan por inmovilizar rata tras movimiento de gato"""
        game = Game.objects.create(
            cat_user=self.users[0], mouse_user=self.users[1], status=GameStatus.ACTIVE)

        game.mouse = 27
        game.cat1 = 18
        game.cat2 = 20
        game.cat3 = 34
        game.cat4 = 29
        game.save()

        Move.objects.create(game=game, player=self.users[0], origin=29, target=36)
        self.assertEqual(game.status, GameStatus.FINISHED)


