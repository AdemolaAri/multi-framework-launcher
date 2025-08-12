from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game/start/', views.start_game, name='start_game'),
    path('game/submit/', views.submit_response, name='submit_response'),
]
