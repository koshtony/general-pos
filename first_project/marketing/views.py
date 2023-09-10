from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .forms import ContactsForm,MessageForm
from .models import Contacts,SentRecord
from django.contrib import messages
import os
from django.conf import settings
from firstapp.sms import send_text
import json
import re
# Create your views here.
BASE_DIR =  settings.BASE_DIR
def market_home(request):
    contact_form = ContactsForm()
    contxt = {
        'contact_form':contact_form,
        'message_form':MessageForm(),
        "template_url":os.path.join(BASE_DIR, 'media/made_templates/bulk_sms_template.xlsx'),
        "contacts":Contacts.objects.filter(current_user = request.user.username),
        "spending":sum([amount.cost for amount in SentRecord.objects.filter(creator = request.user.username)]),
        "all_sent":len([amount for amount in SentRecord.objects.filter(creator = request.user.username)])
    }
    if request.POST:

        cnames = request.POST.get("cnames").split('\n')
        cphones = request.POST.get("cphones").split()
        print(cnames)
        if len(cnames)==len(cphones):
            for i in range(len(cphones)):

                contacts = Contacts(
                  
                  current_user = request.user.username,
                  contact_name = cnames[i],
                  contact_number = cphones[i]
                  

                )

                contacts.save()
            return JsonResponse("contacts saved successfully",safe=False)
        
        else:

            return JsonResponse("number of contacts and name does not match",safe=False)

    return render(request,'marketing/market_home.html',contxt)

def sys_message(request):
    if request.POST:

        msg = request.POST.get("msgone")
        cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        msg = re.sub(cleaner,'',msg)
        #print(msg.strip().split(','))
        status = []
        for contact in Contacts.objects.filter(current_user = request.user.username):

            resp = send_text(contact.contact_number,msg)
            status.append(resp[0])
            if resp[0]['status_desc']=="Success":
                sent_records = SentRecord(
                    name = contact.contact_name,number = contact.contact_number,message = msg, cost = resp[0]["message_cost"],
                    creator = request.user.username
                )
                sent_records.save()

        return JsonResponse(json.dumps(status),safe=False)
    
def unsaved_one_msg(request):
     if request.POST:
         
        phone = request.POST.get("phone")
        msg = request.POST.get("unsavedmsg")
        phone = phone.split()
        status = []
       
        for i in range(len(phone)):

            resp = send_text(phone[i],msg)
            status.append(resp[0])
            print(resp)
            if resp[0]['status_desc']=="Success":
                sent_records = SentRecord(
                    name = "not saved",number = phone[i],message = msg, cost = resp[0]["message_cost"],
                    creator = request.user.username
                )
                sent_records.save()

        return JsonResponse(json.dumps(status),safe=False)
        
def unsaved_mult_msg(request):

    if request.POST:
         
        phone = request.POST.get("multphone")
        msg = request.POST.get("multunsavedmsg")
        phone = phone.split()
        msg = msg.split('\n')
        print(msg)
        status = []
        if len(msg) == len(phone):
            for i in range(len(phone)):

                resp = send_text(phone[i],msg[i])
                print(resp)
                status.append(resp[0])

                if resp[0]['status_desc']=="Success":
                    sent_records = SentRecord(
                        name = "not saved",number = phone[i],message = msg[i], cost = resp[0]["message_cost"],
                        creator = request.user.username
                    )
                    sent_records.save()

            return JsonResponse(json.dumps(status),safe=False)
        err = [{"status_desc":"failed! length phone # not equal length message"}]
        return JsonResponse(json.dumps(err),safe=False)

   
def del_all_contacts(request):
    
    msg = ""
    try:
        del_contacts = Contacts.objects.filter(current_user = request.user.username)
        del_contacts.delete()

        msg+="contacts deleted succcessfully"

    except Exception as e:

        msg+=str(e)

    return JsonResponse(msg,safe=False)