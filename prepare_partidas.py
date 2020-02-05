"""Prepara partidas a pnto de finalizar"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from datamodel.models import Game, Move

# Gato gana
try:
    user1 = User.objects.get(id=55)
except User.DoesNotExist:
    user1 = User.objects.create_user(id=55, username="el_que_gana", password="gana")

try:
    user2 = User.objects.get(id=56)
except User.DoesNotExist:
    user2 = User.objects.create_user(id=56, username="el_que_pierde", password="pierde")


game = Game(cat_user=user1)
game.full_clean()
game.save()

query = Game.objects.filter(mouse_user=None)
query = Game.objects.filter(mouse_user=None).order_by("id")

juego = query[0]
juego.mouse_user = user2

juego.cat1 = 9
juego.cat2 = 18

juego.mouse = 16
juego.save()

# Raton gana
try:
    user1 = User.objects.get(id=55)
except User.DoesNotExist:
    user1 = User.objects.create_user(id=55, username="el_que_gana", password="gana")

try:
    user2 = User.objects.get(id=56)
except User.DoesNotExist:
    user2 = User.objects.create_user(id=56, username="el_que_pierde", password="pierde")


game = Game(cat_user=user2)
game.full_clean()
game.save()

query = Game.objects.filter(mouse_user=None)
query = Game.objects.filter(mouse_user=None).order_by("id")

juego = query[0]
juego.mouse_user = user1

juego.mouse = 20
juego.cat1 = 22
juego.cat2 = 25
juego.cat3 = 31
juego.cat4 = 29

juego.save()

Move.objects.create(game=juego, player=user2, origin=29, target=38)

