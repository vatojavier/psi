from django.db import models
from django import utils
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class GameStatus:
    CREATED = 1
    ACTIVE = 2
    FINISHED = 3


class Ganador:
    NADIE = 0
    GATO = 1
    RATON = 2


#  python manage.py migrate --run-syncdb
class Game(models.Model):
    cat_user = models.ForeignKey(User,
                                 related_name="games_as_cat",
                                 on_delete=models.CASCADE)
    mouse_user = models.ForeignKey(User,
                                   related_name="games_as_mouse",
                                   on_delete=models.CASCADE,
                                   blank=True, null=True)

    es_AI = models.BooleanField(default=False)

    ganador = models.IntegerField(default=Ganador.NADIE)

    #  Posiciones del gato
    cat1 = models.IntegerField(default=0)
    cat2 = models.IntegerField(default=2)
    cat3 = models.IntegerField(default=4)
    cat4 = models.IntegerField(default=6)
    # Posicion del raton
    mouse = models.IntegerField(default=59)

    cat_turn = models.BooleanField(default=True)
    status = models.IntegerField(default=GameStatus.CREATED)

    MIN_CELL = 0
    MAX_CELL = 63

    #  Inicialiando pos validas del gato
    pos_validas_gato = []
    es_fila_par = -1
    for i in range(64):
        if i % 8 == 0:
            es_fila_par = es_fila_par * -1

        if es_fila_par == 1:
            if i % 2 == 0:
                pos_validas_gato.append(i)
        else:
            if i % 2 != 0:
                pos_validas_gato.append(i)

    def clean(self):
        if self.mouse_user is None:

            if self.status == GameStatus.ACTIVE \
                    or self.status == GameStatus.FINISHED:
                raise ValidationError("Game status not valid|Estado no válido")

            self.status = GameStatus.CREATED

        fichas = [self.cat1, self.cat2, self.cat3, self.cat4, self.mouse]

        for posicion in fichas:
            if posicion < self.MIN_CELL \
                    or posicion > self.MAX_CELL:
                raise ValidationError("Invalid cell for a "
                                      "cat or the mouse|Gato "
                                      "o ratón en posición no válida")

    #  the save()method is always called when
    #  creating or updating an instance of a Django model.
    def save(self, *args, **kwargs):

        if self.mouse_user is None:
            self.status = GameStatus.CREATED

        else:  # Si hay dos usuarios:
            if self.status == GameStatus.CREATED:
                self.status = GameStatus.ACTIVE

        fichas = [self.cat1, self.cat2, self.cat3, self.cat4, self.mouse]
        for ficha in fichas:
            if ficha not in self.pos_validas_gato:
                raise ValidationError("Invalid cell for a cat "
                                      "or the mouse|Gato o "
                                      "ratón en posición no válida")

        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        if self.status == GameStatus.CREATED:
            estado = "Created"
        elif self.status == GameStatus.ACTIVE:
            estado = "Active"
        else:
            estado = "Finished"

        if self.cat_turn:
            turno_cat = "Cat [X] "
            turno_rata = "Mouse [ ] "
        else:
            turno_cat = "Cat [ ] "
            turno_rata = "Mouse [X] "

        str_solo_cat = ("(" + str(self.id) + ", " + estado + ")\t" + turno_cat
                        + self.cat_user.username +
                        "(" + str(self.cat1) + ", " +
                        str(self.cat2) + ", " + str(self.cat3)
                        + ", " + str(self.cat4) + ")")

        str_cat_rata = ("(" + str(self.id) + ", " + estado + ")\t" + turno_cat
                        + self.cat_user.username +
                        "(" + str(self.cat1) + ", " +
                        str(self.cat2) + ", " + str(self.cat3) +
                        ", " + str(self.cat4) + ") --- "
                        + turno_rata + str(self.mouse_user)
                        + "(" + str(self.mouse) + ")")

        if self.mouse_user is None:
            return str_solo_cat
        else:
            return str_cat_rata


def es_mov_valido(game, jugador, origen, destino, pos_val_gatos, pos_val_rata):
    origen = int(origen)
    destino = int(destino)

    if jugador != game.cat_user and jugador != game.mouse_user:
        return False

    if jugador == game.cat_user:
        if destino in pos_val_gatos[origen]:
            return True
        else:
            return False
    else:
        if origen != game.mouse:
            return False  # Si no se selecciona la pos de la rata
        if destino in pos_val_rata:
            return True
        else:
            return False


def es_mov_valido_g(game, jugador, origen, destino):
    origen = int(origen)
    destino = int(destino)
    pos_gatos = [game.cat1, game.cat2, game.cat3, game.cat4]

    if jugador != game.cat_user and jugador != game.mouse_user:
        return False

    if origen not in pos_gatos:
        return False
    if origen > 55:  # Si está en última fila...
        return False
    if origen % 8 == 0 and destino != (origen + 9):
        return False  # Si esta a la izq
    if origen % 7 == 0 and origen != 0 and \
            destino != (origen + 7):
        return False  # Si esta a la dcha
    elif destino != (origen + 9) and \
            destino != (origen + 7):
        return False
    elif destino in pos_gatos or destino == game.mouse:
        return False  # Si ya esta ocupado por otro jueputa...
    else:
        return True


def es_mov_valido_r(game, jugador, origen, destino, mov_val_gatos):
    origen = int(origen)
    destino = int(destino)

    if jugador != game.cat_user and jugador != game.mouse_user:
        return False

    if origen != game.mouse:
        return False  # Si no se selecciona la pos de la rata

    if destino in mov_val_gatos:
        return False  # Si ya esta ocupado por un gato...

    if destino > 63 or destino < 0:
        return False
    if origen % 8 == 0 and (destino != (origen + 9) and
                            destino != (origen - 7)):
        return False  # Si esta a la izq...
    if origen % 8 == 7 and (destino != (origen - 9) and
                            destino != (origen + 7)):
        return False  # Si esta a la dcha...
    elif destino != (origen + 7) and \
            destino != (origen - 7) and \
            destino != (origen + 9) and \
            destino != (origen - 9):
        return False
    else:
        return True


