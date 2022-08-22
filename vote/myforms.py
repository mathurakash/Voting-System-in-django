from django import forms
from django.db.models import fields
from .models import UserDetails,Candidate
from django.contrib.auth.hashers import check_password

class Signupform(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    retype_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:    
        model=UserDetails
        fields=['name','email','username','address','age','phone','pincode','image']
    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get('retype_password')
        if p!=p1:
            raise forms.ValidationError("Both password did not match")

class Signinform(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        u=self.cleaned_data.get('username')
        p=self.cleaned_data.get('password')
        try:
            us=UserDetails.objects.get(username=u)
        except:
            raise forms.ValidationError("user doesnot exits")
        else:
            if not check_password(p,us.password):
                raise forms.ValidationError("password doesnot match")



class CandidateForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    retype_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:    
        model=Candidate
        fields=['name','email','username','address','age','phone','pincode','image','party_name','party_logo']
    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get('retype_password')
        print(p)
        print(p1)
        if p!=p1:
            raise forms.ValidationError("Both password did not match")

class UpdateCandidateForm(forms.ModelForm):
    class Meta:    
        model=Candidate
        fields=['name','email','username','address','age','phone','pincode','image','party_name','party_logo']
    