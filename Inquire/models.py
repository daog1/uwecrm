# coding: utf-8
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.translation import ugettext as _
from identities.models import Contact

class InquireRecord(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")
    note = models.CharField(max_length=3072, blank=True,verbose_name=u"备注")
    phone = models.CharField(max_length=765,verbose_name=u"来电号码")
    reason = models.CharField(max_length=3072, blank=True,verbose_name=u"咨询事由")
    results = models.CharField(max_length=3072, blank=True,verbose_name=u"沟通结果")
    sqid = models.CharField(max_length=765,null=True,blank=True,verbose_name=u"工单号")
    ucompany = models.CharField(max_length=256,verbose_name=u"公司")
    uagent = models.CharField(max_length=256,verbose_name=u"坐席")
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    class Meta:
        db_table = u'inquire_record'
    def __unicode__(self):
        return self.phone
    def get_contact(self):
        if(self.contact==None):
            return ""
        return self.contact.name