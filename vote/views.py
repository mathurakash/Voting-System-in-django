from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .models import UserDetails,Candidate
from django.urls import reverse_lazy
from .myforms import Signinform, Signupform,CandidateForm,UpdateCandidateForm
from django.http import HttpResponseRedirect

############## for mail####################
from django.core.mail import send_mail,EmailMessage
################ for template loader ################
from django.template.loader import get_template
from datetime import datetime,date

from superuser.models import ElectionSchedule

from django.utils import timezone

# Create your views here.
class Index(ListView):
    template_name="vote/index.html"
    context_object_name="form"
    def get_queryset(self):
        return{}



# class Home(ListView):
#     template_name="vote/dashboard.html"
#     context_object_name="form"
#     def get_queryset(self):
#         u=self.request.session.get('user_log')
#         # alb1=UserDetails.objects.get(username=u.get('username'))
#         return render(request,'vote/dashboard.html')

def Home(request):
    
    return render(request,'vote/dashboard.html')


class Signupview(CreateView):
    template_name='vote/signup.html'
    context_object_name='form'
    model=UserDetails
    form_class=Signupform
    success_url=reverse_lazy('vote:signin')
    def form_valid(self, form):
        tempform=form.save(commit=False)
        
        p=form.cleaned_data['password']
        phone=form.cleaned_data['phone']
        tempform.password=make_password(p)
        tempform.voterid=make_password(phone)
        uid=make_password(phone)
        #send Registration Successfull Email
        subject="Thanks For Registration !!!!"
        html_content=get_template("vote/signintemp.html").render({'Uid':uid})
        from_email="mathurakash700@gmail.com"
        to=form.cleaned_data['email']
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        tempform.save()
        return super().form_valid(form)

    
def signin(request):
    f=Signinform(request.POST or None)
    if f.is_valid():
        u=f.cleaned_data.get('username')
        obj=UserDetails.objects.get(username=u)
        request.session['user_log']={'username':obj.username,'id':obj.id,'name':obj.name,'email':obj.email,'pincode':obj.pincode,'votingstatus':obj.votingstatus}
        print(obj.id,'--------------')
        return redirect('vote:dashboard')
    return render(request,'vote/signin.html',{'form':f})


def signout(request):
    request.session.pop("user_log")
    return redirect("vote:home")


class UpdateUser(UpdateView):
    template_name='vote/updateprofile.html'
    model=UserDetails
    fields=['name','email','username','age','address','phone','pincode','image']
    context_object_name='form'
    success_url=reverse_lazy('vote:dashboard')




class add_candidate(CreateView):
    template_name='vote/addcandidate.html'
    context_object_name='form'
    model=Candidate
    form_class=CandidateForm
    success_url=reverse_lazy('vote:signinCandidate')
    def form_valid(self, form):
        tempform=form.save(commit=False)
        p=form.cleaned_data['password']
        phone=form.cleaned_data['phone']
        tempform.password=make_password(p)
        tempform.candidateid=make_password(phone)
        uid=make_password(phone)
        #send Registration Successfull Email
        subject="Thanks For Registration !!!!"
        html_content=get_template("vote/signincandidatetemp.html").render({'Uid':uid})
        from_email="mathurakash700@gmail.com"
        to=form.cleaned_data['email']
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        tempform.save()
        return super().form_valid(form)
    

def signinCandidate(request):
    f=Signinform(request.POST or None)
    if f.is_valid():
        u=f.cleaned_data.get('username')
        obj=Candidate.objects.get(username=u)
        request.session['user_log']={'username':obj.username,'id':obj.id,'name':obj.name,'email':obj.email}
        print(obj.id,'--------------')
        return redirect('vote:candidatedashboard')
    return render(request,'vote/signincandidate.html',{'form':f})



def candidatedashboard(request):
    return render(request,'vote/candidatedashboard.html')

def update_candidate(request,pk):
    if request.method =='POST':
        pi=Candidate.objects.get(id=pk)
        form=UpdateCandidateForm(request.POST,instance=pi)
        if form.is_valid():
            tempform=form.save(commit=False)
            tempform.details=request.user.username
            tempform.save()
            return redirect('dashboard')        
    else:

        pi=Candidate.objects.get(id=pk)
        form=UpdateCandidateForm(instance=pi) 
        return render(request,"vote/updatepcandidate.html",{'form':form,'pi':pi})
    return HttpResponseRedirect(request,"vote/signincandidate.html")



    



class delete_candidate(DeleteView): 
    template_name='vote/deletecandidate.html'
    model=Candidate
    context_object_name='candidate'
    success_url=reverse_lazy('vote:signinCandidate')






def Download(request,pk):
    data=UserDetails.objects.get(id=pk)
    print(data)
    return render(request,'vote/download.html',{'data':data})





def vote_now(request,pincode):
    candidates=Candidate.objects.filter(pincode=pincode)
    electiondate=ElectionSchedule.objects.get(pincode=pincode)
    test_date = date.today()
    
    if test_date == electiondate.date:
        userid=request.session['user_log']['id']
        print(userid,'---------------------------------************************')
        user=UserDetails.objects.get(id=userid)
        print(user.votingstatus,'********************')
        now = timezone.now()
        
        return render(request,'vote/vote_now.html',{'candidates':candidates,'votingstatus':user.votingstatus,'starttime':electiondate.startTime,'endtime':electiondate.endTime,'date':test_date,'now':now})
        
    else:
        return redirect('vote:election_schedules')






def election_schedules(request):
    schedule=ElectionSchedule.objects.all()
    userid=request.session['user_log']['id']
    print(userid,'---------------------------------************************')
    user=UserDetails.objects.get(id=userid)
    print(user.votingstatus,'********************')
    return render(request,'vote/election_schedules.html',{'schedule':schedule,'votingstatus':user.votingstatus}) 

def Vote_user(request,ui,ci):
    candidateusername=Candidate.objects.get(id=ci)
    voterusername=UserDetails.objects.get(id=ui)
    print(voterusername.username,'----------------------------------')
    candidateusername.votes.add(voterusername.id)
    voterusername.votingstatus="Disable"
    voterusername.save()
    
    # ElectionResult.voter=voterusername
    # ElectionResult.candidate=candidateusername
    return render(request,"vote/Vote_user.html")



        
    