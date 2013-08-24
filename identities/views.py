# -*- coding: utf-8 -*-
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from coffin import shortcuts
from django import forms
from identities.models import *
from django.utils import simplejson as json
from rest_framework import serializers
from django.core.paginator import Paginator
from identities.models import *
from django.utils.simplejson import JSONEncoder,JSONDecoder
from datetime import datetime, timedelta
from identities.forms import *
class MyJSONEncoder(JSONEncoder):
    '''支持序列化 datetime 类型和 ObjectId 类型的 json writter 以及 OrderedDict 类型'''
    def default(self, obj):
        ty = type(obj)
        if ty is datetime:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return JSONEncoder.default(self, obj)
class ContactSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='get_phone')
    company = serializers.CharField(source='get_company')
    class Meta:
        model = Contact
def index(request):
    e = request.GET['e']
    u= request.GET['u']
    c ={
        "e":e,
        "u":u
    }
    return shortcuts.render_to_response("identities/list.html",c)
def new(request):
    e = request.GET['e']
    u= request.GET['u']

    #phone= request.GET['phone']
    form = ContactForm()
    if request.GET.has_key('phone'):
        form.initial['phone1']=request.GET['phone']
    c ={"form":form,
        "e":e,
        "u":u
        }
    return shortcuts.render_to_response("identities/new.html",c)
@csrf_exempt
def save(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("保存成功")
    return HttpResponse(form.errors.as_text())
def edit(request):
    id = request.REQUEST['id']
    contact = Contact.objects.get(id = id)
    form=ContactForm(instance =contact)
    c ={"form":form,'id':id}
    return shortcuts.render_to_response("identities/edit.html",c)
@csrf_exempt
def update(request,id):
    contact = Contact.objects.get(id = id)
    form = ContactForm(request.POST,instance =contact)
    if form.is_valid():
        form.update()
        return HttpResponse("保存成功")
    return HttpResponse(form.errors.as_text())

@csrf_exempt
def getListAjax(request):
    cos =[]
    e = request.GET['e']
    users =Contact.objects.filter(ucompany=e)
    rows =  request.POST['rp']
    pagen = request.POST['page']
    paginator = Paginator(users, rows)
    page = paginator.page(pagen)
    js ={
        "total":len(users),
        }
    js["page"] = pagen
    js["rows"] = ContactSerializer(page.object_list).data
    #ContactSerializer(page.object_list).data
    jsstr =json.dumps(js,cls=MyJSONEncoder)
    return HttpResponse(jsstr, mimetype='application/json', status=200)
@csrf_exempt
def getlatelys(request):
    cos =[]
    e = request.GET['e']
    users =Contact.objects.filter(ucompany=e)
    rows =  request.POST['rp']
    pagen = request.POST['page']
    paginator = Paginator(users, rows)
    page = paginator.page(pagen)
    js ={
        "total":len(users),
        }
    js["page"] = pagen
    js["rows"] = ContactSerializer(page.object_list).data
    #ContactSerializer(page.object_list).data
    jsstr =json.dumps(js,cls=MyJSONEncoder)
    return HttpResponse(jsstr, mimetype='application/json', status=200)
