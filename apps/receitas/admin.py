from django.contrib import admin
from .models import Receita

class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'categoria', 'publicada',)
    list_display_links = ('id', 'nome_receita',)
    search_fields = ('nome_receita',)
    list_filter = ('categoria',)
    list_per_page = 2
    list_editable = ('publicada',)

admin.site.register(Receita, ListandoReceitas)