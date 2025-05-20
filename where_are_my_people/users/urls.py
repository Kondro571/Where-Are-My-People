from django.urls import path
from .users_views import UserView,UserLastLocationView

urlpatterns = [
    path('users/', UserView.as_view()),
    path('users/<int:user_id>/location/', UserLastLocationView.as_view()),
]
