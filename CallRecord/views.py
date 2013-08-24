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
        "u":u
    }
    return shortcuts.render_to_response("CallRecord/list.html",c)
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

