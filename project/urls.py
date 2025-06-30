from django.urls import path
import chatbot.views as views
urlpatterns = [
    path('', views.chatbot_view, name='chat')
]