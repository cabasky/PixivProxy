from django.contrib import admin
from .models import User
from django.db import models
from django import forms
from PixivProxy.settings import COOKIES_DIRS
from base64 import b64encode
from utils.pixivc import updateUserCollections


class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['userName', 'userAccount','updateCollections',
                  'userCookies', 'admission', 'userId']
    cookiesText = forms.CharField(
        required=False, widget=forms.Textarea(attrs={'cols': 120, 'rows': 20}))

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    form = Userform
    fieldsets = (
        ('Basic Informations', {
         'fields': ('userName', 'userAccount', 'userId')}),
        ('Admission', {'fields': ('admission','updateCollections',
                                  'pixivPassword', 'userCookies', 'cookiesText')}),
    )
    readonly_fields = ('userName', 'userAccount',
                       'userCookies', 'pixivPassword')

    def save_model(self, request, obj, form, change):
        if not len(request.POST['cookiesText']) <= 100:
            obj.setCookies(b64encode(request.POST['cookiesText'].encode()))
            obj.setId(request.POST['cookiesText'])
        if 'updateCollections' in request.POST:
            updateUserCollections(obj)
            obj.updateCollections = 0
        obj.pixivPassword = ''
        obj.save()


admin.site.register(User, UserAdmin)
