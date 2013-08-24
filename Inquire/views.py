# coding: utf-8

from django.http import HttpResponse,Http404
from django.utils.safestring import mark_safe
from django.shortcuts import render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
#import json
from django.utils import simplejson as json
from django.utils.simplejson import JSONEncoder,JSONDecoder
from coffin import shortcuts
from rest_framework.pagination import PaginationSerializer
from rest_framework import serializers
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import Http404, HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from Inquire.forms import InquireRecordForm
from Inquire.models import InquireRecord

class MyJSONEncoder(JSONEncoder):
    '''支持序列化 datetime 类型和 ObjectId 类型的 json writter 以及 OrderedDict 类型'''
    def default(self, obj):
        ty = type(obj)
        if ty is datetime:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return JSONEncoder.default(self, obj)
class InquireRecordSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(source='get_contact')
    class Meta:
        model = InquireRecord
def index(request):
    #form = InquireRecordForm()
    #c ={"form":form}
    return shortcuts.render_to_response("Inquire/list.html")
def new(request):
    e = request.GET['e']
    u= request.GET['u']
    form = InquireRecordForm()
    if request.GET.has_key('phone'):
        form.initial['phone']=request.GET['phone']
    c ={"form":form,
        "e":e,
        "u":u
    }
    return shortcuts.render_to_response("Inquire/new.html",c)
@csrf_exempt
def edit(request):
    id = request.REQUEST['id']
    contact = InquireRecord.objects.get(id = id)
    form=InquireRecordForm(instance =contact)
    c ={"form":form,'id':id}
    return shortcuts.render_to_response("Inquire/edit.html",c)
@csrf_exempt
def save(request):
    form = InquireRecordForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("保存成功")
    return HttpResponse(form.errors.as_text())
@csrf_exempt
def update(request):
    form = InquireRecordForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponse("保存成功")
    return HttpResponse(form.errors.as_text())
@csrf_exempt
def getListAjax(request):
    cos =[]
    e = request.GET['e']
    users =InquireRecord.objects.filter(ucompany=e)
    rows =  request.POST['rp']
    pagen = request.POST['page']
    paginator = Paginator(users, rows)
    page = paginator.page(pagen)
    js ={
        "total":len(users),
        }
    js["page"] = pagen
    js["rows"] = InquireRecordSerializer(page.object_list).data
    jsstr =json.dumps(js,cls=MyJSONEncoder)
    return HttpResponse(jsstr, mimetype='application/json', status=200)

@csrf_exempt
def getlatelys(request):
    cos =[]
    e = request.GET['e']
    phone =request.GET['phone']
    users =InquireRecord.objects.filter(ucompany=e,phone=phone)
    rows =  request.POST['rp']
    pagen = request.POST['page']
    paginator = Paginator(users, rows)
    page = paginator.page(pagen)
    js ={
        "total":len(users),
        }
    js["page"] = pagen
    js["rows"] = InquireRecordSerializer(page.object_list).data
    jsstr =json.dumps(js,cls=MyJSONEncoder)
    return HttpResponse(jsstr, mimetype='application/json', status=200)