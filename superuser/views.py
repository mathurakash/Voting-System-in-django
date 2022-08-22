from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from .myforms import  CReg,Clog, ElectionScheduleForm
from django.contrib.auth import login,logout,authenticate
from vote.models import Candidate,UserDetails
from vote.myforms import Signupform
from .models import ElectionSchedule
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.db.models import Max

from vote.myforms import Signinform,CandidateForm
############## for mail####################
from django.core.mail import send_mail,EmailMessage
################ for template loader ################
from django.template.loader import get_template
from datetime import datetime,date

def home(request):
    candidates=Candidate.objects.all().count()
    users=UserDetails.objects.all().count()
    return render(request,'superuser/home.html',{'candidates':candidates,'users':users})


class Register(generic.View):
    def get(self,request):
        return render(request,"superuser/form.html",{'form':CReg(None)})
    def post(self,request):
        f=CReg(request.POST)
        if f.is_valid():
            data=f.save(commit=False)
            p=f.cleaned_data.get("password")
            data.set_password(p)
            # data.is_superuser=True
            data.save()
            return redirect("superuser:signin")
        return render(request,"superuser/form.html",{'form':f})



class LoginPage(generic.View):
    def get(self,request):
        return render(request,"superuser/signin.html",{'form':Clog(None)})
    def post(self,request):
        f=Clog(request.POST)
        if f.is_valid():
            u=f.cleaned_data.get("username")
            p=f.cleaned_data.get("password")
            usr=authenticate(username=u,password=p)
            nxt=request.GET.get('next')
            if usr:
                login(request,usr)
            if nxt:
                return redirect(nxt)
            return redirect("superuser:main")
        return render(request,"superuser/signin.html",{'form':f})


def signout(request):
    logout(request)
    return redirect("/")




def show_all_users(request):
    users=UserDetails.objects.all()
    return render(request,'superuser/show_all_users.html',{'users':users})

def show_all_candidates(request):
    candidates=Candidate.objects.all()
    return render(request,'superuser/show_all_candidates.html',{'candidates':candidates})

def election_schedules(request):
    schedule=ElectionSchedule.objects.all()
    return render(request,'superuser/election_schedules.html',{'schedule':schedule})

def delete_schedule(request,pk):
    schedule=ElectionSchedule.objects.get(id=pk)
    schedule.delete()
    return redirect('superuser:election_schedules/')



def start_progress(request,pk):
    user=UserDetails.objects.get(id=pk)
    user.status="Progress"
    uid=user.voterid
    status="Progress"
    #send Registration Successfull Email
    subject="Your Application Status Changed to Progress......"
    html_content=get_template("superuser/user_progress_temp.html").render({'Uid':uid,'status':status})
    from_email="mathurakash700@gmail.com"
    to=user.email
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    user.save()
    return redirect('superuser:show_all_users')

def approve_user(request,pk):
    user=UserDetails.objects.get(id=pk)
    user.status="Approved"
    uid=user.voterid
    status="Approved"
    #send Registration Successfull Email
    subject="Your Application has been Approved ......"
    html_content=get_template("superuser/user_appreoved_temp.html").render({'Uid':uid,'status':status})
    from_email="mathurakash700@gmail.com"
    to=user.email
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    user.save()
    return redirect('superuser:show_all_users')

def reset_user(request,pk):
    user=UserDetails.objects.get(id=pk)
    user.status="Pending"
    user.save()
    return redirect('superuser:show_all_users')


class add_candidate(generic.CreateView):
    template_name='superuser/addcandidate.html'
    context_object_name='form'
    model=Candidate
    form_class=CandidateForm
    success_url=reverse_lazy('superuser:show_all_candidates')
    def form_valid(self, form):
        tempform=form.save(commit=False)
        p=form.cleaned_data['password']
        phone=form.cleaned_data['phone']
        tempform.password=make_password(p)
        tempform.candidateid=make_password(phone)
        uid=make_password(phone)
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        #send Registration Successfull Email
        subject="Thanks For Registration !!!!"
        html_content=get_template("vote/signincandidatetemp.html").render({'Uid':uid,'email':email,'password':password})
        from_email="mathurakash700@gmail.com"
        to=form.cleaned_data['email']
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        tempform.save()
        return super().form_valid(form)


class add_user(generic.CreateView):
    template_name='superuser/adduser.html'
    context_object_name='form'
    model=UserDetails
    form_class=Signupform
    success_url=reverse_lazy('superuser:show_all_users')
    def form_valid(self, form):
        tempform=form.save(commit=False)
        p=form.cleaned_data['password']
        phone=form.cleaned_data['phone']
        tempform.password=make_password(p)
        tempform.voterid=make_password(phone)
        uid=make_password(phone)
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        #send Registration Successfull Email
        subject="Thanks For Registration !!!!"
        html_content=get_template("vote/signincandidatetemp.html").render({'Uid':uid,'email':email,'password':password})
        from_email="mathurakash700@gmail.com"
        to=form.cleaned_data['email']
        msg = EmailMessage(subject, html_content, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        tempform.save()
        return super().form_valid(form)

def add_election_schedules(request):
    if request.method=="POST":
        schedule = ElectionSchedule()
        schedule.pincode=request.POST.get('pincode')
        schedule.date=request.POST.get('date')
        schedule.startTime=request.POST.get('starttime')
        schedule.endTime=request.POST.get('endtime')
        schedule.save()
         
    return render(request,"superuser/add_election_schedules.html")


# def get_nearest_date(request):
    # dates=ElectionSchedule.objects.values_list('date', flat=True)
    # print(dates)




def voter_card(request,pk):
    data=UserDetails.objects.get(id=pk)
    return render(request,'vote/download.html',{'data':data})


# write a program to generate the random string in upper and lower case letters.  
import random  
import string  
def random_string(): # define the function and pass the length as argument  
    # Print the string in Lowercase  
    length =3
    lst_name = ''.join((random.choice(string.ascii_lowercase) for x in range(length))) # run loop until the define length   

def election_results(request):
    # result=Candidate.objects.raw('SELECT id,pincode,name, MAX(votes) FROM Candidate GROUP BY pincode')
    unq_pincodes=list(Candidate.objects.values_list('pincode', flat=True).distinct())
    elctionschedule = ElectionSchedule.objects.all()

    result = Candidate.objects.all()
    
    # votes=result.votes.count()
    print(result,'--------------------')
    resultdict={}
    
    for unq_pin in unq_pincodes:
        # lst_name = random_string()
        lst_name = []
        for candidate in result:
            if candidate.pincode == unq_pin:
                lst_name.append(candidate)
        print(lst_name, "-----------------------------------------------------------------123")        
        resultdict[unq_pin] = lst_name
        print(resultdict, "*" * 20)
        print("*" * 20)
    print(resultdict, "*" * 20)

    # for i in elctionschedule:
    #     for j in result:
    #         if i.pincode == j.pincode:
    #             candidatelist.append(j.name)
    #             resultdict[i.pincode]=[candidatelist]
    # print(resultdict)
    
    return render(request,'superuser/election_result.html',{'results':resultdict})