from django import forms
from .models import Contacts,SentRecord
class ContactsForm(forms.ModelForm):
    class Meta:
        model = Contacts
        fields = ['contact_mode','contact_name','contact_number','contact_file']

class MessageForm(forms.ModelForm):

    class Meta:

        model = SentRecord

        fields = ['message']