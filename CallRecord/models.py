# coding: utf-8
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.translation import ugettext as _
from identities.models import Contact

class Callrecord(models.Model):
    id = models.IntegerField(primary_key=True)
    agent = models.CharField(max_length=50L, blank=True)
    company = models.CharField(max_length=50L, blank=True)
    cid = models.CharField(max_length=50L, blank=True)
    sid = models.CharField(max_length=50L, blank=True)
    direction = models.CharField(max_length=50L, blank=True)
    incomingtime = models.DateTimeField(null=True, blank=True)
    answertime = models.DateTimeField(null=True, blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    phone = models.CharField(max_length=50L, blank=True)
    peer = models.CharField(max_length=50L, blank=True)
    icn = models.CharField(max_length=50L, blank=True)
    endcase = models.CharField(max_length=50L, blank=True)
    type = models.CharField(max_length=50L, blank=True)
    line = models.CharField(max_length=50L, blank=True)
    class Meta:
        db_table = 'callrecord'
