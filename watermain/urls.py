from django.urls import path
from watermain import views
from watermain.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="watermain/home.html",
)


urlpatterns = [
    path("", home_list_view, name="home"),
    path("watermain/<name>", views.hello_there, name="hello_there"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("make_contract/<int:months>/<int:shares>", views.make_contract, name="make_contract"),
    path("make_contract/", views.make_contract, name="make_contract"),

    #lessor side
    path("collect_info/", views.submit_info, name="collect_info"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("offers/", views.offers, name="offers"),
    path("counter_offer/", views.counter_offer, name="counter_offer"),
    path("contract_signing/", views.contract_signing, name="contract_signing"),
    path("finish/", views.finish, name="finish"),
    path("log/", views.log_message, name="log"),
]
