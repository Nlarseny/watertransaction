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

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import shutil
import os 
from django.core.files.storage import FileSystemStorage

import datetime

from pathlib import Path

import boto3

def upload_bucket():
    session = boto3.Session(
        aws_access_key_id='AKIA2HVQ5LINIDF5O4U2',
        aws_secret_access_key='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',
    )
    s3 = session.resource('s3')

    # Filename - File to upload
    # Bucket - Bucket to upload to (the top level directory under AWS S3)
    # Key - S3 object name (can contain subdirectories). If not specified then file_name is used
    s3.meta.client.upload_file(Filename=str(Path(__file__).resolve().parent.parent) + "/media/example.pdf", Bucket='lawxbucket', Key='contract.pdf', ExtraArgs={'ContentType': "application/pdf"})


def get_recent_variables():
    queryset = TransferVariables.objects.last() # a little hokey pokey, make better when there is time and a need (when we add users)
    price = queryset.price
    shares = queryset.shares
    start_date = queryset.start_date
    end_date = queryset.end_date
    permitted_uses = queryset.permitted_uses

    return (price, shares, start_date, end_date, permitted_uses)

def contract_builder(months = 0, shares=111, date = str(datetime.date.today()), lessor = "Frank Jones", lessee = "Molly Doe", lessee_price=133):
    variables = get_recent_variables()
    price = variables[0]
    # shares = variables[1]
    start_date = variables[2]
    end_date = variables[3]
    permitted_use = variables[4]


    doc = SimpleDocTemplate("example.pdf", pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    paragraph_1 = Paragraph("WATER RIGHTS LEASE AGREEMENT", styles['Heading1'])
    content.append(paragraph_1)

    paragraph_2 = Paragraph(
        "This Water Rights Lease Agreement (\"Agreement\") is made and entered into on " + date + 
        " by and between " + lessor + " (\"Lessor\") and " + lessee + " (\"Lessee\").",
        styles['BodyText'])
    content.append(paragraph_2)


    content.append(Paragraph("RECITALS", styles['BodyText']))

    content.append(Paragraph("WHEREAS, Lessor owns water rights in Utah, as described in Exhibit A;", styles['BodyText']))

    content.append(Paragraph("WHEREAS, Lessee wants to lease these water rights for beneficial use; and", styles['BodyText']))
 
    content.append(Paragraph("WHEREAS, Lessor agrees to lease the water rights to Lessee under the terms below.", styles['BodyText']))


    content.append(Paragraph("AGREEMENT", styles['BodyText']))

    content.append(Paragraph("The parties agree as follows:", styles['BodyText']))

    content.append(Paragraph("1. Lease of Water Rights: Lessor leases the water rights to Lessee for the term of this agreement.", styles['BodyText']))

    content.append(Paragraph("2. Term", styles['BodyText']))

    content.append(Paragraph("The term of this lease shall be for a period of " 
                                 + str(months) + 
                                 " months, starting on " + start_date + " and ending on " + 
                                 end_date + ", unless terminated earlier as provided herein. " + 
                                 "This agreement may be renewed if both parties agree in writing.", styles['BodyText']))


    content.append(Paragraph("3. Payment", styles['BodyText']))

    content.append(Paragraph("Lessee will pay Lessor $" + 
                             str(lessee_price) + 
                             " for " + str(shares) + " shares.Payment is due by "
                             + str(date) + 
                             " annually, based on actual water use reported to the Utah Division of Water Rights.", styles['BodyText']))


    content.append(Paragraph("4. Use of Water Rights", styles['BodyText']))

    content.append(Paragraph("Lessee can only use the water for " + 
                             permitted_use + 
                             " as allowed by Utah law and the water rights description in Exhibit A. Lessee may not change how or where the water is used without Lessor's written permission and following the applicable legal requirements.", styles['BodyText']))


    content.append(Paragraph("5. Legal Compliance", styles['BodyText']))

    content.append(Paragraph("Lessee must follow all federal, state, and local laws about using these water rights.", styles['BodyText']))


    content.append(Paragraph("6. Ownership", styles['BodyText']))

    content.append(Paragraph("Lessor keeps full ownership of the water rights. " + 
                             "This agreement only gives Lessee the right to use the water, " + 
                             "not own it. Lessee shall not take any action that may impair " + 
                             "or encumber Lessor’s ownership of the Water Rights.", styles['BodyText']))


    content.append(Paragraph("7. Maintaining Water Rights", styles['BodyText']))

    content.append(Paragraph("Lessor will file necessary reports with the Utah Division of Water " + 
                             "Rights to keep the water rights valid. Lessee will assist by providing " + 
                             "any necessary information.", styles['BodyText']))


    content.append(Paragraph("8. Change Application", styles['BodyText']))

    content.append(Paragraph("Before Lessee can use the water, Lessor must file and get approval for " + 
                             "a change application with the Utah State Engineer. The change application " + 
                             "will allow the water rights to be used as described in Section 4. Lessee will " + 
                             "help with this process and reimburse Lessor for all costs associated with the " + 
                             "preparation, filing, prosecution, and any appeals of the change application.", styles['BodyText']))


    content.append(Paragraph("9. Default and Termination", styles['BodyText']))

    content.append(Paragraph("Either party may terminate this agreement with 30 days' written notice if the " + 
                             "other party breaches any term of this Agreement and fails to remedy said breach " + 
                             "within the 30-day notice period. Upon termination, Lessee shall immediately stop " + 
                             "use of the water rights.", styles['BodyText']))


    content.append(Paragraph("10. Transfer", styles['BodyText']))

    content.append(Paragraph("Neither party may transfer their rights or duties under this agreement without " + 
                             "the other party's written permission.", styles['BodyText']))


    content.append(Paragraph("11. Disputes", styles['BodyText']))

    content.append(Paragraph("In the event there is a legal dispute about this agreement, " + 
                             "the winning party can recover reasonable attorney fees from the losing party.", styles['BodyText']))


    content.append(Paragraph("12. Indemnification", styles['BodyText']))

    content.append(Paragraph("Lessee shall indemnify, defend, and hold harmless Lessor from " + 
                             "and against any and all claims, damages, liabilities, and expenses " + 
                             "arising out of or resulting from Lessee's use of the Water Rights.", styles['BodyText']))


    content.append(Paragraph("13. Force Majeure", styles['BodyText']))

    content.append(Paragraph("Neither party shall be liable for any delay or failure to perform " + 
                             "its obligations under this agreement due to causes beyond its " + 
                             "reasonable control, including but not limited to acts of God, " + 
                             "natural disasters, or government actions.", styles['BodyText']))


    content.append(Paragraph("14. Utah Law ", styles['BodyText']))

    content.append(Paragraph("This agreement follows and will be interpreted according to Utah law.", styles['BodyText']))


    content.append(Paragraph("15. Complete Agreement", styles['BodyText']))

    content.append(Paragraph("This document is the entire agreement between the parties " + 
                             "about leasing these water rights.", styles['BodyText']))
    
    content.append(Paragraph("", styles['BodyText']))
    content.append(Paragraph("", styles['BodyText']))
    content.append(Paragraph("Signed by:\n", styles['BodyText']))

    content.append(Paragraph("", styles['BodyText']))
    content.append(Paragraph("\nLESSOR: " + lessor + "\n", styles['BodyText']))

    content.append(Paragraph("", styles['BodyText']))
    content.append(Paragraph("\nLESSEE: " + lessee + "\n", styles['BodyText']))


    # to see the bottom of the contract
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))
    content.append(Paragraph(" ", styles['BodyText']))

  

    # create and move pdf to the static directory
    doc.build(content)
    shutil.move("example.pdf", str(Path(__file__).resolve().parent.parent) + "/media/example.pdf")
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)


    upload_bucket()


    return doc

def make_contract(request, months="nope", shares="nope"):
    # variables = get_recent_variables()
    contract_builder(months, shares)
    print(months, shares)

    return render(request, "watermain/lessor/contract_signing.html")

def submit_info(request):
    form = TransferVariablesForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            # message.log_date = datetime.now()
            message.save()
            return redirect("offers")
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
    get_recent_variables()
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

def finish(request):
    return render(request, "watermain/lessor/finish.html")

