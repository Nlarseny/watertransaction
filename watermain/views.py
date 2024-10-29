import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render



def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'watermain/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home(request):
    return render(request, "watermain/home.html")

def about(request):
    return render(request, "watermain/about.html")

def contact(request):
    return render(request, "watermain/contact.html")

# lessor side
def collect_info(request):
    return render(request, "watermain/lessor/collect_info.html")

def create_listing(request):
    return render(request, "watermain/lessor/create_listing.html")

def offers(request):
    return render(request, "watermain/lessor/offers.html")

def counter_offer(request):
    return render(request, "watermain/lessor/counter_offer.html")

def contract_signing(request):
    return render(request, "watermain/lessor/contract_signing.html")


