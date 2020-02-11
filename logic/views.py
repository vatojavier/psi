from random import randint
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from datamodel import constants
from datamodel.models import Game, GameStatus, Move, Counter, User, get_mov_val_raton, get_mov_val_gatos, fila_de
from .forms import SignupForm, MoveForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


def anonymous_required(f):
    def wrapped(request):
        if request.user.is_authenticated:
            return HttpResponseForbidden(
                errorHTTP(request, exception="Action restricted to anonymous users"))
        else:
            return f(request)

    return wrapped


def errorHTTP(request, exception=None):
    context_dict = {"msg_error": "Action restricted to anonymous users"}
    context_dict[constants.ERROR_MESSAGE_ID] = exception
    return render(request, "mouse_cat/error.html", context_dict)


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'mouse_cat/index.html')
    else:
        return render(request, 'mouse_cat/welcome.html')


@anonymous_required
def login_service(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                request.session['counter'] = 0
                return redirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return render(request, 'mouse_cat/login.html', {"user_form": AuthenticationForm,
                                                            "return_service": "Username/password is not valid|Usuario/clave no válidos"})
    else:
        return render(request, 'mouse_cat/login.html', {"user_form": AuthenticationForm})


def logout_service(request):
    logout(request)
    request.session['counter'] = 0
    return redirect(reverse('index'))


@anonymous_required
def signup_service(request):
    if request.method == 'POST':
        user_form = SignupForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            #request.session['counter'] = 0

            return login_service(request)
        else:
            return render(request, 'mouse_cat/signup.html', {'user_form': user_form})

    else:
        user_form = SignupForm()
        return render(request, 'mouse_cat/signup.html', {'user_form': user_form})


def counter(request):
    if 'counter' not in request.session:
        request.session['counter'] = 1
    else:
        request.session['counter'] = request.session['counter'] + 1

    counter_global = Counter(request.session['counter'])

    context_dict = {"counter_session": request.session['counter'],
                    "counter_global": counter_global}

    return render(request, 'mouse_cat/counter.html', context_dict)


@login_required
def create_game_service(request):
    user = request.user
    game = Game(cat_user=user)
    game.save()
    return render(request, 'mouse_cat/new_game.html', {"game": game})



@login_required
def join_game(request, game_id=None):

    user = request.user
    context_dict = {}

    if game_id is None:
        games = Game.objects.filter(mouse_user__isnull=True). \
            exclude(cat_user=user).order_by('-id')

        if games:
            context_dict['partidas_disp'] = games
        else:
            context_dict['msg_error'] = "No hay partidas disponibles"

        return render(request, 'mouse_cat/join_game.html', context_dict)
    else:  # peticion de ajax
        game_selected = Game.objects.filter(id=game_id).first()
        game_selected.mouse_user = user
        game_selected.save()
        game_selected.full_clean()
        return HttpResponse()


@login_required
def select_game(request, game_id=None):
    user = request.user
    context_dict = {}

    if game_id is None:
        #  Mostrar lista de partidas
        as_cat = Game.objects.filter(cat_user=user, status=GameStatus.ACTIVE)
        if as_cat:
            context_dict['as_cat'] = as_cat

        as_mouse = Game.objects.filter(mouse_user=user, status=GameStatus.ACTIVE)
        if as_mouse:
            context_dict['as_mouse'] = as_mouse
        return render(request, 'mouse_cat/select_game.html', context_dict)
    else:
        #  Meterse en la partida
        game = Game.objects.filter(id=game_id).first()

        #  Si no hay juego
        if game is None or game.status == GameStatus.CREATED:
            return HttpResponseNotFound(errorHTTP(request, "Game does not exist"))
        else:  # Si se pertenece al juego
            if game.mouse_user == user or game.cat_user == user:
                request.session['game_id'] = game.id
                return redirect(reverse('show_game'))     # DEBUGGGGG AQUIIIIIIIII
            else:
                return HttpResponseNotFound(errorHTTP(request, "Game does not exist"))


@login_required
def show_game(request, error=None):
    try:
        gameid = request.session['game_id']
    except KeyError:
        return errorHTTP(request,
                         exception="No has seleccionado juego")

    game = Game.objects.get(id=gameid)

    move_form = MoveForm(data=request.POST)

    context_dict = {"game": game, "move_form": move_form}

    if error:
        context_dict["error"] = error

    gatos = [game.cat1, game.cat2, game.cat3, game.cat4]
    board = []
    for i in range(64):
        if i in gatos:
            board.append(1)
        elif game.mouse == i:
            board.append(-1)
        else:
            board.append(0)

    context_dict["board"] = board
    return render(request, 'mouse_cat/game.html', context_dict)


@login_required
def move_service(request):

    try:
        gameid = request.session["game_id"]
    except KeyError:
        return HttpResponseNotFound()

    game = Game.objects.get(id=gameid)

    jugador = request.user
    print(jugador)

    if request.method == 'POST':
        origen = request.POST.get('origin')
        destino = request.POST.get('target')

        print(origen, destino)

        try:
            Move.objects.create(game=game, origin=origen,
                                target=destino,
                                player=jugador)
        except ValidationError:
            return -1
            #return render(request, 'mouse_cat/game.html', {"error": "mal"})
            #print("hay error")
            #show_game(request, "mal")
            #return redirect(reverse('show_game'))
        except KeyError:
            return render(request, 'mouse_cat/game.html', {"error": "mal"})
            #return redirect(reverse('show_game'))

        if game.es_AI:
            mueve_ia(game)

        return select_game(request, gameid)

    else:
        return HttpResponseNotFound()


def mueve_ia(game):

    if not game.cat_turn and game.status == GameStatus.ACTIVE:
        pos_validas = get_mov_val_raton(game, game.mouse_user, get_mov_val_gatos(game, game.cat_user))

        print("Raton puede mover a " + str(pos_validas))

        # Si puede avanzar
        if fila_de(min(pos_validas)) < fila_de(game.mouse):
            puede_avanzar = True
        else:
            puede_avanzar = False

        mov = avanzar(game.mouse, pos_validas, puede_avanzar)
        print("elgido " + str(mov))
        Move.objects.create(game=game, origin=game.mouse,
                            target=mov,
                            player=game.mouse_user)


def avanzar(pos_raton, pos_validas, puede_avanzar):
    mov = []

    for pos in pos_validas:
        if puede_avanzar:
            if fila_de(pos) < fila_de(pos_raton):
                mov.append(pos)
        else:
            if fila_de(pos) > fila_de(pos_raton):
                mov.append(pos)

    print("Eligiendo entre " + str(mov))

    if len(mov) == 1:
        return mov[0]
    elif len(mov) > 1:
        print(mov)
        return mov[randint(0, 1)]
    else:
        return -1  # Error



@login_required
def repeticion_partida(request):
    return render(request, "mouse_cat/repeticion.html")


@login_required
def crear_game_vs_ia(request):
    user = request.user

    # get usuario IA o crearlo
    nombre_IA = "IA"
    password = "skynet"

    try:
        userIA = User.objects.get(username=nombre_IA)

    except User.DoesNotExist:

        userIA = User.objects.create_user(username=nombre_IA, password=password)
        user.save()
        print("Creado usuario IA")

    # crear juego
    game = Game(cat_user=user, mouse_user=userIA, es_AI=True)
    game.save()

    return redirect(reverse('vsIA'))


@login_required
def jugar_vs_ia(request):
    user = request.user
    context_dict = {}

    vs_ia = Game.objects.filter(cat_user=user, es_AI=True, status=GameStatus.ACTIVE)

    if vs_ia:
        context_dict["vs_ia"] = vs_ia


    return render(request, "mouse_cat/jugarIA.html", context_dict)


@login_required
def partida_terminada(request):
    return render(request, "mouse_cat/partida_terminada.html")
