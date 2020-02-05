import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'ratonGato_project.settings')

import django
django.setup()
from django.contrib.auth.models import User
from datamodel.models import Game, Move


try:
    user1 = User.objects.get(id=10)
except User.DoesNotExist:
    user1 = User.objects.create_user(id=10, username="Gato", password="gato_tq")


try:
    user2 = User.objects.get(id=11)
except User.DoesNotExist:
    user2 = User.objects.create_user(id=11, username="Rata", password="rata_tq")


game = Game(cat_user=user1)
game.full_clean()
game.save()

query = Game.objects.filter(mouse_user=None)

for juego in query:
    print(juego)

print("\n\n")

#  query ordenando por id y pillando el primero
query = Game.objects.filter(mouse_user=None).order_by("id")

juego = query[0]
juego.mouse_user = user2
juego.save()
print(juego)

Move.objects.create(game=juego, player=user1, origin=2, target=11)
print(juego)

Move.objects.create(game=juego, player=user2, origin=59, target=52)
print(juego)

