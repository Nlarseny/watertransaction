import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from watermain.forms import LogMessageForm
from watermain.models import LogMessage
from django.views.generic import ListView
from watermain.forms import TransferVariablesForm
from watermain.models import TransferVariables


def submit_info(request):
    form = TransferVariablesForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            # message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "watermain/lessor/collect_info.html", {"form": form})   

# TEST CODE
class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "watermain/log_message.html", {"form": form})

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


