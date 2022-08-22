from django.urls import path
from . import views
app_name='vote'

urlpatterns = [
   path('',views.Index.as_view(),name='home'),
   path('dashboard',views.Home,name='dashboard'),
    path('signup/',views.Signupview.as_view(),name='signup'),
    path('login/',views.signin,name='signin'),
    path('logout/',views.signout,name='signout'),



    path('dashboard/update_user/<int:pk>', views.UpdateUser.as_view(),name='updateuser'),
    path('dashboard/download_voter_card/<int:pk>', views.Download,name='download_voter_card'),

    path('candidatedashboard',views.candidatedashboard,name="candidatedashboard"),
    # path('candidateProfile',views.candidateProfile.as_view(),name="candidateProfile"),


    path('add_candidate/',views.add_candidate.as_view(),name='add_candidate'),
    path('signinCandidate/',views.signinCandidate,name='signinCandidate'),
    path('update_candidate/<int:pk>',views.update_candidate,name='update_candidate'),
    path('delete_candidate/<int:pk>',views.delete_candidate.as_view(),name='delete_candidate'),


    path('vote_now/<int:pincode>',views.vote_now,name="vote_now"),
    path('election_schedules/',views.election_schedules,name="election_schedules"),

    path('Vote_user/<int:ui>/<int:ci>/',views.Vote_user,name="Vote_user"),
]