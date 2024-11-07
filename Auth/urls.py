from django.urls import path
from .views import RegisterUser,Login,UpdateProfileView
urlpatterns = [
    path('',Login.as_view()),
    path('register',RegisterUser.as_view()),
    path('update_profile',UpdateProfileView.as_view()),
]