from django.urls import path

from users.views import LoginView, RegisterView
from chat.views import CreateRoomView

app_name = 'api'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-room/', CreateRoomView.as_view(), name='create-room'),
]
