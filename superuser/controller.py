from django.urls import path
from . import views
app_name='superuser'

urlpatterns = [
    path('home',views.home,name="main"),
    path("superuser_signup",views.Register.as_view(),name="signup"),
    path('',views.LoginPage.as_view(),name="signin"),
    path('logout/',views.signout,name="logout"),


    path('show_all_users/',views.show_all_users,name="show_all_users"),
    path('show_all_candidates/',views.show_all_candidates,name="show_all_candidates"),
    path('election_schedules/',views.election_schedules,name="election_schedules"),

    path('add_candidate/',views.add_candidate.as_view(),name='add_candidate'),
    path('add_user/',views.add_user.as_view(),name='add_user'),
    path('add_election_schedules/',views.add_election_schedules,name="add_election_schedules"),
    path('delete_schedule/<int:pk>',views.delete_schedule,name="delete_schedule"),


    path('start_progress/<int:pk>',views.start_progress,name="start_progress"),
    path('approve_user/<int:pk>',views.approve_user,name="approve_user"),
    path('reset_user/<int:pk>',views.reset_user,name="reset_user"),

    path('election_results',views.election_results,name="election_results"),
    




    path('voter_card/<int:pk>',views.voter_card,name="voter_card"),
    
    
  
]