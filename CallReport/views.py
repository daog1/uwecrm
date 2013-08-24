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
from CallRecord.models import Callrecord
import datetime

class MyJSONEncoder(JSONEncoder):
    '''支持序列化 datetime 类型和 ObjectId 类型的 json writter 以及 OrderedDict 类型'''
    def default(self, obj):
        ty = type(obj)
        if ty is datetime:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return JSONEncoder.default(self, obj)
class CallrecordSerializer(serializers.ModelSerializer):
    #contact = serializers.CharField(source='get_contact')
    class Meta:
        model = Callrecord
def index(request):
    e = request.GET['e']
    u= request.GET['u']
    c ={
        "e":e,
        "u":u,

    }
    return shortcuts.render_to_response("CallReport/list.html",c)
def report(request):
    e = request.GET['e']
    u= request.GET['u']
    c ={
        "e":e,
        "u":u,
    }
    type = request.GET['type']
    if(type =="edate"):
        c["categories"] = ['0', '1', '2', '3', '4', '5',
                    '6', '7', '8', '9', '10', '11', '12',
                    '13','14', '15', '16', '17', '18', '19',
                    '20','21', '22', '23']
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*),date_format(callrecord.incomingtime,\"%%H\") as hour "
                       "FROM callrecord WHERE callrecord.agent = %s and callrecord.company = %s and TO_DAYS(callrecord.incomingtime) =  TO_DAYS(NOW())"
                       "group by date_format(callrecord.incomingtime,\"%%H\")",[u,e])
        row = cursor.fetchall()
        c["seriescall"] = [0,0,0,0,
                           0,0,0,0,
                           0,0,0,0,
                           0,0,0,0,
                           0,0,0,0,
                           0,0,0,0]
        for v in row :
            c["seriescall"][int(v[1])]= int(v[0])
        return shortcuts.render_to_response("CallReport/list.html",c)
    elif (type =="e30"):
        c["categories"] = []
        i = 14
        while i>=0:
            c["categories"].append((datetime.datetime.now() - datetime.timedelta(days = i)).strftime("%m-%d"))
            i=i-1
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*), date_format(callrecord.incomingtime,\"%%m-%%d\") as date "
                       "FROM callrecord "
                       "WHERE  DATE_SUB(now(), INTERVAL 15 DAY) <= date(callrecord.incomingtime) and callrecord.agent = %s and callrecord.company = %s "
                       "group by date_format(callrecord.incomingtime,\"%%m-%%d\")",[u,e])
        row = cursor.fetchall()
        c["seriescall"] = [0,0,0,0,
                           0,0,0,0,
                           0,0,0,0,
                           0,0,0]
        for v in row :
            catei = 0;
            for cv in c["categories"]:
                if(cv == v[1]):
                    c["seriescall"][catei] = int(v[0])
                catei = catei+1
        return shortcuts.render_to_response("CallReport/report30.html",c)
    elif (type =="emonth"):
        c["categories"] = []
        i = 11
        while i>=0:
            c["categories"].append((datetime.datetime.now() - datetime.timedelta(days = i*30)).strftime("%y-%m"))
            i=i-1
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*), date_format(callrecord.incomingtime,\"%%y-%%m\") as date "
                       "FROM callrecord "
                       "WHERE  DATE_SUB(now(), INTERVAL 12 MONTH) <= date(callrecord.incomingtime) and callrecord.agent = %s and callrecord.company = %s "
                       "group by date_format(callrecord.incomingtime,\"%%y-%%m\")",[u,e])
        row = cursor.fetchall()
        c["seriescall"] = [0,0,0,0,
                           0,0,0,0,
                           0,0,0,0]
        for v in row :
            catei = 0;
            for cv in c["categories"]:
                if(cv == v[1]):
                    c["seriescall"][catei] = int(v[0])
                catei = catei+1
        return shortcuts.render_to_response("CallReport/reportmonth.html",c)
    return shortcuts.render_to_response("CallReport/reportmonth.html",c)
@csrf_exempt
def getListAjax(request):
    cos =[]
    u = request.GET['u']
    e = request.GET['e']
    users =Callrecord.objects.filter(agent=u,company = e)
    rows =  request.POST['rp']
    pagen = request.POST['page']
    paginator = Paginator(users, rows)
    page = paginator.page(pagen)
    js ={
        "total":len(users),
        }
    js["page"] = pagen
    js["rows"] = CallrecordSerializer(page.object_list).data
    jsstr =json.dumps(js,cls=MyJSONEncoder)
    return HttpResponse(jsstr, mimetype='application/json', status=200)

