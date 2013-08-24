# -*- coding: utf-8 -*-
from django import forms
from identities.models import *
#from django.contrib.contenttypes.generic import generic_inlineformset_factory as inlineformset_factory

class ContactForm(forms.ModelForm):
    email1 = forms.CharField(label=u'邮箱',required=False)
    email2 = forms.CharField(label=u'邮箱',required=False)
    phone1 = forms.CharField(label=u'电话',required=False)
    phone2 = forms.CharField(label=u'电话',required=False)
    company1 = forms.CharField(label=u'公司',required=False)
    class Meta:
        model = Contact
        exclude = ('company')
    def __init__(self,*args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['company'] =forms.CharField(label=u'公司',required=False)
        self.fields['email'] =forms.CharField(label=u'邮箱',required=False)
        self.fields['addr'] = forms.CharField(widget=forms.Textarea,label=u'地址',required=False)
        self.fields['addr'].widget.attrs.update({'rows': '2'})
        self.fields['note'] = forms.CharField(widget=forms.Textarea,label=u'备注',required=False)
        self.fields['note'].widget.attrs.update({'rows': '4'})
        b = kwargs.has_key('instance')
        if(b):
            self.InitInstance(kwargs['instance'])
    def InitInstance(self,instance):
        if(instance.company!=None):
            customers = Customer.objects.filter(id = instance.company.id)
            if(len(customers)!=0):
                self.initial['company1'] = customers[0].company
        phones = PhoneNumber.objects.filter(contact=instance)
        if(len(phones)==2):
            self.initial['phone1']=phones[0].phone_number
            self.initial['phone2']=phones[1].phone_number
        elif len(phones)==1:
            self.initial['phone1']=phones[0].phone_number
        emails = EmailAddress.objects.filter(contact=instance)
        if(len(emails)==2):
            self.initial['email1']=emails[0].email_address
            self.initial['email2']=emails[1].email_address
        elif len(emails)==1:
            self.initial['email1']=emails[0].email_address

    def save(self, commit=True):
        self.saveCompany()
        rep =super(ContactForm, self).save(commit)
        self.savePone()
        return rep
    def saveCompany(self):
        company = self.cleaned_data['company1']
        if(len(company) ==0):
            return
        c = None
        customers = Customer.objects.filter(company = company)
        if(len(customers)!=0):
            c= customers[0]
        else:
            c = Customer()
            c.company = company
            c.save()
        self.instance.company=c
    def savePhoneNumber(self,number):
        if(len(number)>0):
            phone = PhoneNumber()
            phone.contact = self.instance
            phone.phone_number = number
            phone.save()
    def savePone(self):
        phone1= self.cleaned_data['phone1']
        self.savePhoneNumber(phone1)
        phone2= self.cleaned_data['phone2']
        self.savePhoneNumber(phone2)
    def update(self):
        self.saveCompany()
        oldInstance = self.instance
        rep =super(ContactForm, self).save(True)
        #rep.phone1
        return rep

'''
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('id','name')'''