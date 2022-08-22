from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import ElectionSchedule

class CReg(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    re_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    def clean(self):
        super().clean()
        p=self.cleaned_data.get("password")
        p1=self.cleaned_data.get("re_password")
        if p!=p1:
            raise forms.ValidationError("Password Does Not Match")



class Clog(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data.get("username")
        p=self.cleaned_data.get("password")

        val=authenticate(username=u,password=p)

        if not val:
            raise forms.ValidationError("User Does not exits")


class ElectionScheduleForm(forms.ModelForm):
    class Meta:
        model = ElectionSchedule
        fields = ['pincode','date','startTime','endTime']
