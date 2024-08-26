from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("user/", views.UserView.as_view(), name="api-user"),
    path("user/<int:pk>/profile/", views.UserProfiles.as_view(), name="user profile")
]
