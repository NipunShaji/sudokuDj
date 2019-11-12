
from django.urls import path
from . import views

app_name = 'solver'

urlpatterns = [
    path('solve/', views.solve, name='solve'),
    path('', views.home, name='home'),
]
