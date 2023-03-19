from django.urls import path
from .views import RegisterView, LoginView, HomePage

urlpatterns = [
    path('', HomePage.as_view(), name='name'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
