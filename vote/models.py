from django.db import models
from django.forms import FileField

# Create your models here.

class UserDetails(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    age=models.IntegerField()
    phone=models.CharField(max_length=12,unique=True,default=0)
    address=models.CharField(max_length=1000)
    pincode=models.CharField(max_length=6)
    image=models.FileField()
    voterid=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="Pending")
    votingstatus=models.CharField(max_length=100,default="Enable")
    def __str__(self):
        return f'{self.username}'

class Candidate(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=100)
    age=models.IntegerField()
    phone=models.CharField(max_length=12,unique=True,default=0)
    address=models.CharField(max_length=1000)
    pincode=models.CharField(max_length=6)
    image=models.FileField()
    party_name=models.CharField(max_length=100)
    party_logo=models.FileField()
    candidateid=models.CharField(max_length=100)
    status=models.CharField(max_length=100,default="Pending")
    votes=models.ManyToManyField(UserDetails,related_name='votes',blank=True)
    def total_votes(self):
        return self.votes.count()
    def __str__(self):
        return f'{self.username}'
    def get_model_fields(model):
        return model._meta.fields

# class VotingDetail(models.Model):
#     voter=models.ForeignKey(UserDetails,on_delete=models.CASCADE)
#     candidate=models.ForeignKey(Candidate,on_delete=models.CASCADE)
#     def __str__(self):
#         return f'{self.voter}'