def get_mov_val_raton(game, jugador, mov_val_gatos):
    """Devuelve todos los posibles movimientos validos del raton"""
    mov_val_rata = []

    for i in range(game.MAX_CELL):
        if es_mov_valido_r(game, jugador, game.mouse, i, mov_val_gatos):
            mov_val_rata.append(i)

    return mov_val_rata


def get_mov_val_gatos(game, jugador):
    """Devuelve todos los posibles movimientos validos de los gatos"""
    pos_gatos = [game.cat1, game.cat2, game.cat3, game.cat4]
    pos_val_gatos = {}

    for pos_gato in pos_gatos:
        pos_val_gatos[pos_gato] = []

    for gato in pos_gatos:
        for i in range(game.MAX_CELL):
            if es_mov_valido_g(game, jugador, gato, i):
                pos_val_gatos[gato].append(i)

    return pos_val_gatos


class ManagerMove(models.Manager):

    def create(self, *args, **kwargs):
        game = kwargs['game']
        jugador = kwargs['player']
        origin = int(kwargs['origin'])
        target = int(kwargs['target'])

        if (game.cat_turn and jugador == game.mouse_user) or \
                (not game.cat_turn and jugador == game.cat_user):
            raise ValidationError("Move not allowed|Movimiento no permitido")

        pos_val_gatos = get_mov_val_gatos(game, jugador)
        pos_val_rata = get_mov_val_raton(game, jugador, pos_val_gatos)

        if game.status == GameStatus.CREATED:
            print("si macho")

        if game.status == GameStatus.CREATED or game.status == GameStatus.FINISHED \
                or not es_mov_valido(game, jugador, origin, target, pos_val_gatos, pos_val_rata):
            raise ValidationError("Move not allowed|Movimiento no permitido")
        else:
            #  Se actualizan los turnos y posiciones
            if game.mouse == origin:
                game.mouse = target
                game.cat_turn = True

            if game.cat1 == origin:
                game.cat1 = target
                game.cat_turn = False

            elif game.cat2 == origin:
                game.cat2 = target
                game.cat_turn = False

            elif game.cat3 == origin:
                game.cat3 = target
                game.cat_turn = False

            elif game.cat4 == origin:
                game.cat4 = target
                game.cat_turn = False

            pos_val_gatos = get_mov_val_gatos(game, jugador)
            pos_val_rata = get_mov_val_raton(game, jugador, pos_val_gatos)

            if raton_gana(game):
                print("------Ha gando el raton------")
                game.ganador = Ganador.RATON
                game.status = GameStatus.FINISHED
            elif gato_gana(pos_val_gatos, pos_val_rata):
                print("------Ha gando el gato------")
                game.ganador = Ganador.GATO
                game.status = GameStatus.FINISHED

            game.save()
            super(ManagerMove, self).create(*args, **kwargs)


def raton_gana(game):
    pos_gatos = [game.cat1, game.cat2, game.cat3, game.cat4]

    if game.mouse <= 7 or pasado_ultimo_gato(game.mouse, pos_gatos):
        return True


def gato_gana(pos_val_gatos, pos_val_rata):

    for opcion in pos_val_rata:
        for gato in pos_val_gatos:
            if opcion not in pos_val_gatos[gato]:
                return False  # Tiene escapatoria

    # Si todas las opciones validas del raton estan
    # en las op validas del gato...
    return True


# Devuelve fila (pos derecha) en la que se encuentra
def fila_de(pos):
    return (8 - pos % 8 + pos) - 1


def pasado_ultimo_gato(pos_rata, pos_gatos):
    # Pasado o en la misma fila:
    if fila_de(pos_rata) <= fila_de(min(pos_gatos)):
        return True
    else:
        return False


class Move(models.Model):
    origin = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="moves")
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=utils.timezone.now)
    #  hacer el objects = Movemanager para calcular mov permitidos
    objects = ManagerMove()

    def save(self, *args, **kwargs):
        super(Move, self).save()

    def __str__(self):
        return "\nID: " + str(self.id) + "\n" +\
               "Origen: " + str(self.origin) + "\n" +\
               "Target: " + str(self.target) + "\n"


class ManagerCounter(models.Manager):

    def create(self, *args, **kwargs):
        raise ValidationError("Insert not allowed|Inseción no permitida")

    @classmethod
    def __create_counter(cls, val):
        counter = Counter(value=val)
        super(Counter, counter).save()
        return counter

    @staticmethod
    def inc():
        try:
            v_antes = Counter.objects.get(pk=1).value
            v_ahora = v_antes + 1
            Counter.objects.all().filter(pk=1).update(value=v_ahora)
            return v_ahora

        except ObjectDoesNotExist:
            counter = ManagerCounter.__create_counter(1)
            return counter.value

    @staticmethod
    def get_current_value():
        try:
            # Se pilla el de la BBDD
            Counter.objects.get(pk=1)
            value = Counter.objects.filter(pk=1).values('value')
            return value.first()['value']

        except ObjectDoesNotExist:
            #  Se crea uno
            counter = ManagerCounter.__create_counter(0)
            return counter.value


class Counter(models.Model):
    value = models.IntegerField(default=0)
    objects = ManagerCounter()

    def save(self, *args, **kwargs):
        raise ValidationError("Insert not allowed|Inseción no permitida")

    def __str__(self):
        return "Value: " + str(self.value)
