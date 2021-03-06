"""when_the_light_go_down URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from when_the_light_go_down import views

urlpatterns = [
    path('fiche_hash', views.fiche_hash, name='fiche_hash'),
    path('fiche', views.fiche_render, name='fiche_render'),
    path('menu_wtlgd', views.menu_wtlgd, name='menu_wtlgd'),
	path('villes', views.villes, name='villes'),
	path('table_prix', views.table_prix, name='table_prix'),
	path('prologue_genese', views.prologue_genese, name='prologue_genese'),
	path('salaire_foncier', views.salaire_foncier, name='salaire_foncier'),
	path('magie', views.magie, name='magie'),
	path('race', views.race, name='race')
]

    