# coding: utf-8
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericRelation
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

class Customer(models.Model):
    analysis = models.CharField(max_length=3072, blank=True)
    company = models.CharField(max_length=384)
    class Meta:
        db_table = u'identities_customer'

    def __unicode__(self):
        return self.company


class Contact(models.Model):
    company = models.ForeignKey(Customer, null=True, blank=True,verbose_name=u"公司")
    name = models.CharField(max_length=765,verbose_name=u"姓名")
    nickname = models.CharField(max_length=100, blank=True,verbose_name=u"昵称")
    title = models.CharField( max_length=200, blank=True,verbose_name=u"职位") #verbose_name=u"职位"
    addr = models.CharField( max_length=700, blank=True,verbose_name=u"地址")
    note = models.CharField( max_length=700, blank=True,verbose_name=u"备注")
    ucompany = models.CharField(max_length=256,verbose_name=u"公司")
    uagent = models.CharField(max_length=256,verbose_name=u"坐席")
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)
    def get_company(self):
        return self.company
        #return ''.join(phones)
    def get_phone(self):
        phones =  self.phonenumber_set.all()
        phonesstr=''
        if len(phones):
            for p in phones:
                phonesstr+=p.phone_number+'('+p.location+'),'
        return phonesstr
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'identities_contacts'

PHONE_LOCATION_CHOICES = (
    ('work', _('Work')),
    ('mobile', _('Mobile')),
    ('fax', _('Fax')),
    ('pager', _('Pager')),
    ('home', _('Home')),
    ('other', _('Other')),
    )

class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True) #verbose_name=u"联系人"
    phone_number = models.CharField(_('number'), max_length=50)
    location = models.CharField(_('location'), max_length=6,
        choices=PHONE_LOCATION_CHOICES, default='work')
    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.phone_number, self.location)

    class Meta:
        db_table = 'identities_contacts_phone_numbers'
        verbose_name = 'phone number'
        verbose_name_plural = 'phone numbers'


LOCATION_CHOICES = (
('work', _('Work')),
('person', _('Personal')),
('other', _('Other'))
    )

class EmailAddress(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")
    email_address = models.EmailField(_('email address'))
    location = models.CharField(_('location'), max_length=6,
        choices=LOCATION_CHOICES, default='work')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.email_address, self.location)

    class Meta:
        db_table = 'contacts_email_addresses'
        verbose_name = 'email address'
        verbose_name_plural = 'email addresses'

IM_SERVICE_CHOICES = (
('aim', 'AIM'),
('msn', 'MSN'),
('icq', 'ICQ'),
('jabber', 'Jabber'),
('yahoo', 'Yahoo'),
('skype', 'Skype'),
('qq', 'QQ'),
('sametime', 'Sametime'),
('gadu-gadu', 'Gadu-Gadu'),
('google-talk', 'Google Talk'),
('other', _('Other'))
    )

class InstantMessenger(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")

    im_account = models.CharField(_('im account'), max_length=100)
    location = models.CharField(_('location'), max_length=6,
        choices=LOCATION_CHOICES, default='work')
    service = models.CharField(_('service'), max_length=11,
        choices=IM_SERVICE_CHOICES, default='jabber')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.im_account, self.location)

    class Meta:
        db_table = 'contacts_instant_messengers'
        verbose_name = 'instant messenger'
        verbose_name_plural = 'instant messengers'

class WebSite(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")

    url = models.URLField(_('URL'))
    location = models.CharField(_('location'), max_length=6,
        choices=LOCATION_CHOICES, default='work')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.url, self.location)

    class Meta:
        db_table = 'contacts_web_sites'
        verbose_name = _('web site')
        verbose_name_plural = _('web sites')

    def get_absolute_url(self):
        return u"%s?web_site=%s" % (self.content_object.get_absolute_url(), self.pk)

class StreetAddress(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")

    street = models.TextField(_('street'), blank=True)
    city = models.CharField(_('city'), max_length=200, blank=True)
    province = models.CharField(_('province'), max_length=200, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    country = models.CharField(_('country'), max_length=100)
    location = models.CharField(_('location'), max_length=6,
        choices=LOCATION_CHOICES, default='work')

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s (%s)" % (self.city, self.location)

    class Meta:
        db_table = 'contacts_street_addresses'
        verbose_name = _('street address')
        verbose_name_plural = _('street addresses')

class SpecialDate(models.Model):
    contact = models.ForeignKey(Contact, null=True, blank=True,verbose_name=u"联系人")

    occasion = models.TextField(_('occasion'), max_length=200)
    date = models.DateField(_('date'))
    every_year = models.BooleanField(_('every year'), default=True)

    date_added = models.DateTimeField(_('date added'), auto_now_add=True)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    def __unicode__(self):
        return u"%s: %s" % (self.occasion, self.date)

    class Meta:
        db_table = 'contacts_special_dates'
        verbose_name = _('special date')
        verbose_name_plural = _('special dates')
