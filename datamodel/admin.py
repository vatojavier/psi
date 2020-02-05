from django.contrib import admin
from datamodel.models import Game, Move


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    fields = ["cat_user", "mouse_user"]


admin.site.register(Game, GameAdmin)
admin.site.register(Move)
