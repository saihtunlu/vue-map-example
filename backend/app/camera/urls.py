from django.urls import path
from . import views

urlpatterns = [
    path('getCameras/', views.Cameras.as_view()),
    path('camera/', views.SingleCamera.as_view()),
    path('activities/', views.Activities.as_view()),

]
