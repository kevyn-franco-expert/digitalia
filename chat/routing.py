from django.urls import re_path

from chat import consumers

app_name = 'message-chat'

urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
]
