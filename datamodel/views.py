from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
# este views es inutil
def index(request):
    print('hola')
    return render(request, 'mouse_cat/index.html')

