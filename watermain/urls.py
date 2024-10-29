from django.urls import path
from watermain import views

urlpatterns = [
    path("", views.home, name="home"),
    path("watermain/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    #lessor side
    path("collect_info/", views.collect_info, name="collect_info"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("offers/", views.offers, name="offers"),
    path("counter_offer/", views.counter_offer, name="counter_offer"),
    path("contract_signing/", views.contract_signing, name="contract_signing"),
]
