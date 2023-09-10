from django.contrib import admin
from .models import Contacts,SentRecord
# Register your models here.

admin.site.register(Contacts)
admin.site.register(SentRecord)