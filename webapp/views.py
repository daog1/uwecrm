# coding: utf-8
from django.shortcuts import render_to_response,render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from coffin import shortcuts
from django.http import Http404, HttpResponse, HttpResponseRedirect
import simplejson as json
from identities.models import *
from Inquire.models import *
@login_required(login_url='/accounts/login/')
def index(request):
    pass
    #acc_groups =CrmUIAccGroup.objects.all()
    #c ={"acc_groups":acc_groups,"user":request.user,}
#    profile = request.user.get_profile()
    #return render_to_response("index.html",c)

def home(request):
    e = request.GET['e']
    u= request.GET['u']
    p=request.GET['p']
    c ={
        "e":e,
        "u":u,
    }
    return shortcuts.render_to_response("home.html",c)
def callin(request): #呼叫记录
    e = request.GET['e']
    u= request.GET['u']
    number= request.GET['number']
    phones = PhoneNumber.objects.filter(phone_number= number)
    contact = None
    if(len(phones)>0):
        contact = phones[0].contact
    c ={
        "e":e,
        "u":u,
        "contact":contact,
        "number":number,
        }
    #records = InquireRecord.objects.filter(phone= number)
    return shortcuts.render_to_response("callin.html",c)
    #number

