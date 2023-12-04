from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from chat.models import Conversation


class CreateRoomView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        conversation = Conversation.objects.create()
        return redirect(f'/message/{conversation.id}/')


class RegisterPageView(TemplateView):
    template_name = 'register/index.html'


class DashBoardView(TemplateView):
    template_name = 'login/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('room/')
        else:
            return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MessageView(TemplateView):
    template_name = 'message/index.html'


@method_decorator(login_required, name='dispatch')
class RoomView(TemplateView):
    template_name = 'room/index.html'
