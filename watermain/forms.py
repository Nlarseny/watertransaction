# TEST CODE

from django import forms
from watermain.models import LogMessage
from watermain.models import TransferVariables

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ["message",]   # NOTE: the trailing comma is required

class TransferVariablesForm(forms.ModelForm):
    class Meta:
        model = TransferVariables
        fields = ["price", "shares", "start_date", "end_date", "permitted_uses"]   # NOTE: the trailing comma is required
