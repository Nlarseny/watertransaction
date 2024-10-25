from django.urls import path
from watermain import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watermain/<name>", views.hello_there, name="hello_there"),

]
